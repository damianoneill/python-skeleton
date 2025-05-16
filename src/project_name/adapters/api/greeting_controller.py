# src/project_name/adapters/api/greeting_controller.py

from fastapi import HTTPException

from project_name.domain.greeting.exceptions import GreetingError
from project_name.use_cases.greeting.dtos import GreetingRequest, GreetingResponse
from project_name.use_cases.greeting.service import GreetingService


class GreetingController:
    """Controller handling greeting-related endpoints."""

    def __init__(self, greeting_service: GreetingService):
        self.greeting_service = greeting_service

    def create_greeting(
        self, recipient: str, message: str = "Hello", include_timestamp: bool = False
    ) -> GreetingResponse:
        """Handle greeting creation endpoint."""
        try:
            request = GreetingRequest(recipient=recipient, message=message, include_timestamp=include_timestamp)
            return self.greeting_service.create_greeting(request)
        except GreetingError as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err)) from err

    def get_latest_greetings(self, limit: int = 5) -> list[GreetingResponse]:
        """Handle get latest greetings endpoint."""
        try:
            return self.greeting_service.get_latest_greetings(limit)
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(err)}") from err
