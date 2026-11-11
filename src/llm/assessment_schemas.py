
from pydantic import BaseModel, Field, field_validator


class AssessmentDimension(BaseModel):
    """Evaluation of one resume assessment dimension."""

    score: int = Field(
        ge=0,
        le=20,
        description="Score between 0 and 20.",
    )
    rationale: str = Field(
        min_length=1,
        description="Evidence-based explanation for the score.",
    )
    supporting_evidence: list[str] = Field(
        default_factory=list,
        description="Statements from the resume supporting the evaluation.",
    )

    @field_validator("rationale")
    @classmethod
    def validate_rationale(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Rationale cannot be empty or whitespace.")
        return cleaned_value


class ResumeAssessment(BaseModel):
    """Structured AI assessment of an entire resume."""

    summary: str = Field(
        min_length=1,
        description="Concise overall resume assessment.",
    )

    technical_capabilities: AssessmentDimension
    experience_and_ownership: AssessmentDimension
    project_depth: AssessmentDimension
    measurable_impact: AssessmentDimension
    resume_clarity: AssessmentDimension

    strengths: list[str] = Field(
        description="Evidence-supported strengths.",
    )
    evidence_gaps: list[str] = Field(
        description="Important information missing or insufficiently supported.",
    )
    recommendations: list[str] = Field(
        description="Specific, actionable resume improvement recommendations.",
    )

    @field_validator("summary")
    @classmethod
    def validate_summary(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Summary cannot be empty or whitespace.")
        return cleaned_value

    @property
    def overall_score(self) -> int:
        """Calculate the total resume evidence score out of 100."""
        return sum(
            dimension.score
            for dimension in [
                self.technical_capabilities,
                self.experience_and_ownership,
                self.project_depth,
                self.measurable_impact,
                self.resume_clarity,
            ]
        )
