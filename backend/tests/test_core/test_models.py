"""
Tests for Pydantic models.
"""

import pytest
from pydantic import ValidationError as PydanticValidationError

from app.core.models import (
    ConversationHistory,
    ConversationMessage,
    DocumentMetadata,
    HealthCheck,
    QueryRequest,
    QueryResponse,
)


class TestQueryRequest:
    """Tests for QueryRequest model."""

    def test_valid_query(self):
        """Test valid query creation."""
        request = QueryRequest(query="What is Python?")
        assert request.query == "What is Python?"
        assert request.content_type == "file"

    def test_query_stripped(self):
        """Test query is stripped of whitespace."""
        request = QueryRequest(query="  What is Python?  ")
        assert request.query == "What is Python?"

    def test_empty_query_raises_error(self):
        """Test empty query raises validation error."""
        with pytest.raises(PydanticValidationError):
            QueryRequest(query="")

    def test_whitespace_only_query_raises_error(self):
        """Test whitespace-only query raises validation error."""
        with pytest.raises(PydanticValidationError):
            QueryRequest(query="   ")

    def test_content_type_options(self):
        """Test different content type options."""
        for content_type in ["file", "url", "text"]:
            request = QueryRequest(query="test", content_type=content_type)
            assert request.content_type == content_type

    def test_optional_url(self):
        """Test optional URL field."""
        request = QueryRequest(query="test", url="https://example.com")
        assert request.url == "https://example.com"

    def test_optional_text(self):
        """Test optional text field."""
        request = QueryRequest(query="test", text="Some text content")
        assert request.text == "Some text content"


class TestQueryResponse:
    """Tests for QueryResponse model."""

    def test_valid_response(self):
        """Test valid response creation."""
        response = QueryResponse(answer="Test answer", source="rag")
        assert response.answer == "Test answer"
        assert response.source == "rag"

    def test_response_with_optional_fields(self):
        """Test response with optional fields."""
        response = QueryResponse(
            answer="Test", source="wikipedia", chunks_used=5, processing_time=1.5
        )
        assert response.chunks_used == 5
        assert response.processing_time == 1.5


class TestDocumentMetadata:
    """Tests for DocumentMetadata model."""

    def test_valid_metadata(self):
        """Test valid metadata creation."""
        metadata = DocumentMetadata(
            filename="test.pdf", file_type="pdf", file_size=1024
        )
        assert metadata.filename == "test.pdf"
        assert metadata.file_type == "pdf"
        assert metadata.file_size == 1024

    def test_default_values(self):
        """Test default values."""
        metadata = DocumentMetadata(filename="test.txt", file_type="txt", file_size=100)
        assert metadata.chunk_count == 0
        assert metadata.source == "file"
        assert metadata.upload_time is not None


class TestConversationMessage:
    """Tests for ConversationMessage model."""

    def test_valid_message(self):
        """Test valid message creation."""
        message = ConversationMessage(role="user", content="Hello")
        assert message.role == "user"
        assert message.content == "Hello"
        assert message.timestamp is not None

    def test_assistant_message(self):
        """Test assistant message."""
        message = ConversationMessage(
            role="assistant", content="Hi there", source="rag"
        )
        assert message.role == "assistant"
        assert message.source == "rag"


class TestConversationHistory:
    """Tests for ConversationHistory model."""

    def test_empty_history(self):
        """Test empty history creation."""
        history = ConversationHistory()
        assert len(history.messages) == 0

    def test_add_message(self):
        """Test adding a message."""
        history = ConversationHistory()
        history.add_message("user", "Hello")
        assert len(history.messages) == 1
        assert history.messages[0].role == "user"
        assert history.messages[0].content == "Hello"

    def test_add_message_with_source(self):
        """Test adding a message with source."""
        history = ConversationHistory()
        history.add_message("assistant", "Response", source="rag")
        assert history.messages[0].source == "rag"

    def test_max_messages_limit(self):
        """Test max messages limit is enforced."""
        history = ConversationHistory(max_messages=3)
        for i in range(5):
            history.add_message("user", f"Message {i}")
        assert len(history.messages) == 3
        assert history.messages[0].content == "Message 2"

    def test_get_context_string(self):
        """Test get_context_string method."""
        history = ConversationHistory()
        history.add_message("user", "Question")
        history.add_message("assistant", "Answer")
        context = history.get_context_string()
        assert "user: Question" in context
        assert "assistant: Answer" in context


class TestHealthCheck:
    """Tests for HealthCheck model."""

    def test_default_values(self):
        """Test default values."""
        health = HealthCheck()
        assert health.status == "healthy"
        assert health.version == "1.0.0"
        assert health.vector_store_connected is False
        assert health.llm_connected is False

    def test_custom_values(self):
        """Test custom values."""
        health = HealthCheck(
            status="degraded", vector_store_connected=True, llm_connected=True
        )
        assert health.status == "degraded"
        assert health.vector_store_connected is True
