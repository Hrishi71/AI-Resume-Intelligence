
from src.section_extractor import extract_resume_sections


def test_extract_basic_resume_sections():
    resume_text = """
    TECHNICAL SKILLS
    Python, Django, FastAPI

    PROFESSIONAL EXPERIENCE
    Developed backend applications using Python.

    PROJECTS
    Built a document assistant using LangChain.

    EDUCATION
    MBA

    CERTIFICATIONS
    Python Programming Certification
    """

    sections = extract_resume_sections(resume_text)

    assert "Python, Django, FastAPI" in sections["technical_skills"]

    assert (
        "Developed backend applications using Python."
        in sections["professional_experience"]
    )

    assert (
        "Built a document assistant using LangChain."
        in sections["projects"]
    )

    assert "MBA" in sections["education"]

    assert (
        "Python Programming Certification"
        in sections["certifications"]
    )


def test_extract_sections_with_different_heading_formats():
    resume_text = """
    Technical Skills:
    Python, Java, SQL

    Work Experience
    Developed REST APIs using FastAPI.

    Personal Projects
    Built an AI chatbot.

    Academic Background
    MBA
    """

    sections = extract_resume_sections(resume_text)

    assert "Python, Java, SQL" in sections["technical_skills"]

    assert (
        "Developed REST APIs using FastAPI."
        in sections["professional_experience"]
    )

    assert "Built an AI chatbot." in sections["projects"]

    assert "MBA" in sections["education"]


def test_missing_sections_return_empty_strings():
    resume_text = """
    TECHNICAL SKILLS
    Python, Django
    """

    sections = extract_resume_sections(resume_text)

    assert sections["technical_skills"] != ""
    assert sections["professional_experience"] == ""
    assert sections["projects"] == ""
    assert sections["education"] == ""
    assert sections["certifications"] == ""


def test_extract_section_with_numbered_heading():
    resume_text = """
    01. PROFESSIONAL EXPERIENCE
    Developed APIs using Python.

    02. PROJECTS
    Built an AI assistant.
    """

    sections = extract_resume_sections(resume_text)

    assert (
        "Developed APIs using Python."
        in sections["professional_experience"]
    )

    assert "Built an AI assistant." in sections["projects"]


def test_extract_section_with_uppercase_and_punctuation():
    resume_text = """
    TECHNICAL SKILLS:
    Python, Django, PostgreSQL

    WORK EXPERIENCE:
    Developed backend services.
    """

    sections = extract_resume_sections(resume_text)

    assert "Python, Django, PostgreSQL" in sections["technical_skills"]
    assert "Developed backend services." in sections["professional_experience"]



def test_unknown_heading_does_not_create_a_section():
    resume_text = """
    TECHNICAL SKILLS
    Python, Django

    UNKNOWN CUSTOM HEADING
    Received employee recognition.
    """

    sections = extract_resume_sections(resume_text)

    assert "Python, Django" in sections["technical_skills"]

    # Unknown headings remain part of the active section
    assert "UNKNOWN CUSTOM HEADING" in sections["technical_skills"]
    assert (
        "Received employee recognition."
        in sections["technical_skills"]
    )



def test_extract_sections_with_additional_aliases():
    resume_text = """
    TECHNICAL EXPERTISE
    Python, Django, FastAPI

    CAREER HISTORY
    Developed backend applications.

    KEY PROJECTS
    Built an AI-powered resume analyzer.

    ACADEMIC QUALIFICATIONS
    MBA

    PROFESSIONAL CERTIFICATIONS
    Python Certification
    """

    sections = extract_resume_sections(resume_text)

    assert "Python, Django, FastAPI" in sections["technical_skills"]

    assert (
        "Developed backend applications."
        in sections["professional_experience"]
    )

    assert (
        "Built an AI-powered resume analyzer."
        in sections["projects"]
    )

    assert "MBA" in sections["education"]

    assert (
        "Python Certification"
        in sections["certifications"]
    )


def test_unknown_section_does_not_contaminate_previous_section():
    resume_text = """
    TECHNICAL SKILLS
    Python, Django, FastAPI

    PROFESSIONAL EXPERIENCE
    Developed backend services using Django.

    ACHIEVEMENTS
    Received employee recognition.

    PROJECTS
    Built an AI Resume Analyzer using Python.
    """

    sections = extract_resume_sections(resume_text)

    assert "Developed backend services" in (
        sections["professional_experience"]
    )

    assert "Received employee recognition" not in (
        sections["professional_experience"]
    )

    assert "Built an AI Resume Analyzer" in sections["projects"]


def test_extract_and_preserve_other_sections():
    resume_text = """
    PROFESSIONAL SUMMARY
    Backend developer experienced in Python.

    TECHNICAL SKILLS
    Python, Django, FastAPI

    ACHIEVEMENTS
    Received employee recognition.

    PROFESSIONAL EXPERIENCE
    Developed backend services using Django.
    """

    sections = extract_resume_sections(resume_text)

    assert "other_sections" in sections

    assert (
        "Backend developer experienced in Python."
        in sections["other_sections"]["professional_summary"]
    )

    assert (
        "Received employee recognition."
        in sections["other_sections"]["achievements"]
    )

    assert "Python, Django, FastAPI" in sections["technical_skills"]

    assert (
        "Developed backend services using Django."
        in sections["professional_experience"]
    )


def test_section_extraction_preserves_line_spacing():
    resume_text = """
    PROFESSIONAL EXPERIENCE
    Developed backend services
    using Python and Django.

    Built REST APIs using FastAPI.
    """

    sections = extract_resume_sections(resume_text)

    experience = sections["professional_experience"]

    assert "Developed backend services" in experience
    assert "using Python and Django." in experience
    assert "Built REST APIs using FastAPI." in experience

    # Separate source lines must not merge into one word.
    assert "servicesusing" not in experience
