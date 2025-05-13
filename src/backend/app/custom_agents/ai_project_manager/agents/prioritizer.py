"""
Prioritizer Agent for the AI Project Manager.

This module defines the Prioritizer Agent, which is responsible for prioritizing
Devin tickets.
"""

from ....utils.logger import get_logger
from ..core.data_models import DevinTicket

logger = get_logger(__name__)


class PrioritizerAgent:
    """
    Agent responsible for prioritizing Devin tickets.

    The Prioritizer Agent takes a list of Devin tickets and prioritizes them based on
    various factors such as complexity, dependencies, and business value.
    """

    def __init__(self) -> None:
        """Initialize the Prioritizer Agent."""
        logger.info("Initializing Prioritizer Agent")

    def prioritize_tickets(self, tickets: list[DevinTicket]) -> list[DevinTicket]:
        """
        Prioritize a list of Devin tickets.

        Args:
            tickets: The list of tickets to prioritize

        Returns:
            A prioritized list of Devin tickets
        """
        logger.info(f"Prioritizing {len(tickets)} tickets")
        # Simple prioritization by ticket priority field
        return sorted(tickets, key=lambda t: t.priority)
