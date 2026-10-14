import re
from collections import Counter


STOP_WORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on",
    "for", "with", "at", "by", "from", "into", "after",
    "before", "during", "over", "under", "is", "are", "was",
    "were", "this", "that", "these", "those", "how", "what",
    "why", "when", "where", "who",

    "new", "latest", "today", "tomorrow", "yesterday",
    "breaking", "live", "update", "updates",

    "says", "said", "say", "according", "report", "reports",
    "announces", "announce", "announced", "launches", "launch",
    "launched", "reveals", "revealed", "shows", "wins", "won",
    "beats",

    "will", "can", "could", "may", "might", "its", "their",
    "his", "her", "our", "your", "about", "than", "more",

    # Months
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november",
    "december",

    # Days
    "monday", "tuesday", "wednesday", "thursday", "friday",
    "saturday", "sunday",
}


def extract_keywords(title):
    """
    Extract meaningful keywords from a news title.
    """

    if not title:
        return []

    title = title.split(" - ")[0]

    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9-]+\b", title.lower())

    keywords = []

    for word in words:

        if word in STOP_WORDS:
            continue

        if len(word) < 3:
            continue

        keywords.append(word)

    return keywords


def extract_trending_topics(articles):
    """
    Extract the most frequently occurring meaningful
    keywords from article titles.
    """

    word_count = Counter()

    for article in articles:
        title = article.get("title", "")

        keywords = extract_keywords(title)

        for keyword in keywords:
            word_count[keyword] += 1

    return [
        topic
        for topic, count in word_count.most_common(5)
        if count >= 1
    ]