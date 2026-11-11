
from src.evidence_scorer import score_evidence


def test_score_simple_skill_mention():
    result = score_evidence("Python")

    assert result["total_score"] == 20


def test_score_action_and_technical_details():
    result = score_evidence(
        "Developed backend applications using Python."
    )

    assert result["breakdown"]["action"] == 20
    assert result["breakdown"]["technical_detail"] == 20
    assert result["total_score"] == 40


def test_score_complex_engineering_evidence():
    result = score_evidence(
        "Designed scalable microservices using Python and Kafka."
    )

    assert result["breakdown"]["action"] == 20
    assert result["breakdown"]["technical_detail"] == 20
    assert result["breakdown"]["complexity"] == 20
    assert result["total_score"] == 60


def test_score_measurable_outcome():
    result = score_evidence(
        "Reduced API latency by 35% using Python."
    )

    assert result["breakdown"]["measurable_outcome"] == 20
    assert result["breakdown"]["impact"] == 20
    assert result["total_score"] == 80


def test_score_all_five_dimensions():
    result = score_evidence(
        "Architected and deployed scalable distributed services "
        "using Python, Kafka, and Redis, reducing processing time by 40%."
    )

    assert result["total_score"] == 100


def test_score_empty_evidence():
    result = score_evidence("")

    assert result["total_score"] == 0


def test_score_whitespace_evidence():
    result = score_evidence("   ")

    assert result["total_score"] == 0


def test_score_returns_all_dimensions():
    result = score_evidence(
        "Developed REST APIs using Python."
    )

    expected_dimensions = {
        "action",
        "technical_detail",
        "complexity",
        "measurable_outcome",
        "impact"
    }

    assert set(result["breakdown"].keys()) == expected_dimensions


def test_score_never_exceeds_100():
    result = score_evidence(
        "Designed, developed, deployed, optimized and maintained "
        "scalable distributed microservices using Python, Kafka, "
        "Redis, PostgreSQL and Docker, reducing latency by 50% "
        "and improving throughput by 60%."
    )

    assert 0 <= result["total_score"] <= 100


def test_detects_modern_ai_technologies():
    result = score_evidence(
        "Developed an application using LangChain, LangGraph, "
        "FastAPI and ChromaDB."
    )

    assert result["breakdown"]["technical_detail"] == 20


def test_detects_rag_and_vector_search():
    result = score_evidence(
        "Implemented semantic vector search and hybrid retrieval "
        "for a RAG application."
    )

    assert result["breakdown"]["technical_detail"] == 20
    assert result["breakdown"]["complexity"] == 20


def test_detects_recursive_engineering_complexity():
    result = score_evidence(
        "Designed a recursive dependency engine with transitive "
        "risk propagation across interconnected assets."
    )

    assert result["breakdown"]["complexity"] == 20


def test_detects_hybrid_reranking_complexity():
    result = score_evidence(
        "Implemented semantic vector search with hybrid re-ranking."
    )

    assert result["breakdown"]["complexity"] == 20


def test_detects_sub_second_measurements():
    result = score_evidence(
        "Optimized API performance to deliver sub-2s responses."
    )

    assert result["breakdown"]["measurable_outcome"] == 20


def test_detects_percentage_improvement():
    result = score_evidence(
        "Reduced processing time by 40% using Python."
    )

    assert result["breakdown"]["measurable_outcome"] == 20
    assert result["breakdown"]["impact"] == 20


def test_detects_agentic_ai_implementation():
    result = score_evidence(
        "Architected an agentic AI workflow using LangGraph "
        "and Azure OpenAI."
    )

    assert result["breakdown"]["action"] == 20
    assert result["breakdown"]["technical_detail"] == 20
    assert result["breakdown"]["complexity"] == 20


def test_technology_list_does_not_receive_action_or_complexity_points():
    result = score_evidence(
        "Python, Django, FastAPI, PostgreSQL and Redis."
    )

    assert result["breakdown"]["action"] == 0
    assert result["breakdown"]["complexity"] == 0
    assert result["breakdown"]["impact"] == 0


def test_negated_action_does_not_receive_action_points():
    result = score_evidence(
        "Did not develop the application using Python."
    )

    assert result["breakdown"]["action"] == 0


def test_assisted_statement_does_not_claim_independent_implementation():
    result = score_evidence(
        "Assisted with Python backend development."
    )

    assert result["breakdown"]["action"] == 0


def test_familiarity_statement_does_not_claim_implementation():
    result = score_evidence(
        "Familiar with Python, Django and REST APIs."
    )

    assert result["breakdown"]["action"] == 0
    assert result["breakdown"]["complexity"] == 0


def test_metric_does_not_automatically_mean_positive_impact():
    result = score_evidence(
        "API response time was 200ms."
    )

    assert result["breakdown"]["measurable_outcome"] == 20
    assert result["breakdown"]["impact"] == 0


def test_metric_without_improvement_does_not_claim_impact():
    result = score_evidence(
        "The system processed 10000 requests per day."
    )

    assert result["breakdown"]["measurable_outcome"] == 20
    assert result["breakdown"]["impact"] == 0


def test_real_engineering_accomplishment_keeps_action_score():
    result = score_evidence(
        "Developed REST APIs using Python and reduced "
        "response time by 35%."
    )

    assert result["breakdown"]["action"] == 20
    assert result["breakdown"]["technical_detail"] == 20
    assert result["breakdown"]["measurable_outcome"] == 20
    assert result["breakdown"]["impact"] == 20


def test_negation_with_action_verb_does_not_get_action_score():
    result = score_evidence(
        "I did not build or deploy the Python application."
    )

    assert result["breakdown"]["action"] == 0


def test_assisted_work_does_not_receive_independent_action_score():
    result = score_evidence(
        "Assisted the team in developing Python microservices."
    )

    assert result["breakdown"]["action"] == 0


def test_action_after_negation_is_not_treated_as_positive_impact():
    result = score_evidence(
        "Did not reduce API latency by 30%."
    )

    assert result["breakdown"]["impact"] == 0


def test_passive_accomplishment_is_recognized():
    result = score_evidence(
        "REST APIs were developed using Python."
    )

    assert result["breakdown"]["action"] == 20
    assert result["breakdown"]["technical_detail"] == 20


def test_skill_list_does_not_receive_complexity_score():
    result = score_evidence(
        "Python, Django, microservices, distributed systems."
    )

    assert result["breakdown"]["action"] == 0
    assert result["breakdown"]["complexity"] == 0


def test_experience_claim_does_not_automatically_receive_action_score():
    result = score_evidence(
        "Experienced in developing Python applications."
    )

    assert result["breakdown"]["action"] == 0

def test_score_evidence_returns_reasons():
    evidence = (
        "Designed a recursive dependency engine "
        "using Python and Django."
    )

    result = score_evidence(evidence)

    assert "reasons" in result
    assert isinstance(result["reasons"], list)
    assert len(result["reasons"]) == 5


def test_score_evidence_reasons_identify_detected_signals():
    evidence = (
        "Designed a recursive dependency engine "
        "using Python and Django."
    )

    result = score_evidence(evidence)
    reasons = " ".join(result["reasons"]).lower()

    assert "action" in reasons
    assert "designed" in reasons

    assert "technical" in reasons
    assert "python" in reasons or "django" in reasons

    assert "complexity" in reasons
    assert "recursive" in reasons


def test_score_evidence_reasons_explain_missing_signals():
    evidence = "Used Python and Django for backend development."

    result = score_evidence(evidence)
    reasons = " ".join(result["reasons"]).lower()

    assert "measurable outcome" in reasons
    assert "impact" in reasons


def test_negated_impact_does_not_receive_impact_score():
    evidence = "Did not reduce API response time by 20%."

    result = score_evidence(evidence)

    assert result["breakdown"]["impact"] == 0


def test_multiple_measurements_are_explained():
    evidence = (
        "Reduced API response time from 5 seconds "
        "to 1.5 seconds."
    )

    result = score_evidence(evidence)

    measurement_reason = next(
        reason for reason in result["reasons"]
        if "measurable outcome" in reason.lower()
    )

    assert "5 seconds" in measurement_reason
    assert "1.5 seconds" in measurement_reason

