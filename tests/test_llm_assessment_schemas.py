
import pytest
from pydantic import ValidationError

from src.llm.assessment_schemas import (
    AssessmentDimension,
    ResumeAssessment,
)


def sample_assessment():
    dimension = {
        "score": 15,
        "rationale": "The resume provides relevant technical evidence.",
        "supporting_evidence": ["Built a Python application."],
    }

    return {
        "summary": "A technically relevant resume with room for stronger impact metrics.",
        "technical_capabilities": dimension,
        "experience_and_ownership": dimension,
        "project_depth": dimension,
        "measurable_impact": dimension,
        "resume_clarity": dimension,
        "strengths": ["Python development", "Project experience"],
        "evidence_gaps": ["Limited measurable outcomes"],
        "recommendations": ["Add quantified project results"],
    }


def test_assessment_dimension_accepts_valid_data():
    dimension = AssessmentDimension(
        score=15,
        rationale="Clear technical evidence.",
        supporting_evidence=["Built a Python application."],
    )

    assert dimension.score == 15
    assert dimension.rationale == "Clear technical evidence."


def test_assessment_dimension_rejects_score_above_20():
    with pytest.raises(ValidationError):
        AssessmentDimension(
            score=21,
            rationale="Invalid score.",
            supporting_evidence=[],
        )


def test_assessment_dimension_rejects_negative_score():
    with pytest.raises(ValidationError):
        AssessmentDimension(
            score=-1,
            rationale="Invalid score.",
            supporting_evidence=[],
        )


def test_resume_assessment_calculates_overall_score():
    assessment = ResumeAssessment(**sample_assessment())

    assert assessment.overall_score == 75


def test_resume_assessment_rejects_blank_summary():
    data = sample_assessment()
    data["summary"] = "   "

    with pytest.raises(ValidationError):
        ResumeAssessment(**data)


def test_resume_assessment_requires_all_five_dimensions():
    data = sample_assessment()
    del data["project_depth"]

    with pytest.raises(ValidationError):
        ResumeAssessment(**data)
