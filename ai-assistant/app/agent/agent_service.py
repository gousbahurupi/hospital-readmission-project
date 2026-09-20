"""Builds answers for the readmission-risk assistant.

Pure Python (no web framework imports) so it can be tested and reused on its
own. All wording that clinicians may want to review lives in
knowledge_base.json; this module only assembles it around the prediction.
"""

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from app.agent.knowledge import FACTOR_DETAILS, KNOWLEDGE_BASE, find_factor_mentions
from app.agent.rules import detect_intent, detect_intents
from app.agent.text import normalize

KB = KNOWLEDGE_BASE
DISCLAIMER: str = KB["general"]["disclaimer"]

_REQUIRED_KEYS = (
    "readmission_prediction",
    "risk_probability",
    "risk_level",
    "top_contributing_factors",
)


@dataclass
class AgentAnswer:
    answer: str
    intent: str
    intents: list[str] = field(default_factory=list)
    suggested_questions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class FactorRef:
    key: Optional[str]
    label: str
    entry: Optional[dict[str, Any]]
    in_prediction: bool


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _coerce_prediction(prediction: dict) -> dict:
    """Validate and normalise a prediction dict (the API already validates)."""
    missing = [key for key in _REQUIRED_KEYS if key not in prediction]
    if missing:
        raise ValueError(f"prediction is missing: {', '.join(missing)}")
    factors = [
        str(item).strip()
        for item in prediction["top_contributing_factors"]
        if str(item).strip()
    ]
    return {
        "readmission_prediction": str(prediction["readmission_prediction"]).strip().upper(),
        "risk_probability": float(prediction["risk_probability"]),
        "risk_level": str(prediction["risk_level"]).strip().upper(),
        "top_contributing_factors": factors,
    }


def _pct(value: float) -> str:
    return f"{round(float(value), 1):g}%"


def _bullets(lines: list[str]) -> str:
    return "\n".join(f"• {line}" for line in lines)


def _prediction_factors(prediction: dict) -> list[FactorRef]:
    refs = []
    for label in prediction["top_contributing_factors"]:
        mentions = find_factor_mentions(label)
        key = mentions[0][1] if mentions else None
        refs.append(FactorRef(key, label, FACTOR_DETAILS.get(key) if key else None, True))
    return refs


def _factors_in_question(question: str, prediction: dict) -> list[FactorRef]:
    """Factors the user asked about, in the order they appear (max 3)."""
    text = normalize(question)
    prediction_refs = _prediction_factors(prediction)
    by_key = {ref.key: ref for ref in prediction_refs if ref.key}
    found: dict[str, tuple[int, FactorRef]] = {}

    for ref in prediction_refs:
        match = re.search(rf"\b{re.escape(normalize(ref.label))}\b", text)
        if match:
            found.setdefault(ref.key or f"label:{normalize(ref.label)}", (match.start(), ref))

    for position, key in find_factor_mentions(text):
        if key in by_key:
            found.setdefault(key, (position, by_key[key]))
        else:
            entry = FACTOR_DETAILS[key]
            found.setdefault(key, (position, FactorRef(key, entry["label"], entry, False)))

    ordered = sorted(found.values(), key=lambda item: item[0])
    return [ref for _, ref in ordered][:3]


def _factor_line(ref: FactorRef) -> str:
    if ref.entry and ref.entry.get("short"):
        return f"{ref.label}: {ref.entry['short']}"
    return ref.label


def _level_info(prediction: dict) -> dict:
    return KB["risk_levels"].get(prediction["risk_level"], {})


# --------------------------------------------------------------------------
# reports
# --------------------------------------------------------------------------
def format_risk_report(prediction: dict) -> str:
    prediction = _coerce_prediction(prediction)
    factor_text = _bullets(prediction["top_contributing_factors"])
    return (
        f"Readmission Prediction: {prediction['readmission_prediction']}\n"
        f"Risk Probability: {_pct(prediction['risk_probability'])}\n"
        f"Risk Level: {prediction['risk_level']}\n\n"
        f"Top Contributing Factors:\n"
        f"{factor_text}\n\n"
        f"{DISCLAIMER}"
    )


# --------------------------------------------------------------------------
# handlers: (question, prediction) -> answer text
# --------------------------------------------------------------------------
def _report(question: str, prediction: dict) -> str:
    return format_risk_report(prediction)


def _risk_summary(question: str, prediction: dict) -> str:
    return (
        f"The model estimates a {_pct(prediction['risk_probability'])} "
        f"probability of readmission within 30 days, with a "
        f"{prediction['risk_level']} risk level. "
        f"The readmission prediction is {prediction['readmission_prediction']}."
    )


def _risk_explanation(question: str, prediction: dict) -> str:
    lines = [
        f"The model estimates a {_pct(prediction['risk_probability'])} "
        f"probability of readmission within 30 days, with a "
        f"{prediction['risk_level']} risk level."
    ]
    refs = _prediction_factors(prediction)
    if refs:
        lines += ["", "The prediction is mainly driven by these factors:"]
        lines.append(_bullets([_factor_line(ref) for ref in refs]))
    lines += [
        "",
        "These factors show what influenced the model's estimate. They are "
        "statistical associations learned from historical data, not confirmed "
        "causes for this individual patient.",
    ]
    return "\n".join(lines)


def _risk_meaning(question: str, prediction: dict) -> str:
    probability = prediction["risk_probability"]
    lines = [
        KB["probability_meaning"].format(
            probability=_pct(probability), expected=f"{round(probability):g}"
        )
    ]
    level = _level_info(prediction)
    if level:
        lines += ["", f"Risk level {prediction['risk_level']}: {level['meaning']}"]
        lines.append(KB["risk_levels"]["note"])
    label = KB["prediction_labels"].get(prediction["readmission_prediction"])
    if label:
        lines += ["", f"Prediction {prediction['readmission_prediction']}: {label}"]
    return "\n".join(lines)


def _factors(question: str, prediction: dict) -> str:
    refs = _prediction_factors(prediction)
    return (
        "The main factors contributing to this prediction are:\n"
        + _bullets([_factor_line(ref) for ref in refs])
    )


def _top_factor(question: str, prediction: dict) -> str:
    refs = _prediction_factors(prediction)
    if not refs:
        return "The prediction did not include any contributing factors."
    first = refs[0]
    if len(refs) == 1:
        lead = f"The only contributing factor listed for this prediction is {first.label}."
    else:
        lead = (
            f"The prediction system lists {first.label} first, which normally "
            "means it contributed most to this prediction."
        )
    detail = first.entry["description"] if first.entry else ""
    tail = (
        "Other factors also contributed, and none of them is a confirmed cause "
        "for this individual patient."
        if len(refs) > 1
        else ""
    )
    return "\n\n".join(part for part in (lead, detail, tail) if part)


def _factor_detail(question: str, prediction: dict) -> str:
    refs = _factors_in_question(question, prediction)
    if not refs:
        return _factors(question, prediction)
    blocks = []
    for ref in refs:
        description = (
            ref.entry["description"]
            if ref.entry
            else "The prediction system listed this as a contributing factor. I don't "
            "have detailed background on it, so please check the model documentation "
            "or ask the team that maintains the model."
        )
        status = (
            "It is one of the top contributing factors for this prediction."
            if ref.in_prediction
            else "It was not listed among the top contributing factors for this prediction."
        )
        blocks.append(f"{ref.label}\n{description}\n{status}")
    return "\n\n".join(blocks)


def _monitoring(question: str, prediction: dict) -> str:
    lines = [KB["monitoring"]["intro"]]
    factor_notes = [
        f"{ref.label}: {ref.entry['monitoring']}"
        for ref in _prediction_factors(prediction)
        if ref.entry and ref.entry.get("monitoring")
    ]
    if factor_notes:
        lines += ["", "Considerations linked to this prediction's factors:", _bullets(factor_notes)]
    level = _level_info(prediction)
    if level:
        lines += ["", level["follow_up"]]
    lines += ["", KB["monitoring"]["boundary"]]
    return "\n".join(lines)


def _care_planning(question: str, prediction: dict) -> str:
    lines = ["General considerations when readmission risk is a concern:", _bullets(KB["care_planning"]["points"])]
    level = _level_info(prediction)
    if level:
        lines += ["", level["follow_up"]]
    lines += ["", KB["care_planning"]["boundary"]]
    return "\n".join(lines)


def _model(question: str, prediction: dict) -> str:
    return f"{KB['model']['description']}\n\n{KB['model']['note']}"


def _limitations(question: str, prediction: dict) -> str:
    return (
        f"{KB['limitations']['description']}\n\n"
        "Things to keep in mind:\n"
        f"{_bullets(KB['limitations']['points'])}"
    )


def _static(section: str) -> Callable[[str, dict], str]:
    def handler(question: str, prediction: dict) -> str:
        return KB[section]["description"]

    return handler


def _help(question: str, prediction: dict) -> str:
    level = prediction["risk_level"].lower()
    lines = ["I can explain this readmission risk prediction. Here are some things you can ask:", ""]
    for category in KB["question_catalog"]:
        lines.append(category["category"])
        for item in category["questions"][:3]:
            lines.append(f"• {item['text'].replace('risk high', f'risk {level}')}")
        lines.append("")
    lines.append(
        f'You can also ask two things at once, for example: "Why is the risk {level} '
        'and what should be monitored?"'
    )
    return "\n".join(lines)


def _about(question: str, prediction: dict) -> str:
    return KB["general"]["system_description"]


def _greeting(question: str, prediction: dict) -> str:
    return (
        "Hello. I can explain this readmission risk prediction: why the risk is "
        f"{prediction['risk_level'].lower()}, which factors contributed, and what the team "
        "may want to monitor. What would you like to know?"
    )


def _closing(question: str, prediction: dict) -> str:
    return "You're welcome. Ask again any time you want to go through the prediction."


def _general(question: str, prediction: dict) -> str:
    return (
        "I couldn't match that to something I can explain. I can answer questions about "
        "this readmission risk prediction, its contributing factors, follow-up "
        "considerations, and how the model works. Here is the current summary:\n\n"
        f"{format_risk_report(prediction)}"
    )


_HANDLERS: dict[str, Callable[[str, dict], str]] = {
    "report": _report,
    "risk_summary": _risk_summary,
    "risk_explanation": _risk_explanation,
    "risk_meaning": _risk_meaning,
    "factors": _factors,
    "top_factor": _top_factor,
    "factor_detail": _factor_detail,
    "monitoring": _monitoring,
    "care_planning": _care_planning,
    "model": _model,
    "explainability": _static("explainability"),
    "limitations": _limitations,
    "training_data": _static("training_data"),
    "data_privacy": _static("data_privacy"),
    "intended_use": _static("intended_use"),
    "readmission_definition": _static("readmission_definition"),
    "what_if": _static("what_if"),
    "medical_advice": _static("medical_advice"),
    "emergency": _static("emergency"),
    "help": _help,
    "about": _about,
    "greeting": _greeting,
    "closing": _closing,
    "general": _general,
}


def suggested_questions(intent: str, prediction: dict, limit: int = 3) -> list[str]:
    """Follow-up questions that make sense after answering `intent`."""
    templates = KB["follow_ups"].get(intent, KB["follow_ups"]["general"])
    factors = prediction["top_contributing_factors"]
    top_factor = factors[0] if factors else "the top factor"
    level = prediction["risk_level"].lower()
    return [
        template.replace("{level}", level).replace("{top_factor}", top_factor)
        for template in templates[:limit]
    ]


# --------------------------------------------------------------------------
# public API
# --------------------------------------------------------------------------
def answer_with_metadata(question: str, prediction: dict) -> AgentAnswer:
    prediction = _coerce_prediction(prediction)
    terms = [normalize(label) for label in prediction["top_contributing_factors"]]
    intents = detect_intents(question, terms)
    parts = [_HANDLERS.get(intent, _general)(question, prediction) for intent in intents]
    return AgentAnswer(
        answer="\n\n".join(parts),
        intent=intents[0],
        intents=intents,
        suggested_questions=suggested_questions(intents[-1], prediction),
    )


def answer_question(question: str, prediction: dict) -> str:
    """Backwards-compatible helper that returns only the answer text."""
    return answer_with_metadata(question, prediction).answer


__all__ = [
    "AgentAnswer",
    "DISCLAIMER",
    "answer_question",
    "answer_with_metadata",
    "detect_intent",
    "format_risk_report",
    "suggested_questions",
]
