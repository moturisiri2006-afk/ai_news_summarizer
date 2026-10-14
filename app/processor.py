
def prepare_article(article):
    """Prepare the available article text for summarization."""

    title = (article.get("title") or "").strip()
    description = (article.get("description") or "").strip()
    content = (article.get("content") or "").strip()

    # Remove duplicate text fields and empty values.
    parts = []
    seen = set()

    for label, value in [
        ("Title", title),
        ("Description", description),
        ("Content", content),
    ]:
        if not value:
            continue

        # NewsAPI may append a truncation marker such as [+1234 chars].
        cleaned = value.rsplit("[+", 1)[0].strip()

        if cleaned and cleaned.lower() not in seen:
            parts.append(f"{label}:\n{cleaned}")
            seen.add(cleaned.lower())

    if not parts:
        return ""

    return "\n\n".join(parts)
