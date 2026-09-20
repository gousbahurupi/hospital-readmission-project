def detect_intent(question: str) -> str:
    question = question.lower().strip()

    if (
        ("why" in question and "risk" in question)
        or "why high" in question
        or "why low" in question
        or "why medium" in question
    ):
        return "risk_explanation"

    if (
        "factor" in question
        or "contribute" in question
        or "important feature" in question
        or "important features" in question
    ):
        return "factors"

    if (
        "monitor" in question
        or "follow up" in question
        or "follow-up" in question
        or "followup" in question
    ):
        return "monitoring"

    if (
        "how does the model work" in question
        or "how does this work" in question
        or "how system works" in question
        or "explain the model" in question
    ):
        return "model"

    if (
        "limitation" in question
        or "limitations" in question
        or "can i trust" in question
        or "trust this prediction" in question
        or "accurate" in question
    ):
        return "limitations"

    return "general"