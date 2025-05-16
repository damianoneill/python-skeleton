"""FastAPI application for the greeting service."""

from typing import Annotated

from fastapi import Depends, FastAPI, Query

from project_name.adapters.api.greeting_controller import GreetingController
from project_name.adapters.repositories.in_memory_greeting_repository import InMemoryGreetingRepository
from project_name.infrastructure.config.settings import settings
from project_name.use_cases.greeting.dtos import GreetingResponse
from project_name.use_cases.greeting.service import GreetingService

# Module-level singleton for dependency injection
greeting_repository = InMemoryGreetingRepository()
greeting_service = GreetingService(greeting_repository)
greeting_controller = GreetingController(greeting_service)


def get_greeting_controller() -> GreetingController:
    """Dependency provider for GreetingController."""
    return greeting_controller


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.title,
        description=settings.description,
        version=settings.version,
    )

    # Define routes
    @app.get(
        "/api/greetings/{recipient}",
        response_model=GreetingResponse,
        summary="Create a greeting",
        description="Generate a personalised greeting for the specified recipient.",
    )
    async def get_greeting(
        controller: Annotated[GreetingController, Depends(get_greeting_controller)],
        recipient: str,
        message: str = Query("Hello", description="Greeting message"),
        include_timestamp: bool = Query(False, description="Include timestamp in response"),
    ) -> GreetingResponse:
        """Generate a greeting for the specified recipient."""
        return controller.create_greeting(recipient, message, include_timestamp)

    @app.get(
        "/api/greetings",
        response_model=list[GreetingResponse],
        summary="Get latest greetings",
        description="Retrieve the most recent greetings.",
    )
    async def get_latest_greetings(
        controller: Annotated[GreetingController, Depends(get_greeting_controller)],
        limit: int = Query(5, description="Number of greetings to return", ge=1, le=100),
    ) -> list[GreetingResponse]:
        """Get the latest greetings."""
        return controller.get_latest_greetings(limit)

    return app
