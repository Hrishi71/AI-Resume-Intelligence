
from streamlit.testing.v1 import AppTest

from src.llm import ui as gemini_ui
from src.llm.schemas import DimensionScore, EvidenceEvaluation


def test_gemini_evaluation_runs_only_after_button_click(monkeypatch):
    """Gemini should run only when the user clicks the evaluation button."""

    fake_evaluation = EvidenceEvaluation(
        action=DimensionScore(
            score=15,
            reason="Clear implementation responsibility."
        ),
        technical_detail=DimensionScore(
            score=10,
            reason="Python is mentioned."
        ),
        complexity=DimensionScore(
            score=8,
            reason="Limited complexity details."
        ),
        measurable_outcome=DimensionScore(
            score=18,
            reason="A 30% improvement is measurable."
        ),
        impact=DimensionScore(
            score=12,
            reason="Operational impact is demonstrated."
        ),
        summary="Good evidence with room for more technical detail."
    )

    calls = []

    def mock_evaluate_evidence(evidence):
        calls.append(evidence)
        return fake_evaluation

    monkeypatch.setattr(
        gemini_ui,
        "evaluate_evidence",
        mock_evaluate_evidence
    )

    app = AppTest.from_string(
        """
from src.llm.ui import render_gemini_evaluation

render_gemini_evaluation(
    evidence="Implemented a Python API that reduced processing time by 30%.",
    key="test_gemini_evaluation"
)
"""
    ).run()

    # Gemini must not run automatically.
    assert calls == []

    # Click the evaluation button.
    app.button[0].click().run()

    # Gemini must run exactly once.
    assert len(calls) == 1

    # The evidence must be passed correctly.
    assert calls[0] == (
        "Implemented a Python API that reduced processing time by 30%."
    )

    # The result must be displayed.
    assert any(
        "63/100" in metric.value
        for metric in app.metric
    )
