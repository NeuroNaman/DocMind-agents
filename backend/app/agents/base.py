"""
Base agent class for all agents.
Provides common interface and functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from app.core.state import AgentState
from app.utils.logger import get_logger


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    Defines the common interface and shared functionality.
    """

    def __init__(self):
        self.name = self.__class__.__name__
        self.logger = get_logger(f"agents.{self.name}")

    @abstractmethod
    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute the agent's logic.

        Args:
            state: Current agent state

        Returns:
            Dictionary with state updates
        """
        pass

    def __call__(self, state: AgentState) -> Dict[str, Any]:
        """
        Make agent callable for LangGraph.

        Args:
            state: Current agent state

        Returns:
            Dictionary with state updates
        """
        self.logger.info(f"{self.name} executing...")
        try:
            result = self.execute(state)
            self.logger.info(f"{self.name} completed")
            return result
        except Exception as e:
            self.logger.error(f"{self.name} failed: {str(e)}")
            return {"error": str(e), "next_agent": "executor_agent"}

    def log_state(self, state: AgentState, keys: list = None):
        """Log relevant state information for debugging."""
        if keys is None:
            keys = ["input", "file_type", "context", "answer"]

        state_info = {k: state.get(k) for k in keys if k in state}
        self.logger.debug(f"State: {state_info}")
