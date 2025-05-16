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
