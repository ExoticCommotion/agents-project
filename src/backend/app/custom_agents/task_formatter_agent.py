"""
Task Formatter Agent Module

This module provides functionality to transform natural language task descriptions
into structured JSON task definitions using the OpenAI Agents SDK.
"""

import json
from typing import Any

from agents import Agent, Runner
from pydantic import BaseModel, Field

from backend.app.utils.logger import get_logger

logger = get_logger(__name__)


class TaskDefinition(BaseModel):
    """Structured task definition model."""

    title: str = Field(description="Brief task title")
    goal: str = Field(description="What the feature or bug fix achieves")
    input: str = Field(description="Input expectations (CLI args, API behavior, files touched)")
    output: str = Field(description="Output expectations (stdout, files, etc.)")
    verify: list[str] = Field(description="Test names, command output, or other pass/fail signals")
    notes: list[str] = Field(description="Important hints, constraints, or potential pitfalls")


def create_task_formatter_agent() -> Agent:
    """
    Create an agent that transforms natural language task descriptions into structured JSON.

    Returns:
        A configured Agent instance.
    """
    return Agent(
        name="TaskFormatter",
        instructions="""
        You are a specialized assistant that transforms natural language task descriptions
        into structured JSON task definitions. Your job is to extract key information from
        the task description and format it according to the following schema:

        {
            "title": "Brief task title",
            "goal": "What the feature or bug fix achieves",
            "input": "Input expectations (CLI args, API behavior, files touched)",
            "output": "Output expectations (stdout, files, etc.)",
            "verify": [
                "Test names, command output, or other pass/fail signals"
            ],
            "notes": [
                "Important hints, constraints, or potential pitfalls"
            ]
        }

        Always respond with valid JSON only, no additional text.
        """,
        model="gpt-4o",
    )


async def format_task(task_description: str) -> dict[str, Any]:
    """
    Transform a natural language task description into a structured JSON task definition.

    Args:
        task_description: The natural language description of the task.

    Returns:
        A dictionary containing the structured task definition.
    """
    logger.info("⏳ Starting task formatting process...")
    logger.debug(f"Processing task description: {task_description[:100]}...")

    try:
        agent = create_task_formatter_agent()
        result = await Runner.run(agent, input=task_description)
        response = str(result.final_output)

        task_json = _parse_json_response(response)

        logger.info("✅ Task formatting completed successfully")
        return task_json

    except Exception as e:
        logger.error(f"Error formatting task: {str(e)}")
        raise


def format_task_sync(task_description: str) -> dict[str, Any]:
    """
    Transform a natural language task description into a structured JSON task definition synchronously.

    Args:
        task_description: The natural language description of the task.

    Returns:
        A dictionary containing the structured task definition.
    """
    logger.info("⏳ Starting task formatting process (sync)...")
    logger.debug(f"Processing task description: {task_description[:100]}...")

    try:
        agent = create_task_formatter_agent()
        result = Runner.run_sync(agent, input=task_description)
        response = str(result.final_output)

        task_json = _parse_json_response(response)

        logger.info("✅ Task formatting completed successfully")
        return task_json

    except Exception as e:
        logger.error(f"Error formatting task: {str(e)}")
        raise


def _parse_json_response(response: str) -> dict[str, Any]:
    """
    Parse the JSON response from the agent.

    Args:
        response: The agent's response text.

    Returns:
        The parsed JSON as a dictionary.
    """
    try:
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]

        cleaned_response = cleaned_response.strip()

        task_json: dict[str, Any] = json.loads(cleaned_response)
        logger.debug("Successfully parsed JSON response")
        return task_json
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {str(e)}")
        logger.error(f"Response was: {response}")
        raise ValueError(f"Invalid JSON response from agent: {str(e)}") from e
