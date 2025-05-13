"""
Main entry point for the AI Project Manager.

This module provides the main entry point for running the AI Project Manager
from the command line.
"""

import json
import sys

from ai_project_manager.core.data_models import HighLevelGoal
from ai_project_manager.core.pipeline import PipelineOrchestrator
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    """
    Main entry point for the AI Project Manager.

    This function processes a high-level goal provided as a command-line argument
    and returns a learning proposal.
    """
    logger.info("Starting AI Project Manager")

    if len(sys.argv) < 2:
        print("Usage: python -m ai_project_manager <goal_description> [goal_title] [goal_context]")
        sys.exit(1)
        return  # This line is never reached in production but helps with testing

    goal_description = sys.argv[1]
    goal_title = sys.argv[2] if len(sys.argv) > 2 else f"Goal: {goal_description[:30]}..."
    goal_context = sys.argv[3] if len(sys.argv) > 3 else None

    goal_id = f"goal-{hash(goal_description) % 10000}"
    goal = HighLevelGoal(
        id=goal_id,
        title=goal_title,
        description=goal_description,
        context=goal_context,
    )

    orchestrator = PipelineOrchestrator()
    learning_proposal = orchestrator.run_placeholder_pipeline(goal)

    result = {
        "proposal_id": learning_proposal.proposal_id,
        "title": learning_proposal.title,
        "description": learning_proposal.description,
        "impact_areas": learning_proposal.impact_areas,
        "implementation_steps": learning_proposal.implementation_steps,
    }

    print(json.dumps(result, indent=2))
    logger.info("AI Project Manager completed successfully")


if __name__ == "__main__":
    main()
