
from unittest.mock import MagicMock, patch

import pytest

from src.llm.assessment_schemas import ResumeAssessment
from src.llm.resume_assessor import assess_resume


def sample_assessment_data():
    dimension = {
        "score": 15,
        "rationale": "Relevant evidence is present.",
        "supporting_evidence": ["Built a Python application."],
    }

    return {
        "summary": "A technically relevant resume.",
        "technical_capabilities": dimension,
        "experience_and_ownership": dimension,
        "project_depth": dimension,
        "measurable_impact": dimension,
        "resume_clarity": dimension,
        "strengths": ["Python development"],
        "evidence_gaps": ["Limited measurable outcomes"],
        "recommendations": ["Add quantified results"],
    }


@patch("src.llm.resume_assessor._generate_assessment")
def test_assess_resume_returns_structured_assessment(mock_generate):
    expected = ResumeAssessment(**sample_assessment_data())
    mock_generate.return_value = expected

    result = assess_resume({"skills": {"Programming": ["Python"]}})

    assert result == expected
    mock_generate.assert_called_once()


@patch("src.llm.resume_assessor._generate_assessment")
def test_assess_resume_rejects_empty_input(mock_generate):
    with pytest.raises(ValueError, match="Resume assessment input cannot be empty"):
        assess_resume({})

    mock_generate.assert_not_called()
