
from src.evidence_classifier import classify_evidence


def test_classify_skill_mention():
    result = classify_evidence(
        "Python, Django and FastAPI",
        "technical_skills"
    )

    assert result == "skill_mention"


def test_classify_practical_application():
    result = classify_evidence(
        "Developed backend applications using Python.",
        "professional_experience"
    )

    assert result == "practical_application"


def test_classify_project_application():
    result = classify_evidence(
        "Built a document chatbot using Python and LangChain.",
        "projects"
    )

    assert result == "project_application"


def test_classify_certification():
    result = classify_evidence(
        "AWS Certified Solutions Architect.",
        "certifications"
    )

    assert result == "certification"


def test_certification_keyword_overrides_section():
    result = classify_evidence(
        "Certified Kubernetes Administrator.",
        "professional_experience"
    )

    assert result == "certification"


def test_empty_evidence():
    result = classify_evidence("", "projects")

    assert result == "skill_mention"


def test_unclassified_section_with_action():
    result = classify_evidence(
        "Implemented REST APIs using Django.",
        "unclassified"
    )

    assert result == "practical_application"


def test_project_without_action_is_skill_mention():
    result = classify_evidence(
        "Python and Django",
        "projects"
    )

    assert result == "skill_mention"
