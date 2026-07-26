import re 
def extract_keywords(title):
    """
    Extract meaningful keywords from a single news title.
    """

    title_stop_words = {
        "The", "This", "That", "These", "Those",
        "A", "An", "For", "With", "From",
        "Into", "After", "Before", "During",
        "Over", "Under", "And", "Or", "Of",
        "To", "In", "On", "By"
    }
    title = title.split(" - ")[0]

    keywords = []

    words = re.findall(r"\b[\w-]+\b", title)

    for word in words:

        if word in title_stop_words:
            continue

        if len(word) == 1:
            continue

        if word[0].isupper():
            keywords.append(word)

        elif any(char.isdigit() for char in word):
            keywords.append(word)

    return keywords


def extract_trending_topics(articles):
    """
    Extract the most frequently occurring meaningful words
    from article titles.
    """

    stop_words = {
    "the", "a", "an", "and", "or", "of", "to","today"
    "in", "on", "for", "with", "at", "by",
    "from", "is", "are", "was", "were","down","up","Live","Latest","Everything","Update"

    "new", "today", "latest", "breaking",
    "after", "before", "during",

    "says", "said", "say",

    "launches", "launch", "launched",
    "announces", "announce", "announced",

    "reveals", "revealed",
    "wins", "won",
    "beats",
    "shows",
    "report",
    "reports",
    "according"
}
    word_count = {}

    for article in articles:
        title = article.get("title", "")

        keywords = extract_keywords(title)

        for keyword in keywords:

            if keyword in word_count:
                word_count[keyword] += 1
            else:
                word_count[keyword] = 1

    sorted_topics = sorted(
        word_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [topic for topic, count in sorted_topics[:5]]