import html
from datetime import datetime

import requests
import streamlit as st

from app.services import generate_summaries
from app.storage import (
    save_summaries,
    save_bookmark,
    load_bookmarks,
    remove_bookmark,
)
from app.utils import clean_display_text


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1100px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .app-title {
    font-size: 1.9rem;
    font-weight: 700;
    line-height: 1.5;
    padding: 8px 0 6px 0;
    margin: 0;
    display: block;
    overflow: visible;
    }

    .subtitle {
        color: #9aa0aa;
        font-size: 0.9rem;
        margin-bottom: 1.4rem;
    }

    .article-title {
    font-size: 1.08rem;
    font-weight: 650;
    line-height: 1.5;
    margin-bottom: 6px;
    overflow-wrap: anywhere;
    word-break: break-word;
}

    .meta {
        color: #8d939e;
        font-size: 0.72rem;
        margin: 5px 0 12px;
    }

    .section {
        font-size: 0.88rem;
        font-weight: 650;
        margin: 13px 0 6px;
    }

    .summary {
        color: #d5d8de;
        font-size: 0.91rem;
        line-height: 1.6;
    }

    .point {
        color: #cdd1d8;
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 5px;
    }

    .takeaway {
        color: #d5d8de;
        font-size: 0.87rem;
        line-height: 1.55;
    }

    .sentiment {
        display: inline-block;
        background: #292e38;
        border-radius: 10px;
        padding: 3px 9px;
        font-size: 0.74rem;
    }

    .placeholder {
        height: 150px;
        background: #171a21;
        border: 1px solid #292e38;
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #858b96;
        font-size: 0.8rem;
    }

    .sidebar-title {
        font-size: 1rem;
        font-weight: 650;
    }

    .sidebar-section {
        font-size: 0.82rem;
        font-weight: 600;
        color: #cfd3da;
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

st.session_state.setdefault("summaries", [])
st.session_state.setdefault("trending_topics", [])
st.session_state.setdefault("selected_bookmark", None)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean(value):
    """Clean and safely escape text for HTML."""
    return html.escape(
        clean_display_text(str(value or ""))
    )


def format_date(value):
    """Convert API timestamp into readable date."""

    try:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        ).strftime("%d %b %Y")

    except (ValueError, AttributeError):
        return "Unknown date"


def show_image(url):
    """Display article image or fallback placeholder."""

    if not url:
        st.markdown(
            '<div class="placeholder">🖼️ No image available</div>',
            unsafe_allow_html=True,
        )
        return

    try:
        response = requests.get(
            url,
            timeout=5
        )

        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        if (
            response.status_code == 200
            and content_type.startswith("image/")
        ):
            st.image(
                response.content,
                use_container_width=True
            )
        else:
            raise requests.RequestException()

    except requests.RequestException:
        st.markdown(
            '<div class="placeholder">🖼️ No image available</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# ARTICLE DISPLAY
# ============================================================

def display_article(article):

    with st.container(border=True):

        image_col, content_col = st.columns(
        [0.9, 3.1],
        gap="medium"
    )

        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------

        with image_col:
            show_image(article.get("image"))

        # ----------------------------------------------------
        # CONTENT
        # ----------------------------------------------------

        with content_col:

            # Article title
            title = clean(
                article.get(
                    "title",
                    "Untitled article"
                )
            )

            st.markdown(
                f"""
                <div class="article-title">
                    {title}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Metadata
            source = clean(
                article.get(
                    "source",
                    "Unknown source"
                )
            )

            date = format_date(
                article.get("published_at")
            )

            st.markdown(
                f"""
                <div class="meta">
                    {source} &nbsp;•&nbsp; {date}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ------------------------------------------------
            # SUMMARY
            # ------------------------------------------------

            st.markdown(
                '<div class="section">✨ AI Summary</div>',
                unsafe_allow_html=True,
            )

            full_summary = clean(
                article.get("summary", "")
            )

            preview = full_summary

            if len(preview) > 300:
                preview = preview[:300] + "..."

            st.markdown(
                f"""
                <div class="summary">
                    {preview}
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander(
                "📖 Read Full AI Summary"
            ):
                st.markdown(
                    f"""
                    <div class="summary">
                        {full_summary}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # ------------------------------------------------
            # KEY POINTS
            # ------------------------------------------------

            key_points = article.get(
                "key_points",
                []
            )

            if key_points:

                st.markdown(
                    '<div class="section">🔑 Key Points</div>',
                    unsafe_allow_html=True,
                )

                for point in key_points:

                    st.markdown(
                        f"""
                        <div class="point">
                            • {clean(point)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            # ------------------------------------------------
            # SENTIMENT
            # ------------------------------------------------

            sentiment = article.get(
                "sentiment",
                "Neutral"
            )

            if sentiment not in {
                "Positive",
                "Neutral",
                "Negative"
            }:
                sentiment = "Neutral"

            st.markdown(
                '<div class="section">📊 Sentiment</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <span class="sentiment">
                    {clean(sentiment)}
                </span>
                """,
                unsafe_allow_html=True,
            )

            # ------------------------------------------------
            # TAKEAWAY
            # ------------------------------------------------

            takeaway = article.get(
                "takeaway",
                ""
            )

            if takeaway:

                st.markdown(
                    '<div class="section">💡 Takeaway</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div class="takeaway">
                        {clean(takeaway)}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # ------------------------------------------------
            # GENERATED TIME
            # ------------------------------------------------

            generated_at = article.get(
                "generated_at"
            )

            if generated_at:
                st.caption(
                    f"Generated: {generated_at}"
                )

            # ------------------------------------------------
            # ACTIONS
            # ------------------------------------------------

            url = article.get("url")

            if url:

                bookmarks = load_bookmarks()

                is_bookmarked = any(
                    bookmark.get("url") == url
                    for bookmark in bookmarks
                )

                button_col1, button_col2 = st.columns(
                    2,
                    gap="small"
                )

                with button_col1:

                    st.link_button(
                        "🔗 Read Full Article",
                        url,
                        use_container_width=True,
                    )

                with button_col2:

                    if is_bookmarked:

                        st.button(
                            "✓ Bookmarked",
                            disabled=True,
                            use_container_width=True,
                            key=f"saved_{url}",
                        )

                    else:

                        if st.button(
                            "🔖 Bookmark",
                            use_container_width=True,
                            key=f"save_{url}",
                        ):

                            save_bookmark(article)

                            st.toast(
                                "Article bookmarked."
                            )

                            st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="app-title">📰 AI News Summarizer</div>
    <div class="subtitle">
        Stay informed with concise AI-generated summaries of current news.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONTROLS
# ============================================================

control_col1, control_col2 = st.columns(2)


countries = {
    "United States": "us",
    "India": "in",
    "United Kingdom": "gb",
    "Canada": "ca",
    "Australia": "au",
}


with control_col1:

    country_name = st.selectbox(
        "🌍 Country",
        list(countries.keys())
    )


with control_col2:

    category = st.selectbox(
        "📰 Category",
        [
            "Technology",
            "Business",
            "Health",
            "Science",
            "Sports",
            "Entertainment",
        ]
    )


keyword = st.text_input(
    "🔍 Search",
    placeholder=(
        "Search by topic, company, person, or event..."
    ),
)


count = st.slider(
    "📄 Articles to summarize",
    min_value=1,
    max_value=10,
    value=5,
)


generate = st.button(
    "🚀 Generate Summaries",
    type="primary",
    use_container_width=True,
)


# ============================================================
# GENERATE SUMMARIES
# ============================================================

if generate:

    st.session_state.selected_bookmark = None

    with st.spinner(
        "Fetching news and generating AI summaries..."
    ):

        try:

            result = generate_summaries(
                countries[country_name],
                category.lower(),
                keyword,
                count,
            )

            st.session_state.summaries = result.get(
                "summaries",
                []
            )

            st.session_state.trending_topics = result.get(
                "trending_topics",
                []
            )

            if st.session_state.summaries:

                save_summaries(
                    st.session_state.summaries
                )

                st.toast(
                    f"✨ {len(st.session_state.summaries)} "
                    "summaries generated."
                )

            else:

                st.warning(
                    "No articles were found."
                )

        except Exception as error:

            st.error(
                "Unable to generate news summaries."
            )

            st.caption(
                f"Details: {error}"
            )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">'
        '📰 AI News Summarizer'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # Topics
    if st.session_state.trending_topics:

        st.markdown(
            '<div class="sidebar-section">'
            '🔥 Topics from Headlines'
            '</div>',
            unsafe_allow_html=True,
        )

        for topic in st.session_state.trending_topics:
            st.write(f"• {topic}")

    else:

        st.caption(
            "Generate news to see topics."
        )

    st.divider()

    # Bookmarks
    bookmarks = load_bookmarks()

    st.markdown(
        f'<div class="sidebar-section">'
        f'🔖 Bookmarks ({len(bookmarks)})'
        f'</div>',
        unsafe_allow_html=True,
    )

    if bookmarks:

        for i, bookmark in enumerate(bookmarks):

            title = bookmark.get(
                "title",
                "Untitled article"
            )

            if len(title) > 40:
                title = title[:40] + "..."

            button_col, delete_col = st.columns(
                [5, 1]
            )

            with button_col:

                if st.button(
                    clean_display_text(title),
                    key=f"open_{i}",
                    use_container_width=True,
                ):

                    st.session_state.selected_bookmark = (
                        bookmark
                    )

                    st.rerun()

            with delete_col:

                if st.button(
                    "×",
                    key=f"delete_{i}",
                ):

                    remove_bookmark(
                        bookmark.get("url")
                    )

                    st.toast(
                        "Bookmark removed."
                    )

                    st.rerun()

    else:

        st.caption(
            "No bookmarks yet."
        )


# ============================================================
# CONTENT
# ============================================================

if st.session_state.selected_bookmark:

    st.markdown(
        '<div class="section">📌 Saved Article</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "← Back to Latest News"
    ):

        st.session_state.selected_bookmark = None
        st.rerun()

    articles = [
        st.session_state.selected_bookmark
    ]

else:

    articles = st.session_state.summaries

# ============================================================
# DASHBOARD
# ============================================================

if (
    articles
    and not st.session_state.selected_bookmark
):

    sources = {
        article.get("source")
        for article in articles
        if article.get("source")
    }

    neutral_count = sum(
        article.get("sentiment") == "Neutral"
        for article in articles
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            label="📰 Articles",
            value=len(articles),
        )

    with metric2:
        st.metric(
            label="🌐 Sources",
            value=len(sources),
        )

    with metric3:
        st.metric(
            label="📊 Neutral",
            value=neutral_count,
        )

    st.write("")
# ============================================================
# ARTICLES
# ============================================================

if articles:

    for article in articles:

        display_article(article)

        st.write("")

else:

    st.info(
        "👆 Choose your preferences and click "
        "Generate Summaries to get started."
    )