"""Main module for the project_name package."""


def hello_world(name: str | None = None, greeting_format: str | None = None) -> str:
    """Return a greeting message.

    Args:
        name: Optional name to personalize the greeting
        greeting_format: Optional custom format for the greeting (must include '{}' placeholder)

    Returns:
        A greeting message
    """
    if greeting_format is None:
        greeting_format = "Hello, {}! Welcome to the project."

    recipient = name if name else "World"
    return greeting_format.format(recipient)


def run(name: str | None = None) -> str:
    """Run the main program logic.

    Args:
        name: Optional name to personalize the greeting

    Returns:
        The greeting message
    """
    return hello_world(name)


def main() -> int:
    """Entry point for the CLI command.

    Returns:
        Exit code
    """
    message = run()
    print(message)
    return 0


if __name__ == "__main__":
    exit(main())
