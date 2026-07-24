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
            You are an AI News Assistant.

            Analyze the following news article and return your response in EXACTLY this format.

            Summary:
            (Write a concise summary in 100–150 words.)

            Key Points:
            - Point 1
            - Point 2
            - Point 3

            Sentiment:
            Positive / Neutral / Negative

            Takeaway:
            (One sentence describing the most important insight.)

            Rules:
            - Don't rewrite the article.
            - Don't mention Title, Description or Content.
            - Don't explain your reasoning.
            - Keep it professional.
            - Return only the requested format.

            Article:
            {text}
            """

        response = model.generate_content(prompt)

        logging.info("Summary generated successfully.")

        return response.text.strip()

    except Exception as e:
        logging.error(f"Gemini API Error: {e}")

        return "Unable to generate summary. Please try again later."