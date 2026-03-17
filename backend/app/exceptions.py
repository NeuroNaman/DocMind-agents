"""
Custom exceptions for AutoDocThinker.
Provides structured error handling throughout the application.
"""


class AutoDocThinkerError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return self.message


class DocumentProcessingError(AutoDocThinkerError):
    """Error during document processing."""

    def __init__(self, message: str = "Failed to process document"):
        super().__init__(message, status_code=400)


class UnsupportedFileTypeError(AutoDocThinkerError):
    """Error when file type is not supported."""

    def __init__(self, file_type: str):
        message = f"Unsupported file type: {file_type}"
        super().__init__(message, status_code=400)


class VectorStoreError(AutoDocThinkerError):
    """Error related to vector store operations."""

    def __init__(self, message: str = "Vector store operation failed"):
        super().__init__(message, status_code=500)


class LLMError(AutoDocThinkerError):
    """Error during LLM operations."""

    def __init__(self, message: str = "LLM processing failed"):
        super().__init__(message, status_code=500)


class RetrievalError(AutoDocThinkerError):
    """Error during document retrieval."""

    def __init__(self, message: str = "Failed to retrieve relevant documents"):
        super().__init__(message, status_code=500)


class ValidationError(AutoDocThinkerError):
    """Input validation error."""

    def __init__(self, message: str = "Invalid input"):
        super().__init__(message, status_code=400)


class AgentError(AutoDocThinkerError):
    """Error during agent execution."""

    def __init__(self, agent_name: str, message: str = "Agent execution failed"):
        full_message = f"[{agent_name}] {message}"
        super().__init__(full_message, status_code=500)


class WorkflowError(AutoDocThinkerError):
    """Error in workflow execution."""

    def __init__(self, message: str = "Workflow execution failed"):
        super().__init__(message, status_code=500)
