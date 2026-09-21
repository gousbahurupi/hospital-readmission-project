import httpx

from app.config import AI_ASSISTANT_API_KEY, AI_ASSISTANT_API_URL
from app.schemas.agent_schema import AgentRequest, AgentResponse


DEFAULT_PREDICTION = {
    "readmission_prediction": "UNLIKELY",
    "risk_probability": 0,
    "risk_level": "LOW",
    "top_contributing_factors": ["No patient assessment has been provided"],
}


class AgentService:
    def ask(self, request: AgentRequest) -> AgentResponse:
        prediction = request.context or DEFAULT_PREDICTION
        headers = (
            {"X-API-Key": AI_ASSISTANT_API_KEY}
            if AI_ASSISTANT_API_KEY
            else {}
        )

        try:
            with httpx.Client(timeout=httpx.Timeout(30.0, connect=10.0)) as client:
                response = client.post(
                    f"{AI_ASSISTANT_API_URL}/agent/ask",
                    json={"question": request.question, "prediction": prediction},
                    headers=headers,
                )
                response.raise_for_status()
                return AgentResponse.model_validate(response.json())
        except httpx.HTTPStatusError as error:
            if error.response.status_code == 401:
                raise RuntimeError(
                    "The AI assistant rejected the backend API key. "
                    "Check API_KEY on the AI assistant and AI_ASSISTANT_API_KEY on the backend."
                ) from error
            raise RuntimeError("The AI assistant service is unavailable.") from error
        except httpx.HTTPError as error:
            raise RuntimeError("The AI assistant service is unavailable.") from error
        except (TypeError, ValueError) as error:
            raise RuntimeError("The AI assistant returned an invalid response.") from error


agent_service = AgentService()