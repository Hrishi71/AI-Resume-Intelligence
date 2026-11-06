from src.candidate_info_extractor import (
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github,
    extract_name
)
from src.candidate_info_extractor import extract_candidate_info

def test_extract_valid_email():
    resume = "Contact me at hrishi@example.com"

    result = extract_email(resume)

    assert result == "hrishi@example.com"


def test_extract_email_with_subdomain():
    resume = "Email: hrishi@mail.example.co.in"

    result = extract_email(resume)

    assert result == "hrishi@mail.example.co.in"


def test_no_email_found():
    resume = "I am a Python developer."

    result = extract_email(resume)

    assert result is None

def test_extract_email_with_plus_alias():
    resume = "Contact: hrishi+jobs@gmail.com"

    result = extract_email(resume)

    assert result == "hrishi+jobs@gmail.com"


def test_extract_email_case_insensitive():
    resume = "Contact: HRISHI@GMAIL.COM"

    result = extract_email(resume)

    assert result == "HRISHI@GMAIL.COM"


def test_extract_email_with_surrounding_text():
    resume = "Email (Personal): hrishi@example.com | Phone: 1234567890"

    result = extract_email(resume)

    assert result == "hrishi@example.com"

def test_extract_indian_mobile_number():
    resume = "Phone: 9876543210"

    result = extract_phone(resume)

    assert result == "9876543210"


def test_extract_phone_with_country_code():
    resume = "Contact: +91 9876543210"

    result = extract_phone(resume)

    assert result == "+91 9876543210"


def test_extract_phone_with_hyphen():
    resume = "Mobile: +91-9876543210"

    result = extract_phone(resume)

    assert result == "+91-9876543210"


def test_no_phone_found():
    resume = "Python developer with Django experience."

    result = extract_phone(resume)

    assert result is None

def test_extract_linkedin_profile():
    resume = "LinkedIn: https://www.linkedin.com/in/hrishi-dev"
    assert extract_linkedin(resume) == "https://www.linkedin.com/in/hrishi-dev"


def test_extract_linkedin_without_www():
    resume = "linkedin.com/in/hrishi-dev"
    assert extract_linkedin(resume) == "linkedin.com/in/hrishi-dev"


def test_no_linkedin_found():
    resume = "Python developer with Django experience."
    assert extract_linkedin(resume) is None


def test_extract_github_profile():
    resume = "GitHub: https://github.com/hrishi-dev"
    assert extract_github(resume) == "https://github.com/hrishi-dev"


def test_extract_github_without_www():
    resume = "github.com/hrishi-dev"
    assert extract_github(resume) == "github.com/hrishi-dev"


def test_no_github_found():
    resume = "Python developer with Django experience."
    assert extract_github(resume) is None

def test_extract_name_with_label():
    resume = "Name: Hrishikesh Deshpande\nEmail: hrishi@example.com"
    assert extract_name(resume) == "Hrishikesh Deshpande"


def test_extract_name_with_full_name_label():
    resume = "Full Name: Hrishikesh Anant Deshpande"
    assert extract_name(resume) == "Hrishikesh Anant Deshpande"


def test_no_name_found():
    resume = "Python developer with Django experience."
    assert extract_name(resume) is None

def test_extract_candidate_info():
    resume = """
    Name: Hrishikesh Deshpande
    Email: hrishi@example.com
    Phone: +91 9876543210
    LinkedIn: https://linkedin.com/in/hrishi-dev
    GitHub: https://github.com/hrishi-dev
    """

    result = extract_candidate_info(resume)

    assert result == {
        "name": "Hrishikesh Deshpande",
        "email": "hrishi@example.com",
        "phone": "+91 9876543210",
        "linkedin": "https://linkedin.com/in/hrishi-dev",
        "github": "https://github.com/hrishi-dev"
    }

def test_extract_name_without_label():
    resume = """
    Hrishikesh Anant Deshpande
    AI Engineer | Backend Software Engineer
    Email: hrishi@example.com
    """

    result = extract_name(resume)

    assert result == "Hrishikesh Anant Deshpande"