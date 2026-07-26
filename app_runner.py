import streamlit as st
from app.services import generate_summaries
from app.storage import save_summaries
from datetime import datetime
import inspect

st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

.block-container{
    max-width:1100px;
    padding-top:2rem;
    padding-bottom:2rem;
}

div[data-testid="stVerticalBlockBorderWrapper"]{
    border-radius:16px;
    padding:18px;
}

h1{
    margin-bottom:0.2rem;
}

</style>
""", unsafe_allow_html=True)


st.title("📰 AI News Summarizer")

st.write(
    "Stay updated with AI-powered summaries of the latest news."
)

st.write("")

country_options = {
    "United States": "us",
    "India": "in",
    "United Kingdom": "gb",
    "Canada": "ca",
    "Australia": "au"
}

st.subheader("⚙️ Controls")

country_name = st.selectbox(
        "🌍 Choose a Country",
        list(country_options.keys())
    )

selected_country = country_options[country_name]

category = st.selectbox(
        "📰 Choose a News Category",
        [
            "Technology",
            "Business",
            "Health",
            "Science",
            "Sports",
            "Entertainment"
        ]
    )

keyword = st.text_input(
    "🔍 Search News (Optional)",
    placeholder="Search for any topic, company, person or event..."
)

count = st.slider(
        "📄 Number of Articles",
        min_value=1,
        max_value=10,
        value=5
    )

st.write("")

generate = st.button(
        "🚀 Generate Summaries",
        use_container_width=True
    )

if generate:


    with st.spinner("Generating summaries..."):

        result = generate_summaries(
            selected_country,
            category.lower(),
            keyword,
            count
        )
        

        summaries = result["summaries"]
        trending_topics = result["trending_topics"]


    if not summaries:
        st.warning("No articles were found.")
        st.stop()

    save_summaries(summaries)

    st.success("Summaries generated successfully!")
    st.sidebar.markdown("---")
    st.sidebar.subheader("📰 Top News Topics")

    for topic in trending_topics:
        st.sidebar.write(f"📌 {topic}")

    for summary in summaries:
        with st.container(border=True):

            
            col1, col2 = st.columns([1.8, 3])

            with col1:
                if summary["image"]:
                    st.image(summary["image"], width=280)

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

                st.write("")