import pytest
from pydantic import ValidationError

from src.llm.schemas import DimensionScore, EvidenceEvaluation


def test_dimension_score_accepts_valid_score():
    result = DimensionScore(
        score=15,
        reason="The candidate describes a concrete implementation."
    )

    assert result.score == 15


@pytest.mark.parametrize("score", [-1, 21])
def test_dimension_score_rejects_out_of_range_score(score):
    with pytest.raises(ValidationError):
        DimensionScore(
            score=score,
            reason="Test reason"
        )


def test_evidence_evaluation_calculates_total_score():
    result = EvidenceEvaluation(
        action=DimensionScore(score=15, reason="Clear action."),
        technical_detail=DimensionScore(score=18, reason="Technical detail."),
        complexity=DimensionScore(score=12, reason="Moderate complexity."),
        measurable_outcome=DimensionScore(score=10, reason="Some measurement."),
        impact=DimensionScore(score=16, reason="Clear impact."),
        summary="The evidence demonstrates good technical capability."
    )

    assert result.total_score == 71

def test_dimension_score_rejects_empty_reason():
    with pytest.raises(ValidationError):
        DimensionScore(
            score=15,
            reason="   "
        )

def test_evidence_evaluation_total_score_is_between_zero_and_hundred():
    result = EvidenceEvaluation(
        action=DimensionScore(score=20, reason="Strong action."),
        technical_detail=DimensionScore(score=20, reason="Detailed technologies."),
        complexity=DimensionScore(score=20, reason="Complex implementation."),
        measurable_outcome=DimensionScore(score=20, reason="Measured results."),
        impact=DimensionScore(score=20, reason="Strong business impact."),
        summary="The evidence demonstrates strong overall impact."
    )

    assert 0 <= result.total_score <= 100
    assert result.total_score == 100

def test_evidence_evaluation_supports_zero_total_score():
    result = EvidenceEvaluation(
        action=DimensionScore(score=0, reason="No action evidence."),
        technical_detail=DimensionScore(score=0, reason="No technical detail."),
        complexity=DimensionScore(score=0, reason="No complexity evidence."),
        measurable_outcome=DimensionScore(score=0, reason="No measurement."),
        impact=DimensionScore(score=0, reason="No impact evidence."),
        summary="No meaningful evidence was identified."
    )

    assert result.total_score == 0

def test_evidence_evaluation_includes_overall_summary():
    result = EvidenceEvaluation(
        action=DimensionScore(score=15, reason="Clear action."),
        technical_detail=DimensionScore(score=18, reason="Good technical detail."),
        complexity=DimensionScore(score=12, reason="Moderate complexity."),
        measurable_outcome=DimensionScore(score=10, reason="Some measurement."),
        impact=DimensionScore(score=16, reason="Clear impact."),
        summary="The resume demonstrates good technical evidence."
    )

    assert result.summary == (
        "The resume demonstrates good technical evidence."
    )