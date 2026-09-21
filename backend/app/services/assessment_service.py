import httpx

from app.config import AI_ASSISTANT_API_KEY, AI_ASSISTANT_API_URL, ML_API_URL
from app.schemas.prediction_schema import AssessmentResponse, PatientFeatures, PredictionResponse


def _risk_level(probability: float) -> str:
    if probability >= 0.50:
        return "HIGH"
    if probability >= 0.25:
        return "MEDIUM"
    return "LOW"


class AssessmentService:
    def assess(self, patient: PatientFeatures) -> AssessmentResponse:
        payload = patient.to_feature_dict()
        timeout = httpx.Timeout(30.0, connect=10.0)

        try:
            with httpx.Client(timeout=timeout) as client:
                ml_response = client.post(f"{ML_API_URL}/predict", json=payload)
                ml_response.raise_for_status()
                model_result = ml_response.json()

                probability = float(model_result["model_estimated_probability"])
                prediction = PredictionResponse(
                    model_estimated_probability=probability,
                    decision_threshold=float(model_result["decision_threshold"]),
                    prediction=int(model_result["prediction"]),
                    label=str(model_result["label"]),
                )

                assistant_payload = {
                    "question": (
                        "Explain this patient's readmission risk, summarize the result, "
                        "and identify the most important contributing factors."
                    ),
                    "prediction": {
                        "readmission_prediction": (
                            "LIKELY" if prediction.prediction else "UNLIKELY"
                        ),
                        "risk_probability": round(probability * 100, 2),
                        "risk_level": _risk_level(probability),
                        "top_contributing_factors": [
                            "Model-estimated readmission probability",
                            "Hospitalization and diagnosis information",
                            "Medication and glucose-related features",
                        ],
                    },
                }
                headers = (
                    {"X-API-Key": AI_ASSISTANT_API_KEY}
                    if AI_ASSISTANT_API_KEY
                    else {}
                )
                assistant_response = client.post(
                    f"{AI_ASSISTANT_API_URL}/agent/ask",
                    json=assistant_payload,
                    headers=headers,
                )
                assistant_response.raise_for_status()

        except httpx.HTTPError as error:
            raise RuntimeError("A prediction service is currently unavailable.") from error
        except (KeyError, TypeError, ValueError) as error:
            raise RuntimeError("The prediction service returned an invalid response.") from error

        return AssessmentResponse(
            prediction=prediction,
            explanation=assistant_response.json(),
        )


assessment_service = AssessmentService()
