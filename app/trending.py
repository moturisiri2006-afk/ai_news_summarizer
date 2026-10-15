
import re
from collections import Counter


STOP_WORDS = {
    # Common words
    "the", "a", "an", "and", "or", "of", "to", "in", "on",
    "for", "with", "at", "by", "from", "into", "after",
    "before", "during", "over", "under", "is", "are", "was",
    "were", "this", "that", "these", "those", "how", "what",
    "why", "when", "where", "who", "as", "it", "its", "be",
    "been", "being", "has", "have", "had", "do", "does", "did",
    "not", "but", "if", "than", "then", "so", "up", "out",
    "about", "their", "his", "her", "our", "your", "they",
    "them", "we", "you", "he", "she", "i", "all", "both",
    "can", "could", "may", "might", "will", "would", "should",

    # News filler
    "new", "latest", "today", "tomorrow", "yesterday",
    "breaking", "live", "update", "updates", "report", "reports",
    "says", "said", "say", "according", "announces", "announce",
    "announced", "launches", "launch", "launched", "reveals",
    "revealed", "shows", "wins", "won", "beats", "gets", "get",
    "make", "makes", "made", "could", "amid", "after", "over",
    "first", "one", "two", "here", "why", "what", "how",
    "everything", "watch", "look", "looks", "now", "back",
    "free", "pro", "ways", "way", "best", "top", "big",
    "video", "photos", "photo", "images", "explained",
    "explainer", "opinion", "analysis", "liveblog",

    # Months and weekdays
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november",
    "december", "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday",

    # Common publisher-style words
    "news", "times", "daily", "today's", "edition", "exclusive",
    "breakingnews", "official", "officially",
}


def extract_keywords(title):
    """Extract useful candidate keywords from a news title."""

    if not title:
        return []

    # Remove publisher suffixes such as " - BBC News".
    title = title.split(" - ")[0].lower()

    words = re.findall(r"\b[a-z][a-z0-9-]*\b", title)

    return [
        word for word in words
        if len(word) >= 3
        and word not in STOP_WORDS
        and not word.isdigit()
    ]


def extract_trending_topics(articles):
    """
    Rank candidate keywords by how many distinct article titles contain them.
    """

    article_counts = Counter()

    for article in articles:
        title = article.get("title") or ""

        # Count a word at most once per article.
        keywords = set(extract_keywords(title))
        article_counts.update(keywords)

    # Prefer topics appearing in multiple articles.
    repeated_topics = [
        (topic, count)
        for topic, count in article_counts.items()
        if count >= 2
    ]

    # If there are no repeated terms, show the strongest candidates
    # rather than returning an empty list.
    if not repeated_topics:
        repeated_topics = list(article_counts.items())

    ranked_topics = sorted(
        repeated_topics,
        key=lambda item: (-item[1], item[0]),
    )

    return [topic for topic, _ in ranked_topics[:5]]
