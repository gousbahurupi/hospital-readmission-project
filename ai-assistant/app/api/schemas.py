"""Request and response models for the agent API."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

Question = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)]
FactorLabel = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
PredictionLabel = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=40)]

VALID_LEVELS = {"LOW", "MEDIUM", "HIGH"}
LEVEL_ALIASES = {"MODERATE": "MEDIUM", "MED": "MEDIUM"}

_EXAMPLE_PREDICTION = {
    "readmission_prediction": "LIKELY",
    "risk_probability": 72,
    "risk_level": "HIGH",
    "top_contributing_factors": [
        "A1C result",
        "Number of diagnoses",
        "Time in hospital",
        "Medication-related factors",
    ],
}


class PredictionData(BaseModel):
    """Output of the readmission model. risk_probability is a percentage (0-100)."""

    model_config = ConfigDict(json_schema_extra={"example": _EXAMPLE_PREDICTION})

    readmission_prediction: PredictionLabel
    risk_probability: float = Field(ge=0, le=100)
    risk_level: str
    top_contributing_factors: list[FactorLabel] = Field(min_length=1, max_length=15)

    @field_validator("readmission_prediction")
    @classmethod
    def _upper_prediction(cls, value: str) -> str:
        return value.upper()

    @field_validator("risk_level")
    @classmethod
    def _valid_level(cls, value: str) -> str:
        level = value.strip().upper()
        level = LEVEL_ALIASES.get(level, level)
        if level not in VALID_LEVELS:
            raise ValueError("risk_level must be LOW, MEDIUM or HIGH")
        return level


class AgentRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "Why is the risk high?",
                "prediction": _EXAMPLE_PREDICTION,
            }
        }
    )

    question: Question
    prediction: PredictionData


class AgentResponse(BaseModel):
    answer: str
    intent: str
    intents: list[str]
    suggested_questions: list[str]
    prediction: PredictionData
    disclaimer: str


class ReportRequest(BaseModel):
    prediction: PredictionData


class ReportResponse(BaseModel):
    report: str
    prediction: PredictionData
    disclaimer: str
