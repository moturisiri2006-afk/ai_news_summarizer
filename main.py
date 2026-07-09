from app.storage import read_news, save_summaries
from app.processor import prepare_article
from app.summarizer import summarize_article
from app.utils import get_article_count


def main():
    # Read saved news articles
    articles = read_news()

    # Get the number of articles to summarize
    count = get_article_count(len(articles))

    # Stop if the input is invalid
    if count is None:
        return

    # List to store all summaries
    summaries = []

    # Generate summaries
    for article in articles[:count]:

        prepared_text = prepare_article(article)

        summary = summarize_article(prepared_text)

        print("=" * 70)
        print(summary)
        print("=" * 70)

        summary_data = {
            "title": article.get("title"),
            "summary": summary
        }

        summaries.append(summary_data)

    # Save all summaries after the loop
    save_summaries(summaries)

    print("\n✅ All summaries have been saved successfully!")


if __name__ == "__main__":
    main()