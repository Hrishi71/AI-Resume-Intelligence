import pytest
from unittest.mock import MagicMock
from src.llm import evaluator
from src.llm.schemas import DimensionScore, EvidenceEvaluation
from pydantic import ValidationError


def test_evaluate_evidence_returns_validated_evaluation(monkeypatch):
    mock_evaluation = EvidenceEvaluation(
        action=DimensionScore(
            score=18,
            reason="The candidate clearly describes implementing a solution."
        ),
        technical_detail=DimensionScore(
            score=17,
            reason="The candidate identifies specific technologies."
        ),
        complexity=DimensionScore(
            score=15,
            reason="The work demonstrates moderate technical complexity."
        ),
        measurable_outcome=DimensionScore(
            score=16,
            reason="The evidence includes a measurable result."
        ),
        impact=DimensionScore(
            score=14,
            reason="The work describes a practical outcome."
        ),
        summary="The evidence demonstrates strong technical application."
    )

    mock_client = MagicMock()

    monkeypatch.setattr(
        evaluator,
        "get_gemini_client",
        lambda: mock_client
    )

    monkeypatch.setattr(
        evaluator,
        "_generate_evaluation",
        lambda client, evidence: mock_evaluation
    )

    result = evaluator.evaluate_evidence(
        "Implemented a Python API that reduced processing time by 30%."
    )

    assert isinstance(result, EvidenceEvaluation)
    assert result.total_score == 80
    assert result.summary == (
        "The evidence demonstrates strong technical application."
    )

@pytest.mark.parametrize("evidence", ["", "   ", "\n\t"])
def test_evaluate_evidence_rejects_empty_input(evidence, monkeypatch):
    mock_get_client = MagicMock()

    monkeypatch.setattr(
        evaluator,
        "get_gemini_client",
        mock_get_client
    )

    with pytest.raises(ValueError, match="Evidence cannot be empty"):
        evaluator.evaluate_evidence(evidence)

    mock_get_client.assert_not_called()

def test_evaluate_evidence_strips_surrounding_whitespace(monkeypatch):
    mock_client = MagicMock()
    mock_generate = MagicMock(
        return_value=MagicMock(spec=EvidenceEvaluation)
    )

    monkeypatch.setattr(
        evaluator,
        "get_gemini_client",
        lambda: mock_client
    )

    monkeypatch.setattr(
        evaluator,
        "_generate_evaluation",
        mock_generate
    )

    evaluator.evaluate_evidence(
        "   Built a Python API.   "
    )

    mock_generate.assert_called_once_with(
        client=mock_client,
        evidence="Built a Python API."
    )

def test_generate_evaluation_uses_structured_output():
    mock_client = MagicMock()

    expected_evaluation = EvidenceEvaluation(
        action=DimensionScore(score=18, reason="Clear implementation."),
        technical_detail=DimensionScore(score=17, reason="Specific technologies."),
        complexity=DimensionScore(score=15, reason="Moderate complexity."),
        measurable_outcome=DimensionScore(score=16, reason="Measured result."),
        impact=DimensionScore(score=14, reason="Practical impact."),
        summary="Strong technical evidence."
    )

    mock_response = MagicMock()
    mock_response.parsed = expected_evaluation

    mock_client.models.generate_content.return_value = mock_response

    result = evaluator._generate_evaluation(
        client=mock_client,
        evidence="Implemented a Python API that reduced processing time by 30%."
    )

    assert result == expected_evaluation

    mock_client.models.generate_content.assert_called_once()

    call_arguments = mock_client.models.generate_content.call_args.kwargs

    assert call_arguments["model"] == evaluator.get_model_name()
    assert "30%" in call_arguments["contents"]
    assert call_arguments["config"].response_mime_type == "application/json"
    assert call_arguments["config"].response_schema == EvidenceEvaluation

def test_generate_evaluation_rejects_empty_gemini_response():
    mock_client = MagicMock()

    mock_response = MagicMock()
    mock_response.parsed = None

    mock_client.models.generate_content.return_value = mock_response

    with pytest.raises(
        ValueError,
        match="empty or invalid evaluation response"
    ):
        evaluator._generate_evaluation(
            client=mock_client,
            evidence="Built a Python API."
        )

def test_generate_evaluation_rejects_malformed_response():
    mock_client = MagicMock()

    mock_response = MagicMock()
    mock_response.parsed = {
        "action": {
            "score": 18,
            "reason": "Clear implementation."
        }
    }

    mock_client.models.generate_content.return_value = mock_response

    with pytest.raises(ValidationError):
        evaluator._generate_evaluation(
            client=mock_client,
            evidence="Built a Python API."
        )

def test_generate_evaluation_propagates_api_errors():
    mock_client = MagicMock()

    mock_client.models.generate_content.side_effect = RuntimeError(
        "Gemini API unavailable"
    )

    with pytest.raises(RuntimeError, match="Gemini API unavailable"):
        evaluator._generate_evaluation(
            client=mock_client,
            evidence="Built a Python API."
        )