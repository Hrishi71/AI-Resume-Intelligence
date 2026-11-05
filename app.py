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
    "Upload your resume to automatically identify "
    "your technical skills."
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

        # Calculate total extracted skills
        total_skills = sum(
            len(skills)
            for skills in results.values()
        )

        st.subheader("Analysis Results")

        st.metric(
            label="Total Skills Found",
            value=total_skills
        )

        # Display skills by category
        if total_skills > 0:

            for category, skills in results.items():

                if skills:
                    st.subheader(category)
                    st.write(", ".join(skills))

        else:
            st.info("No matching skills were found.")

    except Exception as error:

        st.error(f"Unable to analyze resume: {error}")