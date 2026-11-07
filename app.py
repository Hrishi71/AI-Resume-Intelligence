
import streamlit as st

from src.resume_processor import process_resume_pdf


# Page configuration
st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="📄",
    layout="wide"
)


# Application heading
st.title("📄 AI Resume Intelligence")
st.write(
    "Upload your resume to extract candidate information "
    "and identify technical skills."
)

st.divider()


# PDF upload
uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
    help="Upload a PDF version of your resume."
)


# Analyze button
if st.button(
    "Analyze Resume",
    type="primary",
    disabled=uploaded_file is None
):

    try:
        with st.spinner("Analyzing your resume..."):

            # Read uploaded PDF as bytes
            pdf_bytes = uploaded_file.getvalue()

            # Process the resume
            results = process_resume_pdf(pdf_bytes)

        st.success("Resume analyzed successfully!")

        # Separate extracted information
        candidate_info = results["candidate_info"]
        skills = results["skills"]
        skill_evidence = results.get("skill_evidence", {})

        # Calculate total extracted skills
        total_skills = sum(
            len(category_skills)
            for category_skills in skills.values()
        )

        st.divider()
        st.header("Resume Analysis Results")

        # Candidate information
        st.subheader("👤 Candidate Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Name**")
            st.write(candidate_info["name"] or "Not found")

            st.write("**Email**")
            st.write(candidate_info["email"] or "Not found")

            st.write("**Phone**")
            st.write(candidate_info["phone"] or "Not found")

        with col2:
            st.write("**LinkedIn**")
            st.write(candidate_info["linkedin"] or "Not found")

            st.write("**GitHub**")
            st.write(candidate_info["github"] or "Not found")

        st.divider()

        # Skills overview
        st.subheader("💻 Technical Skills")

        st.metric(
            label="Total Skills Found",
            value=total_skills
        )


        # Display skills by category
        if total_skills > 0:

            for category, category_skills in skills.items():

                if category_skills:
                    with st.expander(
                        f"{category} ({len(category_skills)})",
                        expanded=True
                    ):

                        for skill in category_skills:

                            with st.expander(skill, expanded=False):

                                evidence_sentences = skill_evidence.get(
                                    skill, []
                                )

                                if evidence_sentences:
                                    st.write("**Evidence from your resume:**")

                                    for sentence in evidence_sentences:
                                        st.write(f"- {sentence}")

                                else:
                                    st.info(
                                        "No supporting sentence found in the resume."
                                    )

        else:
            st.info("No matching technical skills were found.")


    except Exception as error:
        st.error(f"Unable to analyze resume: {error}")
