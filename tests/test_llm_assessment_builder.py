from copy import deepcopy

from src.llm.assessment_builder import build_resume_assessment_input


def sample_resume_results():
    return {
        "candidate_info": {
            "name": "Test Candidate",
            "email": "test@example.com",
            "phone": "9876543210",
            "linkedin": "linkedin.com/in/test",
        },
        "skills": {
            "Programming": ["Python", "Java"],
        },
        "sections": {
            "professional_experience": "Built a Python application.",
            "projects": "Created a document assistant.",
        },
        "skill_evidence": {
            "Python": [
                {
                    "evidence": "Designed and implemented a Python application.",
                    "section": "professional_experience",
                    "classification": "practical_application",
                    "score": {
                        "total_score": 60,
                        "breakdown": {
                            "action": 20,
                            "technical_detail": 20,
                            "complexity": 20,
                            "measurable_outcome": 0,
                            "impact": 0,
                        },
                    },
                }
            ]
        },
    }


def test_builder_preserves_relevant_resume_information():
    result = build_resume_assessment_input(sample_resume_results())

    assert result["candidate_name"] == "Test Candidate"
    assert result["skills"] == {"Programming": ["Python", "Java"]}
    assert result["sections"]["professional_experience"] == (
        "Built a Python application."
    )

    python_evidence = result["evidence_by_skill"]["Python"][0]

    assert python_evidence["statement"] == (
        "Designed and implemented a Python application."
    )
    assert python_evidence["section"] == "professional_experience"
    assert python_evidence["classification"] == "practical_application"
    assert python_evidence["existing_score"] == 60


def test_builder_excludes_contact_information():
    result = build_resume_assessment_input(sample_resume_results())

    result_text = str(result)

    assert "test@example.com" not in result_text
    assert "9876543210" not in result_text
    assert "linkedin.com/in/test" not in result_text


def test_builder_does_not_modify_original_input():
    resume_results = sample_resume_results()
    original = deepcopy(resume_results)

    build_resume_assessment_input(resume_results)

    assert resume_results == original


def test_builder_handles_missing_optional_data():
    result = build_resume_assessment_input({})

    assert result["candidate_name"] is None
    assert result["skills"] == {}
    assert result["sections"] == {}
    assert result["evidence_by_skill"] == {}