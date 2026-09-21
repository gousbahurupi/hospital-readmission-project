from fastapi import APIRouter, HTTPException

from app.schemas.agent_schema import AgentRequest, AgentResponse
from app.services.agent_service import agent_service


router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("/ask", response_model=AgentResponse)
def ask_agent(request: AgentRequest) -> AgentResponse:
    try:
        return agent_service.ask(request)
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error