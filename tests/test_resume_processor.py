from unittest import result

from src.resume_processor import process_resume


def test_process_resume():
    resume = """
        I have experience in Python,
        Django, React.js, PostgreSQL
        and GenAI.
    """

    result = process_resume(resume)

    assert result["skills"] == {
        "Programming Languages": ["Python"],
        "Backend Development": ["Django"],
        "Frontend Development": ["React"],
        "Databases and Storage": ["PostgreSQL"],
        "Generative AI and LLMs": ["Generative AI"]
    }

    assert result["candidate_info"] == {
        "name": None,
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None
    }

def test_process_resume_extracts_unlabelled_name():

    resume = """
    Hrishikesh Anant Deshpande
    AI Engineer | Backend Software Engineer
    Email: hrishi@example.com
    """

    result = process_resume(resume)

    assert result["candidate_info"]["name"] == (
        "Hrishikesh Anant Deshpande"
    )