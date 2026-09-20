from pathlib import Path
from typing import Any

from joblib import load

from app.config import MODEL_BUNDLE_PATH


class ModelPredictor:
    def __init__(self, bundle_path: Path = MODEL_BUNDLE_PATH) -> None:
        if not bundle_path.exists():
            raise FileNotFoundError(f"Model bundle not found: {bundle_path}")
        bundle = load(bundle_path)
        if not isinstance(bundle, dict) or not {"model", "threshold"}.issubset(bundle):
            raise ValueError("Model bundle must contain 'model' and 'threshold'.")
        self.model = bundle["model"]
        self.threshold = float(bundle["threshold"])

    def predict(self, processed_features: Any) -> tuple[float, int]:
        probability = float(self.model.predict_proba(processed_features)[0, 1])
        prediction = int(probability >= self.threshold)
        return probability, prediction