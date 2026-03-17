"""
Text splitter tool for chunking documents.
Provides configurable text splitting for optimal retrieval.
"""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_config
from app.utils.logger import get_logger

logger = get_logger("text_splitter")


class TextSplitterTool:
    """
    Tool for splitting documents into chunks.
    Uses recursive character text splitter for optimal chunking.
    """

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize the text splitter.

        Args:
            chunk_size: Size of each chunk (default from config)
            chunk_overlap: Overlap between chunks (default from config)
        """
        config = get_config()

        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        logger.info(
            f"Text splitter initialized: chunk_size={self.chunk_size}, "
            f"overlap={self.chunk_overlap}"
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.

        Args:
            documents: List of documents to split

        Returns:
            List of chunked documents
        """
        if not documents:
            return []

        chunks = self._splitter.split_documents(documents)

        # Add chunk metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i
            chunk.metadata["total_chunks"] = len(chunks)

        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks

    def split_text(self, text: str) -> List[str]:
        """
        Split raw text into chunks.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        chunks = self._splitter.split_text(text)
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks

    def get_chunk_count(self, text: str) -> int:
        """
        Get estimated number of chunks for text.

        Args:
            text: Text to estimate

        Returns:
            Estimated chunk count
        """
        # Rough estimate based on chunk size
        return max(1, len(text) // (self.chunk_size - self.chunk_overlap))


# Default splitter instance
_default_splitter: TextSplitterTool = None


def get_text_splitter() -> TextSplitterTool:
    """Get the default text splitter instance."""
    global _default_splitter
    if _default_splitter is None:
        _default_splitter = TextSplitterTool()
    return _default_splitter
