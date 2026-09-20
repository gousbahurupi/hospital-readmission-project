from fastapi import APIRouter

from app.schemas.prediction_schema import PatientFeatures, PredictionResponse
from app.services.prediction_service import prediction_service


router = APIRouter(prefix="/api", tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientFeatures) -> PredictionResponse:
    return prediction_service.predict(patient)