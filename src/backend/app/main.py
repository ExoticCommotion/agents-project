"""
Main application for the Devin Task Formatter Agent.

This module provides the FastAPI application for the Devin Task Formatter Agent.
"""

from __future__ import annotations

from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from backend.app.custom_agents.task_formatter_agent import format_task
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Devin Task Formatter Agent")


class TaskRequest(BaseModel):
    """Request model for task formatting."""

    task_description: str


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/format-task/", status_code=status.HTTP_200_OK)
async def format_task_endpoint(request: TaskRequest) -> dict[str, Any]:
    """
    Transform a natural language task description into a structured JSON task definition.

    Args:
        request: The request containing the task description.

    Returns:
        A JSON response containing either the structured task definition or error details.

    Raises:
        HTTPException: If the task description is invalid or an error occurs during processing.
    """
    logger.info("Received request to format task")
    logger.debug(f"Task description: {request.task_description[:100]}...")

    response = await format_task(request.task_description)

    if not response.success:
        error_type = "unknown_error"
        error_message = "An unknown error occurred"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if response.error:
            error_type = response.error.get("type", error_type)
            error_message = response.error.get("message", error_message)

            if error_type == "validation_error":
                status_code = status.HTTP_400_BAD_REQUEST
            elif error_type == "authentication_error":
                status_code = status.HTTP_401_UNAUTHORIZED
            elif error_type == "rate_limit_error":
                status_code = status.HTTP_429_TOO_MANY_REQUESTS

        logger.error(f"Error formatting task: {error_message}")
        raise HTTPException(
            status_code=status_code,
            detail={
                "success": False,
                "error": {
                    "type": error_type,
                    "message": error_message,
                    "details": response.error.get("details", {}) if response.error else {},
                },
            },
        )

    logger.info("Task formatting completed successfully")
    return {"success": True, "data": response.data}


def run_app() -> None:
    """Run the FastAPI application."""
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_app()
