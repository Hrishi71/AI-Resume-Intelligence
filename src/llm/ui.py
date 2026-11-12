
import streamlit as st

from src.llm.evaluator import evaluate_evidence
from src.llm.assessment_builder import build_resume_assessment_input
from src.llm.resume_assessor import assess_resume


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


def render_resume_assessment(
    resume_results: dict
) -> None:
    """
    Render a consolidated Gemini assessment of the complete resume.
    """

    if st.button(
        "Assess Full Resume with Gemini",
        key="full_resume_assessment_button",
        type="primary"
    ):
        try:
            with st.spinner("Gemini is assessing your complete resume..."):
                assessment_input = build_resume_assessment_input(
                    resume_results
                )

                assessment = assess_resume(assessment_input)

                st.session_state["full_resume_assessment"] = assessment

        except Exception as error:
            st.error(f"Full resume assessment failed: {error}")

    assessment = st.session_state.get("full_resume_assessment")

    if assessment is None:
        return

    st.success("Full resume assessment completed!")

    st.subheader("AI Resume Assessment")

    st.metric(
        label="Overall Resume Evidence Score",
        value=f"{assessment.overall_score}/100"
    )

    st.write("### Assessment Breakdown")

    dimensions = {
        "Technical Capabilities": assessment.technical_capabilities,
        "Experience & Ownership": assessment.experience_and_ownership,
        "Project Depth": assessment.project_depth,
        "Measurable Impact": assessment.measurable_impact,
        "Resume Clarity": assessment.resume_clarity,
    }

    for name, dimension in dimensions.items():
        st.write(f"**{name}: {dimension.score}/20**")
        st.caption(dimension.rationale)

        if dimension.supporting_evidence:
            with st.expander(f"Supporting evidence — {name}"):
                for evidence in dimension.supporting_evidence:
                    st.write(f"- {evidence}")

    st.write("### Assessment Summary")
    st.info(assessment.summary)

    st.write("### Strengths")
    for strength in assessment.strengths:
        st.markdown(f"- {strength}")

    st.write("### Evidence Gaps")
    for gap in assessment.evidence_gaps:
        st.markdown(f"- {gap}")

    st.write("### Recommendations")
    for recommendation in assessment.recommendations:
        st.markdown(f"- {recommendation}")
