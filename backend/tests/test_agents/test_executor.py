"""
Tests for executor agent.
"""

from langgraph.graph import END

from app.agents.executor import ExecutorAgent, executor_agent


class TestExecutorAgent:
    """Tests for ExecutorAgent class."""

    def test_execute_with_answer_and_source(self):
        """Test execute with answer and source."""
        agent = ExecutorAgent()
        state = {
            "input": "What is Python?",
            "answer": "Python is a programming language.",
            "source": "rag",
            "history": [],
        }

        result = agent.execute(state)

        assert result["answer"] == "Python is a programming language."
        assert result["source"] == "rag"
        assert result["next_agent"] == END

    def test_execute_with_error_state(self):
        """Test execute with error state and no answer."""
        agent = ExecutorAgent()
        state = {
            "input": "test",
            "answer": "",
            "error": "Something went wrong",
            "history": [],
        }

        result = agent.execute(state)

        assert "error occurred" in result["answer"].lower()
        assert result["source"] == "error"

    def test_execute_updates_history(self):
        """Test that execute updates history."""
        agent = ExecutorAgent()
        state = {
            "input": "Question?",
            "answer": "Answer.",
            "source": "rag",
            "history": [],
        }

        result = agent.execute(state)

        assert len(result["history"]) == 2
        assert result["history"][0]["role"] == "user"
        assert result["history"][0]["content"] == "Question?"
        assert result["history"][1]["role"] == "assistant"
        assert result["history"][1]["content"] == "Answer."

    def test_execute_preserves_existing_history(self):
        """Test that existing history is preserved."""
        agent = ExecutorAgent()
        state = {
            "input": "New question?",
            "answer": "New answer.",
            "source": "rag",
            "history": [{"role": "user", "content": "Old question"}],
        }

        result = agent.execute(state)

        assert len(result["history"]) == 3

    def test_execute_without_question_or_answer(self):
        """Test execute without question or answer."""
        agent = ExecutorAgent()
        state = {"history": []}

        result = agent.execute(state)

        # History should not be updated
        assert len(result["history"]) == 0

    def test_execute_returns_end_as_next_agent(self):
        """Test that execute returns END as next_agent."""
        agent = ExecutorAgent()
        state = {"answer": "Test", "source": "test", "history": []}

        result = agent.execute(state)

        assert result["next_agent"] == END


class TestExecutorAgentFunction:
    """Tests for executor_agent standalone function."""

    def test_executor_agent_function(self):
        """Test standalone executor_agent function."""
        state = {
            "input": "Test question",
            "answer": "Test answer",
            "source": "rag",
            "history": [],
        }

        result = executor_agent(state)

        assert "answer" in result
        assert "source" in result
        assert result["next_agent"] == END
