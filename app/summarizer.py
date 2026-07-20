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
        response = model.generate_content(text)

        logging.info("Summary generated successfully.")

        return response.text

    except Exception as e:
        logging.error(f"Gemini API Error: {e}")

        return "Unable to generate summary. Please try again later."