
from src.text_cleaner import clean_resume_text
from src.skill_extractor import extract_skills_by_category
from src.resume_parser import extract_text_from_pdf
from src.candidate_info_extractor import extract_candidate_info
from src.section_extractor import extract_resume_sections
from src.evidence_extractor import extract_section_aware_evidence


def process_resume(resume_text):

    # Extract candidate information from original text
    candidate_info = extract_candidate_info(resume_text)

    # Clean text for skill extraction
    cleaned_text = clean_resume_text(resume_text)

    # Extract technical skills
    extracted_skills = extract_skills_by_category(cleaned_text)

    # Identify resume sections
    sections = extract_resume_sections(resume_text)

    # Prepare sections for evidence extraction
    evidence_sections = {
        key: value
        for key, value in sections.items()
        if key != "other_sections" and value.strip()
    }

    # Include additional recognized sections
    evidence_sections.update(sections.get("other_sections", {}))

    # Fallback for resumes without recognized section headings
    if not evidence_sections:
        evidence_sections = {
            "unclassified": resume_text
        }

    # Extract skill evidence with section metadata
    skill_evidence = extract_section_aware_evidence(evidence_sections)

    result = {
        "candidate_info": candidate_info,
        "skills": extracted_skills,
        "skill_evidence": skill_evidence,
        "sections": sections
    }

    return result


def process_resume_pdf(pdf_path):

    extracted_text = extract_text_from_pdf(pdf_path)

    result = process_resume(extracted_text)

    return result
