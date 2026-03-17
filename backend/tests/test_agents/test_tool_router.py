"""
Tests for Tool Router Agent.
"""

from app.agents.tool_router import ToolRouterAgent, tool_router_agent


class TestToolRouterAgent:
    """Test cases for ToolRouterAgent."""

    def test_routes_to_ingestion_with_file(self, initial_state):
        """Test routing to ingestion when file is provided."""
        state = {
            **initial_state,
            "file_type": "pdf",
            "file_content": "/path/to/file.pdf",
        }

        agent = ToolRouterAgent()
        result = agent.execute(state)

        assert result["next_agent"] == "ingestion_agent"

    def test_routes_to_planner_without_file(self, initial_state):
        """Test routing to planner when no file is provided."""
        result = tool_router_agent(initial_state)

        assert result["next_agent"] == "planner_agent"

    def test_routes_to_planner_with_empty_file_content(self, initial_state):
        """Test routing to planner when file_content is empty."""
        state = {**initial_state, "file_type": "pdf", "file_content": None}

        result = tool_router_agent(state)

        assert result["next_agent"] == "planner_agent"
