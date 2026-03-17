"""
Planner Agent - Determines execution strategy.
Decides whether to use RAG or fallback based on available context.
"""

from typing import Any, Dict

from app.agents.base import BaseAgent
from app.core.state import AgentState
from app.services.vector_store import get_vector_store


class PlannerAgent(BaseAgent):
    """
    Plans the execution strategy based on available resources.
    Routes to retriever if documents exist, else to fallback.
    """

    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Plan the execution path.

        Args:
            state: Current agent state

        Returns:
            Next agent to execute
        """
        vector_store = get_vector_store()
        has_documents = vector_store.has_documents()
        doc_count = vector_store.get_document_count()

        self.logger.info(f"Planning execution - documents in store: {doc_count}")

        if has_documents:
            self.logger.info("Documents available, routing to retriever")
            return {"next_agent": "retriever_agent"}
        else:
            self.logger.info("No documents, routing to fallback")
            return {"next_agent": "fallback_agent"}


# Standalone function for LangGraph compatibility
def planner_agent(state: AgentState) -> Dict[str, Any]:
    """Standalone function wrapper for LangGraph."""
    agent = PlannerAgent()
    return agent(state)
