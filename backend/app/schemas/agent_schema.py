from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AgentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1, max_length=500)
    context: dict[str, Any] | None = None


class AgentResponse(BaseModel):
    answer: str
    intent: str | None = None
    intents: list[str] = Field(default_factory=list)
    suggested_questions: list[str] = Field(default_factory=list)
    prediction: dict[str, Any] | None = None
    disclaimer: str | None = None