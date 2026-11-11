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





def test_process_resume_includes_skill_evidence():
    resume_text = (
        "Developed backend applications using Python and Django.\n"
        "Built REST APIs using FastAPI."
    )

    result = process_resume(resume_text)

    assert "skill_evidence" in result

    evidence = result["skill_evidence"]

    python_evidence = evidence["Python"][0]

    assert python_evidence["evidence"] == (
        "Developed backend applications using Python and Django."
    )
    assert python_evidence["section"] == "unclassified"
    assert python_evidence["classification"] == "practical_application"

    assert "score" in python_evidence
    assert python_evidence["score"]["total_score"] == 40



def test_process_resume_preserves_existing_output():
    resume_text = (
        "Developed applications using Python and Django."
    )

    result = process_resume(resume_text)

    assert "candidate_info" in result
    assert "skills" in result
    assert "skill_evidence" in result

    assert isinstance(result["candidate_info"], dict)
    assert isinstance(result["skills"], dict)
    assert isinstance(result["skill_evidence"], dict)
