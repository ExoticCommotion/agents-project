"""
Unit tests for the Execution Coordinator Agent.
"""

from backend.app.core.data_models import DevinTicket, ExecutionResult
from backend.app.custom_agents.ai_project_manager.agents.execution_coordinator import (
    ExecutionCoordinatorAgent,
)


def test_execution_coordinator_agent_exists() -> None:
    """Test that the ExecutionCoordinatorAgent class exists."""
    assert ExecutionCoordinatorAgent is not None


def test_execution_coordinator_agent_initialization() -> None:
    """Test that an ExecutionCoordinatorAgent can be initialized."""
    agent = ExecutionCoordinatorAgent()
    assert isinstance(agent, ExecutionCoordinatorAgent)


def test_execute_ticket() -> None:
    """Test that the execute_ticket method returns an ExecutionResult."""
    agent = ExecutionCoordinatorAgent()
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

    result = agent.execute_ticket(ticket)

    assert isinstance(result, ExecutionResult)
    assert result.ticket_id == ticket.ticket_id
    assert result.status is not None
    assert result.output is not None
    assert result.execution_time is not None
