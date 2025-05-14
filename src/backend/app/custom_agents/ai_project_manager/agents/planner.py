"""
Planner Agent for the AI Project Manager.

This module defines the Planner Agent, which is responsible for creating decomposition plans
from initiative goals.
"""

from backend.app.custom_agents.ai_project_manager.core.data_models import (
    DecompositionPlan,
    InitiativeGoal,
    WorkPackage,
)
from backend.app.utils.logger import get_logger

__all__ = ["PlannerAgent", "DecompositionPlan"]

logger = get_logger(__name__)


class PlannerAgent:
    """
    Agent responsible for creating decomposition plans from initiative goals.

    The Planner Agent takes an initiative goal and breaks it down into a decomposition plan
    with work packages, complexity estimates, and time estimates.
    """

    def __init__(self) -> None:
        """Initialize the Planner Agent."""
        logger.info("Initializing Planner Agent")

    def create_plan(self, goal: InitiativeGoal) -> DecompositionPlan:
        """
        Create a decomposition plan from an initiative goal.

        Args:
            goal: The initiative goal to plan for

        Returns:
            A decomposition plan with work packages, complexity estimates, and time estimates
        """
        logger.info(f"Creating plan for goal: {goal.title}")

        work_package = WorkPackage(
            package_id=f"package-{hash(goal.id) % 10000}",
            plan_id=f"plan-{hash(goal.id) % 10000}",
            title=f"Work Package for {goal.title}",
            description=f"Work package derived from goal: {goal.description}",
            tasks=["Task 1: Placeholder", "Task 2: Placeholder"],
            estimated_complexity=2,
            estimated_time="2 days",
        )

        return DecompositionPlan(
            goal_id=goal.id,
            plan_id=f"plan-{hash(goal.id) % 10000}",
            title=f"Plan for {goal.title}",
            description=f"Decomposition plan derived from goal: {goal.description}",
            work_packages=[work_package],
            estimated_complexity=3,
            estimated_time="3 days",
        )
