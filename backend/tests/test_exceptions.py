"""
Tests for custom exceptions.
"""

from app.exceptions import (
    AgentError,
    AutoDocThinkerError,
    DocumentProcessingError,
    LLMError,
    RetrievalError,
    UnsupportedFileTypeError,
    ValidationError,
    VectorStoreError,
    WorkflowError,
)


class TestAutoDocThinkerError:
    """Tests for base exception class."""

    def test_init_with_message_and_status(self):
        """Test initialization with message and status code."""
        error = AutoDocThinkerError("Test error", status_code=404)
        assert error.message == "Test error"
        assert error.status_code == 404

    def test_init_default_status_code(self):
        """Test default status code is 500."""
        error = AutoDocThinkerError("Test error")
        assert error.status_code == 500

    def test_str_returns_message(self):
        """Test __str__ returns message."""
        error = AutoDocThinkerError("Test error message")
        assert str(error) == "Test error message"


class TestDocumentProcessingError:
    """Tests for DocumentProcessingError."""

    def test_default_message(self):
        """Test default error message."""
        error = DocumentProcessingError()
        assert error.message == "Failed to process document"
        assert error.status_code == 400

    def test_custom_message(self):
        """Test custom error message."""
        error = DocumentProcessingError("Custom error")
        assert error.message == "Custom error"


class TestUnsupportedFileTypeError:
    """Tests for UnsupportedFileTypeError."""

    def test_message_includes_file_type(self):
        """Test error message includes file type."""
        error = UnsupportedFileTypeError("xyz")
        assert "xyz" in error.message
        assert error.status_code == 400


class TestVectorStoreError:
    """Tests for VectorStoreError."""

    def test_default_message(self):
        """Test default error message."""
        error = VectorStoreError()
        assert error.message == "Vector store operation failed"
        assert error.status_code == 500


class TestLLMError:
    """Tests for LLMError."""

    def test_default_message(self):
        """Test default error message."""
        error = LLMError()
        assert error.message == "LLM processing failed"
        assert error.status_code == 500


class TestRetrievalError:
    """Tests for RetrievalError."""

    def test_default_message(self):
        """Test default error message."""
        error = RetrievalError()
        assert error.message == "Failed to retrieve relevant documents"
        assert error.status_code == 500


class TestValidationError:
    """Tests for ValidationError."""

    def test_default_message(self):
        """Test default error message."""
        error = ValidationError()
        assert error.message == "Invalid input"
        assert error.status_code == 400


class TestAgentError:
    """Tests for AgentError."""

    def test_message_includes_agent_name(self):
        """Test error message includes agent name."""
        error = AgentError("TestAgent", "Something went wrong")
        assert "[TestAgent]" in error.message
        assert "Something went wrong" in error.message
        assert error.status_code == 500

    def test_default_message(self):
        """Test default error message."""
        error = AgentError("TestAgent")
        assert "[TestAgent]" in error.message
        assert "Agent execution failed" in error.message


class TestWorkflowError:
    """Tests for WorkflowError."""

    def test_default_message(self):
        """Test default error message."""
        error = WorkflowError()
        assert error.message == "Workflow execution failed"
        assert error.status_code == 500

    def test_custom_message(self):
        """Test custom error message."""
        error = WorkflowError("Custom workflow error")
        assert error.message == "Custom workflow error"
