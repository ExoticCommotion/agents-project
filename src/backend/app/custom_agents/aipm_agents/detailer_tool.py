"""
Detailer Tool Agent for the AI Project Manager.

This module defines the Detailer Tool Agent, which is responsible for providing
detailed information about plans and tasks.
"""

from backend.app.core.data_models import DevinTicket, StructuredPlan
from backend.app.utils.logger import get_logger

__all__ = ["DetailerTool", "DevinTicket"]

logger = get_logger(__name__)


class DetailerTool:
    """
    Tool agent responsible for providing detailed information about plans and tasks.

    The Detailer Tool provides functionality to create detailed tickets from structured plans
    that can be used by other agents in the AI Project Manager system.
    """

    def __init__(self) -> None:
        """Initialize the Detailer Tool."""
        logger.info("Initializing Detailer Tool")

    def create_ticket(self, plan: StructuredPlan, step_index: int) -> DevinTicket:
        """
        Create a detailed ticket from a structured plan step.

        Args:
            plan: The structured plan containing the step
            step_index: The index of the step to create a ticket for

        Returns:
            A detailed ticket with acceptance criteria and expectations
        """
        logger.info(f"Creating ticket for plan: {plan.title}, step: {step_index}")

        if step_index >= len(plan.steps):
            logger.warning(
                f"Step index {step_index} out of range for plan with {len(plan.steps)} steps"
            )
            step_index = 0

        step = plan.steps[step_index]

        return DevinTicket(
            ticket_id=f"ticket-{hash(plan.plan_id + str(step_index)) % 10000}",
            epic_id=f"epic-{hash(plan.plan_id) % 10000}",
            title=f"Implement: {step}",
            description=f"Implementation of step {step_index + 1} from plan: {plan.title}",
            input_files=["placeholder.py"],
            output_expectation="Expected functionality as described",
            acceptance_criteria=["Code compiles", "Tests pass", "Documentation complete"],
            priority=3,
            status="ready",
        )
