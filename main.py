from app.news_api import fetch_news
from app.storage import save_news

articles = fetch_news()

save_news(articles)

for index, article in enumerate(articles, start=1):
    print(f"{index}. {article['title']}")