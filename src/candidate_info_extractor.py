import re


def extract_email(text):
    """
    Extract the first email address from resume text.
    """

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None

def extract_phone(text):
    """
    Extract an Indian mobile number from resume text.
    Supports optional +91 country code and spaces or hyphens.
    """

    pattern = r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None

def extract_linkedin(text):
    """
    Extract a LinkedIn profile URL from resume text.
    """

    pattern = r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group()

    return None

def extract_github(text):
    """
    Extract a GitHub profile URL from resume text.
    """

    pattern = r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group()

    return None

def extract_name(text):
    """
    Extract candidate name from resume text.
    Supports labelled and unlabelled names.
    """

    # Strategy 1: Look for an explicitly labelled name
    pattern = r"(?im)^\s*(?:full\s+name|name)\s*:\s*([^\r\n|]+)"

    match = re.search(pattern, text)

    if match:
        return match.group(1).strip()

    # Strategy 2: Look for a name in the first few lines
    lines = text.strip().splitlines()

    for line in lines[:5]:

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip lines containing contact information
        if re.search(r"@|https?://|www\.|linkedin\.com|github\.com", line, re.IGNORECASE):
            continue

        # Skip common resume headings and job titles
        if re.search(
            r"\b(engineer|developer|manager|consultant|architect|"
            r"professional|resume|curriculum vitae|software|"
            r"experience|summary)\b",
            line,
            re.IGNORECASE
        ):
            continue

        # A basic name candidate: 2–4 alphabetic name parts
        if re.fullmatch(
            r"[A-Za-z]+(?:[ '-][A-Za-z]+){1,3}",
            line
        ):
            return line

    return None

def extract_candidate_info(text):
    """
    Extract all available candidate information from resume text.
    """

    candidate_info = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text)
    }

    return candidate_info