# Contributing Guide

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Development Environment

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) (recommended package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/project_name.git
cd project_name

# Install development dependencies
make install-dev
```

### Development Workflow

The project uses a Makefile to streamline common development tasks:

```bash
# Show all available commands
make help

# Install development dependencies
make install-dev

# Run code formatting
make format

# Run linting
make lint

# Run tests
make test

# Run tests with coverage
make test-cov

# Run all checks (formatting, linting, tests)
make check
```

## Code Structure

The project follows Clean Architecture principles with these layers:

1. **Domain Layer**: Core business logic and entities
2. **Use Case Layer**: Application-specific business rules
3. **Adapter Layer**: Interface between domain and external systems
4. **Infrastructure Layer**: Implementation details for external systems

## Coding Standards

- Follow PEP 8 guidelines as enforced by Ruff
- Write tests for all new functionality
- Add type annotations to all functions and methods
- Use docstrings for all modules, classes, and methods
- Follow the Arrange-Act-Assert pattern for tests

## Pull Request Process

1. Fork the repository and create a feature branch
2. Ensure all tests pass with `make test`
3. Ensure code is properly formatted with `make format`
4. Submit a pull request with a clear description of the changes

## Commit Guidelines

- Use descriptive commit messages
- Reference issue numbers when relevant
- Follow the conventional commits format:
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation changes
  - `refactor`: Code refactoring
  - `test`: Add or update tests
  - `chore`: Maintenance tasks

## Help and Questions

If you have questions about the project or need assistance, please open an issue on the GitHub repository.
