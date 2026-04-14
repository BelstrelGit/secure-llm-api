from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str
    system: str | None = None
    max_history: int = Field(default=10, ge=0)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    answer: str
