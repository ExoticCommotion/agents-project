"""
Unit tests for the Devin Session Manager.
"""

import re

from backend.app.core.data_models import DevinTicket, ExecutionResult
from backend.app.tools.devin_session_manager import DevinSessionManager


def test_devin_session_manager_exists() -> None:
    """Test that the DevinSessionManager class exists."""
    assert DevinSessionManager is not None


def test_devin_session_manager_initialization() -> None:
    """Test that a DevinSessionManager can be initialized."""
    manager = DevinSessionManager()
    assert isinstance(manager, DevinSessionManager)


def test_create_session() -> None:
    """Test that the create_session method returns a session ID."""
    manager = DevinSessionManager()
    ticket = DevinTicket(
        ticket_id="ticket-101",
        epic_id="epic-789",
        title="Test Ticket",
        description="This is a test ticket",
        input_files=["file1.py", "file2.py"],
        output_expectation="Expected output",
        acceptance_criteria=["Criteria 1", "Criteria 2"],
        priority=2,
        status="ready",
    )

    session_id = manager.create_session(ticket)

    assert isinstance(session_id, str)
    assert len(session_id) > 0
    assert session_id.startswith("session-")
    assert re.match(r"session-\d+", session_id) is not None


def test_get_session_result() -> None:
    """Test that the get_session_result method returns an ExecutionResult."""
    manager = DevinSessionManager()
    session_id = "session-placeholder"

    result = manager.get_session_result(session_id)

    assert isinstance(result, ExecutionResult)
    assert result.ticket_id is not None
    assert result.status is not None
    assert result.output is not None
    assert result.execution_time is not None
    assert result.status == "completed"
    assert result.output == "Execution output"
    assert result.execution_time == "2 hours"
