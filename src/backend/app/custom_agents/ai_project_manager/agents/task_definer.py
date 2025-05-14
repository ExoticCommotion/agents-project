"""
Task Definer Agent for the AI Project Manager.

This module defines the Task Definer Agent, which is responsible for creating epics and
tickets from structured plans.
"""

from backend.app.core.data_models import DevinTicket, Epic
from backend.app.custom_agents.ai_project_manager.core.data_models import DecompositionPlan
from backend.app.utils.logger import get_logger

__all__ = ["TaskDefinerAgent"]

logger = get_logger(__name__)


class TaskDefinerAgent:
    """
    Agent responsible for creating epics and tickets from structured plans.

    The Task Definer Agent takes a structured plan and breaks it down into epics and
    tickets that can be executed by Devin.
    """

    def __init__(self) -> None:
        """Initialize the Task Definer Agent."""
        logger.info("Initializing Task Definer Agent")

    def create_epics(self, plan: DecompositionPlan) -> list[Epic]:
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
                epic_id="epic-placeholder",
                plan_id=plan.plan_id,
                title=f"Epic for {plan.title}",
                description=f"Epic derived from plan: {plan.description}",
                priority=1,
                status="pending",
            )
        ]

    def create_tickets(self, epic: Epic) -> list[DevinTicket]:
        """
        Create Devin tickets from an epic.

        Args:
            epic: The epic to create tickets from

        Returns:
            A list of Devin tickets derived from the epic
        """
        logger.info(f"Creating tickets for epic: {epic.title}")
        return [
            DevinTicket(
                ticket_id="ticket-placeholder",
                epic_id=epic.epic_id,
                title=f"Ticket for {epic.title}",
                description=f"Ticket derived from epic: {epic.description}",
                input_files=["file1.py", "file2.py"],
                output_expectation="Expected output",
                acceptance_criteria=["Criteria 1", "Criteria 2"],
                priority=1,
                status="pending",
            )
        ]
