import logging

from fastapi import APIRouter, Depends

from app.agent.agent_service import (
    DISCLAIMER,
    answer_with_metadata,
    format_risk_report,
)
from app.agent.knowledge import KNOWLEDGE_BASE
from app.api.schemas import (
    AgentRequest,
    AgentResponse,
    ReportRequest,
    ReportResponse,
)
from app.core.security import require_api_key
from app.ml.prediction import get_sample_prediction

logger = logging.getLogger("assistant.agent")

router = APIRouter(prefix="/agent", tags=["Agent"], dependencies=[Depends(require_api_key)])


@router.post("/ask", response_model=AgentResponse)
def ask_agent(request: AgentRequest):
    """Answer a question about one prediction.

    The service is stateless: send the prediction with every question.
    """
    prediction = request.prediction.model_dump()
    result = answer_with_metadata(request.question, prediction)

    # Log only the detected intents. Never log the question or prediction:
    # they can contain patient information.
    logger.info("answered intents=%s", ",".join(result.intents))

    return AgentResponse(
        answer=result.answer,
        intent=result.intent,
        intents=result.intents,
        suggested_questions=result.suggested_questions,
        prediction=request.prediction,
        disclaimer=DISCLAIMER,
    )


@router.post("/report", response_model=ReportResponse)
def risk_report(request: ReportRequest):
    """Return the standard text summary of a prediction."""
    return ReportResponse(
        report=format_risk_report(request.prediction.model_dump()),
        prediction=request.prediction,
        disclaimer=DISCLAIMER,
    )


@router.get("/questions")
def supported_questions():
    """Example questions the assistant understands, grouped by topic."""
    return {"categories": KNOWLEDGE_BASE["question_catalog"]}


@router.get("/sample-prediction")
def sample_prediction():
    """A ready-made prediction for trying the API."""
    return get_sample_prediction()
