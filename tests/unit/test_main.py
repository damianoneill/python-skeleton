"""Unit tests for the main module."""

from collections.abc import Callable

import pytest

from project_name.main import hello_world, run


@pytest.mark.unit
def test_hello_world_without_name():
    """Test that hello_world returns the default greeting when no name is provided."""
    result = hello_world()
    assert result == "Hello, World! Welcome to the project."
    assert "World" in result


@pytest.mark.unit
def test_hello_world_with_name():
    """Test that hello_world returns a personalized greeting when a name is provided."""
    name = "Alice"
    result = hello_world(name)
    assert result == f"Hello, {name}! Welcome to the project."
    assert name in result


@pytest.mark.unit
def test_run():
    """Test that the run function returns the expected greeting message."""
    result = run()
    assert result == "Hello, World! Welcome to the project."


@pytest.mark.unit
def test_hello_world_with_custom_format(greeting_format: str):
    """Test that hello_world works with a custom greeting format."""
    name = "Bob"
    result = hello_world(name, greeting_format)
    assert result == f"Greetings, {name}! Welcome to the project."
    assert name in result
    assert "Greetings" in result


@pytest.mark.unit
def test_with_custom_greeter(custom_greeter: Callable[[str], str]):
    """Test using the custom greeter fixture."""
    name = "Charlie"
    result = custom_greeter(name)
    assert result == f"Greetings, {name}! Welcome to the project."
    assert "Charlie" in result
