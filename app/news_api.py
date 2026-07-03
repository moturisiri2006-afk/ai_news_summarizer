import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_news():

    api_key = os.getenv("NEWS_API_KEY")

    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "country": "us",
        "apiKey": api_key
    }

    response = requests.get(url, params=params)

    data = response.json()

    articles = data["articles"]

    return articles