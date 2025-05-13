"""
Master Orchestrator Agent for the AI Project Manager.

This module defines the Master Orchestrator Agent, which is responsible for
orchestrating the AI Project Manager pipeline.
"""


from backend.app.core.data_models import DevinTicket, HighLevelGoal
from backend.app.custom_agents.aipm_agents.detailer_tool import DetailerTool
from backend.app.custom_agents.aipm_agents.planner_tool import PlannerTool
from backend.app.utils.logger import get_logger

__all__ = ["MasterOrchestratorAgent"]

logger = get_logger(__name__)


class MasterOrchestratorAgent:
    """
    Agent responsible for orchestrating the AI Project Manager pipeline.

    The Master Orchestrator Agent is the brain of the AIPM. It coordinates the execution
    of the various tools and agents in the pipeline to process high-level goals and
    generate Devin tickets.
    """

    def __init__(self) -> None:
        """Initialize the Master Orchestrator Agent."""
        logger.info("Initializing Master Orchestrator Agent")
        self.planner_tool = PlannerTool()
        self.detailer_tool = DetailerTool()

    def process_initiative(self, initiative_goal: HighLevelGoal) -> list[DevinTicket]:
        """
        Process an initiative goal through the AIPM pipeline.

        This method orchestrates the execution of the pipeline by:
        1. Using the PlannerTool to create a structured plan from the initiative goal
        2. Using the DetailerTool to create detailed tickets for each step in the plan
        3. Aggregating all tickets and returning them

        Args:
            initiative_goal: The high-level initiative goal to process

        Returns:
            A list of Devin tickets generated from the initiative goal
        """
        logger.info(f"Processing initiative: {initiative_goal.title}")

        plan = self.planner_tool.create_plan(initiative_goal)
        logger.info(f"Received plan: {plan.title} with {len(plan.steps)} steps")

        all_tickets = []

        for step_index, step in enumerate(plan.steps):
            logger.info(f"Processing step {step_index + 1}: {step}")

            ticket = self.detailer_tool.create_ticket(plan, step_index)
            logger.info(f"Created ticket: {ticket.title}")

            all_tickets.append(ticket)

        logger.info(f"Generated {len(all_tickets)} tickets for initiative: {initiative_goal.title}")
        return all_tickets
