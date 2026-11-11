
import streamlit as st

from src.llm.evaluator import evaluate_evidence


def render_gemini_evaluation(
    evidence: str,
    key: str
) -> None:
    """
    Render an on-demand Gemini evaluation for one evidence statement.
    """

    if st.button(
        "Evaluate with Gemini",
        key=key,
        type="secondary"
    ):
        try:
            with st.spinner("Gemini is evaluating this evidence..."):
                evaluation = evaluate_evidence(evidence)

            st.success("Gemini evaluation completed!")

            st.subheader("Gemini Evidence Evaluation")

            st.metric(
                label="AI Evidence Score",
                value=f"{evaluation.total_score}/100"
            )

            dimensions = {
                "Action": evaluation.action,
                "Technical Detail": evaluation.technical_detail,
                "Complexity": evaluation.complexity,
                "Measurable Outcome": evaluation.measurable_outcome,
                "Impact": evaluation.impact,
            }

            for dimension, result in dimensions.items():
                st.write(
                    f"**{dimension}: {result.score}/20**"
                )
                st.caption(result.reason)

            st.write("**AI Evaluation Summary**")
            st.info(evaluation.summary)

        except Exception as error:
            st.error(
                f"Gemini evaluation failed: {error}"
            )
