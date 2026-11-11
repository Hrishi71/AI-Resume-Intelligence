from google import genai

from src.llm.config import (
    get_gemini_api_key,
    get_gemini_model,
)


def get_gemini_client():
    """
    Initialize and return a Google Gemini API client.
    """
    api_key = get_gemini_api_key()

    return genai.Client(api_key=api_key)


def get_model_name() -> str:
    """
    Return the configured Gemini model name.
    """
    return get_gemini_model()