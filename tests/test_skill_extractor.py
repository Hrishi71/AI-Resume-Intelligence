from unittest import result

from src.skill_extractor import extract_skills
from src.skill_extractor import extract_skills_by_category


def test_extract_multiple_skills():
    resume = "I know Python, Django and React."
    result = extract_skills(resume)

    assert result == ["Python", "Django", "React"]


def test_case_insensitive_matching():
    resume = "I KNOW PYTHON AND DJANGO."
    result = extract_skills(resume)

    assert result == ["Python", "Django"]


def test_java_should_not_match_javascript():
    resume = "I have experience in JavaScript."
    result = extract_skills(resume)

    assert "JavaScript" in result
    assert "Java" not in result


def test_no_skills_found():
    resume = "I enjoy learning new things."
    result = extract_skills(resume)

    assert result == []


def test_extract_skills_by_category():
    resume = """
    I have experience in Python, Django,
    React.js, PostgreSQL and GenAI.
    """

    result = extract_skills_by_category(resume)

    assert result == {
        "Programming Languages": ["Python"],
        "Backend Development": ["Django"],
        "Frontend Development": ["React"],
        "Databases and Storage": ["PostgreSQL"],
        "Generative AI and LLMs": ["Generative AI"]
    }
    
def test_react_js_should_not_match_javascript():
    resume = "I have experience in React.js."

    result = extract_skills(resume)

    assert "React" in result
    assert "JavaScript" not in result


def test_alias_react_js():

    resume = "Experienced in React.js"

    result = extract_skills(resume)

    assert "React" in result


def test_alias_genai():

    resume = "Worked with GenAI applications"

    result = extract_skills(resume)

    assert "Generative AI" in result


def test_alias_postgres():

    resume = "Used Postgres databases"

    result = extract_skills(resume)

    assert "PostgreSQL" in result


def test_no_duplicate_skills():

    resume = "Python, Django, React.js and PostgreSQL"

    result = extract_skills(resume)

    assert len(result) == len(set(result))


def test_c_should_not_match_cpp():

    resume = "Experienced in C++ development"

    result = extract_skills(resume)

    assert "C" not in result
