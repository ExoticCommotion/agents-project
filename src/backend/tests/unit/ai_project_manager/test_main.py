"""
Unit tests for the AI Project Manager main entry point.
"""

import json
from unittest.mock import MagicMock, patch

from ai_project_manager.__main__ import main
from ai_project_manager.core.data_models import HighLevelGoal, LearningProposal


@patch("sys.argv", ["ai_project_manager", "Test goal description"])
@patch("ai_project_manager.__main__.PipelineOrchestrator")
@patch("builtins.print")
def test_main_with_minimal_args(mock_print: MagicMock, mock_orchestrator_class: MagicMock) -> None:
    """Test the main function with minimal arguments."""
    # Setup mock
    mock_orchestrator_instance = MagicMock()
    mock_orchestrator_class.return_value = mock_orchestrator_instance
    mock_orchestrator_instance.run_placeholder_pipeline.return_value = LearningProposal(
        proposal_id="proposal-test",
        title="Test Learning Proposal",
        description="This is a test learning proposal",
        impact_areas=["Test impact area"],
        implementation_steps=["Test implementation step"],
    )

    # Call the function
    main()

    # Verify the orchestrator was called with the correct goal
    mock_orchestrator_instance.run_placeholder_pipeline.assert_called_once()
    goal_arg = mock_orchestrator_instance.run_placeholder_pipeline.call_args[0][0]
    assert isinstance(goal_arg, HighLevelGoal)
    assert goal_arg.description == "Test goal description"

    # Verify the output was printed
    mock_print.assert_called_once()
    printed_json = json.loads(mock_print.call_args[0][0])
    assert printed_json["proposal_id"] == "proposal-test"
    assert printed_json["title"] == "Test Learning Proposal"


@patch("sys.argv", ["ai_project_manager", "Test goal description", "Custom Title", "Some context"])
@patch("ai_project_manager.__main__.PipelineOrchestrator")
@patch("builtins.print")
def test_main_with_all_args(mock_print: MagicMock, mock_orchestrator_class: MagicMock) -> None:
    """Test the main function with all arguments."""
    # Setup mock
    mock_orchestrator_instance = MagicMock()
    mock_orchestrator_class.return_value = mock_orchestrator_instance
    mock_orchestrator_instance.run_placeholder_pipeline.return_value = LearningProposal(
        proposal_id="proposal-test",
        title="Test Learning Proposal",
        description="This is a test learning proposal",
        impact_areas=["Test impact area"],
        implementation_steps=["Test implementation step"],
    )

    # Call the function
    main()

    # Verify the orchestrator was called with the correct goal
    mock_orchestrator_instance.run_placeholder_pipeline.assert_called_once()
    goal_arg = mock_orchestrator_instance.run_placeholder_pipeline.call_args[0][0]
    assert isinstance(goal_arg, HighLevelGoal)
    assert goal_arg.description == "Test goal description"
    assert goal_arg.title == "Custom Title"
    assert goal_arg.context == "Some context"


@patch("sys.argv", ["ai_project_manager"])
@patch("sys.exit")
@patch("builtins.print")
def test_main_no_args(mock_print: MagicMock, mock_exit: MagicMock) -> None:
    """Test the main function with no arguments."""
    # Call the function
    main()

    # Verify sys.exit was called with the correct code
    mock_exit.assert_called_once_with(1)
    # Verify the usage message was printed
    assert "Usage:" in mock_print.call_args[0][0]
