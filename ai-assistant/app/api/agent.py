from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.agent_service import answer_question


router = APIRouter()


class PredictionData(BaseModel):
    readmission_prediction: str
    risk_probability: float
    risk_level: str
    top_contributing_factors: list[str]


class AgentRequest(BaseModel):
    question: str
    prediction: PredictionData


@router.post("/agent/ask")
def ask_agent(request: AgentRequest):

    prediction = request.prediction.model_dump()

    answer = answer_question(
        request.question,
        prediction
    )

    return {
        "answer": answer,
        "prediction": prediction
    }