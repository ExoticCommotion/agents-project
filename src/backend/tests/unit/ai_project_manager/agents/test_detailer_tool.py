"""
Unit tests for the Detailer Tool Agent.
"""

from backend.app.core.data_models import DevinTicket, StructuredPlan
from backend.app.custom_agents.ai_project_manager.tools.detailer_tool import DetailerTool


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
    plan = StructuredPlan(
        goal_id="goal-123",
        plan_id="plan-456",
        title="Test Plan",
        description="This is a test plan",
        steps=["Step 1: Do something", "Step 2: Do something else"],
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
    """Test that the create_ticket method handles out of range step indices."""
    tool = DetailerTool()
    plan = StructuredPlan(
        goal_id="goal-123",
        plan_id="plan-456",
        title="Test Plan",
        description="This is a test plan",
        steps=["Step 1: Do something"],
        estimated_complexity=3,
        estimated_time="2 days",
    )

    ticket = tool.create_ticket(plan, 5)  # Out of range index

    assert isinstance(ticket, DevinTicket)
    assert ticket.ticket_id is not None
    assert ticket.epic_id is not None
    assert ticket.title is not None
    assert ticket.description is not None
