"""
Unit tests for the Planner Agent.
"""

from backend.app.core.data_models import HighLevelGoal
from backend.app.custom_agents.ai_project_manager.agents.planner_tool import DecompositionPlan, PlannerTool
from backend.app.custom_agents.ai_project_manager.core.data_models import InitiativeGoal


def test_planner_agent_exists() -> None:
    """Test that the PlannerTool class exists."""
    assert PlannerTool is not None


def test_planner_agent_initialization() -> None:
    """Test that a PlannerTool can be initialized."""
    agent = PlannerTool()
    assert isinstance(agent, PlannerTool)


def test_create_plan() -> None:
    """Test that the plan_initiative method returns a DecompositionPlan."""
    agent = PlannerTool()
    goal = InitiativeGoal(
        id="goal-123",
        title="Test Goal",
        description="This is a test goal",
        context="Test context",
    )

    plan = agent.plan_initiative(goal)

    assert isinstance(plan, DecompositionPlan)
    assert plan.goal_id == goal.id
    assert plan.plan_id is not None
    assert plan.title is not None
    assert plan.description is not None
    assert len(plan.work_packages) > 0
    assert plan.estimated_complexity > 0
    assert plan.estimated_time is not None
