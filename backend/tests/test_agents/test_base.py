"""
Tests for base agent class.
"""

import pytest

from app.agents.base import BaseAgent
from app.core.state import AgentState


class ConcreteAgent(BaseAgent):
    """Concrete implementation for testing."""

    def execute(self, state: AgentState):
        return {"result": "success", "next_agent": "test_agent"}


class FailingAgent(BaseAgent):
    """Agent that raises an exception."""

    def execute(self, state: AgentState):
        raise ValueError("Test error")


class TestBaseAgent:
    """Tests for BaseAgent class."""

    def test_init_sets_name(self):
        """Test that __init__ sets agent name."""
        agent = ConcreteAgent()
        assert agent.name == "ConcreteAgent"

    def test_init_sets_logger(self):
        """Test that __init__ sets logger."""
        agent = ConcreteAgent()
        assert agent.logger is not None
        assert "ConcreteAgent" in agent.logger.name

    def test_call_invokes_execute(self):
        """Test that __call__ invokes execute."""
        agent = ConcreteAgent()
        state = {"input": "test"}

        result = agent(state)

        assert result["result"] == "success"

    def test_call_handles_exception(self):
        """Test that __call__ handles exceptions."""
        agent = FailingAgent()
        state = {"input": "test"}

        result = agent(state)

        assert "error" in result
        assert "Test error" in result["error"]
        assert result["next_agent"] == "executor_agent"

    def test_log_state_with_default_keys(self):
        """Test log_state with default keys."""
        agent = ConcreteAgent()
        state = {
            "input": "test query",
            "file_type": "pdf",
            "context": ["chunk1"],
            "answer": "test answer",
            "extra": "ignored",
        }

        # Should not raise any exceptions
        agent.log_state(state)

    def test_log_state_with_custom_keys(self):
        """Test log_state with custom keys."""
        agent = ConcreteAgent()
        state = {"input": "test", "custom_key": "value"}

        # Should not raise any exceptions
        agent.log_state(state, keys=["input", "custom_key"])

    def test_log_state_handles_missing_keys(self):
        """Test log_state handles missing keys gracefully."""
        agent = ConcreteAgent()
        state = {"input": "test"}

        # Should not raise any exceptions even with missing keys
        agent.log_state(state, keys=["input", "missing_key"])

    def test_execute_is_abstract(self):
        """Test that execute is abstract method."""
        with pytest.raises(TypeError):
            BaseAgent()
