
from app.trending import extract_keywords, extract_trending_topics


sample_articles = [
    {"title": "Apple launches new AI features"},
    {"title": "Apple announces new technology"},
    {"title": "Google launches AI tools"},
    {"title": "AI technology improves healthcare"},
    {"title": "Free games available now"},
]

print("Keyword test:")
print(extract_keywords("Apple launches new AI features"))

print("\nTrending topics test:")
print(extract_trending_topics(sample_articles))
