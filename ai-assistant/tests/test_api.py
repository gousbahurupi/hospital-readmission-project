import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _no_api_key(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)


def _ask(question, prediction):
    return client.post("/agent/ask", json={"question": question, "prediction": prediction})


def test_root_and_health():
    assert client.get("/").json()["message"] == "Explainable AI Assistant API is running"
    assert client.get("/health").json() == {"status": "ok"}


def test_ask_returns_answer_and_metadata(prediction):
    response = _ask("Why is the risk high?", prediction)
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "risk_explanation"
    assert "72%" in body["answer"]
    assert len(body["suggested_questions"]) == 3
    assert body["prediction"]["risk_level"] == "HIGH"
    assert "decision support" in body["disclaimer"]


def test_prediction_is_normalised(prediction):
    prediction["risk_level"] = "moderate"
    prediction["readmission_prediction"] = "likely"
    body = _ask("Give me a summary", prediction).json()
    assert body["prediction"]["risk_level"] == "MEDIUM"
    assert body["prediction"]["readmission_prediction"] == "LIKELY"


def test_report_endpoint(prediction):
    response = client.post("/agent/report", json={"prediction": prediction})
    assert response.status_code == 200
    assert "Risk Level: HIGH" in response.json()["report"]


def test_questions_and_sample_endpoints():
    categories = client.get("/agent/questions").json()["categories"]
    assert len(categories) >= 4
    assert client.get("/agent/sample-prediction").json()["risk_level"] == "HIGH"


@pytest.mark.parametrize(
    "change",
    [
        {"risk_probability": 140},
        {"risk_probability": -1},
        {"risk_level": "EXTREME"},
        {"top_contributing_factors": []},
        {"readmission_prediction": ""},
    ],
)
def test_invalid_prediction_is_rejected(prediction, change):
    prediction.update(change)
    assert _ask("Why is the risk high?", prediction).status_code == 422


def test_empty_and_oversized_questions_are_rejected(prediction):
    assert _ask("   ", prediction).status_code == 422
    assert _ask("x" * 501, prediction).status_code == 422


def test_extra_prediction_fields_are_not_echoed(prediction):
    prediction["patient_name"] = "Should not come back"
    body = _ask("Give me a summary", prediction).json()
    assert "patient_name" not in body["prediction"]
    assert "Should not come back" not in body["answer"]


def test_api_key_is_enforced_when_configured(monkeypatch, prediction):
    monkeypatch.setenv("API_KEY", "s3cret")
    assert _ask("Give me a summary", prediction).status_code == 401
    wrong = client.post(
        "/agent/ask",
        json={"question": "Give me a summary", "prediction": prediction},
        headers={"X-API-Key": "nope"},
    )
    assert wrong.status_code == 401
    right = client.post(
        "/agent/ask",
        json={"question": "Give me a summary", "prediction": prediction},
        headers={"X-API-Key": "s3cret"},
    )
    assert right.status_code == 200
    assert client.get("/health").status_code == 200  # health stays open


def test_demo_is_disabled_and_security_headers():
    response = client.get("/demo")
    assert response.status_code == 404
    assert response.headers["x-content-type-options"] == "nosniff"
    assert client.get("/agent/questions").headers["cache-control"] == "no-store"
