"""
Tests for LLM answer agent.
"""

from unittest.mock import MagicMock, patch

from app.agents.llm_answer import LLMAnswerAgent, llm_answer_agent


class TestLLMAnswerAgent:
    """Tests for LLMAnswerAgent class."""

    @patch("app.agents.llm_answer.get_llm_service")
    def test_execute_with_context_no_history(self, mock_get_service):
        """Test execute with context but no history."""
        mock_service = MagicMock()
        mock_service.generate_answer.return_value = "Generated answer"
        mock_get_service.return_value = mock_service

        agent = LLMAnswerAgent()
        state = {
            "input": "What is Python?",
            "context": ["Python is a language."],
            "history": [],
        }

        result = agent.execute(state)

        assert result["answer"] == "Generated answer"
        assert result["source"] == "rag"
        assert result["next_agent"] == "executor_agent"
        mock_service.generate_answer.assert_called_once()

    @patch("app.agents.llm_answer.get_llm_service")
    def test_execute_with_context_and_history(self, mock_get_service):
        """Test execute with context and history."""
        mock_service = MagicMock()
        mock_service.generate_with_history.return_value = "Answer with history"
        mock_get_service.return_value = mock_service

        agent = LLMAnswerAgent()
        state = {
            "input": "Follow up question?",
            "context": ["Some context"],
            "history": [{"role": "user", "content": "Previous question"}],
        }

        result = agent.execute(state)

        assert result["answer"] == "Answer with history"
        assert result["source"] == "rag"
        mock_service.generate_with_history.assert_called_once()

    @patch("app.agents.llm_answer.get_llm_service")
    def test_execute_without_context(self, mock_get_service):
        """Test execute without context falls back to simple generation."""
        mock_service = MagicMock()
        mock_service.generate_simple.return_value = "Simple answer"
        mock_get_service.return_value = mock_service

        agent = LLMAnswerAgent()
        state = {"input": "General question?", "context": [], "history": []}

        result = agent.execute(state)

        assert result["answer"] == "Simple answer"
        assert result["source"] == "error"  # No context means error source
        mock_service.generate_simple.assert_called_once()

    def test_execute_with_no_question(self):
        """Test execute with no question."""
        agent = LLMAnswerAgent()
        state = {"input": "", "context": [], "history": []}

        result = agent.execute(state)

        assert "No question was provided" in result["answer"]
        assert result["source"] == "error"
        assert result["next_agent"] == "executor_agent"

    def test_execute_with_missing_input(self):
        """Test execute with missing input key."""
        agent = LLMAnswerAgent()
        state = {"context": [], "history": []}

        result = agent.execute(state)

        assert result["source"] == "error"

    @patch("app.agents.llm_answer.get_llm_service")
    def test_execute_with_llm_exception(self, mock_get_service):
        """Test execute with LLM exception."""
        mock_service = MagicMock()
        mock_service.generate_answer.side_effect = Exception("LLM API error")
        mock_get_service.return_value = mock_service

        agent = LLMAnswerAgent()
        state = {"input": "Test question", "context": ["Context"], "history": []}

        result = agent.execute(state)

        assert "error" in result["answer"].lower()
        assert result["source"] == "error"
        assert result["next_agent"] == "executor_agent"


class TestLLMAnswerAgentFunction:
    """Tests for llm_answer_agent standalone function."""

    def test_llm_answer_agent_function_no_question(self):
        """Test standalone llm_answer_agent function with no question."""
        state = {"input": "", "context": [], "history": []}

        result = llm_answer_agent(state)

        assert "answer" in result
        assert result["source"] == "error"
