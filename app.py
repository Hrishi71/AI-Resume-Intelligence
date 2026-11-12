
import streamlit as st

from src.resume_processor import process_resume_pdf
from src.llm.ui import (
    render_gemini_evaluation,
    render_resume_assessment,
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    [data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
    }

    [data-testid="stExpander"] {
        border-radius: 12px;
        border-color: var(--border-color);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
    }

    .section-description {
        color: var(--text-color);
        opacity: 0.65;
        font-size: 0.9rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "resume_results" not in st.session_state:
    st.session_state["resume_results"] = None


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

header_left, header_right = st.columns([4, 1])

with header_left:
    st.title("📄 Resume Intelligence")
    st.caption(
        "Understand your resume. Discover your strengths. "
        "Improve your engineering profile."
    )

with header_right:
    st.markdown(" ")
    st.caption("AI-powered resume analysis")


st.divider()


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

with st.container(border=True):

    st.subheader("📤 Upload Resume")

    upload_col, button_col = st.columns([3, 1])

    with upload_col:
        uploaded_file = st.file_uploader(
            "Choose your resume",
            type=["pdf"],
            help="Upload a PDF version of your resume.",
            label_visibility="collapsed",
        )

    with button_col:
        st.markdown(" ")

        analyze_clicked = st.button(
            "Analyze Resume",
            type="primary",
            use_container_width=True,
            disabled=uploaded_file is None,
        )

    if uploaded_file:
        st.caption(f"Selected file: {uploaded_file.name}")


if analyze_clicked:

    try:
        with st.spinner("Analyzing your resume..."):

            pdf_bytes = uploaded_file.getvalue()

            st.session_state["resume_results"] = (
                process_resume_pdf(pdf_bytes)
            )

        st.success("Resume analyzed successfully!")

    except Exception as error:
        st.error(f"Unable to analyze resume: {error}")


# --------------------------------------------------
# RESULTS DASHBOARD
# --------------------------------------------------

results = st.session_state["resume_results"]


if results is not None:

    candidate_info = results.get("candidate_info", {})
    skills = results.get("skills", {})
    skill_evidence = results.get("skill_evidence", {})

    total_skills = sum(
        len(category_skills)
        for category_skills in skills.values()
    )

    total_evidence = sum(
        len(entries)
        for entries in skill_evidence.values()
    )

    st.markdown("## Analysis Dashboard")
    st.caption("Your extracted resume information at a glance.")

    # --------------------------------------------------
    # SUMMARY CARDS
    # --------------------------------------------------

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Technical Skills",
            total_skills,
            help="Total unique skills detected by the extractor.",
        )

    with metric2:
        st.metric(
            "Evidence Entries",
            total_evidence,
            help="Extracted statements associated with skills.",
        )

    with metric3:
        st.metric(
            "Skill Categories",
            sum(bool(value) for value in skills.values()),
        )

    st.divider()

    # --------------------------------------------------
    # DASHBOARD NAVIGATION
    # --------------------------------------------------

    overview_tab, candidate_tab, skills_tab = st.tabs(
        [
            "📊 Overview",
            "👤 Candidate",
            "💻 Skills & Evidence",
        ]
    )

    # --------------------------------------------------
    # OVERVIEW TAB
    # --------------------------------------------------

    with overview_tab:

        st.subheader("Resume Overview")

        overview_col1, overview_col2 = st.columns(2)

        with overview_col1:

            with st.container(border=True):

                st.markdown("### 👤 Candidate")

                st.write(
                    f"**Name:** {candidate_info.get('name') or 'Not found'}"
                )

                st.write(
                    f"**Email:** {candidate_info.get('email') or 'Not found'}"
                )

                st.write(
                    f"**Phone:** {candidate_info.get('phone') or 'Not found'}"
                )

        with overview_col2:

            with st.container(border=True):

                st.markdown("### 🔗 Professional Profiles")

                st.write(
                    f"**LinkedIn:** {candidate_info.get('linkedin') or 'Not found'}"
                )

                st.write(
                    f"**GitHub:** {candidate_info.get('github') or 'Not found'}"
                )

        st.subheader("Technical Skill Distribution")

        if total_skills:

            populated_categories = {
                category: category_skills
                for category, category_skills in skills.items()
                if category_skills
            }

            category_columns = st.columns(3)

            for index, (category, category_skills) in enumerate(
                populated_categories.items()
            ):

                with category_columns[index % 3]:

                    with st.container(border=True):

                        st.markdown(f"**{category}**")

                        st.metric(
                            "Skills",
                            len(category_skills),
                        )

                        st.caption(
                            ", ".join(category_skills)
                        )

        else:
            st.info("No technical skills were detected.")

            # --------------------------------------------------
        # FULL RESUME AI ASSESSMENT
        # --------------------------------------------------

        st.divider()

        st.subheader("AI-Powered Resume Assessment")

        st.caption(
            "Get a consolidated assessment of your technical "
            "capabilities, experience, projects and resume quality."
        )

        render_resume_assessment(results)

    # --------------------------------------------------
    # CANDIDATE TAB
    # --------------------------------------------------

    with candidate_tab:

        st.subheader("Candidate Profile")

        with st.container(border=True):

            st.markdown("### Personal Information")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Full Name**")
                st.write(candidate_info.get("name") or "Not found")

                st.write("**Email Address**")
                st.write(candidate_info.get("email") or "Not found")

                st.write("**Phone Number**")
                st.write(candidate_info.get("phone") or "Not found")

            with col2:
                st.write("**LinkedIn Profile**")
                st.write(candidate_info.get("linkedin") or "Not found")

                st.write("**GitHub Profile**")
                st.write(candidate_info.get("github") or "Not found")


    # --------------------------------------------------
    # SIMPLE SKILLS & EVIDENCE EXPLORER
    # --------------------------------------------------

    with skills_tab:

        st.subheader("Skills & Evidence")
        st.caption(
            "Select a category and skill to explore its resume evidence."
        )

        # Step 1: Select category
        available_categories = [
            category
            for category, category_skills in skills.items()
            if category_skills
        ]

        if not available_categories:

            st.info("No technical skills found.")

        else:

            selected_category = st.selectbox(
                "Select a skill category",
                available_categories,
                key="explorer_category",
            )

            # Step 2: Select skill
            category_skills = skills[selected_category]

            selected_skill = st.selectbox(
                "Select a skill",
                category_skills,
                key="explorer_skill",
            )

            # Get evidence for selected skill
            evidence_entries = skill_evidence.get(
                selected_skill,
                [],
            )

            st.divider()

            st.markdown(f"### {selected_skill}")

            if not evidence_entries:

                st.info(
                    "This skill was detected in the resume, "
                    "but no supporting experience was identified."
                )

            else:

                # Sort strongest evidence first
                sorted_evidence = sorted(
                    evidence_entries,
                    key=lambda entry: entry.get(
                        "score", {}
                    ).get("total_score", 0),
                    reverse=True,
                )

                st.caption(
                    f"{len(sorted_evidence)} supporting evidence entries"
                )

                # Step 3: Select evidence
                evidence_options = list(
                    range(len(sorted_evidence))
                )

                selected_evidence_index = st.selectbox(
                    "Choose evidence to inspect",
                    evidence_options,
                    format_func=lambda index: (
                        f"Evidence {index + 1} · "
                        f"{sorted_evidence[index].get('section', 'Unknown').replace('_', ' ').title()}"
                    ),
                    key=f"evidence_select_{selected_category}_{selected_skill}",
                )

                entry = sorted_evidence[selected_evidence_index]

                evidence_text = entry.get("evidence", "")

                score_data = entry.get("score", {})

                score = score_data.get("total_score", 0)

                breakdown = score_data.get("breakdown", {})

                # Main evidence display
                st.markdown("**Resume evidence**")

                st.write(evidence_text)

                # Basic metadata
                meta_col1, meta_col2 = st.columns(2)

                with meta_col1:
                    st.caption(
                        "Section: "
                        + entry.get("section", "Unknown")
                        .replace("_", " ")
                        .title()
                    )

                with meta_col2:
                    st.caption(
                        "Evidence type: "
                        + entry.get("classification", "Unknown")
                        .replace("_", " ")
                        .title()
                    )

                # Score
                score_col, progress_col = st.columns([1, 3])

                with score_col:
                    st.metric(
                        "Evidence quality",
                        f"{score}/100",
                    )

                with progress_col:
                    st.write("Score strength")
                    st.progress(score)

                # Details only when requested
                with st.expander("View detailed evaluation"):

                    st.markdown("**Score breakdown**")

                    for dimension, points in breakdown.items():

                        st.write(
                            f"{dimension.replace('_', ' ').title()}: "
                            f"{points}/20"
                        )

                    st.markdown("**Scoring reasons**")

                    reasons = score_data.get("reasons", [])

                    if reasons:
                        for reason in reasons:
                            st.write(f"• {reason}")
                    else:
                        st.caption("No scoring reasons available.")

                    st.divider()

                    render_gemini_evaluation(
                        evidence=evidence_text,
                        key=(
                            f"gemini_{selected_category}_"
                            f"{selected_skill}_"
                            f"{selected_evidence_index}"
                        ),
                    )

                st.caption(
                    "Evidence quality measures how strongly the resume "
                    "demonstrates this skill. It does not verify proficiency."
                )

else:

    # --------------------------------------------------
    # EMPTY STATE
    # --------------------------------------------------

    with st.container(border=True):

        st.markdown("### 🚀 Ready to analyze your resume?")

        st.write(
            "Upload your PDF resume above to explore your "
            "candidate profile, technical skills and supporting evidence."
        )

        st.caption(
            "Supported format: PDF"
        )
