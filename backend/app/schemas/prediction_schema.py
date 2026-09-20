from typing import Any

from pydantic import BaseModel, ConfigDict


class PatientFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")

    age: Any
    gender: Any
    admission_type_id: Any
    admission_source_id: Any
    discharge_disposition_id: Any
    diag_1_group: Any
    diag_2_group: Any
    diag_3_group: Any
    A1Cresult: Any
    max_glu_serum: Any
    diabetesMed: Any
    change: Any
    insulin: Any
    time_in_hospital: Any
    num_lab_procedures: Any
    num_procedures: Any
    num_medications: Any
    number_diagnoses: Any

    def to_feature_dict(self) -> dict[str, Any]:
        return self.model_dump()


class PredictionResponse(BaseModel):
    model_estimated_probability: float
    decision_threshold: float
    prediction: int
    label: str