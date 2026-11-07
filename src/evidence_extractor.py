
from src.skill_extractor import extract_skill_evidence


def extract_section_aware_evidence(sections):
    """
    Extract skill evidence from each resume section
    and attach section metadata.
    """

    evidence_by_skill = {}

    # Process the primary resume sections
    for section_name, section_text in sections.items():

        # Handle additional sections separately
        if section_name == "other_sections":
            continue

        if not section_text.strip():
            continue

        section_evidence = extract_skill_evidence(section_text)

        for skill, evidence_sentences in section_evidence.items():

            evidence_by_skill.setdefault(skill, [])

            for sentence in evidence_sentences:

                evidence_entry = {
                    "evidence": sentence,
                    "section": section_name
                }

                if evidence_entry not in evidence_by_skill[skill]:
                    evidence_by_skill[skill].append(evidence_entry)

    # Process additional recognized resume sections
    other_sections = sections.get("other_sections", {})

    for section_name, section_text in other_sections.items():

        if not section_text.strip():
            continue

        section_evidence = extract_skill_evidence(section_text)

        for skill, evidence_sentences in section_evidence.items():

            evidence_by_skill.setdefault(skill, [])

            for sentence in evidence_sentences:

                evidence_entry = {
                    "evidence": sentence,
                    "section": section_name
                }

                if evidence_entry not in evidence_by_skill[skill]:
                    evidence_by_skill[skill].append(evidence_entry)

    return evidence_by_skill
