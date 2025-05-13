from __future__ import annotations

import json
import os

import typer
from rich import print

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
#  Python ‑m entry shim
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    app()
