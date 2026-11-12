
from streamlit.testing.v1 import AppTest

from src.llm import ui as assessment_ui
from src.llm.assessment_schemas import (
    AssessmentDimension,
    ResumeAssessment,
)


def sample_assessment():
    dimension = AssessmentDimension(
        score=15,
        rationale="Relevant technical evidence is present.",
        supporting_evidence=[
            "Developed a Django REST API using Python."
        ],
    )

    return ResumeAssessment(
        summary="A technically relevant resume with room for improvement.",
        technical_capabilities=dimension,
        experience_and_ownership=dimension,
        project_depth=dimension,
        measurable_impact=dimension,
        resume_clarity=dimension,
        strengths=["Python development", "Backend experience"],
        evidence_gaps=["Limited measurable outcomes"],
        recommendations=["Add quantified project results"],
    )


def test_full_resume_assessment_runs_only_after_button_click(monkeypatch):
    """The full assessment must run only after explicit user action."""

    builder_calls = []
    assessment_calls = []

    def mock_builder(resume_results):
        builder_calls.append(resume_results)
        return {"skills": {"Programming": ["Python"]}}

    def mock_assessor(assessment_input):
        assessment_calls.append(assessment_input)
        return sample_assessment()

    monkeypatch.setattr(
        assessment_ui,
        "build_resume_assessment_input",
        mock_builder,
    )

    monkeypatch.setattr(
        assessment_ui,
        "assess_resume",
        mock_assessor,
    )

    app = AppTest.from_string(
        """
from src.llm.ui import render_resume_assessment

render_resume_assessment(
    resume_results={"skills": {"Programming": ["Python"]}}
)
"""
    ).run()

    # No assessment before the button click.
    assert builder_calls == []
    assert assessment_calls == []

    # Trigger the assessment.
    app.button[0].click().run()

    # Builder and Gemini evaluator should each run once.
    assert len(builder_calls) == 1
    assert len(assessment_calls) == 1

    # Overall score should be displayed.
    assert any(
        "75/100" in metric.value
        for metric in app.metric
    )

    # Assessment insights should be visible.
    displayed_text = " ".join(
        element.value
        for element in app.markdown
    )

    assert "Python development" in displayed_text
    assert "Limited measurable outcomes" in displayed_text


def test_full_resume_assessment_is_persisted_in_session_state(monkeypatch):
    """Assessment results should survive Streamlit reruns."""

    monkeypatch.setattr(
        assessment_ui,
        "build_resume_assessment_input",
        lambda resume_results: {"skills": {"Programming": ["Python"]}},
    )

    monkeypatch.setattr(
        assessment_ui,
        "assess_resume",
        lambda assessment_input: sample_assessment(),
    )

    app = AppTest.from_string(
        """
from src.llm.ui import render_resume_assessment

render_resume_assessment(
    resume_results={"skills": {"Programming": ["Python"]}}
)
"""
    ).run()

    app.button[0].click().run()

    assert (
        app.session_state["full_resume_assessment"].overall_score
        == 75
    )
