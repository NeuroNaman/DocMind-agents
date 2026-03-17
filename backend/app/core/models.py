"""
Pydantic models for data validation.
Provides type-safe data structures for API requests/responses.
"""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    """Request model for processing queries."""

    query: str = Field(..., min_length=1, description="User's question")
    content_type: Literal["file", "url", "text"] = Field(
        default="file", description="Type of content being processed"
    )
    url: Optional[str] = Field(None, description="URL to process")
    text: Optional[str] = Field(None, description="Direct text content")

    @field_validator("query")
    @classmethod
    def query_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


class QueryResponse(BaseModel):
    """Response model for query results."""

    answer: str = Field(..., description="Generated answer")
    source: Literal["rag", "wikipedia", "error"] = Field(
        ..., description="Source of the answer"
    )
    chunks_used: Optional[int] = Field(
        None, description="Number of document chunks used"
    )
    processing_time: Optional[float] = Field(
        None, description="Time taken to process in seconds"
    )


class DocumentMetadata(BaseModel):
    """Metadata for processed documents."""

    filename: str
    file_type: str
    file_size: int
    upload_time: datetime = Field(default_factory=datetime.now)
    chunk_count: int = 0
    source: Literal["file", "url", "text"] = "file"


class ConversationMessage(BaseModel):
    """Single message in conversation history."""

    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    source: Optional[str] = None


class ConversationHistory(BaseModel):
    """Conversation history container."""

    messages: List[ConversationMessage] = Field(default_factory=list)
    max_messages: int = Field(default=10)

    def add_message(self, role: str, content: str, source: str = None):
        """Add a message to history, maintaining max size."""
        message = ConversationMessage(role=role, content=content, source=source)
        self.messages.append(message)

        # Keep only last max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

    def get_context_string(self) -> str:
        """Get conversation history as formatted string."""
        return "\n".join([f"{msg.role}: {msg.content}" for msg in self.messages])


class HealthCheck(BaseModel):
    """Health check response model."""

    status: str = "healthy"
    version: str = "1.0.0"
    vector_store_connected: bool = False
    llm_connected: bool = False
