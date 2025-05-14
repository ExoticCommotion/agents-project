"""
Unit tests for the Master Orchestrator Agent.
"""

from backend.app.core.data_models import DevinTicket
from backend.app.custom_agents.ai_project_manager.core.data_models import (
    InitiativeGoal,
)
from backend.app.custom_agents.ai_project_manager.core.master_orchestrator import (
    MasterOrchestratorAgent,
)


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
    goal = InitiativeGoal(
        id="goal-123",
        title="Test Initiative",
        description="This is a test initiative",
        context="Test context",
    )

    tickets = agent.process_initiative(goal)

    assert isinstance(tickets, list)
    assert len(tickets) > 0
    assert all(isinstance(ticket, DevinTicket) for ticket in tickets)

    plan = agent.planner_tool.plan_initiative(goal)
    expected_ticket_count = sum(len(wp.tasks) for wp in plan.work_packages)
    assert len(tickets) == expected_ticket_count
