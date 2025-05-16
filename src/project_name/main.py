"""Main module for the project_name package."""

import uvicorn

from project_name.infrastructure.api.app import create_app
from project_name.infrastructure.config.settings import settings

# FastAPI application instance
app = create_app()


def run(host: str = settings.host, port: int = settings.port) -> None:
    """Run the FastAPI application.

    Args:
        host: Host address to bind the server to.
             Default is localhost (127.0.0.1) for security.
             Set environment variable API_HOST="0.0.0.0" to bind to all interfaces.
        port: Port to bind the server to
    """
    uvicorn.run(app, host=host, port=port, reload=settings.debug)


def main() -> int:
    """Entry point for the CLI command.

    Returns:
        Exit code
    """
    run()
    return 0


if __name__ == "__main__":
    exit(main())
