
from src.evidence_extractor import extract_section_aware_evidence


def test_evidence_contains_quality_score():
    sections = {
        "professional_experience": (
            "Developed REST APIs using Python."
        )
    }

    result = extract_section_aware_evidence(sections)

    python_evidence = result["Python"][0]

    assert "score" in python_evidence
    assert python_evidence["score"]["total_score"] == 40


def test_evidence_score_contains_all_dimensions():
    sections = {
        "projects": (
            "Designed scalable microservices using Python and Kafka."
        )
    }

    result = extract_section_aware_evidence(sections)

    score = result["Python"][0]["score"]

    expected_dimensions = {
        "action",
        "technical_detail",
        "complexity",
        "measurable_outcome",
        "impact"
    }

    assert set(score["breakdown"].keys()) == expected_dimensions


def test_same_skill_has_scores_for_multiple_sections():
    sections = {
        "professional_experience": (
            "Developed REST APIs using Python."
        ),
        "projects": (
            "Built a Python application."
        )
    }

    result = extract_section_aware_evidence(sections)

    assert len(result["Python"]) == 2

    for entry in result["Python"]:
        assert "score" in entry
        assert 0 <= entry["score"]["total_score"] <= 100


def test_evidence_classification_is_preserved():
    sections = {
        "projects": (
            "Developed a REST API using Python."
        )
    }

    result = extract_section_aware_evidence(sections)

    evidence = result["Python"][0]

    assert evidence["classification"] == "project_application"
    assert evidence["section"] == "projects"


def test_evidence_from_other_sections_is_scored():
    sections = {
        "other_sections": {
            "technical_skills": "Python, Django"
        }
    }

    result = extract_section_aware_evidence(sections)

    assert "Python" in result
    assert "score" in result["Python"][0]
