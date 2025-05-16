"""Unit tests for the API endpoints."""

import pytest
from fastapi.testclient import TestClient

# No need to define the client fixture here as it's now in conftest.py


@pytest.mark.unit
def test_get_greeting_without_params(client: TestClient) -> None:
    """Test the greeting endpoint with default parameters."""
    response = client.get("/api/greetings/World")
    assert response.status_code == 200
    data = response.json()
    assert data["greeting"] == "Hello, World!"
    assert data["recipient"] == "World"
    assert data["timestamp"] is None


@pytest.mark.unit
def test_get_greeting_with_name(client: TestClient) -> None:
    """Test the greeting endpoint with a custom name."""
    name = "Alice"
    response = client.get(f"/api/greetings/{name}")
    assert response.status_code == 200
    data = response.json()
    assert data["greeting"] == f"Hello, {name}!"
    assert data["recipient"] == name
    assert data["timestamp"] is None


@pytest.mark.unit
def test_get_greeting_with_custom_message(client: TestClient) -> None:
    """Test the greeting endpoint with a custom message."""
    name = "Bob"
    message = "Greetings"
    response = client.get(f"/api/greetings/{name}?message={message}")
    assert response.status_code == 200
    data = response.json()
    assert data["greeting"] == f"{message}, {name}!"
    assert data["recipient"] == name
    assert data["timestamp"] is None


@pytest.mark.unit
def test_get_greeting_with_timestamp(client: TestClient) -> None:
    """Test the greeting endpoint with timestamp included."""
    name = "Charlie"
    response = client.get(f"/api/greetings/{name}?include_timestamp=true")
    assert response.status_code == 200
    data = response.json()
    assert data["greeting"].startswith(f"Hello, {name}!")
    assert "The time is" in data["greeting"]
    assert data["recipient"] == name
    assert data["timestamp"] is not None


@pytest.mark.unit
def test_get_latest_greetings(client: TestClient) -> None:
    """Test the latest greetings endpoint."""
    # First create some greetings
    client.get("/api/greetings/Alice")
    client.get("/api/greetings/Bob")
    client.get("/api/greetings/Charlie")

    # Then get the latest greetings
    response = client.get("/api/greetings")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3

    # Check that the latest greetings include the ones we just created
    recipients = [item["recipient"] for item in data]
    assert "Alice" in recipients
    assert "Bob" in recipients
    assert "Charlie" in recipients


@pytest.mark.unit
def test_get_latest_greetings_with_limit(client: TestClient) -> None:
    """Test the latest greetings endpoint with a custom limit."""
    # First create some greetings
    client.get("/api/greetings/David")
    client.get("/api/greetings/Eve")
    client.get("/api/greetings/Frank")
    client.get("/api/greetings/Grace")

    # Then get the latest greetings with a limit of 2
    response = client.get("/api/greetings?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
