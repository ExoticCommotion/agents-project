"""
Unit tests for the AI Project Manager Detailer Tool Agent.
"""


from backend.app.core.data_models import DevinTicket
from backend.app.custom_agents.ai_project_manager.agents.detailer_tool import DetailerTool
from backend.app.custom_agents.ai_project_manager.core.data_models import WorkPackage


def test_detailer_tool_exists() -> None:
    """Test that the DetailerTool class exists."""
    assert DetailerTool is not None


def test_detailer_tool_initialization() -> None:
    """Test that a DetailerTool can be initialized."""
    tool = DetailerTool()
    assert isinstance(tool, DetailerTool)


def test_detail_work_package() -> None:
    """Test that the detail_work_package method returns a list of DevinTickets."""
    tool = DetailerTool()
    work_package = WorkPackage(
        package_id="wp-123",
        plan_id="plan-456",
        title="Test Work Package",
        description="This is a test work package",
        tasks=["Task 1: Do something", "Task 2: Do something else"],
        estimated_complexity=3,
        estimated_time="2 days",
    )

    tickets = tool.detail_work_package(work_package)

    assert isinstance(tickets, list)
    assert len(tickets) > 0
    assert all(isinstance(ticket, DevinTicket) for ticket in tickets)
    assert len(tickets) == len(work_package.tasks)

    for ticket in tickets:
        assert ticket.ticket_id is not None
        assert ticket.epic_id is not None
        assert ticket.title is not None
        assert ticket.description is not None
        assert len(ticket.input_files) > 0
        assert ticket.output_expectation is not None
        assert len(ticket.acceptance_criteria) > 0
        assert ticket.priority > 0
        assert ticket.status is not None
