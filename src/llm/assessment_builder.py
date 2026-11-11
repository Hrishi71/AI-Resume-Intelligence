
def build_resume_assessment_input(
    resume_results: dict
) -> dict:
    """
    Prepare extracted resume information for full AI assessment.

    Excludes personal contact information and preserves
    the existing evidence and rule-based scores.
    """

    candidate_info = resume_results.get("candidate_info", {})

    skills = resume_results.get("skills", {})
    skill_evidence = resume_results.get("skill_evidence", {})
    sections = resume_results.get("sections", {})

    evidence_by_skill = {}

    for skill, entries in skill_evidence.items():

        evidence_by_skill[skill] = []

        for entry in entries:

            score = entry.get("score", {})

            evidence_by_skill[skill].append({
                "statement": entry.get("evidence", ""),
                "section": entry.get("section", ""),
                "classification": entry.get("classification", ""),
                "existing_score": score.get("total_score", 0),
                "score_breakdown": score.get("breakdown", {})
            })

    return {
        "candidate_name": candidate_info.get("name"),
        "skills": skills,
        "sections": sections,
        "evidence_by_skill": evidence_by_skill
    }
