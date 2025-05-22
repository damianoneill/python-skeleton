# src/project_name/domain/greeting/entities.py
from datetime import datetime


class Greeting:
    """Domain entity representing a greeting message."""

    def __init__(self, message: str, recipient: str, timestamp: datetime | None = None) -> None:
        self.message = message
        self.recipient = recipient
        self.timestamp = timestamp or datetime.now()

    def format_greeting(self) -> str:
        """Format the greeting message with the recipient name."""
        return f"{self.message}, {self.recipient}!"

    def format_with_timestamp(self) -> str:
        """Format the greeting with timestamp."""
        formatted_time = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.format_greeting()} The time is {formatted_time}."
