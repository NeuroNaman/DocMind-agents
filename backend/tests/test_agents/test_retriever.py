"""
Tests for retriever agent.
"""

from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from app.agents.retriever import RetrieverAgent, retriever_agent


class TestRetrieverAgent:
    """Tests for RetrieverAgent class."""

    @patch("app.agents.retriever.get_vector_store")
    @patch("app.agents.retriever.get_config")
    def test_execute_with_successful_retrieval(self, mock_config, mock_get_vs):
        """Test execute with successful retrieval."""
        mock_config.return_value.RETRIEVAL_K = 3

        mock_vs = MagicMock()
        mock_vs.similarity_search.return_value = [
            Document(page_content="Chunk 1", metadata={"source": "doc1"}),
            Document(page_content="Chunk 2", metadata={"source": "doc2"}),
        ]
        mock_get_vs.return_value = mock_vs

        agent = RetrieverAgent()
        state = {"input": "What is Python?"}

        result = agent.execute(state)

        assert len(result["context"]) == 2
        assert "Chunk 1" in result["context"]
        assert result["next_agent"] == "llm_answer_agent"
        assert result["metadata"]["chunks_retrieved"] == 2

    @patch("app.agents.retriever.get_config")
    def test_execute_with_no_query(self, mock_config):
        """Test execute with no query."""
        mock_config.return_value.RETRIEVAL_K = 3

        agent = RetrieverAgent()
        state = {"input": ""}

        result = agent.execute(state)

        assert result["context"] == []
        assert result["next_agent"] == "llm_answer_agent"

    @patch("app.agents.retriever.get_config")
    def test_execute_with_missing_input(self, mock_config):
        """Test execute with missing input."""
        mock_config.return_value.RETRIEVAL_K = 3

        agent = RetrieverAgent()
        state = {}

        result = agent.execute(state)

        assert result["context"] == []

    @patch("app.agents.retriever.get_vector_store")
    @patch("app.agents.retriever.get_config")
    def test_execute_with_retrieval_exception(self, mock_config, mock_get_vs):
        """Test execute with retrieval exception."""
        mock_config.return_value.RETRIEVAL_K = 3

        mock_vs = MagicMock()
        mock_vs.similarity_search.side_effect = Exception("Database error")
        mock_get_vs.return_value = mock_vs

        agent = RetrieverAgent()
        state = {"input": "Test query"}

        result = agent.execute(state)

        assert result["context"] == []
        assert result["next_agent"] == "fallback_agent"
        assert "error" in result

    @patch("app.agents.retriever.get_vector_store")
    @patch("app.agents.retriever.get_config")
    def test_execute_extracts_sources_from_metadata(self, mock_config, mock_get_vs):
        """Test that execute extracts sources from metadata."""
        mock_config.return_value.RETRIEVAL_K = 3

        mock_vs = MagicMock()
        mock_vs.similarity_search.return_value = [
            Document(page_content="Content", metadata={"source": "file.pdf"}),
        ]
        mock_get_vs.return_value = mock_vs

        agent = RetrieverAgent()
        state = {"input": "Query"}

        result = agent.execute(state)

        assert "file.pdf" in result["metadata"]["sources"]


class TestRetrieverAgentFunction:
    """Tests for retriever_agent standalone function."""

    @patch("app.agents.retriever.get_vector_store")
    @patch("app.agents.retriever.get_config")
    def test_retriever_agent_function(self, mock_config, mock_get_vs):
        """Test standalone retriever_agent function."""
        mock_config.return_value.RETRIEVAL_K = 3
        mock_vs = MagicMock()
        mock_vs.similarity_search.return_value = []
        mock_get_vs.return_value = mock_vs

        state = {"input": "Test"}

        result = retriever_agent(state)

        assert "context" in result
