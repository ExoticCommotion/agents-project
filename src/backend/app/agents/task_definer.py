"""
Task Definer Agent for the AI Project Manager.

This module defines the Task Definer Agent, which is responsible for breaking down
structured plans into epics and well-defined tasks (tickets) that can be executed by Devin.
"""

from backend.app.core.data_models import DevinTicket, Epic, StructuredPlan
from backend.app.utils.logger import get_logger

__all__ = ["TaskDefinerAgent"]

logger = get_logger(__name__)


class TaskDefinerAgent:
    """
    Agent responsible for breaking down structured plans into epics and tasks.

    The Task Definer Agent takes a structured plan and breaks it down into epics
    and well-defined tasks (tickets) that can be executed by Devin.
    """

    def __init__(self) -> None:
        """Initialize the Task Definer Agent."""
        logger.info("Initializing Task Definer Agent")

    def create_epics(self, plan: StructuredPlan) -> list[Epic]:
        """
        Create epics from a structured plan.

        Args:
            plan: The structured plan to create epics from

        Returns:
            A list of epics derived from the plan
        """
        logger.info(f"Creating epics for plan: {plan.title}")
        return [
            Epic(
                epic_id=f"epic-{hash(plan.plan_id + str(i)) % 10000}",
                plan_id=plan.plan_id,
                title=f"Epic {i + 1}: {step}",
                description=f"Epic derived from step: {step}",
                priority=i + 1,
                status="ready",
            )
            for i, step in enumerate(plan.steps)
        ]

    def create_tickets(self, epic: Epic) -> list[DevinTicket]:
        """
        Create tickets from an epic.

        Args:
            epic: The epic to create tickets from

        Returns:
            A list of tickets derived from the epic
        """
        logger.info(f"Creating tickets for epic: {epic.title}")
        return [
            DevinTicket(
                ticket_id=f"ticket-{hash(epic.epic_id + str(i)) % 10000}",
                epic_id=epic.epic_id,
                title=f"Ticket {i + 1} for {epic.title}",
                description=f"Implement functionality for {epic.title}",
                input_files=["file1.py", "file2.py"],
                output_expectation="Expected output for the ticket",
                acceptance_criteria=["Criterion 1", "Criterion 2"],
                priority=i + 1,
                status="ready",
            )
            for i in range(2)  # Create 2 tickets per epic as a placeholder
        ]
