from fastapi import APIRouter

from fastapi import HTTPException

from app.schemas.prediction_schema import (
    AssessmentResponse,
    PatientFeatures,
    PredictionResponse,
)
from app.services.assessment_service import assessment_service
from app.services.prediction_service import prediction_service


router = APIRouter(prefix="/api", tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientFeatures) -> PredictionResponse:
    return prediction_service.predict(patient)


@router.post("/assess", response_model=AssessmentResponse)
def assess(patient: PatientFeatures) -> AssessmentResponse:
    try:
        return assessment_service.assess(patient)
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error