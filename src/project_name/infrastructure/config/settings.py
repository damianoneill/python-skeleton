"""API configuration settings."""

import os

from pydantic import BaseModel, Field


class APISettings(BaseModel):
    """API configuration settings."""

    title: str = "Greeting API"
    description: str = "API for generating and retrieving greetings"
    version: str = "1.0.0"
    # Default to localhost for security, can be overridden by environment variable
    host: str = Field(default=os.environ.get("API_HOST", "127.0.0.1"))
    port: int = Field(default=int(os.environ.get("API_PORT", "8000")))
    debug: bool = Field(default=os.environ.get("API_DEBUG", "false").lower() == "true")


# Global settings instance
settings = APISettings()
