from fastapi import APIRouter


router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/model-info")
def model_info() -> dict[str, object]:
    return {
        "version": "1.0",
        "trainingData": "UCI Diabetes 130-US hospitals dataset",
        "limitations": (
            "This model estimates 30-day readmission risk from the supplied "
            "patient fields. It is not a diagnosis, has not been clinically "
            "validated, and may perform differently for patient groups that "
            "were underrepresented in the training data. Review the result "
            "with the healthcare team."
        ),
        "model": "Random Forest",
        "target": "readmitted_30",
        "decisionThreshold": 0.5,
        "encodedFeatureCount": 141,
    }