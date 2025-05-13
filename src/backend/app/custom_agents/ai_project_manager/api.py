"""
API interface for the AI Project Manager.

This module provides a FastAPI interface for interacting with the
AI Project Manager system.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai_project_manager.core.data_models import HighLevelGoal
from ai_project_manager.core.pipeline import PipelineOrchestrator
from backend.app.utils.logger import get_logger

router = APIRouter(prefix="/aipm", tags=["AI Project Manager"])
logger = get_logger(__name__)


class GoalRequest(BaseModel):
    """Request model for goal processing."""

    description: str
    title: str | None = None
    context: str | None = None


class ProposalResponse(BaseModel):
    """Response model for learning proposals."""

    proposal_id: str
    title: str
    description: str
    impact_areas: list[str]
    implementation_steps: list[str]


@router.post("/process-goal", response_model=ProposalResponse)
async def process_goal(request: GoalRequest) -> ProposalResponse:
    """
    Process a high-level goal through the AI Project Manager pipeline.

    Args:
        request: The goal request containing description, title, and context

    Returns:
        A learning proposal based on the processed goal
    """
    logger.info(f"Processing goal: {request.title or request.description[:30]}")

    if not request.description or request.description.strip() == "":
        logger.error("Error: Goal description cannot be empty")
        raise HTTPException(status_code=400, detail="Goal description cannot be empty")

    try:
        goal_id = f"goal-{hash(request.description) % 10000}"
        goal = HighLevelGoal(
            id=goal_id,
            title=request.title or f"Goal: {request.description[:30]}...",
            description=request.description,
            context=request.context,
        )

        orchestrator = PipelineOrchestrator()
        learning_proposal = orchestrator.run_placeholder_pipeline(goal)

        response = ProposalResponse(
            proposal_id=learning_proposal.proposal_id,
            title=learning_proposal.title,
            description=learning_proposal.description,
            impact_areas=learning_proposal.impact_areas,
            implementation_steps=learning_proposal.implementation_steps,
        )

        logger.info(f"Goal processing completed successfully: {response.proposal_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing goal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing goal: {str(e)}") from e
