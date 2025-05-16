# src/project_name/use_cases/greeting/service.py

from project_name.domain.greeting.entities import Greeting
from project_name.domain.greeting.exceptions import EmptyMessageError, InvalidRecipientError
from project_name.domain.greeting.repositories import GreetingRepository
from project_name.use_cases.greeting.dtos import GreetingRequest, GreetingResponse


class GreetingService:
    """Service implementing greeting-related use cases."""

    def __init__(self, greeting_repository: GreetingRepository):
        self.greeting_repository = greeting_repository

    def create_greeting(self, request: GreetingRequest) -> GreetingResponse:
        """Create a new greeting."""
        # Domain validation
        if not request.recipient:
            raise InvalidRecipientError("Recipient is required")

        if not request.message:
            raise EmptyMessageError("Message cannot be empty")

        # Create domain entity
        greeting = Greeting(message=request.message, recipient=request.recipient)

        # Save to repository
        self.greeting_repository.save(greeting)

        # Transform to response DTO
        formatted_message = (
            greeting.format_with_timestamp() if request.include_timestamp else greeting.format_greeting()
        )

        return GreetingResponse(
            greeting=formatted_message,
            recipient=greeting.recipient,
            timestamp=greeting.timestamp if request.include_timestamp else None,
        )

    def get_latest_greetings(self, limit: int = 5) -> list[GreetingResponse]:
        """Get the latest greetings."""
        greetings = self.greeting_repository.get_latest(limit)

        return [
            GreetingResponse(greeting=g.format_greeting(), recipient=g.recipient, timestamp=g.timestamp)
            for g in greetings
        ]
