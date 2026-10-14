
import os
import logging

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2"
TIMEOUT = 10
PAGE_SIZE = 50

COUNTRY_NAMES = {
    "us": "United States",
    "in": "India",
    "gb": "United Kingdom",
    "ca": "Canada",
    "au": "Australia",
}

# Terms used to check whether an article matches its category.
CATEGORY_TERMS = {
    "technology": [
        "technology", "tech", "software", "artificial intelligence",
        "AI", "cybersecurity", "smartphone", "computer", "digital",
        "Google", "Microsoft", "Apple", "OpenAI", "robotics",
    ],
    "business": [
        "business", "economy", "market", "stock", "company",
        "finance", "trade", "investment", "corporate", "industry",
    ],
    "health": [
        "health", "medical", "medicine", "hospital", "doctor",
        "disease", "patient", "treatment", "clinical", "healthcare",
    ],
    "science": [
        "science", "scientific", "research", "space", "NASA",
        "physics", "biology", "discovery", "experiment", "climate",
    ],
    "sports": [
        "sport", "football", "cricket", "tennis", "basketball",
        "match", "tournament", "player", "team", "championship",
    ],
    "entertainment": [
        "entertainment", "movie", "film", "actor", "actress",
        "music", "celebrity", "series", "Hollywood", "Bollywood",
    ],
}


def _validate_api_key():
    if not API_KEY:
        raise ValueError(
            "NEWS_API_KEY is missing. Add it to your .env file."
        )


def _request(endpoint, params):
    _validate_api_key()

    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            params={**params, "apiKey": API_KEY},
            timeout=TIMEOUT,
        )

        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            raise RuntimeError(
                data.get("message", "NewsAPI request failed.")
            )

        return data

    except requests.Timeout as error:
        raise RuntimeError(
            "News service timed out. Please try again."
        ) from error

    except requests.RequestException as error:
        logging.exception("NewsAPI request failed.")
        raise RuntimeError(
            "Unable to fetch news. Check the API response and connection."
        ) from error


def _remove_duplicates(articles):
    unique_articles = []
    seen_urls = set()

    for article in articles:
        url = article.get("url")

        if not url or url in seen_urls:
            continue

        seen_urls.add(url)
        unique_articles.append(article)

    return unique_articles


def _article_text(article):
    return " ".join([
        article.get("title") or "",
        article.get("description") or "",
    ]).lower()


def _filter_category(articles, category):
    """Keep articles mentioning terms relevant to the chosen category."""

    terms = CATEGORY_TERMS.get(category.lower())

    if not terms:
        return articles

    filtered = []

    for article in articles:
        text = _article_text(article)

        if any(term.lower() in text for term in terms):
            filtered.append(article)

    return filtered


def fetch_news(country, category):
    """
    Fetch top headlines for a country and category.

    If NewsAPI has no top headlines for the selection, search for
    country- and category-related articles, then filter by category.
    """

    category = category.lower()

    # Prefer NewsAPI's actual country/category headline endpoint.
    data = _request(
        "top-headlines",
        {
            "country": country,
            "category": category,
            "pageSize": PAGE_SIZE,
        },
    )

    articles = _remove_duplicates(data.get("articles", []))

    if articles:
        return articles

    # Fallback: search globally for articles mentioning the country
    # and terms associated with the selected category.
    country_name = COUNTRY_NAMES.get(country, country)
    terms = CATEGORY_TERMS.get(category, [category])

    # Use a smaller group of common terms to keep the query manageable.
    category_query = " OR ".join(
        f'"{term}"' for term in terms[:5]
    )

    query = f'"{country_name}" AND ({category_query})'

    logging.info("Using fallback news query for %s / %s", country, category)

    fallback = _request(
        "everything",
        {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": PAGE_SIZE,
        },
    )

    articles = _remove_duplicates(fallback.get("articles", []))
    return _filter_category(articles, category)


def search_news(keyword, country=None, category=None):
    """
    Search for a keyword, optionally combined with country and category.

    Country context in a text search is not a strict geographic filter.
    """

    if not keyword or not keyword.strip():
        return []

    keyword = keyword.strip()
    query_parts = [f'"{keyword}"']

    if category:
        terms = CATEGORY_TERMS.get(category.lower(), [])
        if terms:
            category_query = " OR ".join(
                f'"{term}"' for term in terms[:5]
            )
            query_parts.append(f"({category_query})")

    if country:
        country_name = COUNTRY_NAMES.get(country, country)
        query_parts.append(f'"{country_name}"')

    query = " AND ".join(query_parts)

    data = _request(
        "everything",
        {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": PAGE_SIZE,
        },
    )

    articles = _remove_duplicates(data.get("articles", []))

    if category:
        articles = _filter_category(articles, category)

    # Require the searched phrase to appear in the title or description.
    keyword_lower = keyword.lower()
    articles = [
        article for article in articles
        if keyword_lower in _article_text(article)
    ]

    return articles
