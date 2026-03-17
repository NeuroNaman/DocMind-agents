"""
Tests for fallback agent.
"""

from unittest.mock import MagicMock, patch

from app.agents.fallback import FallbackAgent, fallback_agent


class TestFallbackAgent:
    """Tests for FallbackAgent class."""

    @patch("app.agents.fallback.get_wikipedia_service")
    def test_execute_with_wikipedia_success(self, mock_get_service):
        """Test execute with successful Wikipedia search."""
        mock_service = MagicMock()
        mock_service.search.return_value = "Wikipedia result about Python."
        mock_get_service.return_value = mock_service

        agent = FallbackAgent()
        state = {"input": "What is Python?"}

        result = agent.execute(state)

        assert "Wikipedia" in result["answer"]
        assert "Python" in result["answer"]
        assert result["source"] == "wikipedia"
        assert result["next_agent"] == "executor_agent"

    def test_execute_with_no_question(self):
        """Test execute with no question."""
        agent = FallbackAgent()
        state = {"input": ""}

        result = agent.execute(state)

        assert "No question was provided" in result["answer"]
        assert result["source"] == "error"
        assert result["next_agent"] == "executor_agent"

    def test_execute_with_missing_input(self):
        """Test execute with missing input key."""
        agent = FallbackAgent()
        state = {}

        result = agent.execute(state)

        assert result["source"] == "error"

    @patch("app.agents.fallback.get_wikipedia_service")
    def test_execute_with_wikipedia_no_results(self, mock_get_service):
        """Test execute with Wikipedia returning no results."""
        mock_service = MagicMock()
        mock_service.search.return_value = None
        mock_get_service.return_value = mock_service

        agent = FallbackAgent()
        state = {"input": "XYZ123 nonexistent topic"}

        result = agent.execute(state)

        assert "couldn't find" in result["answer"].lower()
        assert result["source"] == "wikipedia"

    @patch("app.agents.fallback.get_wikipedia_service")
    def test_execute_with_wikipedia_empty_result(self, mock_get_service):
        """Test execute with Wikipedia returning empty string."""
        mock_service = MagicMock()
        mock_service.search.return_value = ""
        mock_get_service.return_value = mock_service

        agent = FallbackAgent()
        state = {"input": "Test query"}

        result = agent.execute(state)

        assert "couldn't find" in result["answer"].lower()

    @patch("app.agents.fallback.get_wikipedia_service")
    def test_execute_with_wikipedia_exception(self, mock_get_service):
        """Test execute with Wikipedia raising exception."""
        mock_service = MagicMock()
        mock_service.search.side_effect = Exception("API error")
        mock_get_service.return_value = mock_service

        agent = FallbackAgent()
        state = {"input": "Test question"}

        result = agent.execute(state)

        assert "couldn't find" in result["answer"].lower()
        assert result["source"] == "error"


class TestFallbackAgentFunction:
    """Tests for fallback_agent standalone function."""

    @patch("app.agents.fallback.get_wikipedia_service")
    def test_fallback_agent_function(self, mock_get_service):
        """Test standalone fallback_agent function."""
        mock_service = MagicMock()
        mock_service.search.return_value = "Result"
        mock_get_service.return_value = mock_service

        state = {"input": "Test query"}

        result = fallback_agent(state)

        assert "answer" in result
        assert "source" in result
