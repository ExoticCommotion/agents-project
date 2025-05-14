"""
Unit tests for the Prioritizer Agent.
"""

from backend.app.core.data_models import DevinTicket
from backend.app.custom_agents.ai_project_manager.agents.prioritizer import PrioritizerAgent


def test_prioritizer_agent_exists() -> None:
    """Test that the PrioritizerAgent class exists."""
    assert PrioritizerAgent is not None


def test_prioritizer_agent_initialization() -> None:
    """Test that a PrioritizerAgent can be initialized."""
    agent = PrioritizerAgent()
    assert isinstance(agent, PrioritizerAgent)


def test_prioritize_tickets() -> None:
    """Test that the prioritize_tickets method returns a prioritized list of tickets."""
    agent = PrioritizerAgent()
    tickets = [
        DevinTicket(
            ticket_id="ticket-1",
            epic_id="epic-1",
            title="Test Ticket 1",
            description="This is test ticket 1",
            input_files=["file1.py"],
            output_expectation="Expected output 1",
            acceptance_criteria=["Criteria 1"],
            priority=2,
            status="ready",
        ),
        DevinTicket(
            ticket_id="ticket-2",
            epic_id="epic-1",
            title="Test Ticket 2",
            description="This is test ticket 2",
            input_files=["file2.py"],
            output_expectation="Expected output 2",
            acceptance_criteria=["Criteria 2"],
            priority=1,
            status="ready",
        ),
    ]

    prioritized_tickets = agent.prioritize_tickets(tickets)

    assert isinstance(prioritized_tickets, list)
    assert len(prioritized_tickets) == len(tickets)
    assert all(isinstance(ticket, DevinTicket) for ticket in prioritized_tickets)
