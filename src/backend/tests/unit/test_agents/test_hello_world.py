"""
Tests for the hello_world.py module.

This module contains tests for the hello world agent implementation.
"""

import pytest
from unittest.mock import AsyncMock, patch

from agents import Agent
from backend.app.custom_agents.hello_world import (
    create_hello_world_agent,
    run_hello_world_agent,
    run_hello_world_sync,
)


def test_create_hello_world_agent():
    """Test that the hello world agent can be created."""
    agent = create_hello_world_agent()
    assert isinstance(agent, Agent)
    assert agent.name == "HelloWorld"
    assert "haikus" in agent.instructions


@pytest.mark.asyncio
async def test_run_hello_world_agent():
    """Test that the hello world agent can be run asynchronously."""
    with patch("agents.Runner.run", new_callable=AsyncMock) as mock_run:
        mock_result = AsyncMock()
        mock_result.final_output = "AI in three lines,\nThinking without a body,\nHuman's creation."
        mock_run.return_value = mock_result

        result = await run_hello_world_agent("Tell me about AI")

        assert result == "AI in three lines,\nThinking without a body,\nHuman's creation."
        mock_run.assert_called_once()


def test_run_hello_world_sync():
    """Test that the hello world agent can be run synchronously."""
    with patch("agents.Runner.run_sync") as mock_run_sync:
        mock_result = mock_run_sync.return_value
        mock_result.final_output = (
            "Code flows like stream,\nBugs hide in dark corners wait,\nDebugger reveals."
        )

        result = run_hello_world_sync("Tell me about programming")

        assert (
            result == "Code flows like stream,\nBugs hide in dark corners wait,\nDebugger reveals."
        )
        mock_run_sync.assert_called_once()
