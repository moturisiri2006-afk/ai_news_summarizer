import os
import google.generativeai as genai
from dotenv import load_dotenv
from config import GEMINI_MODEL

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(GEMINI_MODEL)

def summarize_article(text):
    prompt = f"""
    You are an AI news assistant.

    Summarize the following news article in 3-5 concise bullet points.
    Keep the summary simple and easy to understand.

    {text}
    """

    response = model.generate_content(prompt)

    return response.text