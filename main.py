from app.storage import read_news
from app.processor import prepare_article

articles = read_news()

for article in articles:
    prepared_text = prepare_article(article)
    print(prepared_text)
    print("-" * 50)