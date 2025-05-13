"""
Detailer Tool Agent for the AI Project Manager.

This module defines the Detailer Tool Agent, which is responsible for providing
detailed information about work packages and tasks.
"""


from backend.app.core.data_models import DevinTicket
from backend.app.custom_agents.ai_project_manager.core.data_models import WorkPackage
from backend.app.utils.logger import get_logger

__all__ = ["DetailerTool", "DevinTicket"]

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

    def detail_work_package(self, work_package: WorkPackage) -> list[DevinTicket]:
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
