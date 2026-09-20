from __future__ import annotations

from typing import Any

import pandas as pd
from joblib import load

from app.config import MODEL_BUNDLE_PATH, PREPROCESSOR_PATH


class ModelService:
    def __init__(self) -> None:
        if not MODEL_BUNDLE_PATH.is_file():
            raise FileNotFoundError(f"Model bundle not found: {MODEL_BUNDLE_PATH}")
        if not PREPROCESSOR_PATH.is_file():
            raise FileNotFoundError(f"Preprocessor not found: {PREPROCESSOR_PATH}")

        bundle = load(MODEL_BUNDLE_PATH)
        if not isinstance(bundle, dict) or not {"model", "threshold", "feature_names"}.issubset(bundle):
            raise ValueError(
                "Model bundle must contain model, threshold, and feature_names."
            )

        self.model = bundle["model"]
        self.threshold = float(bundle["threshold"])
        self.feature_names = list(bundle["feature_names"])
        self.preprocessor = load(PREPROCESSOR_PATH)
        self.input_features = list(self.preprocessor.feature_names_in_)

        transformed_names = list(self.preprocessor.get_feature_names_out())
        if transformed_names != self.feature_names:
            raise ValueError(
                "Saved model feature_names do not match the preprocessor output."
            )

    def predict(self, patient: dict[str, Any]) -> dict[str, Any]:
        missing = [name for name in self.input_features if name not in patient]
        if missing:
            raise ValueError(f"Missing required input features: {missing}")

        frame = pd.DataFrame(
            [{name: patient[name] for name in self.input_features}]
        )
        processed = self.preprocessor.transform(frame)
        probability = float(self.model.predict_proba(processed)[0, 1])
        prediction = int(probability >= self.threshold)

        return {
            "model_estimated_probability": probability,
            "decision_threshold": self.threshold,
            "prediction": prediction,
            "label": (
                "Readmitted within 30 days"
                if prediction == 1
                else "Not readmitted within 30 days"
            ),
        }


model_service = ModelService()
