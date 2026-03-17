"""
Agent state definitions for LangGraph workflow.
Defines the shared state structure passed between agents.
"""

from typing import Dict, List, Literal, Optional, TypedDict


class AgentState(TypedDict, total=False):
    """
    Shared state for all agents in the workflow.

    Attributes:
        input: User's query/question
        file_content: Path to uploaded file or URL
        file_type: Type of content (pdf, docx, txt, url)
        context: Retrieved document chunks for RAG
        answer: Generated answer
        history: Conversation history
        next_agent: Next agent to execute
        error: Error message if any
        metadata: Additional metadata
    """

    # Input fields
    input: str
    file_content: Optional[str]
    file_type: Optional[Literal["pdf", "docx", "txt", "url"]]

    # Processing fields
    context: Optional[List[str]]
    chunks_added: Optional[int]

    # Output fields
    answer: Optional[str]
    source: Optional[Literal["rag", "wikipedia", "error"]]

    # Workflow control
    next_agent: Optional[str]
    error: Optional[str]

    # Memory
    history: List[Dict[str, str]]

    # Metadata
    metadata: Optional[Dict[str, any]]


class DocumentChunk(TypedDict):
    """Represents a single document chunk."""

    content: str
    metadata: Dict[str, any]
    page: Optional[int]
    source: str


class QueryResult(TypedDict):
    """Result of a query operation."""

    answer: str
    source: str
    chunks_used: int
    confidence: Optional[float]
