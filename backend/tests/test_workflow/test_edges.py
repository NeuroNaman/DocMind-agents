"""
Tests for workflow edge routing functions.
"""

from app.workflow.edges import (
    has_error,
    route_after_planner,
    route_after_tool_router,
    should_use_rag,
)


class TestRouteAfterPlanner:
    """Tests for route_after_planner function."""

    def test_routes_to_retriever(self):
        """Test routing to retriever agent."""
        state = {"next_agent": "retriever_agent"}
        result = route_after_planner(state)
        assert result == "retriever_agent"

    def test_routes_to_fallback(self):
        """Test routing to fallback agent."""
        state = {"next_agent": "fallback_agent"}
        result = route_after_planner(state)
        assert result == "fallback_agent"

    def test_default_routes_to_fallback(self):
        """Test default routing is to fallback."""
        state = {}
        result = route_after_planner(state)
        assert result == "fallback_agent"

    def test_unknown_agent_routes_to_fallback(self):
        """Test unknown agent routes to fallback."""
        state = {"next_agent": "unknown_agent"}
        result = route_after_planner(state)
        assert result == "fallback_agent"


class TestRouteAfterToolRouter:
    """Tests for route_after_tool_router function."""

    def test_routes_to_ingestion(self):
        """Test routing to ingestion agent."""
        state = {"next_agent": "ingestion_agent"}
        result = route_after_tool_router(state)
        assert result == "ingestion_agent"

    def test_routes_to_planner(self):
        """Test routing to planner agent."""
        state = {"next_agent": "planner_agent"}
        result = route_after_tool_router(state)
        assert result == "planner_agent"

    def test_default_routes_to_planner(self):
        """Test default routing is to planner."""
        state = {}
        result = route_after_tool_router(state)
        assert result == "planner_agent"


class TestShouldUseRag:
    """Tests for should_use_rag function."""

    def test_returns_true_with_context(self):
        """Test returns True when context exists."""
        state = {"context": ["chunk1", "chunk2"]}
        assert should_use_rag(state) is True

    def test_returns_false_without_context(self):
        """Test returns False when no context."""
        state = {"context": []}
        assert should_use_rag(state) is False

    def test_returns_false_with_missing_context(self):
        """Test returns False when context key missing."""
        state = {}
        assert should_use_rag(state) is False


class TestHasError:
    """Tests for has_error function."""

    def test_returns_true_with_error(self):
        """Test returns True when error exists."""
        state = {"error": "Something went wrong"}
        assert has_error(state) is True

    def test_returns_false_without_error(self):
        """Test returns False when no error."""
        state = {"error": None}
        assert has_error(state) is False

    def test_returns_false_with_empty_error(self):
        """Test returns False when error is empty string."""
        state = {"error": ""}
        assert has_error(state) is False

    def test_returns_false_with_missing_error(self):
        """Test returns False when error key missing."""
        state = {}
        assert has_error(state) is False
