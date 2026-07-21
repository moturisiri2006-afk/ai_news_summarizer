import logging
import os
import google.generativeai as genai
from dotenv import load_dotenv
from config import GEMINI_MODEL

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(GEMINI_MODEL)


def summarize_article(text):
    try:

        prompt = f"""
            You are a professional news summarizer.

            Read the following news article and produce a concise summary.

            Instructions:
            - Keep the summary between 80 and 120 words.
            - Explain only the important information.
            - Do NOT rewrite the article.
            - Do NOT repeat the title.
            - Do NOT use headings like "Title", "Description", or "Content".
            - Do NOT say "Here's a revised version".
            - Write in a professional news style.

            Article:
            {text}
            """

        response = model.generate_content(prompt)

        logging.info("Summary generated successfully.")

        return response.text.strip()

    except Exception as e:
        logging.error(f"Gemini API Error: {e}")

        return "Unable to generate summary. Please try again later."