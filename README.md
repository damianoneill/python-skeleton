# Project Name

A Python project template following clean architecture principles.

## Overview

This project follows a structured approach to software development with:

- Clean Architecture principles
- Domain-Driven Design
- Modular component design
- Comprehensive testing

## Features

- **Modern Python**: Requires Python 3.11+
- **Clean Architecture**: Structured layers with clear boundaries
- **Test-Driven**: Comprehensive test suite with pytest
- **Quality Tools**: Ruff for linting and formatting
- **CI/CD Ready**: GitHub Actions workflows included

## Project Structure

```
src/
├── domain/       # Core business logic and entities
├── use_cases/    # Application business logic
├── adapters/     # Interface adapters
└── infrastructure/ # Implementation details
```

## Clean Architecture

This project follows Clean Architecture principles, organising code into four concentric layers with dependencies pointing inward.

### Layer Structure

1. **[Domain Layer](./src/project_name/domain/README.md)** (Innermost)
   - Contains business entities and core logic
   - Independent of frameworks, databases, and external services
   - Location: `src/project_name/domain/`

2. **[Use Case Layer](./src/project_name/use_cases/README.md)**
   - Orchestrates domain objects to fulfill application flows
   - Defines boundaries between external world and domain
   - Location: `src/project_name/use_cases/`

3. **[Adapter Layer](./src/project_name/adapters/README.md)**
   - Converts between external formats and internal models
   - Transforms API requests into use case inputs and vice versa
   - Location: `src/project_name/adapters/`

4. **[Infrastructure Layer](./src/project_name/infrastructure/README.md)** (Outermost)
   - Implements technical details for external interactions
   - Contains database connections, API clients, and frameworks
   - Location: `src/project_name/infrastructure/`

### Key Principles

- Dependencies always point inward
- Inner layers define interfaces that outer layers implement
- Business rules remain isolated from delivery mechanisms
- The system becomes testable and adaptable to change

### Application Flow Example

For a REST API that processes requests and interacts with external systems:

1. **Request Received**:
   - Infrastructure layer (FastAPI) receives HTTP request
   - Request is passed to adapter layer

2. **Request Processing**:
   - Adapter layer converts HTTP request to use case input
   - Use case orchestrates domain entities and business logic
   - Domain layer enforces core business rules

3. **External Interactions**:
   - Domain layer defines repository interfaces
   - Adapter layer implements these interfaces
   - Infrastructure layer handles database and API connections

4. **Response Delivery**:
   - Results flow back through layers
   - Use case assembles response data
   - Adapter layer formats response for HTTP
   - Infrastructure layer delivers HTTP response

You can find more details about this architecture in the [Architecture Document](docs/ARCHITECTURE.md).

## Development

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/project_name.git
cd project_name

# Install dependencies
make install-dev
```

### Common Tasks

Use the Makefile for common development tasks:

```bash
# Show all available commands
make help

# Run tests
make test

# Run linting and formatting
make lint
make format

# Run all checks
make check
```

## License

[MIT](LICENSE)
