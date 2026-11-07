
import re


# Maps different resume headings to standard section names

SECTION_ALIASES = {
    "technical_skills": [
        "technical skills",
        "skills",
        "core competencies",
        "technical expertise",
        "technology stack",
        "technical proficiencies",
        "key skills"
    ],

    "professional_experience": [
        "professional experience",
        "work experience",
        "employment history",
        "work history",
        "experience",
        "career history",
        "professional background"
    ],

    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "project experience",
        "key projects",
        "selected projects"
    ],

    "education": [
        "education",
        "academic background",
        "educational qualifications",
        "academic qualifications"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "licenses and certifications",
        "professional certifications"
    ]
}


# Additional resume headings that mark section boundaries.
# These sections are recognized but not extracted yet.

OTHER_SECTION_HEADINGS = [
    "summary",
    "professional summary",
    "career summary",
    "profile",
    "profile summary",
    "career objective",
    "objective",
    "achievements",
    "key achievements",
    "awards",
    "awards and honors",
    "honors and awards",
    "publications",
    "interests",
    "hobbies",
    "languages",
    "volunteer experience",
    "volunteer work",
    "references"
]


def normalize_heading(heading):
    """
    Normalize a heading for consistent comparison.
    """

    heading = heading.strip().lower()

    # Remove numbering such as 01. or 1.
    heading = re.sub(r"^\d+[\.\)]\s*", "", heading)

    # Remove trailing punctuation
    heading = re.sub(r"[:\-\s]+$", "", heading)

    # Normalize multiple spaces
    heading = re.sub(r"\s+", " ", heading)

    return heading

def normalize_section_key(heading):
    """
    Convert a heading into a dictionary-friendly key.
    """

    heading = normalize_heading(heading)

    heading = re.sub(r"[^a-z0-9]+", "_", heading)

    return heading.strip("_")

def extract_resume_sections(resume_text):

    # Initialize all sections
    sections = {
        section: ""
        for section in SECTION_ALIASES
    }
    sections["other_sections"] = {}
    current_section = None

    # Process resume line by line
    for line in resume_text.splitlines():

        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        normalized_line = normalize_heading(cleaned_line)

        detected_section = None

        # Identify whether the line is a section heading
        for section, aliases in SECTION_ALIASES.items():

            normalized_aliases = [
                normalize_heading(alias)
                for alias in aliases
            ]

            if normalized_line in normalized_aliases:
                detected_section = section
                break

        if detected_section:
            current_section = detected_section
            continue

        # Stop collecting content when an unsupported
        # but recognized resume section is encountered.
        if normalized_line in OTHER_SECTION_HEADINGS:

            other_section_key = normalize_section_key(normalized_line)

            sections["other_sections"].setdefault(
                other_section_key, ""
            )

            current_section = other_section_key
            continue

        # Add content to the currently active section
        if current_section:

            if current_section in sections["other_sections"]:

                if sections["other_sections"][current_section]:
                    sections["other_sections"][current_section] += "\n"

                sections["other_sections"][current_section] += cleaned_line

            else:

                if sections[current_section]:
                    sections[current_section] += "\n"

                sections[current_section] += cleaned_line

    return sections
