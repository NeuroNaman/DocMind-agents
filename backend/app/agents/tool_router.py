"""
Tool Router Agent - Routes requests based on content type.
First agent in the workflow that determines processing path.
"""

from typing import Any, Dict

from app.agents.base import BaseAgent
from app.core.state import AgentState


class ToolRouterAgent(BaseAgent):
    """
    Routes incoming requests to appropriate processing agents.
    Determines whether to ingest new documents or go directly to planning.
    """

    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Route the request based on content availability.

        Args:
            state: Current agent state

        Returns:
            Next agent to execute
        """
        file_type = state.get("file_type")
        file_content = state.get("file_content")

        self.logger.info(
            f"Routing request - file_type: {file_type}, "
            f"has_content: {bool(file_content)}"
        )

        # If we have new content to process, go to ingestion
        if file_type and file_content:
            return {"next_agent": "ingestion_agent"}

        # Otherwise, go directly to planning (use existing data)
        return {"next_agent": "planner_agent"}


# Standalone function for LangGraph compatibility
def tool_router_agent(state: AgentState) -> Dict[str, Any]:
    """Standalone function wrapper for LangGraph."""
    agent = ToolRouterAgent()
    return agent(state)
