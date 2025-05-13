"""
Unit tests for the AI Project Manager Planner Tool Agent.
"""

from backend.app.custom_agents.ai_project_manager.agents.planner_tool import PlannerTool
from backend.app.custom_agents.ai_project_manager.core.data_models import (
    DecompositionPlan,
    InitiativeGoal,
    WorkPackage,
)


def test_planner_tool_exists() -> None:
    """Test that the PlannerTool class exists."""
    assert PlannerTool is not None


def test_planner_tool_initialization() -> None:
    """Test that a PlannerTool can be initialized."""
    tool = PlannerTool()
    assert isinstance(tool, PlannerTool)


def test_plan_initiative() -> None:
    """Test that the plan_initiative method returns a DecompositionPlan."""
    tool = PlannerTool()
    goal = InitiativeGoal(
        id="goal-123",
        title="Test Goal",
        description="This is a test goal",
        context="Test context",
    )

    plan = tool.plan_initiative(goal)

    assert isinstance(plan, DecompositionPlan)
    assert plan.goal_id == goal.id
    assert plan.plan_id is not None
    assert plan.title is not None
    assert plan.description is not None
    assert len(plan.work_packages) > 0
    assert all(isinstance(wp, WorkPackage) for wp in plan.work_packages)
    assert plan.estimated_complexity > 0
    assert plan.estimated_time is not None
