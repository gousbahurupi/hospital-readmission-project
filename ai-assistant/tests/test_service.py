import pytest

from app.agent.agent_service import (
    answer_question,
    answer_with_metadata,
    format_risk_report,
)


def test_report_matches_original_layout(prediction):
    report = format_risk_report(prediction)
    assert "Readmission Prediction: LIKELY" in report
    assert "Risk Probability: 72%" in report
    assert "Risk Level: HIGH" in report
    assert "• A1C result" in report
    assert "does not provide a medical diagnosis" in report


def test_float_probability_is_formatted_cleanly(prediction):
    prediction["risk_probability"] = 72.0
    assert "72%" in format_risk_report(prediction)
    prediction["risk_probability"] = 72.46
    assert "72.5%" in format_risk_report(prediction)


def test_risk_explanation_includes_probability_and_factors(prediction):
    answer = answer_question("Why is the risk high?", prediction)
    assert "72%" in answer and "HIGH" in answer
    assert "A1C result" in answer
    assert "not confirmed causes" in answer


def test_factor_list(prediction):
    answer = answer_question("What are the contributing factors?", prediction)
    assert "Time in hospital" in answer
    assert "Medication-related factors" in answer


def test_top_factor_is_first_listed(prediction):
    answer = answer_question("What is the most important factor?", prediction)
    assert "lists A1C result first" in answer


def test_factor_detail_for_listed_factor(prediction):
    answer = answer_question("What does A1C mean?", prediction)
    assert "HbA1c" in answer
    assert "one of the top contributing factors" in answer


def test_factor_detail_for_factor_not_in_prediction(prediction):
    answer = answer_question("What does age mean for readmission?", prediction)
    assert "not listed among the top contributing factors" in answer


def test_unknown_custom_factor_gets_honest_answer(prediction):
    prediction["top_contributing_factors"].append("Serum sodium level")
    answer = answer_question("What does serum sodium level mean?", prediction)
    assert "don't have detailed background" in answer


def test_monitoring_is_general_not_treatment(prediction):
    answer = answer_question("What should be monitored?", prediction)
    assert "reviewed by the healthcare team" in answer
    assert "not treatment or medication instructions" in answer
    assert "A1C result:" in answer


def test_risk_meaning_uses_prediction_values(prediction):
    answer = answer_question("What does 72% mean?", prediction)
    assert "about 72 out of 100" in answer
    assert "HIGH" in answer and "LIKELY" in answer


def test_low_risk_uses_low_wording(prediction):
    prediction.update(risk_level="LOW", risk_probability=12, readmission_prediction="UNLIKELY")
    answer = answer_question("What does this risk level mean?", prediction)
    assert "lower-risk group" in answer
    assert "UNLIKELY" in answer


def test_medical_advice_is_declined_with_pointer_to_care_team(prediction):
    answer = answer_question("Should I stop the insulin?", prediction)
    assert "can't diagnose" in answer
    assert "healthcare team" in answer


def test_emergency_message(prediction):
    answer = answer_question("The patient has chest pain", prediction)
    assert "emergency" in answer.lower()


def test_compound_answer_contains_both_parts(prediction):
    result = answer_with_metadata(
        "Why is the risk high and what should be monitored?", prediction
    )
    assert result.intents == ["risk_explanation", "monitoring"]
    assert "driven by these factors" in result.answer
    assert "monitoring considerations" in result.answer.lower()


def test_unknown_question_falls_back_to_summary(prediction):
    result = answer_with_metadata("What is the weather today?", prediction)
    assert result.intent == "general"
    assert "Readmission Prediction: LIKELY" in result.answer


def test_suggested_questions_are_filled_in_and_answerable(prediction):
    from app.agent.rules import detect_intent

    result = answer_with_metadata("What are the contributing factors?", prediction)
    assert len(result.suggested_questions) == 3
    for question in result.suggested_questions:
        assert "{" not in question
        assert detect_intent(question, ["a1c result"]) != "general", question


def test_every_follow_up_template_is_answerable(prediction):
    from app.agent.agent_service import suggested_questions
    from app.agent.knowledge import KNOWLEDGE_BASE
    from app.agent.rules import detect_intent

    for intent in KNOWLEDGE_BASE["follow_ups"]:
        for question in suggested_questions(intent, prediction):
            assert detect_intent(question, ["a1c result"]) != "general", question


def test_missing_prediction_field_raises(prediction):
    del prediction["risk_level"]
    with pytest.raises(ValueError):
        answer_question("Why is the risk high?", prediction)
