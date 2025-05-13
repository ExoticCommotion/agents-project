"""
Unit tests for the Pipeline Orchestrator.
"""

from ai_project_manager.core.data_models import HighLevelGoal, LearningProposal
from ai_project_manager.core.pipeline import PipelineOrchestrator


def test_pipeline_orchestrator_exists() -> None:
    """Test that the PipelineOrchestrator class exists."""
    assert PipelineOrchestrator is not None


def test_pipeline_orchestrator_initialization() -> None:
    """Test that a PipelineOrchestrator can be initialized."""
    orchestrator = PipelineOrchestrator()
    assert isinstance(orchestrator, PipelineOrchestrator)


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
