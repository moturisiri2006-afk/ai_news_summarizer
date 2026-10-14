
from datetime import datetime

import app.news_api as news_api
from app.processor import prepare_article
from app.summarizer import summarize_article
from app.trending import extract_trending_topics


def generate_summaries(country, category, keyword, count):
    """Fetch articles, generate summaries, and extract topics."""

    if keyword and keyword.strip():
        articles = news_api.search_news(
            keyword=keyword,
            country=country,
            category=category,
        )
    else:
        articles = news_api.fetch_news(country, category)

    if not articles:
        return {
            "summaries": [],
            "trending_topics": [],
        }

    articles = articles[:count]
    trending_topics = extract_trending_topics(articles)
    summaries = []

    for article in articles:
        prepared_text = prepare_article(article)
        summary = summarize_article(prepared_text)

        summary_data = {
            "title": article.get("title") or "Untitled article",
            "summary": summary.get("summary", ""),
            "key_points": summary.get("key_points", []),
            "sentiment": summary.get("sentiment", "Neutral"),
            "takeaway": summary.get("takeaway", ""),
            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "image": article.get("urlToImage"),
            "source": (article.get("source") or {}).get("name"),
            "published_at": article.get("publishedAt"),
            "url": article.get("url"),
        }

        summaries.append(summary_data)

    return {
        "summaries": summaries,
        "trending_topics": trending_topics,
    }
