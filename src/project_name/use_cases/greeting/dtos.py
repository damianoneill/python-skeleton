# src/project_name/use_cases/greeting/dtos.py
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class GreetingRequest(BaseModel):
    """Input DTO for greeting requests using Pydantic v2."""

    recipient: str = Field(min_length=1, max_length=100)
    message: str = Field(default="Hello", min_length=1)
    include_timestamp: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {"examples": [{"recipient": "World", "message": "Hello", "include_timestamp": True}]}
    }

    @field_validator("recipient")
    @classmethod
    def recipient_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Recipient cannot be empty")
        return v


class GreetingResponse(BaseModel):
    """Output DTO for greeting responses using Pydantic v2."""

    greeting: str
    recipient: str
    timestamp: datetime | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [{"greeting": "Hello, World!", "recipient": "World", "timestamp": "2025-05-16T12:00:00"}]
        }
    }
