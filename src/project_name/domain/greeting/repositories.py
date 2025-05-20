# src/project_name/domain/greeting/repositories.py
from typing import Protocol

from project_name.domain.greeting.entities import Greeting


class GreetingRepository(Protocol):
    """Repository interface for greeting operations."""

    async def save(self, greeting: Greeting) -> None:
        """Save a greeting to the repository."""
        ...

    async def find_by_recipient(self, recipient: str) -> list[Greeting]:
        """Find greetings by recipient name."""
        ...

    async def get_latest(self, limit: int = 5) -> list[Greeting]:
        """Get the latest greetings."""
        ...
