"""
Tests for the tools.py module.

This module contains tests for the tool-using agent implementation.
"""

from unittest.mock import AsyncMock, patch

import pytest
from agents import Agent

from backend.app.custom_agents.tools import (
    create_tool_using_agent,
    get_current_time,
    get_current_weather,
    run_tool_using_agent,
    run_tool_using_sync,
)


def test_get_current_weather_tool():
    """Test that the get_current_weather function is properly decorated as a function tool."""
    from agents.tool import FunctionTool

    assert isinstance(get_current_weather, FunctionTool)
    assert get_current_weather.name == "get_current_weather"
    assert "location" in get_current_weather.description


def test_get_current_time_tool():
    """Test that the get_current_time function is properly decorated as a function tool."""
    from agents.tool import FunctionTool

    assert isinstance(get_current_time, FunctionTool)
    assert get_current_time.name == "get_current_time"
    assert "timezone" in get_current_time.description


def test_create_tool_using_agent():
    """Test that the tool-using agent can be created."""
    agent = create_tool_using_agent()
    assert isinstance(agent, Agent)
    assert agent.name == "ToolUsingAgent"
    assert "tools" in agent.instructions
    assert len(agent.tools) == 2


@pytest.mark.asyncio
async def test_run_tool_using_agent():
    """Test that the tool-using agent can be run asynchronously."""
    with patch("agents.Runner.run", new_callable=AsyncMock) as mock_run:
        mock_result = AsyncMock()
        mock_result.final_output = "The weather in San Francisco is 22°C and sunny with wind."
        mock_run.return_value = mock_result

        result = await run_tool_using_agent("What's the weather in San Francisco?")

        assert result == "The weather in San Francisco is 22°C and sunny with wind."
        mock_run.assert_called_once()


def test_run_tool_using_sync():
    """Test that the tool-using agent can be run synchronously."""
    with patch("agents.Runner.run_sync") as mock_run_sync:
        mock_result = mock_run_sync.return_value
        mock_result.final_output = "The current time in New York is 12:00 PM on 2025-05-11."

        result = run_tool_using_sync("What time is it in New York?")

        assert result == "The current time in New York is 12:00 PM on 2025-05-11."
        mock_run_sync.assert_called_once()
