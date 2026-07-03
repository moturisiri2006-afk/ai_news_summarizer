from app.news_api import fetch_news

articles = fetch_news()

for index, article in enumerate(articles, start=1):
    print(f"{index}. {article['title']}")