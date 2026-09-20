from app.ml.predict import ModelPredictor
from app.ml.preprocessing import Preprocessor
from app.schemas.prediction_schema import PatientFeatures, PredictionResponse


class PredictionService:
    def __init__(self) -> None:
        self.preprocessor = Preprocessor()
        self.predictor = ModelPredictor()

    def predict(self, patient: PatientFeatures) -> PredictionResponse:
        processed = self.preprocessor.transform(patient.to_feature_dict())
        probability, prediction = self.predictor.predict(processed)
        return PredictionResponse(
            model_estimated_probability=probability,
            decision_threshold=self.predictor.threshold,
            prediction=prediction,
            label=(
                "Readmitted within 30 days"
                if prediction == 1
                else "Not readmitted within 30 days"
            ),
        )


prediction_service = PredictionService()