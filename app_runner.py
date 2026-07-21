import streamlit as st

from app.services import generate_summaries
from app.storage import save_summaries
from datetime import datetime

st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    layout="centered"
)

st.sidebar.title("📌 About")

st.sidebar.info(
    """
    AI News Summarizer

    Built using:

    • Python
    • Streamlit
    • NewsAPI
    • Google Gemini AI
    """
)

st.title("📰 AI News Summarizer")

st.write(
    "Stay updated with AI-powered summaries of the latest news."
)

st.divider()

country_options = {
    "United States": "us",
    "India": "in",
    "United Kingdom": "gb",
    "Canada": "ca",
    "Australia": "au"
}

country_name = st.selectbox(
    "Choose a Country",
    list(country_options.keys())
)

selected_country = country_options[country_name]
st.caption(f"Country code being sent: {selected_country}")

category = st.selectbox(
    "Choose a News Category",
    [
        "Technology",
        "Business",
        "Health",
        "Science",
        "Sports",
        "Entertainment"
    ]
)

count = st.slider(
    "Number of Articles",
    min_value=1,
    max_value=10,
    value=5
)

generate = st.button("🚀 Generate Summaries")

if generate:

    with st.spinner("Generating summaries..."):

        summaries = generate_summaries(
            selected_country,
            category.lower(),
            count
        )

    st.write("Number of summaries:", len(summaries))
    #st.write(summaries)

    if not summaries:
        st.warning("No articles were found.")
        st.stop()

    save_summaries(summaries)

    st.success("Summaries generated successfully!")

    for summary in summaries:
        with st.container(border=True):

            if summary["image"]:
                col1, col2 = st.columns([1, 3])

            with col1:
                if summary["image"]:
                    st.image(summary["image"], width=180)

            with col2:

                st.subheader(summary["title"])
                published = datetime.fromisoformat(
                    summary["published_at"].replace("Z", "+00:00")
                )

                formatted_date = published.strftime("%d %b %Y")

                st.caption(
                    f"📰 {summary['source']} | 📅 {formatted_date}"
                )

                st.markdown("### 🤖 AI Summary")

                summary_text = summary["summary"]

                if len(summary_text) > 250:
                    summary_text = summary_text[:250] + "..."

                st.write(summary_text)

                with st.expander("📖 Read Full AI Summary"):
                    st.write(summary["summary"])

                st.caption(
                    f"⏱️ Summary generated at: {summary['generated_at']}"
                )

                if summary["url"]:
                    st.link_button(
                        "🔗 Read Full Article",
                        summary["url"]
                    )

                st.divider()