"""
Unit tests for the Planner Agent.
"""

from backend.app.custom_agents.ai_project_manager.agents.planner import PlannerAgent
from backend.app.custom_agents.ai_project_manager.core.data_models import (
    DecompositionPlan,
    InitiativeGoal,
)


def test_planner_agent_exists() -> None:
    """Test that the PlannerAgent class exists."""
    assert PlannerAgent is not None


def test_planner_agent_initialization() -> None:
    """Test that a PlannerAgent can be initialized."""
    agent = PlannerAgent()
    assert isinstance(agent, PlannerAgent)


def test_create_plan() -> None:
    """Test that the create_plan method returns a DecompositionPlan."""
    agent = PlannerAgent()
    goal = InitiativeGoal(
        id="goal-123",
        title="Test Goal",
        description="This is a test goal",
        context="Test context",
    )

    plan = agent.create_plan(goal)

    assert isinstance(plan, DecompositionPlan)
    assert plan.goal_id == goal.id
    assert plan.plan_id is not None
    assert plan.title is not None
    assert plan.description is not None
    assert len(plan.work_packages) > 0
    assert plan.estimated_complexity > 0
    assert plan.estimated_time is not None
