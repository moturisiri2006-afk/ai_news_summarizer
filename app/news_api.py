import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NEWS_API_KEY")


def fetch_news(country,category):
    url = "https://newsapi.org/v2/top-headlines"

    params = {
    "country": country,
    "category": category,
    "apiKey": api_key
}


    response = requests.get(url, params=params)

    response.raise_for_status()

    data = response.json()

    articles = data.get("articles", [])

    if not articles:

        country_names = {
            "in": "India",
            "us": "United States",
            "gb": "United Kingdom",
            "ca": "Canada",
            "au": "Australia"
        }

        search_query = f"{category} {country_names.get(country, country)}"

        return search_news(search_query)

    return articles

def search_news(keyword):
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": keyword,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": api_key
    }

    print("Keyword:", keyword)
    print("Params:", params)

    response = requests.get(url, params=params)

    response.raise_for_status()

    data = response.json()

    print(data)

    articles = data.get("articles", [])

    return articles

if __name__ == "__main__":

    articles = fetch_news("us", "technology")

    print(f"Number of articles: {len(articles)}")