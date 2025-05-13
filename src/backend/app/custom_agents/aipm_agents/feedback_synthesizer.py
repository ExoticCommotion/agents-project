"""
Feedback Synthesizer Agent for the AI Project Manager.

This module defines the Feedback Synthesizer Agent, which is responsible for synthesizing
feedback and analysis reports into learning proposals.
"""

from collections import Counter

from backend.app.core.data_models import FeedbackContent, LearningProposal, StructuredAnalysisReport
from backend.app.utils.logger import get_logger

__all__ = ["FeedbackSynthesizerAgent", "FeedbackContent"]

logger = get_logger(__name__)


class FeedbackSynthesizerAgent:
    """
    Agent responsible for synthesizing feedback and analysis reports.

    The Feedback Synthesizer Agent takes structured analysis reports and feedback content
    and synthesizes them into learning proposals for improving the AI Project Manager.
    """

    def __init__(self) -> None:
        """Initialize the Feedback Synthesizer Agent."""
        logger.info("Initializing Feedback Synthesizer Agent")

    def synthesize_feedback(
        self, reports: list[StructuredAnalysisReport], feedback: list[FeedbackContent]
    ) -> LearningProposal:
        """
        Synthesize feedback and analysis reports into a learning proposal.

        Args:
            reports: List of structured analysis reports
            feedback: List of feedback content

        Returns:
            A learning proposal based on the feedback and reports
        """
        logger.info(
            f"Synthesizing feedback from {len(reports)} reports and {len(feedback)} feedback items"
        )

        report_ticket_ids = {report.ticket_id for report in reports}
        feedback_ticket_ids = {item.feedback_id for item in feedback}
        all_ticket_ids = report_ticket_ids.union(feedback_ticket_ids)

        proposal_id = f"proposal-{hash(frozenset(all_ticket_ids)) % 10000}"

        success_factors: list[str] = []
        improvement_suggestions: list[str] = []

        for report in reports:
            success_factors.extend(report.success_factors)
            improvement_suggestions.extend(report.improvement_suggestions)

        success_counter = Counter(success_factors)
        improvement_counter = Counter(improvement_suggestions)

        positive_feedback = [item for item in feedback if item.sentiment == "positive"]
        negative_feedback = [item for item in feedback if item.sentiment == "negative"]

        impact_areas = self._determine_impact_areas(improvement_suggestions, feedback)

        implementation_steps = self._generate_implementation_steps(improvement_counter)

        title = self._generate_title(success_counter, improvement_counter)
        description = self._generate_description(
            success_counter, improvement_counter, positive_feedback, negative_feedback
        )

        return LearningProposal(
            proposal_id=proposal_id,
            title=title,
            description=description,
            impact_areas=impact_areas,
            implementation_steps=implementation_steps,
        )

    def _determine_impact_areas(
        self, improvement_suggestions: list[str], feedback: list[FeedbackContent]
    ) -> list[str]:
        """
        Determine impact areas based on improvement suggestions and feedback.

        Args:
            improvement_suggestions: List of improvement suggestions from reports
            feedback: List of feedback content

        Returns:
            List of impact areas
        """
        impact_area_keywords: dict[str, list[str]] = {
            "Process": ["process", "workflow", "procedure", "methodology", "approach"],
            "Tools": ["tool", "library", "framework", "technology", "infrastructure"],
            "Documentation": ["document", "documentation", "comment", "explanation", "guide"],
            "Testing": ["test", "coverage", "validation", "verification", "quality"],
            "Performance": ["performance", "speed", "efficiency", "optimization", "latency"],
            "User Experience": ["user", "experience", "interface", "usability", "accessibility"],
        }

        all_text = " ".join(improvement_suggestions).lower()
        for item in feedback:
            all_text += " " + item.content.lower()

        identified_areas: set[str] = set()
        for area, keywords in impact_area_keywords.items():
            for keyword in keywords:
                if keyword in all_text:
                    identified_areas.add(area)
                    break

        if not identified_areas:
            identified_areas.add("Process")  # Default impact area

        return list(identified_areas)

    def _generate_implementation_steps(self, improvement_counter: Counter[str]) -> list[str]:
        """
        Generate implementation steps based on improvement suggestions.

        Args:
            improvement_counter: Counter of improvement suggestions

        Returns:
            List of implementation steps
        """
        common_improvements = [item for item, _ in improvement_counter.most_common(5)]

        if len(common_improvements) < 2:
            common_improvements.extend(
                [
                    "Improve documentation and knowledge sharing",
                    "Enhance testing and quality assurance processes",
                ]
            )

        implementation_steps = []
        for i, improvement in enumerate(common_improvements, 1):
            formatted_improvement = improvement[0].upper() + improvement[1:]
            if not formatted_improvement.endswith("."):
                formatted_improvement += "."

            implementation_steps.append(f"Step {i}: {formatted_improvement}")

        return implementation_steps

    def _generate_title(
        self, success_counter: Counter[str], improvement_counter: Counter[str]
    ) -> str:
        """
        Generate a title based on success factors and improvement suggestions.

        Args:
            success_counter: Counter of success factors
            improvement_counter: Counter of improvement suggestions

        Returns:
            A title for the learning proposal
        """
        most_common_success = next(iter(success_counter.most_common(1)), ("Success", 0))[0]
        most_common_improvement = next(
            iter(improvement_counter.most_common(1)), ("Improvement", 0)
        )[0]

        return f"Learning Proposal: Building on {most_common_success} to {most_common_improvement}"

    def _generate_description(
        self,
        success_counter: Counter[str],
        improvement_counter: Counter[str],
        positive_feedback: list[FeedbackContent],
        negative_feedback: list[FeedbackContent],
    ) -> str:
        """
        Generate a description based on success factors, improvement suggestions, and feedback.

        Args:
            success_counter: Counter of success factors
            improvement_counter: Counter of improvement suggestions
            positive_feedback: List of positive feedback items
            negative_feedback: List of negative feedback items

        Returns:
            A description for the learning proposal
        """
        top_successes = [item for item, _ in success_counter.most_common(3)]
        top_improvements = [item for item, _ in improvement_counter.most_common(3)]

        description = "This learning proposal synthesizes feedback and analysis reports to identify key strengths and areas for improvement.\n\n"

        description += "Key Strengths:\n"
        for success in top_successes:
            description += f"- {success}\n"

        description += "\nAreas for Improvement:\n"
        for improvement in top_improvements:
            description += f"- {improvement}\n"

        if positive_feedback or negative_feedback:
            description += "\nFeedback Summary:\n"
            if positive_feedback:
                description += f"- Received {len(positive_feedback)} positive feedback items\n"
            if negative_feedback:
                description += f"- Addressed {len(negative_feedback)} concerns or suggestions\n"

        return description
