"""
Feedback Synthesizer Agent for the AI Project Manager.

This module defines the Feedback Synthesizer Agent, which is responsible for synthesizing
feedback from multiple sources into learning proposals for future improvement.
"""

from backend.app.core.data_models import (
    FeedbackContent,
    LearningProposal,
    StructuredAnalysisReport,
)
from backend.app.utils.logger import get_logger

__all__ = ["FeedbackSynthesizerAgent"]

logger = get_logger(__name__)


class FeedbackSynthesizerAgent:
    """
    Agent responsible for synthesizing feedback.

    The Feedback Synthesizer Agent synthesizes feedback from multiple sources into
    learning proposals for future improvement.
    """

    def __init__(self) -> None:
        """Initialize the Feedback Synthesizer Agent."""
        logger.info("Initializing Feedback Synthesizer Agent")

    def synthesize_feedback(
        self, reports: list[StructuredAnalysisReport], feedback: list[FeedbackContent]
    ) -> LearningProposal:
        """
        Synthesize feedback from multiple sources into a learning proposal.

        Args:
            reports: A list of structured analysis reports
            feedback: A list of feedback content

        Returns:
            A learning proposal for future improvement
        """
        logger.info(
            f"Synthesizing feedback from {len(reports)} reports and {len(feedback)} feedback items"
        )

        success_factors = []
        for report in reports:
            success_factors.extend(report.success_factors)

        improvement_suggestions = []
        for report in reports:
            improvement_suggestions.extend(report.improvement_suggestions)

        feedback_content = [item.content for item in feedback]

        return LearningProposal(
            proposal_id=f"proposal-{hash(''.join(feedback_content)) % 10000}",
            title="Learning Proposal from Feedback",
            description=f"Learning proposal based on {len(reports)} reports and {len(feedback)} feedback items",
            impact_areas=["Process Improvement", "Tool Integration"],
            implementation_steps=[
                f"Address: {suggestion}" for suggestion in improvement_suggestions[:3]
            ],
        )
