"""
Prioritizer Agent for the AI Project Manager.

This module defines the Prioritizer Agent, which is responsible for prioritizing
tickets based on their importance and dependencies.
"""

from backend.app.core.data_models import DevinTicket
from backend.app.utils.logger import get_logger

__all__ = ["PrioritizerAgent"]

logger = get_logger(__name__)


class PrioritizerAgent:
    """
    Agent responsible for prioritizing tickets.

    The Prioritizer Agent takes a list of tickets and prioritizes them based on their
    importance and dependencies.
    """

    def __init__(self) -> None:
        """Initialize the Prioritizer Agent."""
        logger.info("Initializing Prioritizer Agent")

    def prioritize_tickets(self, tickets: list[DevinTicket]) -> list[DevinTicket]:
        """
        Prioritize a list of tickets.

        Args:
            tickets: The list of tickets to prioritize

        Returns:
            A prioritized list of tickets
        """
        logger.info(f"Prioritizing {len(tickets)} tickets")

        # Simple prioritization based on the priority field
        return sorted(tickets, key=lambda ticket: ticket.priority)
