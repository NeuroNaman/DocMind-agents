"""
Fallback Agent - Wikipedia fallback search.
Used when no document context is available.
"""

from typing import Any, Dict

from app.agents.base import BaseAgent
from app.core.state import AgentState
from app.services.wikipedia_service import get_wikipedia_service


class FallbackAgent(BaseAgent):
    """
    Fallback agent that searches Wikipedia.
    Used when vector store has no relevant documents.
    """

    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Search Wikipedia for the query.

        Args:
            state: Current agent state

        Returns:
            State updates with Wikipedia results
        """
        question = state.get("input", "")

        if not question:
            self.logger.warning("No question provided for fallback")
            return {
                "answer": "No question was provided.",
                "source": "error",
                "next_agent": "executor_agent",
            }

        try:
            self.logger.info(f"Searching Wikipedia for: {question[:50]}...")

            wikipedia_service = get_wikipedia_service()
            result = wikipedia_service.search(question)

            if result:
                answer = f"From Wikipedia:\n\n{result}"
                self.logger.info("Wikipedia search successful")
            else:
                answer = "Sorry, I couldn't find relevant information on Wikipedia."
                self.logger.warning("Wikipedia returned no results")

            return {
                "answer": answer,
                "source": "wikipedia",
                "next_agent": "executor_agent",
            }

        except Exception as e:
            self.logger.error(f"Wikipedia fallback failed: {e}")
            return {
                "answer": "Sorry, I couldn't find an answer to your question.",
                "source": "error",
                "next_agent": "executor_agent",
            }


# Standalone function for LangGraph compatibility
def fallback_agent(state: AgentState) -> Dict[str, Any]:
    """Standalone function wrapper for LangGraph."""
    agent = FallbackAgent()
    return agent(state)
