"""
Data models for the AI Project Manager.

This module defines the data models used by the AI Project Manager system.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class HighLevelGoal:
    """High-level goal to be processed by the AI Project Manager."""

    id: str
    title: str
    description: str
    context: str | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class StructuredPlan:
    """Structured plan created from a high-level goal."""

    goal_id: str
    plan_id: str
    title: str
    description: str
    steps: list[str]
    estimated_complexity: int
    estimated_time: str
    dependencies: list[str] | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class Epic:
    """Epic created from a structured plan."""

    epic_id: str
    plan_id: str
    title: str
    description: str
    priority: int
    status: str
    metadata: dict[str, Any] | None = None


@dataclass
class DevinTicket:
    """Ticket to be executed by Devin."""

    ticket_id: str
    epic_id: str
    title: str
    description: str
    input_files: list[str]
    output_expectation: str
    acceptance_criteria: list[str]
    priority: int
    status: str
    metadata: dict[str, Any] | None = None


@dataclass
class ExecutionResult:
    """Result of executing a Devin ticket."""

    ticket_id: str
    status: str
    output: str
    execution_time: str
    logs: str | None = None
    artifacts: list[str] | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class StructuredAnalysisReport:
    """Structured analysis report of an execution result."""

    report_id: str
    ticket_id: str
    success_factors: list[str]
    improvement_suggestions: list[str]
    failure_factors: list[str] | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class ActionDecision:
    """Decision about what action to take next."""

    decision_id: str
    ticket_id: str
    action_description: str
    rationale: str
    metadata: dict[str, Any] | None = None


@dataclass
class FeedbackContent:
    """Feedback content from a user or system."""

    feedback_id: str
    ticket_id: str
    content: str
    source: str
    sentiment: str
    metadata: dict[str, Any] | None = None


@dataclass
class LearningProposal:
    """Learning proposal based on feedback and analysis."""

    proposal_id: str
    title: str
    description: str
    impact_areas: list[str]
    implementation_steps: list[str]
    metadata: dict[str, Any] | None = None
