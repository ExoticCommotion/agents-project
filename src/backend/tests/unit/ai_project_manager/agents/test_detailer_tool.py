"""
Unit tests for the Detailer Tool Agent.
"""

from backend.app.core.data_models import DevinTicket
from backend.app.custom_agents.ai_project_manager.agents.detailer_tool import DetailerTool
from backend.app.custom_agents.ai_project_manager.core.data_models import (
    DecompositionPlan,
    WorkPackage,
)


def test_detailer_tool_exists() -> None:
    """Test that the DetailerTool class exists."""
    assert DetailerTool is not None


def test_detailer_tool_initialization() -> None:
    """Test that a DetailerTool can be initialized."""
    tool = DetailerTool()
    assert isinstance(tool, DetailerTool)


def test_create_ticket() -> None:
    """Test that the create_ticket method returns a DevinTicket."""
    tool = DetailerTool()
    work_package = WorkPackage(
        package_id="package-789",
        plan_id="plan-456",
        title="Test Work Package",
        description="This is a test work package",
        tasks=["Task 1: Do something", "Task 2: Do something else"],
        estimated_complexity=2,
        estimated_time="1 day",
    )
    plan = DecompositionPlan(
        goal_id="goal-123",
        plan_id="plan-456",
        title="Test Plan",
        description="This is a test plan",
        work_packages=[work_package],
        estimated_complexity=3,
        estimated_time="2 days",
    )

    ticket = tool.create_ticket(plan, 0)

    assert isinstance(ticket, DevinTicket)
    assert ticket.ticket_id is not None
    assert ticket.epic_id is not None
    assert ticket.title is not None
    assert ticket.description is not None
    assert len(ticket.input_files) > 0
    assert ticket.output_expectation is not None
    assert len(ticket.acceptance_criteria) > 0
    assert ticket.priority > 0
    assert ticket.status is not None


def test_create_ticket_out_of_range() -> None:
    """Test that the create_ticket method handles out of range work package indices."""
    tool = DetailerTool()
    work_package = WorkPackage(
        package_id="package-789",
        plan_id="plan-456",
        title="Test Work Package",
        description="This is a test work package",
        tasks=["Task 1: Do something"],
        estimated_complexity=2,
        estimated_time="1 day",
    )
    plan = DecompositionPlan(
        goal_id="goal-123",
        plan_id="plan-456",
        title="Test Plan",
        description="This is a test plan",
        work_packages=[work_package],
        estimated_complexity=3,
        estimated_time="2 days",
    )

    ticket = tool.create_ticket(plan, 5)  # Out of range index

    assert isinstance(ticket, DevinTicket)
    assert ticket.ticket_id is not None
    assert ticket.epic_id is not None
    assert ticket.title is not None
    assert ticket.description is not None
