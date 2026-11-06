from src.text_cleaner import clean_resume_text
from src.skill_extractor import extract_skills_by_category
from src.resume_parser import extract_text_from_pdf
from src.candidate_info_extractor import extract_candidate_info


def process_resume(resume_text):

    # Extract candidate information from original text
    candidate_info = extract_candidate_info(resume_text)

    # Clean text for skill extraction
    cleaned_text = clean_resume_text(resume_text)

    # Extract technical skills
    extracted_skills = extract_skills_by_category(cleaned_text)

    result = {
        "candidate_info": candidate_info,
        "skills": extracted_skills
    }

    return result


def process_resume_pdf(pdf_path):

    extracted_text = extract_text_from_pdf(pdf_path)

    result = process_resume(extracted_text)

    return result