from fastapi import FastAPI, HTTPException

from app.model_service import model_service
from app.schemas import PatientFeatures, PredictionResponse


app = FastAPI(
    title="Hospital Readmission ML API",
    version="1.0.0",
    description="Standalone model-estimated 30-day readmission risk API.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/model-info")
def model_info() -> dict[str, object]:
    return {
        "model_type": type(model_service.model).__name__,
        "decision_threshold": model_service.threshold,
        "input_features": model_service.input_features,
        "encoded_feature_count": len(model_service.feature_names),
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientFeatures) -> PredictionResponse:
    try:
        result = model_service.predict(patient.as_dict())
    except (TypeError, ValueError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return PredictionResponse(**result)
