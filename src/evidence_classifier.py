
import re


# Action verbs indicating practical work
ACTION_VERBS = {
    "built",
    "developed",
    "designed",
    "implemented",
    "created",
    "engineered",
    "integrated",
    "deployed",
    "maintained",
    "optimized",
    "automated",
    "managed",
    "configured",
    "architected",
    "tested",
    "improved",
    "migrated",
    "processed",
    "analyzed",
    "trained",
    "fine-tuned",
    "debugged",
    "implemented",
    "established"
}


# Words indicating certification
CERTIFICATION_KEYWORDS = {
    "certified",
    "certification",
    "certifications",
    "certificate",
    "certificates",
    "licensed"
}


def classify_evidence(evidence, section):
    """
    Classify skill evidence based on its content and resume section.
    """

    if not evidence or not evidence.strip():
        return "skill_mention"

    normalized_evidence = evidence.lower().strip()
    normalized_section = section.lower().strip()

    # 1. Certification classification
    words = set(re.findall(r"\b[\w-]+\b", normalized_evidence))

    if words.intersection(CERTIFICATION_KEYWORDS):
        return "certification"

    # 2. Detect meaningful action verbs
    has_action = bool(words.intersection(ACTION_VERBS))

    # 3. Project application
    if normalized_section == "projects" and has_action:
        return "project_application"

    # 4. Professional application
    if normalized_section == "professional_experience" and has_action:
        return "practical_application"

    # 5. Practical application in unclassified content
    if normalized_section == "unclassified" and has_action:
        return "practical_application"

    # 6. Default classification
    return "skill_mention"
