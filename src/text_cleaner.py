def clean_resume_text(text):
    """
    Remove unnecessary whitespace from resume text.
    """
    cleaned_text = " ".join(text.split())

    return cleaned_text