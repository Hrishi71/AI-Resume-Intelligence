from unittest.mock import MagicMock

from src.llm import client


def test_get_gemini_client_initializes_with_api_key(monkeypatch):
    mock_gemini_client = MagicMock()

    monkeypatch.setattr(
        client.genai,
        "Client",
        lambda api_key: mock_gemini_client
    )

    monkeypatch.setattr(
        client,
        "get_gemini_api_key",
        lambda: "test-api-key"
    )

    result = client.get_gemini_client()

    assert result is mock_gemini_client

def test_get_model_name_returns_configured_model(monkeypatch):
    monkeypatch.setattr(
        client,
        "get_gemini_model",
        lambda: "gemini-3.5-flash-lite"
    )

    model = client.get_model_name()

    assert model == "gemini-3.5-flash-lite"