"""
Master Orchestrator Agent for the AI Project Manager.

This module defines the Master Orchestrator Agent, which is responsible for
orchestrating the AI Project Manager pipeline.
"""


from backend.app.core.data_models import DevinTicket
from backend.app.custom_agents.ai_project_manager.agents.detailer_tool import DetailerTool
from backend.app.custom_agents.ai_project_manager.agents.planner_tool import PlannerTool
from backend.app.custom_agents.ai_project_manager.core.data_models import InitiativeGoal
from backend.app.utils.logger import get_logger

__all__ = ["MasterOrchestratorAgent"]

logger = get_logger(__name__)


class MasterOrchestratorAgent:
    """
    Agent responsible for orchestrating the AI Project Manager pipeline.

    The Master Orchestrator Agent is the brain of the AIPM. It coordinates the execution
    of the various tools and agents in the pipeline to process initiative goals and
    generate Devin tickets.
    """

    def __init__(self) -> None:
        """Initialize the Master Orchestrator Agent."""
        logger.info("Initializing Master Orchestrator Agent")
        self.planner_tool = PlannerTool()
        self.detailer_tool = DetailerTool()

    def process_initiative(self, initiative_goal: InitiativeGoal) -> list[DevinTicket]:
        """
        Process an initiative goal through the AIPM pipeline.

        This method orchestrates the execution of the pipeline by:
        1. Using the PlannerTool to create a decomposition plan from the initiative goal
        2. Using the DetailerTool to create detailed tickets for each work package in the plan
        3. Aggregating all tickets and returning them

        Args:
            initiative_goal: The initiative goal to process

        Returns:
            A list of Devin tickets generated from the initiative goal
        """
        logger.info(f"Processing initiative: {initiative_goal.title}")

        plan = self.planner_tool.plan_initiative(initiative_goal)
        logger.info(f"Received plan: {plan.title} with {len(plan.work_packages)} work packages")

        all_tickets = []

        for work_package_index, work_package in enumerate(plan.work_packages):
            logger.info(f"Processing work package {work_package_index + 1}: {work_package.title}")

            tickets = self.detailer_tool.detail_work_package(work_package)
            logger.info(f"Created {len(tickets)} tickets for work package: {work_package.title}")

            all_tickets.extend(tickets)

        logger.info(f"Generated {len(all_tickets)} tickets for initiative: {initiative_goal.title}")
        return all_tickets
