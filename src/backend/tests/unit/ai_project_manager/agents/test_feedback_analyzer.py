"""
Unit tests for the Feedback Analyzer Agent.
"""

from backend.app.custom_agents.ai_project_manager.agents.feedback_analyzer import (
    FeedbackAnalyzerAgent,
)
from backend.app.custom_agents.ai_project_manager.core.data_models import (
    ExecutionResult,
    StructuredAnalysisReport,
)


def test_feedback_analyzer_agent_exists() -> None:
    """Test that the FeedbackAnalyzerAgent class exists."""
    assert FeedbackAnalyzerAgent is not None


def test_feedback_analyzer_agent_initialization() -> None:
    """Test that a FeedbackAnalyzerAgent can be initialized."""
    agent = FeedbackAnalyzerAgent()
    assert isinstance(agent, FeedbackAnalyzerAgent)


def test_analyze_result() -> None:
    """Test that the analyze_result method returns a StructuredAnalysisReport."""
    agent = FeedbackAnalyzerAgent()
    result = ExecutionResult(
        ticket_id="ticket-101",
        status="completed",
        output="Test output",
        execution_time="1 hour",
    )

    report = agent.analyze_result(result)

    assert isinstance(report, StructuredAnalysisReport)
    assert report.ticket_id == result.ticket_id
    assert report.report_id is not None
    assert len(report.success_factors) > 0
    assert len(report.improvement_suggestions) > 0
