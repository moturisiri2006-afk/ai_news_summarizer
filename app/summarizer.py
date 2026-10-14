
import json
import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv

from config import GEMINI_MODEL


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Add it to your .env file."
    )

genai.configure(api_key=api_key)
model = genai.GenerativeModel(GEMINI_MODEL)


def summarize_article(text):
    """Generate and validate a structured summary of a news article."""

    if not text or not text.strip():
        return _failure("The article contains no text to summarize.")

    prompt = f"""
You are an AI news assistant. Analyze the article below.

Return ONLY valid JSON in this exact structure:
{{
    "summary": "A concise summary in 100-150 words.",
    "key_points": [
        "Important point 1",
        "Important point 2",
        "Important point 3"
    ],
    "sentiment": "Neutral",
    "takeaway": "One concise sentence."
}}

Rules:
- Write a factual summary of 100-150 words where possible.
- Provide exactly 3 relevant key points.
- sentiment must be Positive, Neutral, or Negative.
- Do not invent facts or add information absent from the article.
- Return valid JSON only, without Markdown fences.

Article:
{text}
"""

    try:
        response = model.generate_content(prompt)

        # A response may exist without containing usable text.
        raw_response = response.text if response else None

        if not raw_response or not raw_response.strip():
            logging.error(
                "Gemini returned an empty response. Check response "
                "candidates, finish reason, and safety feedback."
            )
            return _failure("Gemini returned an empty response.")

        raw_response = raw_response.strip()

        # Remove optional Markdown fences.
        if raw_response.startswith("```"):
            lines = raw_response.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            raw_response = "\n".join(lines).strip()

        result = json.loads(raw_response)

        if not isinstance(result, dict):
            raise ValueError("Gemini response must be a JSON object.")

        required_fields = {
            "summary": str,
            "key_points": list,
            "sentiment": str,
            "takeaway": str,
        }

        for field, expected_type in required_fields.items():
            if not isinstance(result.get(field), expected_type):
                raise ValueError(
                    f"Invalid or missing field: {field}"
                )

        result["summary"] = result["summary"].strip()
        result["takeaway"] = result["takeaway"].strip()
        result["key_points"] = [
            point.strip()
            for point in result["key_points"]
            if isinstance(point, str) and point.strip()
        ][:3]

        if not result["summary"]:
            raise ValueError("The summary is empty.")

        if not result["takeaway"]:
            raise ValueError("The takeaway is empty.")

        if result["sentiment"] not in {
            "Positive", "Neutral", "Negative"
        }:
            result["sentiment"] = "Neutral"

        logging.info("Structured summary generated successfully.")
        return result

    except json.JSONDecodeError as error:
        logging.exception(
            "Gemini returned invalid JSON at position %s.",
            error.pos,
        )
        return _failure("Gemini returned an invalid response format.")

    except Exception:
        logging.exception("Failed to generate article summary.")
        return _failure("The AI service could not process this article.")


def _failure(message):
    """Return a consistent fallback result."""
    return {
        "summary": message,
        "key_points": [],
        "sentiment": "Neutral",
        "takeaway": "Check the application logs for details and try again.",
    }
