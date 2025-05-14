"""
Project Orchestrator for the AI Project Manager.

This module defines the Project Orchestrator, which is responsible for orchestrating
the flow of data between the different agents in the AI Project Manager.
"""

from backend.app.core.data_models import (
    DevinTicket,
    HighLevelGoal,
    InitiativeGoal,
    LearningProposal,
)
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)


class ProjectOrchestrator:
    """
    Orchestrator for the AI Project Manager pipeline.

    The Project Orchestrator is responsible for orchestrating the flow of data between
    the different agents in the AI Project Manager.
    """

    def __init__(self) -> None:
        """Initialize the Project Orchestrator."""
        logger.info("Initializing Project Orchestrator")
        from backend.app.agents.execution_coordinator import (
            ExecutionCoordinatorAgent,
        )
        from backend.app.agents.feedback_analyzer import FeedbackAnalyzerAgent
        from backend.app.agents.feedback_synthesizer import (
            FeedbackSynthesizerAgent,
        )
        from backend.app.agents.planner import PlannerAgent
        from backend.app.agents.prioritizer import PrioritizerAgent
        from backend.app.agents.task_definer import TaskDefinerAgent
        from backend.app.tools.devin_session_manager import DevinSessionManager

        self.planner = PlannerAgent()
        self.task_definer = TaskDefinerAgent()
        self.prioritizer = PrioritizerAgent()
        self.execution_coordinator = ExecutionCoordinatorAgent()
        self.feedback_analyzer = FeedbackAnalyzerAgent()
        self.feedback_synthesizer = FeedbackSynthesizerAgent()
        self.devin_session_manager = DevinSessionManager()

    def run_placeholder_pipeline(self, goal: HighLevelGoal) -> LearningProposal:
        """
        Run a placeholder pipeline for the AI Project Manager.

        This is a simplified version of the pipeline that returns a placeholder
        learning proposal. In a real implementation, this would orchestrate the
        flow of data between the different agents.

        Args:
            goal: The high-level goal to process

        Returns:
            A learning proposal based on the processed goal
        """
        logger.info(f"Running placeholder pipeline for goal: {goal.title}")
        return LearningProposal(
            proposal_id=f"proposal-{hash(goal.description) % 10000}",
            title=f"Learning Proposal for {goal.title}",
            description=f"This is a learning proposal for the goal: {goal.description}",
            impact_areas=["Process Improvement", "Tool Integration"],
            implementation_steps=[
                "Step 1: Implement core functionality",
                "Step 2: Add integration tests",
                "Step 3: Deploy to production",
            ],
        )

    def process_initiative(self, initiative_goal: InitiativeGoal) -> list[DevinTicket]:
        """
        Process an initiative goal through the AIPM pipeline.

        This method orchestrates the execution of the pipeline by:
        1. Using the Planner to create a decomposition plan from the initiative goal
        2. Using the TaskDefiner to create detailed tickets for each work package in the plan
        3. Using the Prioritizer to prioritize the tickets
        4. Aggregating all tickets and returning them

        Args:
            initiative_goal: The initiative goal to process

        Returns:
            A list of Devin tickets generated from the initiative goal
        """
        logger.info(f"Processing initiative: {initiative_goal.title}")

        from backend.app.agents.detailer_tool import DetailerTool
        from backend.app.agents.planner_tool import PlannerTool

        planner_tool = PlannerTool()
        detailer_tool = DetailerTool()

        plan = planner_tool.plan_initiative(initiative_goal)

        tickets = []
        for work_package in plan.work_packages:
            work_package_tickets = detailer_tool.detail_work_package(work_package)
            tickets.extend(work_package_tickets)

        return tickets
