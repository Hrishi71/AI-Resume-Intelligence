from unittest import result

from src.skill_extractor import extract_skills
from src.skill_extractor import extract_skills_by_category
from src.skill_extractor import normalize_skill
from src.skill_extractor import extract_skill_evidence


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

def test_normalize_jwt():
    assert normalize_skill("JWT") == "JWT Authentication"


def test_normalize_jwt_authentication():
    assert normalize_skill("JWT Authentication") == "JWT Authentication"


def test_normalize_rbac():
    assert normalize_skill("RBAC") == "Role-Based Access Control"


def test_normalize_rest():
    assert normalize_skill("REST") == "RESTful APIs"


def test_normalize_react_js():
    assert normalize_skill("React.js") == "React"


def test_normalize_postgres():
    assert normalize_skill("Postgres") == "PostgreSQL"


def test_preserve_distinct_ci_cd_concepts():
    assert normalize_skill("Continuous Delivery") == "Continuous Delivery"
    assert normalize_skill("Continuous Deployment") == "Continuous Deployment"

def test_extract_skills_normalizes_jwt():
    text = "Experienced in JWT and JWT Authentication."

    skills = extract_skills(text)

    assert "JWT Authentication" in skills
    assert "JWT" not in skills


def test_extract_skills_normalizes_rbac():
    text = "Experienced in RBAC and Role-Based Access Control."

    skills = extract_skills(text)

    assert "Role-Based Access Control" in skills
    assert "RBAC" not in skills


def test_extract_skills_normalizes_postgres():
    text = "Experienced in Postgres and PostgreSQL."

    skills = extract_skills(text)

    assert "PostgreSQL" in skills

def test_no_duplicate_skills_across_categories():
    text = "JavaScript TypeScript Cypher Pandas"

    categorized_skills = extract_skills_by_category(text)

    all_skills = [
        skill
        for skills in categorized_skills.values()
        for skill in skills
    ]

    assert all_skills.count("JavaScript") == 1
    assert all_skills.count("TypeScript") == 1
    assert all_skills.count("Cypher") == 1
    assert all_skills.count("Pandas") == 1

def test_jwt_authentication_belongs_to_security_category():
    text = "Experienced in JWT Authentication."

    categorized_skills = extract_skills_by_category(text)

    assert "JWT Authentication" in categorized_skills["Security"]

    assert "JWT Authentication" not in categorized_skills.get(
        "Backend Development", []
    )

def test_extract_skill_evidence():
    text = (
        "Built backend applications using Python and Django. "
        "Used PostgreSQL for database persistence."
    )

    evidence = extract_skill_evidence(text)

    assert evidence["Python"] == [
        "Built backend applications using Python and Django."
    ]

    assert evidence["Django"] == [
        "Built backend applications using Python and Django."
    ]

    assert evidence["PostgreSQL"] == [
        "Used PostgreSQL for database persistence."
    ]


def test_extract_skill_evidence_with_alias():
    text = "Developed applications using Postgres."

    evidence = extract_skill_evidence(text)

    assert "PostgreSQL" in evidence
    assert evidence["PostgreSQL"] == [
        "Developed applications using Postgres."
    ]


def test_no_evidence_for_unmatched_skills():
    text = "Worked on several software projects."

    evidence = extract_skill_evidence(text)

    assert evidence == {}

def test_extract_skill_evidence_from_resume_bullets():
    text = """
    Professional Experience

    Developed backend applications using Django
    Built REST APIs using FastAPI
    Worked with PostgreSQL
    Implemented authentication using JWT
    """

    evidence = extract_skill_evidence(text)

    assert "Django" in evidence
    assert "FastAPI" in evidence
    assert "PostgreSQL" in evidence
    assert "JWT Authentication" in evidence

    assert evidence["Django"] == [
        "Developed backend applications using Django"
    ]

    assert evidence["FastAPI"] == [
        "Built REST APIs using FastAPI"
    ]

def test_extract_skill_evidence_from_wrapped_lines():
    text = """
    Developed scalable backend applications
    using Python and Django for enterprise
    workloads.
    """

    evidence = extract_skill_evidence(text)

    expected_sentence = (
        "Developed scalable backend applications "
        "using Python and Django for enterprise workloads."
    )

    assert evidence["Python"] == [expected_sentence]
    assert evidence["Django"] == [expected_sentence]