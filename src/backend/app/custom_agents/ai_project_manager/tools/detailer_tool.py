"""
Detailer Tool Agent for the AI Project Manager.

This module defines the Detailer Tool Agent, which is responsible for providing
detailed information about work packages and tasks.
"""

from typing import TYPE_CHECKING

from backend.app.core.data_models import DevinTicket, StructuredPlan
from backend.app.utils.logger import get_logger

if TYPE_CHECKING:
    from backend.app.custom_agents.ai_project_manager.core.data_models import WorkPackage

__all__ = ["DetailerTool"]

logger = get_logger(__name__)


class DetailerTool:
    """
    Tool agent responsible for providing detailed information about work packages and tasks.

    The Detailer Tool provides functionality to create detailed tickets from work packages
    that can be used by other agents in the AI Project Manager system.
    """

    def __init__(self) -> None:
        """Initialize the Detailer Tool."""
        logger.info("Initializing Detailer Tool")

    def detail_work_package(self, work_package: "WorkPackage") -> list[DevinTicket]:
        """
        Create detailed tickets from a work package.

        Args:
            work_package: The work package to create tickets for

        Returns:
            A list of detailed tickets with acceptance criteria and expectations
        """
        logger.info(f"Creating tickets for work package: {work_package.title}")

        tickets = []

        for task_index, task in enumerate(work_package.tasks):
            ticket = DevinTicket(
                ticket_id=f"ticket-{hash(work_package.package_id + str(task_index)) % 10000}",
                epic_id=f"epic-{hash(work_package.plan_id) % 10000}",
                title=f"Implement: {task}",
                description=f"Implementation of task {task_index + 1} from work package: {work_package.title}",
                input_files=["placeholder.py"],
                output_expectation="Expected functionality as described",
                acceptance_criteria=["Code compiles", "Tests pass", "Documentation complete"],
                priority=3,
                status="ready",
            )
            tickets.append(ticket)
            logger.info(f"Created ticket: {ticket.title}")

        return tickets

    def create_ticket(self, plan: "StructuredPlan", step_index: int) -> DevinTicket:
        """
        Create a detailed ticket from a structured plan and step index.

        Args:
            plan: The structured plan to create a ticket for
            step_index: The index of the step in the plan to create a ticket for

        Returns:
            A detailed ticket with acceptance criteria and expectations
        """
        logger.info(f"Creating ticket for plan: {plan.title}, step index: {step_index}")

        if step_index < 0 or step_index >= len(plan.steps):
            logger.warning(
                f"Step index {step_index} is out of range for plan with {len(plan.steps)} steps"
            )
            step_index = 0  # Default to first step if out of range

        step = plan.steps[step_index] if step_index < len(plan.steps) else "Default step"

        ticket = DevinTicket(
            ticket_id=f"ticket-{hash(plan.plan_id + str(step_index)) % 10000}",
            epic_id=f"epic-{hash(plan.goal_id) % 10000}",
            title=f"Implement: {step}",
            description=f"Implementation of step {step_index + 1} from plan: {plan.title}",
            input_files=["placeholder.py"],
            output_expectation="Expected functionality as described",
            acceptance_criteria=["Code compiles", "Tests pass", "Documentation complete"],
            priority=3,
            status="ready",
        )

        logger.info(f"Created ticket: {ticket.title}")
        return ticket
