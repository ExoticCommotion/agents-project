"""
Unit tests for the Master Orchestrator Agent.
"""

from backend.app.core.data_models import DevinTicket, HighLevelGoal
from backend.app.core.master_orchestrator import MasterOrchestratorAgent


def test_master_orchestrator_agent_exists() -> None:
    """Test that the MasterOrchestratorAgent class exists."""
    assert MasterOrchestratorAgent is not None


def test_master_orchestrator_agent_initialization() -> None:
    """Test that a MasterOrchestratorAgent can be initialized."""
    agent = MasterOrchestratorAgent()
    assert isinstance(agent, MasterOrchestratorAgent)
    assert agent.planner_tool is not None
    assert agent.detailer_tool is not None


def test_process_initiative() -> None:
    """Test that the process_initiative method returns a list of DevinTickets."""
    agent = MasterOrchestratorAgent()
    goal = HighLevelGoal(
        id="goal-123",
        title="Test Initiative",
        description="This is a test initiative",
        context="Test context",
    )

    tickets = agent.process_initiative(goal)

    assert isinstance(tickets, list)
    assert len(tickets) > 0
    assert all(isinstance(ticket, DevinTicket) for ticket in tickets)
    assert len(tickets) == len(agent.planner_tool.create_plan(goal).steps)
