"""
Executor Agent - Final response handler.
Formats and returns the final response to the user.
"""

from typing import Any, Dict

from langgraph.graph import END

from app.agents.base import BaseAgent
from app.core.state import AgentState


class ExecutorAgent(BaseAgent):
    """
    Final executor agent that prepares the response.
    Handles response formatting and cleanup.
    """

    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Prepare final response.

        Args:
            state: Current agent state

        Returns:
            Final state with answer
        """
        answer = state.get("answer", "")
        source = state.get("source", "unknown")
        error = state.get("error")

        # Handle error state
        if error and not answer:
            answer = f"An error occurred: {error}"
            source = "error"

        # Update history
        history = state.get("history", [])
        question = state.get("input", "")

        if question and answer:
            history.append({"role": "user", "content": question})
            history.append({"role": "assistant", "content": answer})

        self.logger.info(f"Executor sending final answer (source: {source})")

        return {
            "answer": answer,
            "source": source,
            "history": history,
            "next_agent": END,
        }


# Standalone function for LangGraph compatibility
def executor_agent(state: AgentState) -> Dict[str, Any]:
    """Standalone function wrapper for LangGraph."""
    agent = ExecutorAgent()
    return agent(state)
