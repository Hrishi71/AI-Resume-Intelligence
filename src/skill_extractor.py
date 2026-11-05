
import re

# Skills organized by category
SKILL_DATABASE = {
    "Programming Languages": [
        "Python",
        "Java",
        "C++",
        "JavaScript"
    ],

    "Backend": [
        "Django",
        "FastAPI",
        "Flask",
        "Node.js",
        "Express.js"
    ],

    "Frontend": [
        "React",
        "Angular"
    ],

    "Databases": [
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "SQLite"
    ],

    "AI and Machine Learning": [
        "LangChain",
        "LangGraph",
        "Machine Learning",
        "Deep Learning",
        "Generative AI",
        "Large Language Models"
    ],

    "Tools and Cloud": [
        "Git",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure"
    ]
}


# Alternative names for technical skills
SKILL_ALIASES = {
    "JavaScript": ["JS"],
    "React": ["React.js"],
    "Node.js": ["Node", "NodeJS"],
    "Express.js": ["Express"],
    "Generative AI": ["GenAI"],
    "Large Language Models": ["LLM", "LLMs"]
}


def matches_skill(text, skill):
    """
    Check whether a skill appears as a complete term.
    """

    pattern = r"(?<![\w.])" + re.escape(skill) + r"(?!\w)"

    return re.search(pattern, text, re.IGNORECASE) is not None


def extract_skills(resume_text):
    """
    Extract standard skill names and their aliases.
    """

    detected_skills = []

    for category, skills in SKILL_DATABASE.items():

        for skill in skills:

            # Check standard skill name
            found = matches_skill(resume_text, skill)

            # Check alternative names
            if not found:

                aliases = SKILL_ALIASES.get(skill, [])

                for alias in aliases:

                    if matches_skill(resume_text, alias):
                        found = True
                        break

            if found:
                detected_skills.append(skill)

    return detected_skills

def extract_skills_by_category(resume_text):
    """
    Extract skills and organize them by category.
    """

    results = {}

    for category, skills in SKILL_DATABASE.items():

        detected = []

        for skill in skills:

            found = matches_skill(resume_text, skill)

            if not found:

                aliases = SKILL_ALIASES.get(skill, [])

                for alias in aliases:

                    if matches_skill(resume_text, alias):
                        found = True
                        break

            if found:
                detected.append(skill)

        if detected:
            results[category] = detected

    return results