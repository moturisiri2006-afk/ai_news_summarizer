import json
from config import NEWS_FILE, SUMMARY_FILE, BOOKMARK_FILE


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

def load_bookmarks():
    try:
        with open(BOOKMARK_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_bookmark(article):
    print("Bookmark function called")
    bookmarks = load_bookmarks()

    if any(bookmark["url"] == article["url"] for bookmark in bookmarks):
        return

    bookmarks.append(article)

    with open(BOOKMARK_FILE, "w") as file:
        json.dump(bookmarks, file, indent=4)

def remove_bookmark(url):
    bookmarks = load_bookmarks()

    bookmarks = [
        bookmark
        for bookmark in bookmarks
        if bookmark["url"] != url
    ]

    with open(BOOKMARK_FILE, "w") as file:
        json.dump(bookmarks, file, indent=4)