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

    print("Country:", country)
    print("Category:", category)
    print("Params:", params)

    response = requests.get(url, params=params)

    response.raise_for_status()

    data = response.json()
    print(data)

    articles = data.get("articles", [])

    return articles

if __name__ == "__main__":

    articles = fetch_news("us","technology")

    print(f"Number of articles: {len(articles)}")

    print(articles)