# src/project_name/domain/greeting/exceptions.py
class GreetingError(Exception):
    """Base exception for greeting-related errors."""

    pass


class InvalidRecipientError(GreetingError):
    """Exception raised when the recipient is invalid."""

    pass


class EmptyMessageError(GreetingError):
    """Exception raised when the greeting message is empty."""

    pass
