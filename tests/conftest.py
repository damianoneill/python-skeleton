"""Shared fixtures for all tests."""

import os
import sys

import pytest
from fastapi.testclient import TestClient

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from project_name.main import app


@pytest.fixture
def client() -> TestClient:
    """Provide a FastAPI test client."""
    return TestClient(app)
