"""Rule-based intent detection.

Every intent has a list of (regex, weight) patterns that run against the
*normalised* question (see app.agent.text.normalize: lower case, no
punctuation, "follow-up" -> "follow up", "72%" -> "72 percent").

The intent with the highest score wins. Ties go to the intent that comes first
in PRIORITY. Scores below MIN_SCORE fall back to "general".

To teach the assistant a new question: add a pattern to the matching intent
(or add a new intent here, a handler in agent_service.py, and text in
knowledge_base.json), then add the question to tests/test_rules.py.
"""

import re
from typing import Iterable, Optional

from app.agent.knowledge import find_factor_mentions
from app.agent.text import normalize

MIN_SCORE = 4
MAX_COMPOUND_INTENTS = 3

INTENT_PATTERNS: dict[str, list[tuple[str, int]]] = {
    # ---- safety first -----------------------------------------------------
    "emergency": [
        (r"\b(chest pain|cant breathe|cannot breathe|trouble breathing|difficulty breathing|shortness of breath|unconscious|unresponsive|seizure|heart attack|stroke|overdose|overdosed|severe bleeding|bleeding heavily|suicid\w*|kill myself|self harm|end my life)\b", 12),
        (r"\b(medical emergency|call an ambulance|need an ambulance|call 911|call 112|call 999)\b", 12),
        (r"\bis (this|it) an emergency\b", 12),
    ],
    "medical_advice": [
        (r"\b(should|can|could|would|do|may|must)\b (i|we|he|she|they|the patient|this patient|patient)\b.{0,40}\b(stop|start|take|increase|decrease|change|skip|reduce|double|discontinue|switch|give|use)\b.{0,40}\b(insulin|medication|medications|medicine|medicines|drug|drugs|dose|doses|pill|pills|tablet|tablets|meds|metformin|statin|antibiotic|antibiotics)\b", 10),
        (r"\b(dose|dosage|dosing|prescribe|prescribed|prescription|mg|milligrams?)\b", 10),
        (r"\bwhat (medication|medications|medicine|medicines|drug|drugs|treatment|dose|dosage)\b.{0,30}\b(should|to|can|do)\b", 10),
        (r"(?<!number of )\bdiagnos(?:e|ed|ing|is)\b", 10),
        (r"\b(do|does|is|are)\b.{0,30}\bhave (a |an )?(diabetes|cancer|infection|disease|condition|disorder|sepsis|pneumonia|heart failure|kidney)\w*", 10),
        (r"\b(treat|treatment|treatments|cure|therapy|therapies|surgery)\b", 10),
        (r"\bmedical advice\b", 10),
        (r"\b(reduc\w*|lower\w*|improv\w*|control\w*|fix\w*|manag\w*|bring down|bringing down)\b.{0,20}\b(a1c|hba1c|blood sugar|glucose|diabetes|sugar levels?)\b", 10),
        (r"\b(can|should|could|may) (the |this )?(patient|he|she)\b.{0,15}\b(go home|be discharged|be sent home)\b", 10),
        (r"\b(is it|is he|is she|is the patient|is this patient) (safe|ready|okay|fine)\b.{0,15}\b(discharg\w*|go home|leave)\b", 10),
        (r"\b(ready for discharge|safe to discharge|fit for discharge)\b", 10),
    ],
    # ---- understanding the result -----------------------------------------
    "risk_explanation": [
        (r"\bwhy\b.{0,40}\b(risk|readmit\w*|readmission|predict\w*|score|flagged|likely|unlikely)\b", 7),
        (r"\bwhy\b.{0,15}\b(high|low|medium|moderate)\b", 7),
        (r"\bexplain\b.{0,20}\b(risk|prediction|result|score|output|outcome)\b", 7),
        (r"\bhow (did|does) (the )?(model|system|assistant|it) (arrive|come|get|reach|decide|conclude)\b", 6),
        (r"\bwhat (is )?(driving|drives|caused|causes|behind)\b.{0,30}\b(risk|prediction|score|result)\b", 7),
        (r"\b(reason|reasons|rationale|justification) (for|behind)\b.{0,30}\b(risk|prediction|score|result)\b", 7),
    ],
    "risk_meaning": [
        (r"\bwhat (does|do|would|is)\b.{0,25}\b(percent|probability|percentage|risk level|risk score|risk category|likely|unlikely|prediction|readmission risk)\b.{0,25}\b(mean|indicate|imply|signify|represent)\b", 8),
        (r"\bwhat (does|do|is)\b.{0,10}\b(high|low|medium|moderate)\b.{0,10}\b(mean|indicate|imply)\b", 6),
        (r"\b(mean|meaning of|interpret\w*|interpretation)\b.{0,30}\b(risk|probability|percent|score|prediction|likely|unlikely)\b", 7),
        (r"\bhow (should|do|can) (i|we) (read|interpret|understand|use)\b.{0,20}\b(result|prediction|score|risk|probability|percentage|number)\b", 8),
        (r"\bis \d+(\.\d+)? percent (high|low|bad|good|serious|a lot)\b", 8),
        (r"\b(risk level|risk category|risk band|risk score)\b", 4),
    ],
    "risk_summary": [
        (r"\b(what is|whats|tell me|give me|show me|state)\b.{0,20}\b(risk|probability|chance|likelihood)\b", 6),
        (r"\bhow (likely|risky|high|probable)\b", 6),
        (r"\bwill (the |this )?(patient|he|she|they)\b.{0,20}\b(be )?(readmitted|readmit|return|come back|be admitted)\b", 7),
        (r"\b(chance|probability|likelihood|odds|percentage) of (readmission|readmit\w*|being readmitted|return\w*)\b", 6),
        (r"\bis (the )?(patient|he|she) (likely|at risk|high risk|at high risk)\b", 6),
        (r"\b(readmission|readmit) (risk|prediction|probability)\b", 4),
    ],
    "report": [
        (r"\b(report|summary|summari[sz]e|overview|full result|full results|complete result|all details|everything)\b", 7),
        (r"\b(show|give|tell) me (the )?(prediction|results?|output)\b", 7),
        (r"\bwhat (is|are) the (prediction|results?|output)\b", 6),
    ],
    "readmission_definition": [
        (r"\b(what is|whats|define|definition of|meaning of) (a |an |the )?(hospital )?readmission(?! (risk|probability|prediction|score|likelihood|chance|rate))\b", 8),
        (r"\bwhat does (a )?(hospital )?readmission mean\b", 9),
        (r"\bwhat counts as (a )?readmission\b", 8),
        (r"\b(30 day\w*|thirty day\w*|within 30)\b", 4),
    ],
    # ---- factors ----------------------------------------------------------
    "factors": [
        (r"\bfactors?\b", 6),
        (r"\bcontribut\w*\b", 6),
        (r"\bimportant features?\b", 6),
        (r"\b(drivers|variables|features)\b", 5),
        (r"\b(reasons|influenc\w*)\b", 4),
    ],
    "top_factor": [
        (r"\b(most|biggest|main|primary|top|largest|key|strongest|major|single|number one)\b (\w+ ){0,2}(factor|driver|reason|contributor|feature|cause)\b", 9),
        (r"\bwhich (one|factor|feature)\b.{0,25}\b(most|biggest|matters|important)\b", 9),
        (r"\bwhat matters (the )?most\b", 9),
    ],
    # ---- follow-up --------------------------------------------------------
    "monitoring": [
        (r"\bmonitor\w*\b", 7),
        (r"\bfollow ?ups?\b", 7),
        (r"\b(after|post) discharge\b", 5),
        (r"\b(check ups?|checkups?|surveillance|watch for|keep an eye)\b", 6),
        (r"\bwhat (should|needs to|must) be (watched|tracked|checked|reviewed)\b", 7),
        (r"\bwarning signs?\b", 6),
    ],
    "care_planning": [
        (r"\b(reduc\w*|lower\w*|decreas\w*|mitigat\w*|prevent\w*|avoid\w*|minimi[sz]\w*|improv\w*)\b.{0,30}\b(risk|readmission|readmissions|readmitted|chance)\b", 8),
        (r"\brisk\b.{0,30}\b(reduc\w*|lower\w*|decreas\w*|mitigat\w*|prevent\w*|improv\w*)", 8),
        (r"\bhow (can|could|do|should|would)\b.{0,25}\b(reduc\w*|lower\w*|prevent\w*|mitigat\w*|decreas\w*)", 7),
        (r"\bnext steps?\b", 7),
        (r"\bwhat (can|should|could|do) (we|i|the team|the clinicians?|clinicians?|staff)\b.{0,10}\bdo\b", 7),
        (r"\bwhat can be done\b", 7),
        (r"\b(recommend\w*|suggest\w*|advice|advise)\b", 6),
        (r"\b(discharge plann?\w*|care plan\w*|care coordination|transition of care|action plan|intervention\w*)\b", 7),
        (r"\bhow (can|do|should) (we|i) (help|support|manage|handle|prepare)\b", 7),
    ],
    # ---- the model --------------------------------------------------------
    "model": [
        (r"\bhow (does|do|is|are)\b.{0,25}\b(model|system|prediction|predictions|algorithm|it|this|risk|probability|score|result)\b.{0,15}\b(work|works|working|calculated|made|generated|produced|predict|predicts)\b", 8),
        (r"\bhow (the )?(system|model|prediction|this) works?\b", 8),
        (r"\b(explain|describe|tell me about|about) (the |this )?(model|algorithm|system)\b", 8),
        (r"\b(what|which) (model|algorithm|type of model|kind of model|machine learning)\b", 8),
        (r"\b(machine learning|ml model|algorithm|artificial intelligence)\b", 6),
    ],
    "explainability": [
        (r"\b(shap|lime|explainab\w*|interpretab\w*|feature attribution|feature importance)\b", 8),
        (r"\bhow (are|were|do you|did you|does the model|is)\b.{0,20}\b(factors?|features?|contributors?)\b.{0,20}\b(identified|determined|selected|chosen|calculated|found|ranked|computed|derived)\b", 9),
        (r"\bhow do you know\b.{0,20}\b(factors?|features?)\b", 8),
        (r"\bhow (are|were) the factors\b", 8),
    ],
    "training_data": [
        (r"\b(training|trained|train)\b.{0,20}\b(data|dataset|records|population|patients)\b", 8),
        (r"\bdata\b.{0,30}\b(train\w*|used to build)\b", 8),
        (r"\b(dataset|data set|data source|data sources)\b", 8),
        (r"\bwhat (data|information|inputs?|variables|features|parameters)\b.{0,25}\b(model|system|prediction)\b.{0,20}\b(use|uses|used|need|needs|take|takes|require|requires|consider|considers)\b", 8),
        (r"\btrained (on|with|using)\b", 8),
        (r"\b(inputs?|input data|input variables)\b", 5),
    ],
    "limitations": [
        (r"\blimitations?\b", 8),
        (r"\btrust\w*\b", 9),
        (r"\b(accura\w*|reliab\w*|precise|precision|recall|auc|calibrat\w*)\b", 8),
        (r"\b(confidence|confident|uncertain\w*|error|errors|wrong|mistake|mistakes|bias|biased|fairness|false positive|false negative|validated|validation)\b", 7),
        (r"\bhow (good|well)\b", 6),
        (r"\bperform\w*\b", 5),
    ],
    "what_if": [
        (r"\bwhat if\b", 8),
        (r"\b(recalculat\w*|re calculat\w*|re run|rerun|simulat\w*|scenario|scenarios|hypothetical\w*)\b", 8),
        (r"\bif (the )?(a1c|patient|stay|age|medication|medications|insulin|diagnoses|number)\b.{0,30}\b(were|was|is|changed|lower|higher|different|decreased|increased|improved)\b", 8),
        (r"\b(change|changing|update|updating|modify|modifying)\b.{0,15}\b(input|inputs|value|values|data)\b", 7),
    ],
    # ---- the assistant ----------------------------------------------------
    "intended_use": [
        (r"\b(replace|substitute|instead of|in place of)\b.{0,25}\b(doctor|doctors|clinician|clinicians|physician|physicians|nurse|nurses|care team|healthcare team|medical professional\w*)\b", 9),
        (r"\bwho (is|should|can|are|would)\b.{0,25}\b(use|using|used|for|intended|target)\b", 8),
        (r"\b(intended use|intended for|intended purpose|clinical use|clinically approved|approved|approval|certified|fda|ce mark|regulat\w*)\b", 8),
        (r"\b(final decision|make decisions|decision support|rely on|depend on this|can i rely)\b", 7),
        (r"\b(can|should|do) (i|we) (rely|depend|base)\b", 8),
        (r"\b(is|are) (this|it|you) (a )?(doctor|medical device|clinician)\b", 8),
    ],
    "data_privacy": [
        (r"\b(hipaa|gdpr)\b", 10),
        (r"\b(compliance|compliant)\b", 6),
        (r"\b(privacy|private|confidential\w*|secur\w*|encrypt\w*|anonymi[sz]\w*|de identified|pii)\b", 8),
        (r"\b(is|are|do|does|will|where)\b.{0,25}\b(data|information|question|questions|conversation|chat)\b.{0,25}\b(stored|store|saved|save|kept|retained|logged|shared|share|sent|transmitted|safe)\b", 9),
        (r"\bwho (can see|has access|sees)\b", 8),
        (r"\b(stored|saved|retain\w*|logged|logging)\b", 5),
    ],
    "help": [
        (r"\bwhat can (you|i) (do|help|answer|ask)\b", 8),
        (r"\bwhat (questions|kind of questions|things)\b", 7),
        (r"^help( me)?$", 8),
        (r"\bhow (do|can) i use (this|you|the assistant)\b", 7),
        (r"\b(capabilities|commands|example questions|sample questions|examples)\b", 6),
    ],
    "about": [
        (r"\bwho are you\b", 8),
        (r"\bwhat are you\b", 8),
        (r"\b(what is|whats) this (assistant|system|tool|app|bot)\b", 8),
        (r"\btell me about (yourself|this assistant)\b", 8),
        (r"\bwhat is your (name|purpose)\b", 8),
    ],
    "greeting": [
        (r"^(hi|hii|hello|hey|hola|namaste|good morning|good afternoon|good evening|greetings)( there| assistant| bot| team)?$", 8),
    ],
    "closing": [
        (r"^(thanks|thank you|thankyou|thx|ok thanks|okay thanks|great thanks|bye|goodbye|see you|cheers)( a lot| so much| very much)?( assistant| bot)?$", 8),
    ],
}

# Order matters only for ties: earlier means preferred.
PRIORITY: list[str] = [
    "emergency",
    "medical_advice",
    "factor_detail",
    "top_factor",
    "risk_explanation",
    "risk_meaning",
    "factors",
    "risk_summary",
    "monitoring",
    "care_planning",
    "model",
    "explainability",
    "limitations",
    "intended_use",
    "data_privacy",
    "training_data",
    "readmission_definition",
    "what_if",
    "report",
    "help",
    "about",
    "greeting",
    "closing",
]

_COMPILED = {
    intent: [(re.compile(pattern), weight) for pattern, weight in patterns]
    for intent, patterns in INTENT_PATTERNS.items()
}

_EXPLAIN_CUE = re.compile(
    r"\b(what|explain|mean|means|meaning|why|how|tell|describe|matter|matters|"
    r"affect|affects|influence|influences|impact|role|important|importance|about)\b"
)
_CLAUSE_SPLIT = re.compile(r"\?|;|\band\b|\balso\b|\bthen\b", re.IGNORECASE)


def _mentions_extra_term(text: str, terms: Iterable[str]) -> bool:
    return any(term and re.search(rf"\b{re.escape(term)}\b", text) for term in terms)


def score_intents(
    question: str, extra_factor_terms: Optional[Iterable[str]] = None
) -> dict[str, int]:
    """Return {intent: score} for every intent that matched the question.

    `extra_factor_terms` are normalised factor labels from the current
    prediction, so users can ask about any factor the model returned, even
    ones the knowledge base has never heard of.
    """
    text = normalize(question)
    if not text:
        return {}

    scores: dict[str, int] = {}
    for intent, patterns in _COMPILED.items():
        weights = [weight for regex, weight in patterns if regex.search(text)]
        if weights:
            # Best pattern plus a small bonus (max +2) for corroborating ones.
            scores[intent] = max(weights) + min(len(weights) - 1, 2)

    if find_factor_mentions(text) or _mentions_extra_term(text, extra_factor_terms or ()):
        cue = 2 if _EXPLAIN_CUE.search(text) else 0
        scores["factor_detail"] = max(scores.get("factor_detail", 0), 5 + cue)

    return scores


def detect_intent(
    question: str, extra_factor_terms: Optional[Iterable[str]] = None
) -> str:
    """Return the single best intent for a question, or "general"."""
    scores = score_intents(question, extra_factor_terms)
    best_intent, best_score = "general", 0
    for intent in PRIORITY:
        score = scores.get(intent, 0)
        if score > best_score:
            best_intent, best_score = intent, score
    return best_intent if best_score >= MIN_SCORE else "general"


def detect_intents(
    question: str, extra_factor_terms: Optional[Iterable[str]] = None
) -> list[str]:
    """Like detect_intent, but answers compound questions.

    "Why is the risk high and what should be monitored?" returns
    ["risk_explanation", "monitoring"]. Always returns at least one intent.
    """
    terms = list(extra_factor_terms or ())
    whole = detect_intent(question, terms)
    if whole == "emergency":
        return [whole]

    clauses = [c for c in _CLAUSE_SPLIT.split(question) if c.strip()]
    if len(clauses) < 2:
        return [whole]

    found: list[str] = []
    for clause in clauses:
        intent = detect_intent(clause, terms)
        if intent != "general" and intent not in found:
            found.append(intent)

    if "emergency" in found:
        return ["emergency"]
    if len(found) >= 2:
        if "medical_advice" in found:
            found.remove("medical_advice")
            found.insert(0, "medical_advice")
        return found[:MAX_COMPOUND_INTENTS]
    return [whole]
