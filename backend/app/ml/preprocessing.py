from typing import Any

import pandas as pd

from app.config import PREPROCESSOR_PATH


class Preprocessor:
    def __init__(self) -> None:
        if not PREPROCESSOR_PATH.exists():
            raise FileNotFoundError(f"Preprocessor not found: {PREPROCESSOR_PATH}")
        from joblib import load

        self._preprocessor = load(PREPROCESSOR_PATH)
        self._input_columns = list(self._preprocessor.feature_names_in_)

    def transform(self, features: dict[str, Any]):
        missing = [column for column in self._input_columns if column not in features]
        if missing:
            raise ValueError(f"Missing required input features: {missing}")
        frame = pd.DataFrame([{column: features[column] for column in self._input_columns}])
        return self._preprocessor.transform(frame)