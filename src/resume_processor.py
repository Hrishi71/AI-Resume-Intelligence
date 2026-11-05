from src.text_cleaner import clean_resume_text
from src.skill_extractor import extract_skills_by_category
from src.resume_parser import extract_text_from_pdf


def process_resume(resume_text):

    cleaned_text = clean_resume_text(resume_text)

    extracted_skills = extract_skills_by_category(cleaned_text)

    return extracted_skills


def process_resume_pdf(pdf_path):

    extracted_text = extract_text_from_pdf(pdf_path)

    result = process_resume(extracted_text)

    return result