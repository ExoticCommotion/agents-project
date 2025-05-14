"""
Planner Tool Agent for the AI Project Manager.

This module defines the Planner Tool Agent, which is responsible for providing
planning functionality as a tool.
"""

from typing import TYPE_CHECKING

from backend.app.core.data_models import HighLevelGoal, StructuredPlan
from backend.app.utils.logger import get_logger

if TYPE_CHECKING:
    from backend.app.custom_agents.ai_project_manager.core.data_models import (
        DecompositionPlan,
        InitiativeGoal,
        WorkPackage,
    )
else:
    from backend.app.custom_agents.ai_project_manager.core.data_models import (
        DecompositionPlan,
        InitiativeGoal,
        WorkPackage,
    )

__all__ = ["PlannerTool"]

logger = get_logger(__name__)


class PlannerTool:
    """
    Tool agent responsible for creating decomposition plans from initiative goals.

    The Planner Tool provides planning functionality that can be used by other agents
    in the AI Project Manager system.
    """

    def __init__(self) -> None:
        """Initialize the Planner Tool."""
        logger.info("Initializing Planner Tool")

    def plan_initiative(self, initiative_goal: InitiativeGoal) -> DecompositionPlan:
        """
        Create a decomposition plan from an initiative goal.

        Args:
            initiative_goal: The initiative goal to plan for

        Returns:
            A decomposition plan with work packages, complexity estimates, and time estimates
        """
        logger.info(f"Creating plan for initiative: {initiative_goal.title}")

        work_packages = [
            WorkPackage(
                package_id=f"wp-1-{hash(initiative_goal.id) % 10000}",
                plan_id=f"plan-{hash(initiative_goal.id) % 10000}",
                title="Work Package 1: Setup",
                description="Initial setup and configuration",
                tasks=["Task 1: Setup environment", "Task 2: Configure dependencies"],
                estimated_complexity=2,
                estimated_time="1 day",
            ),
            WorkPackage(
                package_id=f"wp-2-{hash(initiative_goal.id) % 10000}",
                plan_id=f"plan-{hash(initiative_goal.id) % 10000}",
                title="Work Package 2: Implementation",
                description="Core implementation tasks",
                tasks=["Task 1: Implement core functionality", "Task 2: Add tests"],
                estimated_complexity=4,
                estimated_time="2 days",
            ),
        ]

        return DecompositionPlan(
            goal_id=initiative_goal.id,
            plan_id=f"plan-{hash(initiative_goal.id) % 10000}",
            title=f"Plan for {initiative_goal.title}",
            description=f"Decomposition plan derived from initiative: {initiative_goal.description}",
            work_packages=work_packages,
            estimated_complexity=3,
            estimated_time="3 days",
        )

    def create_plan(self, goal: "HighLevelGoal") -> "StructuredPlan":
        """
        Create a structured plan from a high-level goal.

        Args:
            goal: The high-level goal to create a plan for

        Returns:
            A structured plan with steps, complexity estimates, and time estimates
        """
        logger.info(f"Creating structured plan for goal: {goal.title}")

        from backend.app.core.data_models import StructuredPlan

        steps = [
            "Step 1: Implement core functionality",
            "Step 2: Add tests",
            "Step 3: Add documentation",
            "Step 4: Review and refactor",
        ]

        return StructuredPlan(
            goal_id=goal.id,
            plan_id=f"plan-{hash(goal.id) % 10000}",
            title=f"Plan for {goal.title}",
            description=f"Structured plan derived from goal: {goal.description}",
            steps=steps,
            estimated_complexity=3,
            estimated_time="3 days",
        )
