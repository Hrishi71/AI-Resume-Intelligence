from unittest import result

from src.resume_processor import process_resume


def test_process_resume():

    resume = """
        I have experience in Python,

        Django, React.js, PostgreSQL
        and GenAI.
    """

    result = process_resume(resume)

    assert result == {
        "Programming Languages": ["Python"],
        "Backend Development": ["Django"],
        "Frontend Development": ["React"],
        "Databases and Storage": ["PostgreSQL"],
        "Generative AI and LLMs": ["Generative AI"]
    }