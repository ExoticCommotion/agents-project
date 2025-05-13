"""
Command-line interface for the AI Project Manager.

This module provides a command-line interface for interacting with the
AI Project Manager system.
"""

import json
import os

import typer
from rich import print

from backend.app.utils.logger import get_logger

from .core.data_models import HighLevelGoal, LearningProposal
from .core.pipeline import PipelineOrchestrator

app = typer.Typer(add_completion=False, help="🧠 AI Project Manager CLI")
logger = get_logger(__name__)


@app.command("process-goal")
def process_goal(
    goal_description: str = typer.Argument(...),
    goal_title: str = typer.Option(None, "--title", "-t", help="Goal title"),
    goal_context: str = typer.Option(
        None, "--context", "-c", help="Additional context for the goal"
    ),
    pretty: bool = typer.Option(
        True,
        "--pretty/--compact",
        help="Format JSON output with indentation for readability",
    ),
) -> None:
    """
    Process a high-level goal through the AI Project Manager pipeline.

    Args:
        goal_description: High-level goal description

    Examples:
        uv run python -m backend.app.custom_agents.ai_project_manager.cli process-goal "Build a web application for task management"
        uv run python -m backend.app.custom_agents.ai_project_manager.cli process-goal "Fix login bug" --title "Login Bug Fix" --context "Users report being unable to log in with correct credentials"
    """
    logger.info("Processing goal description...")

    if not goal_description or goal_description.strip() == "":
        logger.error("Error: Goal description cannot be empty")
        print("[bold red]Error:[/] Goal description cannot be empty")
        raise typer.Exit(code=1)

    try:
        goal_id = f"goal-{hash(goal_description) % 10000}"
        goal = HighLevelGoal(
            id=goal_id,
            title=goal_title or f"Goal: {goal_description[:30]}...",
            description=goal_description,
            context=goal_context,
        )

        if os.environ.get("AIPM_TEST_MODE") == "1":
            logger.info("Running in test mode with mock data")
            learning_proposal = LearningProposal(
                proposal_id="proposal-test",
                title="Test Learning Proposal",
                description="This is a test learning proposal",
                impact_areas=["Test impact area"],
                implementation_steps=["Test implementation step"],
            )
        else:
            orchestrator = PipelineOrchestrator()
            learning_proposal = orchestrator.run_placeholder_pipeline(goal)

        result = {
            "proposal_id": learning_proposal.proposal_id,
            "title": learning_proposal.title,
            "description": learning_proposal.description,
            "impact_areas": learning_proposal.impact_areas,
            "implementation_steps": learning_proposal.implementation_steps,
        }

        indent = 2 if pretty else None
        formatted_json = json.dumps(result, indent=indent)
        print(formatted_json)
        logger.info("Goal processing completed successfully")

    except Exception as e:
        logger.error(f"Error processing goal: {str(e)}")
        print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
