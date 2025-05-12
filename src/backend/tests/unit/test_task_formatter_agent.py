"""
Unit tests for the task_formatter_agent module.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from agents.exceptions import AgentsException

from backend.app.custom_agents.task_formatter_agent import (
    ParsingError,
    TaskDefinition,
    TaskFormatterErrorType,
    TaskFormatterResponse,
    ValidationError,
    _parse_json_response,
    create_task_formatter_agent,
    format_task,
    format_task_sync,
    validate_task_description,
)


class MockRunnerResult:
    """Mock for Runner.run result."""

    def __init__(self, final_output):
        self.final_output = final_output


@pytest.fixture
def mock_runner():
    """Fixture to mock the Runner from agents SDK."""
    with patch("backend.app.custom_agents.task_formatter_agent.Runner") as mock_runner:
        mock_runner.run = AsyncMock()
        mock_runner.run.return_value = MockRunnerResult(
            json.dumps(
                {
                    "title": "Test Task",
                    "goal": "Implement a feature",
                    "input": "User input",
                    "output": "Expected output",
                    "verify": ["Test passes"],
                    "notes": ["Important note"],
                }
            )
        )

        mock_runner.run_sync = MagicMock()
        mock_runner.run_sync.return_value = MockRunnerResult(
            json.dumps(
                {
                    "title": "Test Task",
                    "goal": "Implement a feature",
                    "input": "User input",
                    "output": "Expected output",
                    "verify": ["Test passes"],
                    "notes": ["Important note"],
                }
            )
        )

        yield mock_runner


@pytest.fixture
def mock_agent():
    """Fixture to mock the Agent from agents SDK."""
    with patch("backend.app.custom_agents.task_formatter_agent.Agent") as mock_agent_class:
        mock_agent_instance = MagicMock()
        mock_agent_class.return_value = mock_agent_instance
        yield mock_agent_class


def test_create_task_formatter_agent(mock_agent):
    """Test creating a task formatter agent."""
    create_task_formatter_agent()

    mock_agent.assert_called_once()
    call_kwargs = mock_agent.call_args.kwargs
    assert call_kwargs["name"] == "TaskFormatter"
    assert "instructions" in call_kwargs
    assert call_kwargs["model"] == "gpt-4o"


@pytest.mark.asyncio
async def test_format_task(mock_runner, mock_agent):
    """Test formatting a task description asynchronously."""
    task_description = "Create a Python module that does X and Y."
    result = await format_task(task_description)

    assert isinstance(result, TaskFormatterResponse)
    assert result.success is True
    assert result.error is None
    assert isinstance(result.data, dict)
    assert result.data["title"] == "Test Task"
    assert result.data["goal"] == "Implement a feature"
    assert result.data["input"] == "User input"
    assert result.data["output"] == "Expected output"
    assert result.data["verify"] == ["Test passes"]
    assert result.data["notes"] == ["Important note"]

    mock_runner.run.assert_called_once()
    args, kwargs = mock_runner.run.call_args
    assert kwargs["input"] == task_description


def test_format_task_sync(mock_runner, mock_agent):
    """Test formatting a task description synchronously."""
    task_description = "Create a Python module that does X and Y."
    result = format_task_sync(task_description)

    assert isinstance(result, TaskFormatterResponse)
    assert result.success is True
    assert result.error is None
    assert isinstance(result.data, dict)
    assert result.data["title"] == "Test Task"
    assert result.data["goal"] == "Implement a feature"
    assert result.data["input"] == "User input"
    assert result.data["output"] == "Expected output"
    assert result.data["verify"] == ["Test passes"]
    assert result.data["notes"] == ["Important note"]

    mock_runner.run_sync.assert_called_once()
    args, kwargs = mock_runner.run_sync.call_args
    assert kwargs["input"] == task_description


def test_parse_json_response_with_code_block():
    """Test parsing JSON response with markdown code blocks."""
    response = """```json
    {
        "title": "Test Task",
        "goal": "Implement a feature",
        "input": "User input",
        "output": "Expected output",
        "verify": ["Test passes"],
        "notes": ["Important note"]
    }
    ```"""

    result = _parse_json_response(response)
    assert result["title"] == "Test Task"
    assert result["goal"] == "Implement a feature"


def test_parse_json_response_with_invalid_json():
    """Test parsing invalid JSON response."""
    response = "This is not valid JSON"

    with pytest.raises(ParsingError, match="Invalid JSON response from agent"):
        _parse_json_response(response)


def test_parse_json_response_with_empty_response():
    """Test parsing empty response."""
    response = ""

    with pytest.raises(ParsingError, match="Empty response from agent"):
        _parse_json_response(response)


def test_parse_json_response_with_missing_fields():
    """Test parsing JSON response with missing required fields."""
    response = """{"title": "Test Task", "goal": "Implement a feature"}"""

    with pytest.raises(ParsingError, match="Missing required fields"):
        _parse_json_response(response)


@pytest.mark.asyncio
async def test_error_handling_in_format_task(mock_runner):
    """Test error handling in format_task method."""
    mock_runner.run.side_effect = AgentsException("API error")

    result = await format_task("This is a valid task description with sufficient length.")

    assert isinstance(result, TaskFormatterResponse)
    assert result.success is False
    assert result.data is None
    assert result.error is not None
    assert result.error["type"] == TaskFormatterErrorType.API_ERROR
    assert "API error" in result.error["message"]


def test_error_handling_in_format_task_sync(mock_runner):
    """Test error handling in format_task_sync method."""
    mock_runner.run_sync.side_effect = AgentsException("API error")

    result = format_task_sync("This is a valid task description with sufficient length.")

    assert isinstance(result, TaskFormatterResponse)
    assert result.success is False
    assert result.data is None
    assert result.error is not None
    assert result.error["type"] == TaskFormatterErrorType.API_ERROR
    assert "API error" in result.error["message"]


@pytest.mark.asyncio
async def test_rate_limit_error_handling(mock_runner):
    """Test rate limit error handling in format_task method."""
    mock_runner.run.side_effect = AgentsException("Rate limit exceeded")

    result = await format_task("This is a valid task description with sufficient length.")

    assert isinstance(result, TaskFormatterResponse)
    assert result.success is False
    assert result.data is None
    assert result.error is not None
    assert result.error["type"] == TaskFormatterErrorType.RATE_LIMIT_ERROR
    assert "Rate limit" in result.error["message"]


@pytest.mark.asyncio
async def test_authentication_error_handling(mock_runner):
    """Test authentication error handling in format_task method."""
    error = AgentsException("Authentication failed: 401 Unauthorized")
    mock_runner.run.side_effect = error

    result = await format_task("This is a valid task description with sufficient length.")

    assert isinstance(result, TaskFormatterResponse)
    assert result.success is False
    assert result.data is None
    assert result.error is not None
    assert result.error["type"] == TaskFormatterErrorType.AUTHENTICATION_ERROR
    assert "Authentication" in result.error["message"] or "API error" in result.error["message"]


def test_task_definition_model():
    """Test the TaskDefinition model."""
    task = TaskDefinition(
        title="Test Task",
        goal="Implement a feature",
        input="User input",
        output="Expected output",
        verify=["Test passes"],
        notes=["Important note"],
    )

    assert task.title == "Test Task"
    assert task.goal == "Implement a feature"
    assert task.input == "User input"
    assert task.output == "Expected output"
    assert task.verify == ["Test passes"]
    assert task.notes == ["Important note"]


def test_validate_task_description_empty():
    """Test validation of empty task description."""
    with pytest.raises(ValidationError, match="Task description cannot be empty"):
        validate_task_description("")


def test_validate_task_description_too_short():
    """Test validation of too short task description."""
    with pytest.raises(ValidationError, match="Task description is too short"):
        validate_task_description("Short")


def test_validate_task_description_too_long():
    """Test validation of too long task description."""
    long_description = "x" * 9000

    with pytest.raises(ValidationError, match="Task description is too long"):
        validate_task_description(long_description)


def test_validate_task_description_valid():
    """Test validation of valid task description."""
    validate_task_description("This is a valid task description with sufficient length.")


def test_task_formatter_response_model():
    """Test the TaskFormatterResponse model."""
    success_response = TaskFormatterResponse(
        success=True, data={"title": "Test Task", "goal": "Test Goal"}
    )
    assert success_response.success is True
    assert success_response.data == {"title": "Test Task", "goal": "Test Goal"}
    assert success_response.error is None

    error_response = TaskFormatterResponse(
        success=False,
        error={
            "type": TaskFormatterErrorType.VALIDATION_ERROR,
            "message": "Validation failed",
            "details": {"field": "task_description"},
        },
    )
    assert error_response.success is False
    assert error_response.data is None
    assert error_response.error["type"] == TaskFormatterErrorType.VALIDATION_ERROR
    assert error_response.error["message"] == "Validation failed"
