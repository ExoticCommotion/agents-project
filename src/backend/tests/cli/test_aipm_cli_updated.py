"""
Unit tests for the AI Project Manager CLI commands.
"""

from unittest.mock import patch

from typer.testing import CliRunner

from backend.app.cli import app
from backend.app.core.data_models import DevinTicket, InitiativeGoal
from backend.app.core.orchestration.project_orchestrator import ProjectOrchestrator

runner = CliRunner()


def test_aipm_process_initiative_empty_input() -> None:
    """Test that the command fails with an empty input."""
    result = runner.invoke(app, ["aipm-process-initiative", ""])
    assert result.exit_code == 1
    assert "Error: Initiative goal description cannot be empty" in result.stdout


@patch.object(ProjectOrchestrator, "process_initiative")
def test_aipm_process_initiative_success(mock_process_initiative) -> None:
    """Test that the command successfully processes an initiative goal."""
    mock_tickets = [
        DevinTicket(
            ticket_id="ticket-123",
            epic_id="epic-456",
            title="Test Ticket 1",
            description="This is a test ticket",
            input_files=["file1.py", "file2.py"],
            output_expectation="Expected output for test ticket",
            acceptance_criteria=["Criterion 1", "Criterion 2"],
            priority=1,
            status="ready",
        ),
        DevinTicket(
            ticket_id="ticket-456",
            epic_id="epic-456",
            title="Test Ticket 2",
            description="This is another test ticket",
            input_files=["file3.py"],
            output_expectation="Expected output for another test ticket",
            acceptance_criteria=["Criterion 3"],
            priority=2,
            status="ready",
        ),
    ]
    mock_process_initiative.return_value = mock_tickets

    result = runner.invoke(app, ["aipm-process-initiative", "Test initiative goal"])

    assert result.exit_code == 0

    mock_process_initiative.assert_called_once()
    args, _ = mock_process_initiative.call_args
    assert isinstance(args[0], InitiativeGoal)
    assert args[0].description == "Test initiative goal"

    assert "ticket-123" in result.stdout
    assert "Test Ticket 1" in result.stdout
    assert "ticket-456" in result.stdout
    assert "Test Ticket 2" in result.stdout


@patch.object(ProjectOrchestrator, "process_initiative")
def test_aipm_process_initiative_compact_output(mock_process_initiative) -> None:
    """Test that the command outputs compact JSON when requested."""
    mock_tickets = [
        DevinTicket(
            ticket_id="ticket-123",
            epic_id="epic-456",
            title="Test Ticket",
            description="This is a test ticket",
            input_files=["file1.py"],
            output_expectation="Expected output",
            acceptance_criteria=["Criterion 1"],
            priority=1,
            status="ready",
        ),
    ]
    mock_process_initiative.return_value = mock_tickets

    result = runner.invoke(app, ["aipm-process-initiative", "Test goal", "--compact"])

    assert result.exit_code == 0

    assert "  " not in result.stdout


@patch.object(ProjectOrchestrator, "process_initiative")
def test_aipm_process_initiative_error_handling(mock_process_initiative) -> None:
    """Test that the command handles errors properly."""
    mock_process_initiative.side_effect = ValueError("Test error")

    result = runner.invoke(app, ["aipm-process-initiative", "Test goal"])

    assert result.exit_code == 1
    assert "Error: Test error" in result.stdout
