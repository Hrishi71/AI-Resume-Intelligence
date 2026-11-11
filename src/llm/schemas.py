from pydantic import BaseModel, Field
from pydantic import BaseModel, Field, field_validator

class DimensionScore(BaseModel):
    """Score and explanation for one evaluation dimension."""

    score: int = Field(
        ge=0,
        le=20,
        description="Score between 0 and 20."
    )

    reason: str = Field(
        min_length=1,
        description="Explanation supporting the assigned score."
    )

    @field_validator("reason")
    @classmethod
    def validate_reason(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Reason cannot be empty or whitespace.")

        return cleaned_value


class EvidenceEvaluation(BaseModel):
    """Structured evaluation of one piece of resume evidence."""

    action: DimensionScore
    technical_detail: DimensionScore
    complexity: DimensionScore
    measurable_outcome: DimensionScore
    impact: DimensionScore

    summary: str = Field(
    min_length=1,
    description="Overall explanation of the evidence evaluation."
    )

    @field_validator("summary")
    @classmethod
    def validate_summary(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Summary cannot be empty or whitespace.")

        return cleaned_value

    @property
    def total_score(self) -> int:
        """Calculate the total score instead of trusting the LLM."""
        return (
            self.action.score
            + self.technical_detail.score
            + self.complexity.score
            + self.measurable_outcome.score
            + self.impact.score
        )