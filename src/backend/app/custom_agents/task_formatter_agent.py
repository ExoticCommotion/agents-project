"""
Task Formatter Agent Module

This module provides functionality to transform natural language task descriptions
into structured JSON task definitions using the OpenAI Agents SDK.
"""

import json
from enum import Enum
from typing import Any, Dict, Optional, Union

from agents import Agent, Runner
from agents.exceptions import AgentError, APIError, APIStatusError, RateLimitError
from pydantic import BaseModel, Field

from backend.app.utils.logger import get_logger

logger = get_logger(__name__)


class TaskFormatterErrorType(str, Enum):
    """Enumeration of possible error types in the task formatter."""

    VALIDATION_ERROR = "validation_error"
    API_ERROR = "api_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    AUTHENTICATION_ERROR = "authentication_error"
    SERVER_ERROR = "server_error"
    PARSING_ERROR = "parsing_error"
    UNKNOWN_ERROR = "unknown_error"


class TaskFormatterError(Exception):
    """Base exception for task formatter errors."""

    def __init__(
        self,
        message: str,
        error_type: TaskFormatterErrorType = TaskFormatterErrorType.UNKNOWN_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_type = error_type
        self.details = details or {}
        super().__init__(message)


class ValidationError(TaskFormatterError):
    """Exception raised for input validation errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message, error_type=TaskFormatterErrorType.VALIDATION_ERROR, details=details
        )


class ParsingError(TaskFormatterError):
    """Exception raised for JSON parsing errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message, error_type=TaskFormatterErrorType.PARSING_ERROR, details=details
        )


class TaskFormatterResponse(BaseModel):
    """Response model for task formatter operations."""

    success: bool = Field(description="Whether the operation was successful")
    data: Optional[Dict[str, Any]] = Field(
        default=None, description="The formatted task data if successful"
    )
    error: Optional[Dict[str, Any]] = Field(
        default=None, description="Error details if unsuccessful"
    )


class TaskDefinition(BaseModel):
    """Structured task definition model."""

    title: str = Field(description="Brief task title")
    goal: str = Field(description="What the feature or bug fix achieves")
    input: str = Field(description="Input expectations (CLI args, API behavior, files touched)")
    output: str = Field(description="Output expectations (stdout, files, etc.)")
    verify: list[str] = Field(description="Test names, command output, or other pass/fail signals")
    notes: list[str] = Field(description="Important hints, constraints, or potential pitfalls")


def validate_task_description(task_description: str) -> None:
    """
    Validate the task description input.

    Args:
        task_description: The natural language description of the task.

    Raises:
        ValidationError: If the task description is invalid.
    """
    if not task_description:
        raise ValidationError("Task description cannot be empty")

    if len(task_description) < 10:
        raise ValidationError(
            "Task description is too short",
            details={"min_length": 10, "actual_length": len(task_description)},
        )

    if len(task_description) > 8000:
        raise ValidationError(
            "Task description is too long",
            details={"max_length": 8000, "actual_length": len(task_description)},
        )


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


async def format_task(task_description: str) -> TaskFormatterResponse:
    """
    Transform a natural language task description into a structured JSON task definition.

    Args:
        task_description: The natural language description of the task.

    Returns:
        A TaskFormatterResponse containing either the structured task definition or error details.
    """
    logger.info("⏳ Starting task formatting process...")
    logger.debug(f"Processing task description: {task_description[:100]}...")

    try:
        validate_task_description(task_description)

        agent = create_task_formatter_agent()
        result = await Runner.run(agent, input=task_description)
        response = str(result.final_output)

        task_json = _parse_json_response(response)

        logger.info("✅ Task formatting completed successfully")
        return TaskFormatterResponse(success=True, data=task_json)

    except ValidationError as e:
        logger.error(f"Validation error: {e.message}")
        return TaskFormatterResponse(
            success=False,
            error={
                "type": e.error_type,
                "message": e.message,
                "details": e.details,
            },
        )
    except ParsingError as e:
        logger.error(f"Parsing error: {e.message}")
        return TaskFormatterResponse(
            success=False,
            error={
                "type": e.error_type,
                "message": e.message,
                "details": e.details,
            },
        )
    except RateLimitError as e:
        logger.error(f"Rate limit error: {str(e)}")
        return TaskFormatterResponse(
            success=False,
            error={
                "type": TaskFormatterErrorType.RATE_LIMIT_ERROR,
                "message": f"OpenAI API rate limit exceeded: {str(e)}",
                "details": {"original_error": str(e)},
            },
        )
    except APIStatusError as e:
        error_type = TaskFormatterErrorType.API_ERROR
        if e.status_code == 401:
            error_type = TaskFormatterErrorType.AUTHENTICATION_ERROR
            logger.error(f"Authentication error: {str(e)}")
        elif e.status_code >= 500:
            error_type = TaskFormatterErrorType.SERVER_ERROR
            logger.error(f"Server error: {str(e)}")
        else:
            logger.error(f"API error: {str(e)}")

        return TaskFormatterResponse(
            success=False,
            error={
                "type": error_type,
                "message": f"OpenAI API error: {str(e)}",
                "details": {"status_code": e.status_code, "original_error": str(e)},
            },
        )
    except (APIError, AgentError) as e:
        logger.error(f"API error: {str(e)}")
        return TaskFormatterResponse(
            success=False,
            error={
                "type": TaskFormatterErrorType.API_ERROR,
                "message": f"OpenAI API error: {str(e)}",
                "details": {"original_error": str(e)},
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return TaskFormatterResponse(
            success=False,
            error={
                "type": TaskFormatterErrorType.UNKNOWN_ERROR,
                "message": f"Unexpected error: {str(e)}",
                "details": {"original_error": str(e)},
            },
        )


def format_task_sync(task_description: str) -> TaskFormatterResponse:
    """
    Transform a natural language task description into a structured JSON task definition synchronously.

    Args:
        task_description: The natural language description of the task.

    Returns:
        A TaskFormatterResponse containing either the structured task definition or error details.
    """
    logger.info("⏳ Starting task formatting process (sync)...")
    logger.debug(f"Processing task description: {task_description[:100]}...")

    try:
        validate_task_description(task_description)

        agent = create_task_formatter_agent()
        result = Runner.run_sync(agent, input=task_description)
        response = str(result.final_output)

        task_json = _parse_json_response(response)

        logger.info("✅ Task formatting completed successfully")
        return TaskFormatterResponse(success=True, data=task_json)

    except ValidationError as e:
        logger.error(f"Validation error: {e.message}")
        return TaskFormatterResponse(
            success=False,
            error={
                "type": e.error_type,
                "message": e.message,
                "details": e.details,
            },
        )
    except ParsingError as e:
        logger.error(f"Parsing error: {e.message}")
        return TaskFormatterResponse(
            success=False,
            error={
                "type": e.error_type,
                "message": e.message,
                "details": e.details,
            },
        )
    except RateLimitError as e:
        logger.error(f"Rate limit error: {str(e)}")
        return TaskFormatterResponse(
            success=False,
            error={
                "type": TaskFormatterErrorType.RATE_LIMIT_ERROR,
                "message": f"OpenAI API rate limit exceeded: {str(e)}",
                "details": {"original_error": str(e)},
            },
        )
    except APIStatusError as e:
        error_type = TaskFormatterErrorType.API_ERROR
        if e.status_code == 401:
            error_type = TaskFormatterErrorType.AUTHENTICATION_ERROR
            logger.error(f"Authentication error: {str(e)}")
        elif e.status_code >= 500:
            error_type = TaskFormatterErrorType.SERVER_ERROR
            logger.error(f"Server error: {str(e)}")
        else:
            logger.error(f"API error: {str(e)}")

        return TaskFormatterResponse(
            success=False,
            error={
                "type": error_type,
                "message": f"OpenAI API error: {str(e)}",
                "details": {"status_code": e.status_code, "original_error": str(e)},
            },
        )
    except (APIError, AgentError) as e:
        logger.error(f"API error: {str(e)}")
        return TaskFormatterResponse(
            success=False,
            error={
                "type": TaskFormatterErrorType.API_ERROR,
                "message": f"OpenAI API error: {str(e)}",
                "details": {"original_error": str(e)},
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return TaskFormatterResponse(
            success=False,
            error={
                "type": TaskFormatterErrorType.UNKNOWN_ERROR,
                "message": f"Unexpected error: {str(e)}",
                "details": {"original_error": str(e)},
            },
        )


def _parse_json_response(response: str) -> dict[str, Any]:
    """
    Parse the JSON response from the agent.

    Args:
        response: The agent's response text.

    Returns:
        The parsed JSON as a dictionary.

    Raises:
        ParsingError: If the response cannot be parsed as valid JSON.
    """
    if not response:
        logger.error("Empty response from agent")
        raise ParsingError("Empty response from agent")

    try:
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]

        cleaned_response = cleaned_response.strip()

        if not cleaned_response:
            logger.error("Empty JSON content after cleaning")
            raise ParsingError("Empty JSON content after cleaning", details={"original_response": response})

        task_json: dict[str, Any] = json.loads(cleaned_response)
        
        # Validate that the required fields are present
        required_fields = ["title", "goal", "input", "output", "verify", "notes"]
        missing_fields = [field for field in required_fields if field not in task_json]
        
        if missing_fields:
            logger.error(f"Missing required fields in JSON response: {missing_fields}")
            raise ParsingError(
                f"Missing required fields in JSON response: {', '.join(missing_fields)}",
                details={"missing_fields": missing_fields, "parsed_json": task_json},
            )
            
        logger.debug("Successfully parsed JSON response")
        return task_json
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {str(e)}")
        logger.error(f"Response was: {response}")
        raise ParsingError(
            f"Invalid JSON response from agent: {str(e)}",
            details={"original_response": response, "error_message": str(e)},
        ) from e
