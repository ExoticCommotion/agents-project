"""
Detailer Tool for the AI Project Manager.

This module defines the Detailer Tool, which is responsible for creating detailed
tickets for work packages.
"""

from backend.app.core.data_models import DevinTicket, WorkPackage
from backend.app.utils.logger import get_logger

__all__ = ["DetailerTool"]

logger = get_logger(__name__)


class DetailerTool:
    """
    Tool responsible for creating detailed tickets for work packages.

    The Detailer Tool takes a work package and creates detailed tickets that can be
    executed by Devin.
    """

    def __init__(self) -> None:
        """Initialize the Detailer Tool."""
        logger.info("Initializing Detailer Tool")

    def detail_work_package(self, work_package: WorkPackage) -> list[DevinTicket]:
        """
        Create detailed tickets for a work package.

        Args:
            work_package: The work package to create tickets for

        Returns:
            A list of detailed tickets for the work package
        """
        logger.info(f"Detailing work package: {work_package.title}")

        tickets = []

        for i, task in enumerate(work_package.tasks):
            ticket_id = f"ticket-{hash(work_package.package_id + task) % 10000}"

            ticket = DevinTicket(
                ticket_id=ticket_id,
                epic_id=work_package.package_id,  # Using package_id as epic_id for now
                title=f"Implement {task}",
                description=f"Implement the functionality for {task} as part of {work_package.title}",
                input_files=["file1.py", "file2.py"],  # Placeholder
                output_expectation=f"Expected output for {task}",
                acceptance_criteria=[
                    f"Criterion 1 for {task}",
                    f"Criterion 2 for {task}",
                ],
                priority=i + 1,
                status="ready",
            )

            tickets.append(ticket)
            logger.info(f"Created ticket: {ticket.title}")

        return tickets
