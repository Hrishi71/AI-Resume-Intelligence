import os
from pathlib import Path

from dotenv import load_dotenv


def get_gemini_api_key(env_file: Path | None = None) -> str:
    """
    Load and retrieve the Gemini API key.

    Args:
        env_file: Optional path to a .env file.

    Raises:
        ValueError: If the API key is missing or empty.
    """
    if env_file is not None:
        load_dotenv(dotenv_path=env_file, override=True)
    else:
        load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or not api_key.strip():
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Please configure it in your .env file."
        )

    return api_key.strip()

def get_gemini_model() -> str:
    """
    Retrieve the Gemini model name from environment variables.

    Returns:
        Configured model name or the default model.
    """
    return os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()