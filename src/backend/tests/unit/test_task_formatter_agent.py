"""
Unit tests for the task_formatter_agent module.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.custom_agents.task_formatter_agent import (
    TaskDefinition,
    _parse_json_response,
    create_task_formatter_agent,
    format_task,
    format_task_sync,
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

    assert isinstance(result, dict)
    assert result["title"] == "Test Task"
    assert result["goal"] == "Implement a feature"
    assert result["input"] == "User input"
    assert result["output"] == "Expected output"
    assert result["verify"] == ["Test passes"]
    assert result["notes"] == ["Important note"]

    mock_runner.run.assert_called_once()
    args, kwargs = mock_runner.run.call_args
    assert kwargs["input"] == task_description


def test_format_task_sync(mock_runner, mock_agent):
    """Test formatting a task description synchronously."""
    task_description = "Create a Python module that does X and Y."
    result = format_task_sync(task_description)

    assert isinstance(result, dict)
    assert result["title"] == "Test Task"
    assert result["goal"] == "Implement a feature"
    assert result["input"] == "User input"
    assert result["output"] == "Expected output"
    assert result["verify"] == ["Test passes"]
    assert result["notes"] == ["Important note"]

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

    with pytest.raises(ValueError, match="Invalid JSON response from agent"):
        _parse_json_response(response)


@pytest.mark.asyncio
async def test_error_handling_in_format_task(mock_runner):
    """Test error handling in format_task method."""
    mock_runner.run.side_effect = Exception("API error")

    with pytest.raises(Exception, match="API error"):
        await format_task("Test task")


def test_error_handling_in_format_task_sync(mock_runner):
    """Test error handling in format_task_sync method."""
    mock_runner.run_sync.side_effect = Exception("API error")

    with pytest.raises(Exception, match="API error"):
        format_task_sync("Test task")


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
