
from src.evidence_extractor import extract_section_aware_evidence


def test_evidence_from_professional_experience():
    sections = {
        "professional_experience": (
            "Developed backend applications using Python."
        )
    }

    result = extract_section_aware_evidence(sections)

    assert "Python" in result
    assert result["Python"][0]["section"] == "professional_experience"
    assert result["Python"][0]["evidence"] == (
        "Developed backend applications using Python."
    )


def test_evidence_from_projects():
    sections = {
        "projects": "Built a document assistant using Python."
    }

    result = extract_section_aware_evidence(sections)

    assert result["Python"][0]["section"] == "projects"


def test_same_skill_in_multiple_sections():
    sections = {
        "professional_experience": (
            "Developed backend applications using Python."
        ),
        "projects": (
            "Built a document assistant using Python."
        )
    }

    result = extract_section_aware_evidence(sections)

    assert len(result["Python"]) == 2

    section_names = [
        item["section"] for item in result["Python"]
    ]

    assert "professional_experience" in section_names
    assert "projects" in section_names


def test_evidence_from_technical_skills_section():
    sections = {
        "technical_skills": "Python, Django, PostgreSQL"
    }

    result = extract_section_aware_evidence(sections)

    assert "Python" in result
    assert result["Python"][0]["section"] == "technical_skills"


def test_missing_sections_do_not_raise_errors():
    sections = {
        "professional_experience": "",
        "projects": "Built an application using Python."
    }

    result = extract_section_aware_evidence(sections)

    assert "Python" in result


def test_no_matching_skills_returns_empty_dictionary():
    sections = {
        "professional_experience": (
            "Managed business operations and documentation."
        )
    }

    result = extract_section_aware_evidence(sections)

    assert result == {}


def test_multiple_skills_in_one_sentence():
    sections = {
        "projects": (
            "Built a backend application using Python and Django."
        )
    }

    result = extract_section_aware_evidence(sections)

    assert "Python" in result
    assert "Django" in result


def test_evidence_from_other_sections():
    sections = {
        "other_sections": {
            "professional_summary": (
                "Experienced in Python and Django development."
            )
        }
    }

    result = extract_section_aware_evidence(sections)

    assert "Python" in result
    assert (
        result["Python"][0]["section"]
        == "professional_summary"
    )
