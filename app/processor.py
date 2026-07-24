def prepare_article(article):
    title = article.get("title") or "No title available"
    description = article.get("description") or "No description available"
    content = article.get("content") or "No content available"

    prepared_text = f"""Title:
{title}

Description:
{description}

Content:
{content}
"""

    return prepared_text