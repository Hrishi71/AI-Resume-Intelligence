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
        "Backend": ["Django"],
        "Frontend": ["React"],
        "Databases": ["PostgreSQL"],
        "AI and Machine Learning": ["Generative AI"]
    }