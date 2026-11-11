from google.genai import types

from src.llm.client import get_gemini_client, get_model_name
from src.llm.schemas import EvidenceEvaluation


EVALUATION_PROMPT = """
You are an experienced technical recruiter and software engineering evaluator.

Evaluate the strength of the resume evidence provided below.

SCORING DIMENSIONS (each scored from 0 to 20):

1. Action:
   Evaluate whether the candidate clearly describes their own actions,
   responsibilities, and contributions.

2. Technical detail:
   Evaluate the specificity of technologies, tools, methods,
   and technical implementation details.

3. Complexity:
   Evaluate the technical difficulty, problem-solving depth,
   architecture, and engineering challenges demonstrated.

4. Measurable outcome:
   Evaluate whether concrete metrics, quantities, percentages,
   or measurable results are provided.

5. Impact:
   Evaluate the demonstrated technical, operational,
   customer, or business impact.

IMPORTANT EVALUATION RULES:

- Evaluate ONLY the supplied evidence.
- Never invent technologies, achievements, metrics, or outcomes.
- Do not assume the candidate performed work that is not stated.
- Distinguish independent implementation from assisted work.
- A technology mention alone is not proof of implementation.
- Do not award measurable outcome points without actual measurements.
- Do not assume business impact without supporting evidence.
- Be objective and conservative when assigning scores.
- Explain every score using evidence from the supplied statement.
- The summary must accurately reflect the overall evidence quality.

RESUME EVIDENCE:

{evidence}
"""


def _generate_evaluation(
    client,
    evidence: str
) -> EvidenceEvaluation:
    """
    Generate a structured evaluation using Gemini.
    """

    prompt = EVALUATION_PROMPT.format(evidence=evidence)

    response = client.models.generate_content(
        model=get_model_name(),
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EvidenceEvaluation,
            temperature=0.1,
        ),
    )

    if response.parsed is None:
        raise ValueError(
            "Gemini returned an empty or invalid evaluation response."
        )

    return EvidenceEvaluation.model_validate(response.parsed)


def evaluate_evidence(evidence: str) -> EvidenceEvaluation:
    """
    Evaluate one resume evidence statement using Gemini.
    """

    if not evidence or not evidence.strip():
        raise ValueError("Evidence cannot be empty.")

    client = get_gemini_client()

    return _generate_evaluation(
        client=client,
        evidence=evidence.strip()
    )