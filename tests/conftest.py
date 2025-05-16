"""Shared fixtures for all tests."""

import os
import sys
from collections.abc import Callable

import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


@pytest.fixture
def greeting_format() -> str:
    """Provide a custom greeting format for testing."""
    return "Greetings, {}! Welcome to the project."


@pytest.fixture
def custom_greeter(greeting_format: str) -> Callable[[str], str]:
    """Provide a function that creates custom greetings."""

    def _greeter(name: str) -> str:
        return greeting_format.format(name)

    return _greeter
