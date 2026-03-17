"""
Embedding service for vector embeddings.
Uses HuggingFace sentence transformers.
"""

from typing import List, Optional

from langchain_huggingface import HuggingFaceEmbeddings

from app.config import get_config
from app.utils.logger import get_logger

logger = get_logger("embedding_service")


class EmbeddingService:
    """
    Service for generating embeddings.
    Uses HuggingFace sentence transformers for efficient embeddings.
    """

    _instance: Optional["EmbeddingService"] = None
    _embeddings = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._embeddings is None:
            self._initialize()

    def _initialize(self):
        """Initialize the embedding model."""
        config = get_config()

        try:
            self._embeddings = HuggingFaceEmbeddings(
                model_name=config.EMBEDDING_MODEL,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
            logger.info(f"Embedding model initialized: {config.EMBEDDING_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {e}")
            raise

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """Get the embeddings model instance."""
        return self._embeddings

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats
        """
        return self._embeddings.embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        return self._embeddings.embed_documents(texts)


# Global singleton instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get the global embedding service instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
