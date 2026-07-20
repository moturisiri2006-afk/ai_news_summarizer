import logging
import logging_config

from app.services import generate_summaries
from app.storage import save_summaries
from app.utils import get_article_count
from app.news_api import fetch_news

def main():

    logging.info("Application started.")

    category = "technology"

    articles = fetch_news("us",category)

    count = get_article_count(len(articles))
    count = get_article_count(10)

    if count is None:
        return

    summaries = generate_summaries(category, count)

    save_summaries(summaries)

    logging.info("Summaries saved successfully.")

    print("\nGenerated Summaries\n")

    for summary in summaries:

        print("=" * 70)
        print(summary["title"])
        print()
        print(summary["summary"])
        print("=" * 70)


if __name__ == "__main__":
    main()