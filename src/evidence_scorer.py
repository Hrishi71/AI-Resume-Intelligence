
import re


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
    "debugged",
    "reduced",
    "reducing",
}



TECHNICAL_INDICATORS = {
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "sql",

    # Backend and APIs
    "django", "flask", "fastapi", "react",
    "api", "apis", "rest", "microservices",
    "database", "postgresql", "mysql", "mongodb", "redis",

    # Infrastructure
    "kafka", "docker", "kubernetes", "aws", "azure",

    # AI and LLM technologies
    "langchain", "langgraph", "openai",
    "chromadb", "rag", "llm", "llms",
    "embeddings", "vector", "search",
    "retrieval", "reranking", "re-ranking",
    "agentic", "workflow", "workflows",
    "orchestration", "prompting",
}




COMPLEXITY_INDICATORS = {
    "scalable",
    "distributed",
    "microservices",
    "concurrent",
    "asynchronous",
    "architecture",
    "pipeline",
    "fault-tolerant",
    "high-availability",
    "real-time",

    # Advanced engineering concepts
    "recursive",
    "transitive",
    "dependency",
    "propagation",
    "interconnected",
    "hybrid",
    "retrieval",
    "reranking",
    "re-ranking",
    "orchestration",
    "agentic",
    "workflow",
    "workflows",
    "graph",
    "blast-radius",
}



IMPACT_INDICATORS = {
    "reduced",
    "reducing",
    "increased",
    "improved",
    "accelerated",
    "saved",
    "boosted",
    "enhanced",
    "eliminated",
    "decreased",
}




MEASUREMENT_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:%|"
    r"percent\b|ms\b|s\b|sec\b|seconds\b|milliseconds\b|"
    r"minutes\b|hours\b|days\b|requests\b|users\b|"
    r"records\b|transactions\b|gb\b|mb\b)",
    re.IGNORECASE
)





def score_evidence(evidence):
    """
    Score the strength of written skill evidence.

    This measures evidence quality, not actual candidate proficiency.
    Also returns explanations for each scoring dimension.
    """

    breakdown = {
        "action": 0,
        "technical_detail": 0,
        "complexity": 0,
        "measurable_outcome": 0,
        "impact": 0,
    }

    reasons = []

    if not evidence or not evidence.strip():
        return {
            "total_score": 0,
            "breakdown": breakdown,
            "reasons": [
                "Action: No evidence provided.",
                "Technical detail: No evidence provided.",
                "Complexity: No evidence provided.",
                "Measurable outcome: No evidence provided.",
                "Impact: No evidence provided.",
            ],
        }

    normalized_evidence = evidence.lower()
    words = set(re.findall(r"\b[\w-]+\b", normalized_evidence))

    # 1. Action
    detected_actions = words.intersection(ACTION_VERBS)

    if detected_actions:
        breakdown["action"] = 20
        reasons.append(
            f"Action: Detected {', '.join(sorted(detected_actions))}."
        )
    else:
        reasons.append("Action: No action verb detected.")

    # 2. Technical detail
    detected_technical = words.intersection(TECHNICAL_INDICATORS)

    if detected_technical:
        breakdown["technical_detail"] = 20
        reasons.append(
            "Technical detail: Detected "
            + ", ".join(sorted(detected_technical)) + "."
        )
    else:
        reasons.append("Technical detail: No technical indicators detected.")

    # 3. Complexity
    detected_complexity = words.intersection(COMPLEXITY_INDICATORS)

    has_complexity = bool(detected_complexity)
    has_action = breakdown["action"] == 20

    if has_complexity and has_action:
        breakdown["complexity"] = 20
        reasons.append(
            "Complexity: Detected "
            + ", ".join(sorted(detected_complexity)) + "."
        )
    else:
        reasons.append(
            "Complexity: No qualifying combination of engineering "
            "action and complexity indicators detected."
        )

    # 4. Measurable outcome

    measurements = MEASUREMENT_PATTERN.findall(normalized_evidence)

    if measurements:
        breakdown["measurable_outcome"] = 20

        detected_measurements = ", ".join(
            f"'{measurement}'" for measurement in measurements
        )

        reasons.append(
            f"Measurable outcome: Detected metrics {detected_measurements}."
        )
    else:
        reasons.append(
            "Measurable outcome: No explicit metric detected."
        )


    # 5. Impact
    detected_impact = words.intersection(IMPACT_INDICATORS)

    if detected_impact:
        breakdown["impact"] = 20
        reasons.append(
            "Impact: Detected "
            + ", ".join(sorted(detected_impact)) + "."
        )
    else:
        reasons.append("Impact: No impact indicator detected.")

    total_score = sum(breakdown.values())

    return {
        "total_score": total_score,
        "breakdown": breakdown,
        "reasons": reasons,
    }
