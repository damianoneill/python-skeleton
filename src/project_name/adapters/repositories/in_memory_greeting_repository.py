from project_name.domain.greeting.entities import Greeting


class InMemoryGreetingRepository:
    """In-memory implementation of the GreetingRepository interface."""

    def __init__(self) -> None:
        """Initialize the repository with empty storage."""
        self.greetings: dict[str, list[Greeting]] = {}
        self.all_greetings: list[Greeting] = []

    async def save(self, greeting: Greeting) -> None:
        """Save a greeting to the repository."""
        if greeting.recipient not in self.greetings:
            self.greetings[greeting.recipient] = []

        self.greetings[greeting.recipient].append(greeting)
        self.all_greetings.append(greeting)

    async def find_by_recipient(self, recipient: str) -> list[Greeting]:
        """Find greetings by recipient name."""
        return self.greetings.get(recipient, [])

    async def get_latest(self, limit: int = 5) -> list[Greeting]:
        """Get the latest greetings."""
        return sorted(self.all_greetings, key=lambda g: g.timestamp, reverse=True)[:limit]
