import json
from config import NEWS_FILE, SUMMARY_FILE


def save_news(articles):
    with open(NEWS_FILE, "w") as file:
        json.dump(articles, file, indent=4)


def read_news():
    with open(NEWS_FILE, "r") as file:
        articles = json.load(file)
        return articles


def save_summaries(summaries):
    with open(SUMMARY_FILE, "w") as file:
        json.dump(summaries, file, indent=4)