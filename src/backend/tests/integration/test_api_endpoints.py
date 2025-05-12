"""
Integration tests for the API endpoints.

This module contains tests for the FastAPI endpoints.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel

from backend.app.custom_agents.task_formatter_agent import TaskFormatterResponse
from backend.app.main import app


class MockTaskFormatterResponse(BaseModel):
    """Mock response for task formatter."""

    success: bool
    data: dict | None = None
    error: dict | None = None


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_successful_response():
    """Create a mock successful response from the task formatter."""
    return TaskFormatterResponse(
        success=True,
        data={
            "title": "Test Module",
            "goal": "Create a test module for testing",
            "input": "Test input",
            "output": "Test output",
            "verify": ["Test verification"],
            "notes": ["Test note"],
        },
    )


@pytest.fixture
def mock_validation_error_response():
    """Create a mock validation error response from the task formatter."""
    return TaskFormatterResponse(
        success=False,
        error={
            "type": "validation_error",
            "message": "Task description is too short",
            "details": {"min_length": 10, "actual_length": 5},
        },
    )


@pytest.fixture
def mock_api_error_response():
    """Create a mock API error response from the task formatter."""
    return TaskFormatterResponse(
        success=False,
        error={
            "type": "api_error",
            "message": "OpenAI API error: Something went wrong",
            "details": {"original_error": "Something went wrong"},
        },
    )


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("backend.app.main.format_task")
def test_format_task_success(mock_format_task, client, mock_successful_response):
    """Test the format-task endpoint with a successful response."""
    mock_format_task.return_value = mock_successful_response

    response = client.post(
        "/format-task/",
        json={"task_description": "Create a Python module that does X and Y."},
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {
            "title": "Test Module",
            "goal": "Create a test module for testing",
            "input": "Test input",
            "output": "Test output",
            "verify": ["Test verification"],
            "notes": ["Test note"],
        },
    }
    mock_format_task.assert_called_once_with("Create a Python module that does X and Y.")


@patch("backend.app.main.format_task")
def test_format_task_validation_error(mock_format_task, client, mock_validation_error_response):
    """Test the format-task endpoint with a validation error response."""
    mock_format_task.return_value = mock_validation_error_response

    response = client.post("/format-task/", json={"task_description": "Short"})

    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "Task description is too short",
                "details": {"min_length": 10, "actual_length": 5},
            },
        }
    }
    mock_format_task.assert_called_once_with("Short")


@patch("backend.app.main.format_task")
def test_format_task_api_error(mock_format_task, client, mock_api_error_response):
    """Test the format-task endpoint with an API error response."""
    mock_format_task.return_value = mock_api_error_response

    response = client.post(
        "/format-task/",
        json={"task_description": "Create a Python module that does X and Y."},
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": {
            "success": False,
            "error": {
                "type": "api_error",
                "message": "OpenAI API error: Something went wrong",
                "details": {"original_error": "Something went wrong"},
            },
        }
    }
    mock_format_task.assert_called_once_with("Create a Python module that does X and Y.")


def test_format_task_missing_description(client):
    """Test the format-task endpoint with a missing task description."""
    response = client.post("/format-task/", json={})
    assert response.status_code == 422  # Unprocessable Entity


def test_format_task_empty_description(client):
    """Test the format-task endpoint with an empty task description."""
    response = client.post("/format-task/", json={"task_description": ""})
    assert response.status_code == 400  # Bad Request
