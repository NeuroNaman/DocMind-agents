"""
Tests for Planner Agent.
"""

from unittest.mock import MagicMock, patch

from app.agents.planner import PlannerAgent, planner_agent


class TestPlannerAgent:
    """Test cases for PlannerAgent."""

    @patch("app.agents.planner.get_vector_store")
    def test_routes_to_retriever_with_documents(self, mock_get_store, initial_state):
        """Test routing to retriever when documents exist."""
        mock_store = MagicMock()
        mock_store.has_documents.return_value = True
        mock_store.get_document_count.return_value = 5
        mock_get_store.return_value = mock_store

        agent = PlannerAgent()
        result = agent.execute(initial_state)

        assert result["next_agent"] == "retriever_agent"

    @patch("app.agents.planner.get_vector_store")
    def test_routes_to_fallback_without_documents(self, mock_get_store, initial_state):
        """Test routing to fallback when no documents exist."""
        mock_store = MagicMock()
        mock_store.has_documents.return_value = False
        mock_store.get_document_count.return_value = 0
        mock_get_store.return_value = mock_store

        result = planner_agent(initial_state)

        assert result["next_agent"] == "fallback_agent"
