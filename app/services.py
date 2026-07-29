
from datetime import datetime
import app.news_api as news_api
from app.processor import prepare_article
from app.summarizer import summarize_article
from app.trending import extract_trending_topics


def generate_summaries(country,category,keyword, count):


    if keyword.strip():

        articles = news_api.search_news(keyword)

    else:

        articles = news_api.fetch_news(
            country,
            category
        )


    if not articles:
        print("No articles found")
        return {
        "summaries": [],
        "trending_topics": []
    }

    trending_topics = extract_trending_topics(articles)

    summaries = []

    for article in articles[:count]:

        prepared_text = prepare_article(article)

        summary = summarize_article(prepared_text)

        summary_data = {
            "title": article.get("title"),
            "summary": summary,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "image": article.get("urlToImage"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt"),
            "url": article.get("url"),
        }

        summaries.append(summary_data)
    
    return {
    "summaries": summaries,
    "trending_topics": trending_topics
}

