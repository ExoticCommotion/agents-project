"""
Unit tests for the Feedback Synthesizer Agent.
"""

from backend.app.custom_agents.ai_project_manager.agents.feedback_synthesizer import (
    FeedbackSynthesizerAgent,
)
from backend.app.custom_agents.ai_project_manager.core.data_models import (
    FeedbackContent,
    LearningProposal,
    StructuredAnalysisReport,
)


def test_feedback_synthesizer_agent_exists() -> None:
    """Test that the FeedbackSynthesizerAgent class exists."""
    assert FeedbackSynthesizerAgent is not None


def test_feedback_synthesizer_agent_initialization() -> None:
    """Test that a FeedbackSynthesizerAgent can be initialized."""
    agent = FeedbackSynthesizerAgent()
    assert isinstance(agent, FeedbackSynthesizerAgent)


def test_synthesize_feedback() -> None:
    """Test that the synthesize_feedback method returns a LearningProposal."""
    agent = FeedbackSynthesizerAgent()
    reports = [
        StructuredAnalysisReport(
            report_id="report-1",
            ticket_id="ticket-1",
            success_factors=["Success factor 1"],
            improvement_suggestions=["Improvement suggestion 1"],
        )
    ]
    feedback = [
        FeedbackContent(
            feedback_id="feedback-1",
            ticket_id="ticket-1",
            content="Feedback content",
            source="user",
            sentiment="positive",
        )
    ]

    proposal = agent.synthesize_feedback(reports, feedback)

    assert isinstance(proposal, LearningProposal)
    assert proposal.proposal_id is not None
    assert proposal.title is not None
    assert proposal.description is not None
    assert len(proposal.impact_areas) > 0
    assert len(proposal.implementation_steps) > 0
