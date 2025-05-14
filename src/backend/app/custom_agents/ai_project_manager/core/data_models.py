"""
Data models for the AI Project Manager core components.

This module defines the data models used by the AI Project Manager core components.
"""

from dataclasses import dataclass
from typing import Any

__all__ = ["DecompositionPlan", "WorkPackage", "InitiativeGoal"]


@dataclass
class InitiativeGoal:
    """High-level initiative goal to be processed by the AI Project Manager."""

    id: str
    title: str
    description: str
    context: str | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class WorkPackage:
    """Work package created as part of a decomposition plan."""

    package_id: str
    plan_id: str
    title: str
    description: str
    tasks: list[str]
    estimated_complexity: int
    estimated_time: str
    dependencies: list[str] | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class DecompositionPlan:
    """Decomposition plan created from a high-level initiative goal."""

    goal_id: str
    plan_id: str
    title: str
    description: str
    work_packages: list[WorkPackage]
    estimated_complexity: int
    estimated_time: str
    metadata: dict[str, Any] | None = None
