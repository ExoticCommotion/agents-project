"""
Unit tests for the Project Orchestrator.
"""

from backend.app.core.data_models import HighLevelGoal, LearningProposal
from backend.app.core.orchestration.project_orchestrator import ProjectOrchestrator


def test_project_orchestrator_exists() -> None:
    """Test that the ProjectOrchestrator class exists."""
    assert ProjectOrchestrator is not None


def test_project_orchestrator_initialization() -> None:
    """Test that a ProjectOrchestrator can be initialized."""
    orchestrator = ProjectOrchestrator()
    assert isinstance(orchestrator, ProjectOrchestrator)


def test_run_placeholder_pipeline() -> None:
    """Test that the run_placeholder_pipeline method returns a LearningProposal."""
    orchestrator = ProjectOrchestrator()
    goal = HighLevelGoal(
        id="goal-123",
        title="Test Goal",
        description="This is a test goal",
        context="Test context",
    )

    proposal = orchestrator.run_placeholder_pipeline(goal)

    assert isinstance(proposal, LearningProposal)
    assert proposal.proposal_id is not None
    assert proposal.title is not None
    assert proposal.description is not None
    assert len(proposal.impact_areas) > 0
    assert len(proposal.implementation_steps) > 0
