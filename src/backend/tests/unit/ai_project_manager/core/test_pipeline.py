"""
Unit tests for the Pipeline Orchestrator.
"""

from backend.app.core.data_models import HighLevelGoal, LearningProposal
from backend.app.core.pipeline import PipelineOrchestrator
from backend.app.custom_agents.ai_project_manager.agents import (
    ExecutionCoordinatorAgent,
    FeedbackAnalyzerAgent,
    FeedbackSynthesizerAgent,
    PlannerAgent,
    PrioritizerAgent,
    TaskDefinerAgent,
)
from backend.app.tools.devin_session_manager import DevinSessionManager


def test_pipeline_orchestrator_exists() -> None:
    """Test that the PipelineOrchestrator class exists."""
    assert PipelineOrchestrator is not None


def test_pipeline_orchestrator_initialization() -> None:
    """Test that a PipelineOrchestrator can be initialized."""
    orchestrator = PipelineOrchestrator()
    assert isinstance(orchestrator, PipelineOrchestrator)


def test_pipeline_orchestrator_agents_initialization() -> None:
    """Test that all agents are properly initialized in the PipelineOrchestrator."""
    orchestrator = PipelineOrchestrator()

    assert isinstance(orchestrator.planner, PlannerAgent)
    assert isinstance(orchestrator.task_definer, TaskDefinerAgent)
    assert isinstance(orchestrator.prioritizer, PrioritizerAgent)
    assert isinstance(orchestrator.execution_coordinator, ExecutionCoordinatorAgent)
    assert isinstance(orchestrator.feedback_analyzer, FeedbackAnalyzerAgent)
    assert isinstance(orchestrator.feedback_synthesizer, FeedbackSynthesizerAgent)
    assert isinstance(orchestrator.devin_session_manager, DevinSessionManager)


def test_run_placeholder_pipeline() -> None:
    """Test that the run_placeholder_pipeline method returns a LearningProposal."""
    orchestrator = PipelineOrchestrator()
    goal = HighLevelGoal(
        id="goal-123",
        title="Test Goal",
        description="This is a test goal",
    )

    proposal = orchestrator.run_placeholder_pipeline(goal)

    assert isinstance(proposal, LearningProposal)
    assert proposal.proposal_id is not None
    assert proposal.title is not None
    assert proposal.description is not None
    assert len(proposal.impact_areas) > 0
    assert len(proposal.implementation_steps) > 0

    assert f"Learning Proposal for {goal.title}" == proposal.title
    assert f"This is a learning proposal for the goal: {goal.description}" == proposal.description
    assert "Process Improvement" in proposal.impact_areas
    assert "Tool Integration" in proposal.impact_areas
    assert "Step 1: Implement core functionality" in proposal.implementation_steps
