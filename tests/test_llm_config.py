import pytest
from pathlib import Path
from src.llm.config import get_gemini_api_key
from src.llm.config import get_gemini_model


def test_get_gemini_model_returns_default_when_not_configured(monkeypatch):
    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    model = get_gemini_model()

    assert model == "gemini-3.5-flash-lite"


def test_get_gemini_model_reads_environment_variable(monkeypatch):
    monkeypatch.setenv("GEMINI_MODEL", "gemini-custom-model")

    model = get_gemini_model()

    assert model == "gemini-custom-model"

def test_get_gemini_api_key_reads_environment_variable(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")

    api_key = get_gemini_api_key()

    assert api_key == "test-api-key"


def test_get_gemini_api_key_raises_error_when_missing(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    monkeypatch.setattr(
        "src.llm.config.load_dotenv",
        lambda *args, **kwargs: None
    )

    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        get_gemini_api_key()


def test_load_environment_variables_from_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "GEMINI_API_KEY=test-env-key\n",
        encoding="utf-8"
    )

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    api_key = get_gemini_api_key(env_file=env_file)

    assert api_key == "test-env-key"