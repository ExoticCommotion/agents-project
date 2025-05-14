"""
Unit tests for the Planner Tool Agent.
"""

from backend.app.agents.planner_tool import PlannerTool
from backend.app.core.data_models import HighLevelGoal, StructuredPlan


def test_planner_tool_exists() -> None:
    """Test that the PlannerTool class exists."""
    assert PlannerTool is not None


def test_planner_tool_initialization() -> None:
    """Test that a PlannerTool can be initialized."""
    tool = PlannerTool()
    assert isinstance(tool, PlannerTool)


def test_create_plan() -> None:
    """Test that the create_plan method returns a StructuredPlan."""
    tool = PlannerTool()
    goal = HighLevelGoal(
        id="goal-123",
        title="Test Goal",
        description="This is a test goal",
        context="Test context",
    )

    plan = tool.create_plan(goal)

    assert isinstance(plan, StructuredPlan)
    assert plan.goal_id == goal.id
    assert plan.plan_id is not None
    assert plan.title is not None
    assert plan.description is not None
    assert len(plan.steps) > 0
    assert plan.estimated_complexity > 0
    assert plan.estimated_time is not None
