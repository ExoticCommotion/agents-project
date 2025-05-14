"""
Unit tests for the Feedback Synthesizer Agent.
"""

from collections import Counter

from backend.app.core.data_models import FeedbackContent, LearningProposal, StructuredAnalysisReport
from backend.app.custom_agents.ai_project_manager.agents.feedback_synthesizer import (
    FeedbackSynthesizerAgent,
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


def test_synthesize_feedback_with_multiple_reports_and_feedback() -> None:
    """Test synthesizing feedback with multiple reports and feedback items."""
    agent = FeedbackSynthesizerAgent()
    reports = [
        StructuredAnalysisReport(
            report_id="report-1",
            ticket_id="ticket-1",
            success_factors=["Success factor 1", "Common success"],
            improvement_suggestions=["Improvement suggestion 1", "Common improvement"],
        ),
        StructuredAnalysisReport(
            report_id="report-2",
            ticket_id="ticket-2",
            success_factors=["Success factor 2", "Common success"],
            improvement_suggestions=["Improvement suggestion 2", "Common improvement"],
        ),
    ]
    feedback = [
        FeedbackContent(
            feedback_id="feedback-1",
            ticket_id="ticket-1",
            content="Positive feedback content",
            source="user",
            sentiment="positive",
        ),
        FeedbackContent(
            feedback_id="feedback-2",
            ticket_id="ticket-2",
            content="Negative feedback content",
            source="system",
            sentiment="negative",
        ),
    ]

    proposal = agent.synthesize_feedback(reports, feedback)

    assert "Common success" in proposal.title or "Common improvement" in proposal.title
    assert proposal.proposal_id.startswith("proposal-")
    assert len(proposal.implementation_steps) >= 2


def test_determine_impact_areas() -> None:
    """Test the _determine_impact_areas method."""
    agent = FeedbackSynthesizerAgent()

    improvement_suggestions = ["Improve the workflow process", "Enhance methodology"]
    feedback = [
        FeedbackContent(
            feedback_id="feedback-1",
            ticket_id="ticket-1",
            content="The process needs improvement",
            source="user",
            sentiment="negative",
        )
    ]

    impact_areas = agent._determine_impact_areas(improvement_suggestions, feedback)
    assert "Process" in impact_areas

    improvement_suggestions = ["Update the framework", "Improve infrastructure"]
    feedback = [
        FeedbackContent(
            feedback_id="feedback-1",
            ticket_id="ticket-1",
            content="The tools are outdated",
            source="user",
            sentiment="negative",
        )
    ]

    impact_areas = agent._determine_impact_areas(improvement_suggestions, feedback)
    assert "Tools" in impact_areas

    impact_areas = agent._determine_impact_areas([], [])
    assert "Process" in impact_areas  # Default impact area


def test_generate_implementation_steps() -> None:
    """Test the _generate_implementation_steps method."""
    agent = FeedbackSynthesizerAgent()

    improvement_counter = Counter(
        {"Improve documentation": 3, "Enhance testing": 2, "Optimize performance": 1}
    )

    steps = agent._generate_implementation_steps(improvement_counter)
    assert len(steps) == 3
    assert any("documentation" in step.lower() for step in steps)
    assert any("testing" in step.lower() for step in steps)
    assert all(step.startswith("Step ") for step in steps)

    improvement_counter = Counter({"Single improvement": 1})
    steps = agent._generate_implementation_steps(improvement_counter)
    assert len(steps) >= 2  # Should add default steps if fewer than 2


def test_generate_title() -> None:
    """Test the _generate_title method."""
    agent = FeedbackSynthesizerAgent()

    success_counter = Counter({"Team collaboration": 3, "Code quality": 1})
    improvement_counter = Counter({"Documentation": 2, "Testing": 1})

    title = agent._generate_title(success_counter, improvement_counter)
    assert "Team collaboration" in title
    assert "Documentation" in title

    title = agent._generate_title(Counter(), Counter())
    assert "Success" in title
    assert "Improvement" in title


def test_generate_description() -> None:
    """Test the _generate_description method."""
    agent = FeedbackSynthesizerAgent()

    success_counter = Counter({"Success 1": 2, "Success 2": 1, "Success 3": 1})
    improvement_counter = Counter({"Improvement 1": 3, "Improvement 2": 2, "Improvement 3": 1})
    positive_feedback = [
        FeedbackContent(
            feedback_id="feedback-1",
            ticket_id="ticket-1",
            content="Positive feedback",
            source="user",
            sentiment="positive",
        )
    ]
    negative_feedback = [
        FeedbackContent(
            feedback_id="feedback-2",
            ticket_id="ticket-2",
            content="Negative feedback",
            source="user",
            sentiment="negative",
        )
    ]

    description = agent._generate_description(
        success_counter, improvement_counter, positive_feedback, negative_feedback
    )

    assert "Key Strengths" in description
    assert "Areas for Improvement" in description
    assert "Feedback Summary" in description
    assert "Success 1" in description
    assert "Improvement 1" in description
    assert "1 positive feedback" in description
    assert "1 concerns or suggestions" in description
