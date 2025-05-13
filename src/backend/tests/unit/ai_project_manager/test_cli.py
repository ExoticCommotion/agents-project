"""
Unit tests for the AI Project Manager CLI.
"""

import os
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from backend.app.cli import app


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner for testing."""
    return CliRunner()


def test_cli_exists() -> None:
    """Test that the CLI app exists."""
    assert app is not None


@patch.dict(os.environ, {"AIPM_TEST_MODE": "1"})
def test_process_goal_command(runner: CliRunner) -> None:
    """Test that the process-goal command works correctly."""
    result = runner.invoke(app, ["process-goal", "Test goal description"])

    assert result.exit_code == 0
    for field in ["proposal_id", "title", "description", "impact_areas", "implementation_steps"]:
        assert field in result.stdout


@patch.dict(os.environ, {"AIPM_TEST_MODE": "1"})
def test_process_goal_with_options(runner: CliRunner) -> None:
    """Test that the process-goal command works with additional options."""
    result = runner.invoke(
        app,
        [
            "process-goal",
            "Test goal description",
            "--title",
            "Test Title",
            "--context",
            "Test Context",
        ],
    )

    assert result.exit_code == 0
    for field in ["proposal_id", "title", "description"]:
        assert field in result.stdout


def test_process_goal_empty_description(runner: CliRunner) -> None:
    """Test that the process-goal command fails with an empty description."""
    result = runner.invoke(app, ["process-goal", ""])

    assert result.exit_code == 1
    assert "Error" in result.stdout
