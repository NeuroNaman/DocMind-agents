"""
Tests for ingestion agent.
"""

from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from app.agents.ingestion import IngestionAgent, ingestion_agent
from app.exceptions import DocumentProcessingError


class TestIngestionAgent:
    """Tests for IngestionAgent class."""

    def test_execute_with_no_file_content(self):
        """Test execute with no file content."""
        agent = IngestionAgent()
        state = {"file_content": None, "file_type": None}

        result = agent.execute(state)

        assert result["next_agent"] == "planner_agent"

    def test_execute_with_no_file_type(self):
        """Test execute with file content but no file type."""
        agent = IngestionAgent()
        state = {"file_content": "some_file.pdf", "file_type": None}

        result = agent.execute(state)

        assert result["next_agent"] == "planner_agent"

    @patch("app.agents.ingestion.get_vector_store")
    @patch("app.agents.ingestion.get_text_splitter")
    @patch("app.agents.ingestion.DocumentLoader")
    def test_execute_with_successful_ingestion(
        self, mock_loader, mock_splitter, mock_vector_store
    ):
        """Test execute with successful document ingestion."""
        # Mock DocumentLoader
        mock_loader.load.return_value = [
            Document(page_content="Test content", metadata={})
        ]

        # Mock text splitter
        mock_splitter_instance = MagicMock()
        mock_splitter_instance.split_documents.return_value = [
            Document(page_content="Chunk 1", metadata={}),
            Document(page_content="Chunk 2", metadata={}),
        ]
        mock_splitter.return_value = mock_splitter_instance

        # Mock vector store
        mock_vs_instance = MagicMock()
        mock_vector_store.return_value = mock_vs_instance

        agent = IngestionAgent()
        state = {"file_content": "test.pdf", "file_type": "pdf"}

        result = agent.execute(state)

        assert result["next_agent"] == "planner_agent"
        assert result["chunks_added"] == 2
        assert result["metadata"]["source"] == "test.pdf"

    @patch("app.agents.ingestion.DocumentLoader")
    def test_execute_with_empty_documents(self, mock_loader):
        """Test execute with no documents loaded."""
        mock_loader.load.return_value = []

        agent = IngestionAgent()
        state = {"file_content": "empty.pdf", "file_type": "pdf"}

        result = agent.execute(state)

        assert result["next_agent"] == "planner_agent"
        assert result["chunks_added"] == 0

    @patch("app.agents.ingestion.DocumentLoader")
    def test_execute_with_document_processing_error(self, mock_loader):
        """Test execute with DocumentProcessingError."""
        mock_loader.load.side_effect = DocumentProcessingError("Failed to load")

        agent = IngestionAgent()
        state = {"file_content": "bad.pdf", "file_type": "pdf"}

        result = agent.execute(state)

        assert "error" in result
        assert result["next_agent"] == "planner_agent"
        assert result["chunks_added"] == 0

    @patch("app.agents.ingestion.DocumentLoader")
    def test_execute_with_general_exception(self, mock_loader):
        """Test execute with general exception."""
        mock_loader.load.side_effect = Exception("Unexpected error")

        agent = IngestionAgent()
        state = {"file_content": "problem.pdf", "file_type": "pdf"}

        result = agent.execute(state)

        assert "error" in result
        assert "Ingestion failed" in result["error"]

    @patch("app.agents.ingestion.get_vector_store")
    @patch("app.agents.ingestion.get_text_splitter")
    @patch("app.agents.ingestion.DocumentLoader")
    def test_execute_clears_vector_store_before_adding(
        self, mock_loader, mock_splitter, mock_vector_store
    ):
        """Test that vector store is cleared before adding new documents."""
        mock_loader.load.return_value = [Document(page_content="Test", metadata={})]
        mock_splitter_instance = MagicMock()
        mock_splitter_instance.split_documents.return_value = [
            Document(page_content="Chunk", metadata={})
        ]
        mock_splitter.return_value = mock_splitter_instance

        mock_vs_instance = MagicMock()
        mock_vector_store.return_value = mock_vs_instance

        agent = IngestionAgent()
        state = {"file_content": "test.pdf", "file_type": "pdf"}

        agent.execute(state)

        mock_vs_instance.clear.assert_called_once()
        mock_vs_instance.add_documents.assert_called_once()


class TestIngestionAgentFunction:
    """Tests for ingestion_agent standalone function."""

    def test_ingestion_agent_function_no_content(self):
        """Test standalone ingestion_agent function with no content."""
        state = {"file_content": None, "file_type": None}

        result = ingestion_agent(state)

        assert result["next_agent"] == "planner_agent"
