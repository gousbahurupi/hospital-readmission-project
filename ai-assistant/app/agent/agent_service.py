import json
from pathlib import Path

from app.agent.rules import detect_intent


BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "knowledge_base.json", "r", encoding="utf-8") as file:
    KNOWLEDGE_BASE = json.load(file)


def format_risk_report(prediction: dict) -> str:
    risk_probability = prediction["risk_probability"]
    risk_level = prediction["risk_level"]
    readmission_prediction = prediction["readmission_prediction"]
    factors = prediction["top_contributing_factors"]

    factor_text = "\n".join(
        f"• {factor}" for factor in factors
    )

    return (
        f"Readmission Prediction: {readmission_prediction}\n"
        f"Risk Probability: {risk_probability}%\n"
        f"Risk Level: {risk_level}\n\n"
        f"Top Contributing Factors:\n"
        f"{factor_text}\n\n"
        "This system provides decision support and does not provide "
        "a medical diagnosis."
    )


def answer_question(question: str, prediction: dict) -> str:
    intent = detect_intent(question)

    if intent == "risk_explanation":
        return (
            f"The model estimates a {prediction['risk_probability']}% "
            f"probability of readmission within 30 days, with a "
            f"{prediction['risk_level']} risk level."
        )

    if intent == "factors":
        factors = prediction["top_contributing_factors"]

        factor_text = "\n".join(
            f"• {factor}" for factor in factors
        )

        return (
            "The main factors contributing to this prediction are:\n"
            f"{factor_text}"
        )

    if intent == "monitoring":
        return (
            "Follow-up and monitoring considerations should be based "
            "on the identified risk factors and reviewed by the "
            "healthcare team."
        )

    if intent == "model":
        return KNOWLEDGE_BASE["model"]["description"]

    if intent == "limitations":
        return KNOWLEDGE_BASE["limitations"]["description"]

    return format_risk_report(prediction)