# 📰 AI News Summarizer

An AI-powered news application that fetches news articles using **NewsAPI** and generates structured summaries with **Google Gemini**. Built with Python and Streamlit, it helps users explore news by country, category, or keyword and quickly understand the key information from each article.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?logo=googlegemini&logoColor=white)
![NewsAPI](https://img.shields.io/badge/News%20Source-NewsAPI-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📌 Overview

Keeping up with the news can be time-consuming. The AI News Summarizer simplifies this process by retrieving news articles and using a generative AI model to produce concise summaries and structured insights.

Users can browse articles, search for topics, explore trending keywords, save bookmarks, and access the original articles through an interactive web interface.

## ✨ Features

- 🌍 **Country-based news browsing** — select a supported country to explore available news.
- 🗂️ **Category selection** — browse categories such as technology, business, health, science, sports, and entertainment.
- 🔍 **Keyword search** — search for news related to specific topics.
- 🤖 **AI-powered summaries** — generate structured article summaries using Google Gemini.
- 📌 **Key points** — extract three important points from a summary when generation succeeds.
- 📊 **Sentiment analysis** — display a positive, neutral, or negative sentiment label.
- 💡 **Key takeaway** — present the main takeaway from an article.
- 🔥 **Trending topics** — identify frequently occurring keywords in article headlines.
- 🖼️ **Article previews** — display available article images, sources, and publication dates.
- 🔗 **Original article access** — open the source article for further reading.
- 🔖 **Bookmarks** — save articles for later reference.
- 💾 **JSON storage** — store summaries and bookmarks locally.
- 📝 **Application logging** — record application events and errors.
- 🧪 **Automated tests** — test core functionality without making live Gemini requests.
- 🎨 **Interactive interface** — explore results through a Streamlit application.

> **Note:** Search results depend on NewsAPI availability and query relevance. AI summary generation also depends on Gemini API availability and quota limits.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Web interface | Streamlit |
| Generative AI | Google Gemini |
| News data | NewsAPI |
| HTTP requests | Requests |
| Environment configuration | python-dotenv |
| Data storage | JSON |
| Testing | Python `unittest` |
| Version control | Git and GitHub |
| Development environment | Visual Studio Code |

## 🏗️ Project Structure

```text
AI-News-Summarizer/
│
├── app/
│   ├── news_api.py          # Fetch and search news articles
│   ├── processor.py         # Prepare article text
│   ├── services.py          # Coordinate fetching and summarization
│   ├── storage.py           # Manage summaries and bookmarks
│   ├── summarizer.py        # Generate structured AI summaries
│   ├── trending.py          # Extract trending keywords
│   ├── url_builder.py       # Build article-related URLs
│   └── utils.py             # Shared utility functions
│
├── tests/
│   ├── test_news.py     # News API behavior tests
│   ├── test_processor.py    # Article processing tests
│   └── test_trending.py     # Trending topic tests
│
├── data/                    # Local application data
├── logs/                    # Application logs
├── app_runner.py             # Main Streamlit interface
├── config.py                 # Application configuration
├── logging_config.py         # Logging configuration
├── main.py                   # Application entry point, if used
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment configuration
├── .gitignore
└── README.md

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/moturisiri2006-afk/ai_news_summarizer
cd ai_news_summarizer
```

### 2. Create a virtual environment

**Windows — PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python executable directly or follow your system's virtual-environment activation guidance.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
NEWS_API_KEY=your_newsapi_key
GEMINI_API_KEY=your_gemini_api_key
```

Obtain API credentials from:

- [NewsAPI](https://newsapi.org/)
- [Google AI Studio](https://aistudio.google.com/)

**Security:** Never commit your `.env` file or expose API keys in source code, screenshots, logs, or public repositories.

### 5. Run the application

Activate the virtual environment, then run:

```bash
streamlit run app_runner.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open the URL in your browser to use the application.

## 🧪 Running Tests

Run the automated test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

The tests cover core functionality such as article processing, trending keyword extraction, duplicate removal, and mocked NewsAPI behavior.

Mocked tests do not require live NewsAPI or Gemini requests. Live service behavior should be checked separately because API availability, response content, and quotas can vary.

## 🔐 Environment Variables

| Variable | Purpose |
|---|---|
| `NEWS_API_KEY` | Authenticates requests to NewsAPI |
| `GEMINI_API_KEY` | Authenticates requests to Google Gemini |

Keep credentials in your local `.env` file and ensure it is excluded from version control.

## 🚧 Current Limitations

- News availability varies by country, category, and NewsAPI response.
- Global keyword searches may include articles that are not geographically specific to the selected country.
- Trending topics are extracted from article headlines using keyword frequency; they are not a full semantic topic-classification system.
- AI summary generation may fail when the Gemini service is unavailable, rate-limited, or over quota.
- JSON storage is local to the application and is not designed for multi-user production workloads.

## 🔮 Future Improvements

- Improve country and category relevance with stronger article classification.
- Add more robust retries and user-friendly API error handling.
- Improve trending-topic extraction with multi-word phrases.
- Add summary history, filtering, and export options.
- Add persistent database storage for a multi-user deployment.
- Deploy the application and add a public demo.
- Expand automated tests and integration coverage.

## 🎯 Learning Outcomes

This project provides practical experience with:

- Integrating external REST APIs.
- Using generative AI for structured text summarization.
- Building interactive Python web applications with Streamlit.
- Processing and filtering unstructured text.
- Managing environment variables and API credentials.
- Implementing logging, JSON storage, and automated tests.
- Using Git and GitHub for version control.

---

**Developed as a practical project exploring AI-powered news summarization with Python, Streamlit, NewsAPI, and Google Gemini.**