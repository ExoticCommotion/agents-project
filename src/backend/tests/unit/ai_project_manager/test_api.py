"""
Unit tests for the AI Project Manager API.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from ai_project_manager.core.data_models import LearningProposal
from backend.app.custom_agents.ai_project_manager.api import router


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the API."""
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_api_router_exists() -> None:
    """Test that the API router exists."""
    assert router is not None


def test_process_goal_endpoint(client: TestClient) -> None:
    """Test that the process-goal endpoint works correctly."""
    with patch(
        "backend.app.custom_agents.ai_project_manager.api.PipelineOrchestrator"
    ) as MockOrchestrator:
        mock_orchestrator_instance = MagicMock()
        MockOrchestrator.return_value = mock_orchestrator_instance
        mock_orchestrator_instance.run_placeholder_pipeline.return_value = LearningProposal(
            proposal_id="proposal-test",
            title="Test Learning Proposal",
            description="This is a test learning proposal",
            impact_areas=["Test impact area"],
            implementation_steps=["Test implementation step"],
        )

        response = client.post(
            "/aipm/process-goal",
            json={
                "description": "Test goal description",
                "title": "Test Title",
                "context": "Test Context",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["proposal_id"] == "proposal-test"
        assert data["title"] == "Test Learning Proposal"
        assert data["description"] == "This is a test learning proposal"
        assert data["impact_areas"] == ["Test impact area"]
        assert data["implementation_steps"] == ["Test implementation step"]


def test_process_goal_empty_description(client: TestClient) -> None:
    """Test that the process-goal endpoint fails with an empty description."""
    response = client.post(
        "/aipm/process-goal",
        json={
            "description": "",
            "title": "Test Title",
            "context": "Test Context",
        },
    )

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()
