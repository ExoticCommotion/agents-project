"""
Main application for the Agents Project.

This module provides the FastAPI application for the Agents Project.
"""

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from backend.app.custom_agents.ai_project_manager.api import router as aipm_router
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Agents Project API")


class TaskRequest(BaseModel):
    """Request model for task formatting."""

    task_description: str


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


# Include the AI Project Manager router
app.include_router(aipm_router)


def run_app() -> None:
    """Run the FastAPI application."""
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_app()
