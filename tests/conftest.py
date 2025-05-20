"""Shared fixtures for all tests."""

import os
import sys

import pytest
from fastapi.testclient import TestClient

from project_name.main import app

pytest_plugins = ["pytest_asyncio"]

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


@pytest.fixture
def client() -> TestClient:
    """Provide a FastAPI test client."""
    return TestClient(app)
