from __future__ import annotations

import dataclasses
import json
import os

import typer
from rich import print

from backend.app.core.data_models import HighLevelGoal, LearningProposal
from backend.app.core.pipeline import PipelineOrchestrator
from backend.app.custom_agents.ai_project_manager.core.data_models import InitiativeGoal
from backend.app.custom_agents.ai_project_manager.core.master_orchestrator import (
    MasterOrchestratorAgent,
)
from backend.app.utils.logger import get_logger

app = typer.Typer(add_completion=False, help="🧠 Devin template CLI")
logger = get_logger(__name__)

# ------------------------------------------------------------------ #
#  Example command with diverse arguments
# ------------------------------------------------------------------ #


@app.command()
def greet(
    name: str = typer.Argument("Example", help="Name to greet"),
    times: int = typer.Option(1, "--times", "-t", help="Repeat how many times"),
    excited: bool = typer.Option(
        False,
        "--excited/--no-excited",
        help="Add an exclamation mark!",
    ),
) -> None:
    """Greet NAME a number of TIMES.

    Examples
    --------
    uv run python -m backend.app.cli greet
    uv run python -m backend.app.cli greet "Example" --times 3 --excited
    """
    punctuation = "!" if excited else "."
    for _ in range(times):
        print(f"[bold green]Hello, {name}{punctuation}[/]")


# ------------------------------------------------------------------ #
# ------------------------------------------------------------------ #


@app.command("format-task")
def format_task(
    task_description: str = typer.Argument(..., help="Natural language task description"),
    pretty: bool = typer.Option(
        True,
        "--pretty/--compact",
        help="Format JSON output with indentation for readability",
    ),
) -> None:
    """Transform a natural language task description into a structured JSON task definition.

    Examples
    --------
    uv run python -m backend.app.cli format-task "Create a Python module that does X and Y."
    uv run python -m backend.app.cli format-task "Fix bug in login form" --compact
    """
    logger.info("Processing task description...")

    if not task_description or task_description.strip() == "":
        logger.error("Error: Task description cannot be empty")
        print("[bold red]Error:[/] Task description cannot be empty")
        raise typer.Exit(code=1)

    try:
        if os.environ.get("DTFA_TEST_MODE") == "1":
            logger.info("Running in test mode with mock data")
            task_json = {
                "title": "Test Module",
                "goal": "Create a test module for testing",
                "input": "Test input",
                "output": "Test output",
                "verify": ["Test verification"],
                "notes": ["Test note"],
            }

        indent = 2 if pretty else None
        formatted_json = json.dumps(task_json, indent=indent)

        print(formatted_json)
        logger.info("Task formatting completed successfully")

    except Exception as e:
        logger.error(f"Error formatting task: {str(e)}")
        print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Exit(code=1) from e


# ------------------------------------------------------------------ #
# AI Project Manager Commands
# ------------------------------------------------------------------ #


@app.command("process-goal")
def process_goal(
    goal_description: str = typer.Argument(..., help="High-level goal description"),
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
    """Process a high-level goal through the AI Project Manager pipeline.

    Examples
    --------
    uv run python -m backend.app.cli process-goal "Build a web application for task management"
    uv run python -m backend.app.cli process-goal "Fix login bug" --title "Login Bug Fix" --context "Users report being unable to log in with correct credentials"
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


@app.command("aipm-process-initiative")
def aipm_process_initiative(
    initiative_goal_description: str = typer.Argument(..., help="Initiative goal description"),
    pretty: bool = typer.Option(
        True,
        "--pretty/--compact",
        help="Format JSON output with indentation for readability",
    ),
) -> None:
    """Process an initiative goal through the AI Project Manager V0 pipeline.

    This command takes a string for an "Initiative Goal," invokes the V0 pipeline,
    and pretty-prints the resulting list of (mocked) DevinTicket objects to the console.

    Examples
    --------
    uv run python -m backend.app.cli aipm-process-initiative "Build a web application for task management"
    uv run python -m backend.app.cli aipm-process-initiative "Create a mobile app for inventory tracking" --compact
    """
    logger.info(f"Processing initiative goal: {initiative_goal_description}")

    if not initiative_goal_description or initiative_goal_description.strip() == "":
        logger.error("Error: Initiative goal description cannot be empty")
        print("[bold red]Error:[/] Initiative goal description cannot be empty")
        raise typer.Exit(code=1)

    try:
        initiative_id = f"initiative-{hash(initiative_goal_description) % 10000}"
        initiative_goal = InitiativeGoal(
            id=initiative_id,
            title=f"Initiative: {initiative_goal_description[:30]}...",
            description=initiative_goal_description,
        )

        master_orchestrator_agent = MasterOrchestratorAgent()

        tickets = master_orchestrator_agent.process_initiative(initiative_goal)

        ticket_dicts = [dataclasses.asdict(ticket) for ticket in tickets]

        indent = 2 if pretty else None
        formatted_json = json.dumps(ticket_dicts, indent=indent)
        print(formatted_json)
        logger.info(f"Generated {len(tickets)} tickets for initiative: {initiative_goal.title}")

    except Exception as e:
        logger.error(f"Error processing initiative: {str(e)}")
        print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Exit(code=1) from e


# ------------------------------------------------------------------ #
#  Python ‑m entry shim
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    app()
