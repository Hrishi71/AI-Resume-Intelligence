
from src.skill_extractor import extract_skill_evidence
from src.evidence_classifier import classify_evidence
from src.evidence_scorer import score_evidence


def extract_section_aware_evidence(sections):
    """
    Extract skill evidence from resume sections.

    Each evidence entry includes:
    - Original evidence sentence
    - Resume section
    - Evidence classification
    - Evidence quality score
    """

    evidence_by_skill = {}

    def process_section(section_name, section_text):
        if not section_text or not section_text.strip():
            return

        section_evidence = extract_skill_evidence(section_text)

        for skill, evidence_sentences in section_evidence.items():

            evidence_by_skill.setdefault(skill, [])

            for sentence in evidence_sentences:

                classification = classify_evidence(
                    sentence,
                    section_name
                )

                scoring_result = score_evidence(sentence)

                evidence_entry = {
                    "evidence": sentence,
                    "section": section_name,
                    "classification": classification,
                    "score": scoring_result
                }

                if evidence_entry not in evidence_by_skill[skill]:
                    evidence_by_skill[skill].append(evidence_entry)

    # Process primary resume sections
    for section_name, section_text in sections.items():

        if section_name == "other_sections":
            continue

        process_section(section_name, section_text)

    # Process additional recognized sections
    other_sections = sections.get("other_sections", {})

    for section_name, section_text in other_sections.items():
        process_section(section_name, section_text)

    return evidence_by_skill
