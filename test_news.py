
from app.news_api import fetch_news, search_news

tests = [
    ("India Technology", lambda: fetch_news("in", "technology")),
    (
        "India Technology Apple",
        lambda: search_news(
            keyword="Apple",
            country="in",
            category="technology",
        ),
    ),
    (
        "US Technology Apple",
        lambda: search_news(
            keyword="Apple",
            country="us",
            category="technology",
        ),
    ),
    (
        "India Sports Cricket",
        lambda: search_news(
            keyword="cricket",
            country="in",
            category="sports",
        ),
    ),
]

for name, run_test in tests:
    print(f"\n{'=' * 55}")
    print(name)

    try:
        articles = run_test()
        print("Articles returned:", len(articles))

        for article in articles[:5]:
            print("-", article.get("title", "Untitled"))
            print("  Source:", (article.get("source") or {}).get("name"))

    except Exception as error:
        print("ERROR:", error)
