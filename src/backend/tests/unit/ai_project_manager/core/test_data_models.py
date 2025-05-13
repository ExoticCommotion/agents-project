"""
Unit tests for the data models.
"""

from backend.app.core.data_models import DevinTicket, Epic, HighLevelGoal, StructuredPlan


def test_high_level_goal() -> None:
    """Test that a HighLevelGoal can be created."""
    goal = HighLevelGoal(
        id="goal-123",
        title="Test Goal",
        description="This is a test goal",
    )

    assert goal.id == "goal-123"
    assert goal.title == "Test Goal"
    assert goal.description == "This is a test goal"
    assert goal.context is None
    assert goal.metadata is None


def test_structured_plan() -> None:
    """Test that a StructuredPlan can be created."""
    plan = StructuredPlan(
        goal_id="goal-123",
        plan_id="plan-456",
        title="Test Plan",
        description="This is a test plan",
        steps=["Step 1", "Step 2"],
        estimated_complexity=3,
        estimated_time="2 days",
    )

    assert plan.goal_id == "goal-123"
    assert plan.plan_id == "plan-456"
    assert plan.title == "Test Plan"
    assert plan.description == "This is a test plan"
    assert plan.steps == ["Step 1", "Step 2"]
    assert plan.estimated_complexity == 3
    assert plan.estimated_time == "2 days"
    assert plan.dependencies is None
    assert plan.metadata is None


def test_epic() -> None:
    """Test that an Epic can be created."""
    epic = Epic(
        epic_id="epic-789",
        plan_id="plan-456",
        title="Test Epic",
        description="This is a test epic",
        priority=1,
        status="pending",
    )

    assert epic.epic_id == "epic-789"
    assert epic.plan_id == "plan-456"
    assert epic.title == "Test Epic"
    assert epic.description == "This is a test epic"
    assert epic.priority == 1
    assert epic.status == "pending"
    assert epic.metadata is None


def test_devin_ticket() -> None:
    """Test that a DevinTicket can be created."""
    ticket = DevinTicket(
        ticket_id="ticket-101",
        epic_id="epic-789",
        title="Test Ticket",
        description="This is a test ticket",
        input_files=["file1.py", "file2.py"],
        output_expectation="Expected output",
        acceptance_criteria=["Criteria 1", "Criteria 2"],
        priority=2,
        status="ready",
    )

    assert ticket.ticket_id == "ticket-101"
    assert ticket.epic_id == "epic-789"
    assert ticket.title == "Test Ticket"
    assert ticket.description == "This is a test ticket"
    assert ticket.input_files == ["file1.py", "file2.py"]
    assert ticket.output_expectation == "Expected output"
    assert ticket.acceptance_criteria == ["Criteria 1", "Criteria 2"]
    assert ticket.priority == 2
    assert ticket.status == "ready"
    assert ticket.metadata is None
