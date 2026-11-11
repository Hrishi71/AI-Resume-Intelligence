
import json

from google.genai import types

from src.llm.assessment_schemas import ResumeAssessment
from src.llm.client import get_gemini_client, get_model_name


RESUME_ASSESSMENT_PROMPT = """
You are an experienced technical recruiter and software engineering evaluator.

Evaluate the complete resume using the structured information provided.

ASSESSMENT DIMENSIONS (each scored from 0 to 20):

1. Technical capabilities:
   Evaluate the technical skills demonstrated through practical evidence,
   implementation details, and technologies used.

2. Experience and ownership:
   Evaluate responsibilities, individual contributions, problem-solving,
   and ownership demonstrated in professional experience.

3. Project depth:
   Evaluate project complexity, architecture, implementation,
   technical decisions, and engineering depth.

4. Measurable impact:
   Evaluate explicit metrics, measurable outcomes, operational improvements,
   and demonstrated business or technical impact.

5. Resume clarity:
   Evaluate clarity, structure, specificity, consistency, and communication.

IMPORTANT RULES:

- Evaluate only the information supplied in the resume data.
- Never invent experience, achievements, technologies, or metrics.
- A skill appearing in a skills list is not proof of practical proficiency.
- Distinguish practical implementation from simple technology mentions.
- Do not assume the candidate independently completed work unless stated.
- Do not infer measurable outcomes without explicit measurements.
- Distinguish explicit evidence from reasonable inference.
- Identify missing evidence rather than filling gaps with assumptions.
- Keep recommendations specific and actionable.
- Scores measure resume evidence quality, NOT actual engineering ability
  or guaranteed job readiness.
- Supporting evidence must quote or accurately reference supplied statements.
- Return concise, objective assessments.

RESUME DATA:

{resume_data}
"""


def _generate_assessment(resume_data: dict) -> ResumeAssessment:
    client = get_gemini_client()

    prompt = RESUME_ASSESSMENT_PROMPT.format(
        resume_data=json.dumps(resume_data, ensure_ascii=False)
    )

    response = client.models.generate_content(
        model=get_model_name(),
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResumeAssessment,
            temperature=0.1,
        ),
    )

    if response.parsed is None:
        raise ValueError(
            "Gemini returned an empty or invalid resume assessment."
        )

    return ResumeAssessment.model_validate(response.parsed)


def assess_resume(resume_data: dict) -> ResumeAssessment:
    """
    Generate one structured Gemini assessment for a complete resume.
    """

    if not isinstance(resume_data, dict) or not resume_data:
        raise ValueError("Resume assessment input cannot be empty.")

    return _generate_assessment(resume_data)
