"""
Unit tests for the Task Definer Agent.
"""

from backend.app.core.data_models import DevinTicket, Epic, StructuredPlan
from backend.app.custom_agents.ai_project_manager.agents.task_definer import TaskDefinerAgent


def test_task_definer_agent_exists() -> None:
    """Test that the TaskDefinerAgent class exists."""
    assert TaskDefinerAgent is not None


def test_task_definer_agent_initialization() -> None:
    """Test that a TaskDefinerAgent can be initialized."""
    agent = TaskDefinerAgent()
    assert isinstance(agent, TaskDefinerAgent)


def test_create_epics() -> None:
    """Test that the create_epics method returns a list of Epics."""
    agent = TaskDefinerAgent()
    plan = StructuredPlan(
        goal_id="goal-123",
        plan_id="plan-456",
        title="Test Plan",
        description="This is a test plan",
        steps=["Step 1", "Step 2"],
        estimated_complexity=3,
        estimated_time="2 days",
    )

    epics = agent.create_epics(plan)

    assert isinstance(epics, list)
    assert len(epics) > 0
    assert isinstance(epics[0], Epic)
    assert epics[0].plan_id == plan.plan_id


def test_create_tickets() -> None:
    """Test that the create_tickets method returns a list of DevinTickets."""
    agent = TaskDefinerAgent()
    epic = Epic(
        epic_id="epic-789",
        plan_id="plan-456",
        title="Test Epic",
        description="This is a test epic",
        priority=1,
        status="pending",
    )

    tickets = agent.create_tickets(epic)

    assert isinstance(tickets, list)
    assert len(tickets) > 0
    assert isinstance(tickets[0], DevinTicket)
    assert tickets[0].epic_id == epic.epic_id
