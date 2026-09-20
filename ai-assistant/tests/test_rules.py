import pytest

from app.agent.knowledge import KNOWLEDGE_BASE
from app.agent.rules import detect_intent, detect_intents

CASES = [
    # behaviour of the original rules must not change
    ("Why is the risk high?", "risk_explanation"),
    ("why low", "risk_explanation"),
    ("What factors contributed to this?", "factors"),
    ("Which important features matter?", "factors"),
    ("How should we monitor follow-up?", "monitoring"),
    ("followup plan?", "monitoring"),
    ("How does the model work?", "model"),
    ("explain the model", "model"),
    ("How system works", "model"),
    ("What are the limitations?", "limitations"),
    ("Can I trust this prediction?", "limitations"),
    ("Is it accurate?", "limitations"),
    # new: understanding the result
    ("What is the risk level?", "risk_summary"),
    ("How likely is readmission within 30 days?", "risk_summary"),
    ("Will the patient be readmitted?", "risk_summary"),
    ("What does 72% mean?", "risk_meaning"),
    ("What does HIGH risk mean?", "risk_meaning"),
    ("How should I interpret this result?", "risk_meaning"),
    ("What does LIKELY mean?", "risk_meaning"),
    ("Explain the prediction", "risk_explanation"),
    ("What is driving this score?", "risk_explanation"),
    ("Give me the full report", "report"),
    ("Summarize the result", "report"),
    ("What is a readmission?", "readmission_definition"),
    ("What is the readmission risk?", "risk_summary"),
    # new: factors
    ("What is the most important factor?", "top_factor"),
    ("Which factor matters most?", "top_factor"),
    ("What does A1C mean?", "factor_detail"),
    ("Why does time in hospital matter?", "factor_detail"),
    ("Tell me about length of stay", "factor_detail"),
    ("What does number of diagnoses mean?", "factor_detail"),
    ("Explain medication-related factors", "factor_detail"),
    ("How do medications affect the risk?", "factor_detail"),
    # new: follow-up and care planning
    ("What should be monitored after discharge?", "monitoring"),
    ("How can the risk be reduced?", "care_planning"),
    ("How can we lower readmission risk?", "care_planning"),
    ("What are the next steps?", "care_planning"),
    ("What should we do?", "care_planning"),
    ("Any recommendations?", "care_planning"),
    # new: model and assistant
    ("How is the risk calculated?", "model"),
    ("Which algorithm is used?", "model"),
    ("How are the factors identified?", "explainability"),
    ("Do you use SHAP?", "explainability"),
    ("What data does the model use?", "training_data"),
    ("What was the model trained on?", "training_data"),
    ("How accurate is this?", "limitations"),
    ("Can you recalculate the risk with different values?", "what_if"),
    ("What if the A1C were lower?", "what_if"),
    ("Does this replace a clinician?", "intended_use"),
    ("Who is this for?", "intended_use"),
    ("Is patient data stored?", "data_privacy"),
    ("Is this HIPAA compliant?", "data_privacy"),
    ("What can you do?", "help"),
    ("help", "help"),
    ("Who are you?", "about"),
    ("Hello", "greeting"),
    ("hi there", "greeting"),
    ("Thanks", "closing"),
    ("thank you so much", "closing"),
    # safety
    ("Should I stop the insulin?", "medical_advice"),
    ("What dose of metformin should be given?", "medical_advice"),
    ("Does the patient have diabetes?", "medical_advice"),
    ("What treatment do you recommend?", "medical_advice"),
    ("Can you diagnose this patient?", "medical_advice"),
    ("How do I reduce his A1C?", "medical_advice"),
    ("How to lower blood sugar?", "medical_advice"),
    ("Can this patient go home?", "medical_advice"),
    ("Is the patient safe to discharge?", "medical_advice"),
    ("The patient has chest pain right now", "emergency"),
    ("is this a medical emergency", "emergency"),
    # fallback
    ("What is the weather today?", "general"),
    ("", "general"),
    ("???", "general"),
]


@pytest.mark.parametrize("question,expected", CASES)
def test_detect_intent(question, expected):
    assert detect_intent(question) == expected


def test_every_catalog_question_maps_to_its_intent():
    for category in KNOWLEDGE_BASE["question_catalog"]:
        for item in category["questions"]:
            assert detect_intent(item["text"]) == item["intent"], item["text"]


def test_medical_terms_that_are_also_factors_are_not_blocked():
    # "diagnoses" and "medication" are risk factors, not requests for advice.
    assert detect_intent("What does number of diagnoses mean?") == "factor_detail"
    assert detect_intent("Tell me about medication changes") == "factor_detail"


def test_custom_factor_from_the_prediction_is_recognised():
    terms = ["serum sodium level"]
    assert detect_intent("What does serum sodium level mean?", terms) == "factor_detail"
    assert detect_intent("What does serum sodium level mean?") == "general"


def test_compound_question_returns_both_intents():
    result = detect_intents("Why is the risk high and what should be monitored?")
    assert result == ["risk_explanation", "monitoring"]


def test_compound_question_puts_medical_boundary_first():
    result = detect_intents("What dose should be given and what should be monitored?")
    assert result[0] == "medical_advice"
    assert "monitoring" in result


def test_emergency_always_wins_in_compound_questions():
    assert detect_intents("Why is the risk high? The patient has chest pain") == ["emergency"]


def test_single_intent_question_with_and_stays_single():
    assert detect_intents("What is the risk and probability?") == ["risk_summary"]
