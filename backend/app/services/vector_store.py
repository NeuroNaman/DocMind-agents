
"""
Vector store service for ChromaDB operations.
Provides singleton access to vector database.
"""

from typing import List, Optional, Tuple

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import get_config
from app.services.embedding_service import EmbeddingService
from app.utils.logger import get_logger

logger = get_logger("vector_store")


class VectorStoreService:
    """
    Singleton service for ChromaDB vector store operations.
    Handles document storage and similarity search.
    """

    _instance: Optional["VectorStoreService"] = None
    _vector_store: Optional[Chroma] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._vector_store is None:
            self._initialize()

    def _initialize(self):
        """Initialize the vector store."""

        config = get_config()

        embedding_service = EmbeddingService()

        self._vector_store = Chroma(
            embedding_function=embedding_service.get_embeddings(),
            persist_directory=config.VECTOR_DB_PATH,
            collection_name="autodocthinker_collection",
        )

        logger.info(
            f"Vector store initialized at: {config.VECTOR_DB_PATH}"
        )

    @property
    def store(self) -> Chroma:
        """Return vector store instance."""
        return self._vector_store

    # ------------------------------------------------
    # Document Storage
    # ------------------------------------------------

    def add_documents(self, documents: List[Document]) -> int:

        if not documents:
            return 0

        self._vector_store.add_documents(documents)

        count = len(documents)

        logger.info(f"Added {count} documents to vector store")

        return count

    # ------------------------------------------------
    # Retrieval
    # ------------------------------------------------

    def similarity_search(
        self,
        query: str,
        k: int = 3,
        filter: dict = None,
    ) -> List[Document]:

        results = self._vector_store.similarity_search(
            query=query,
            k=k,
            filter=filter,
        )

        logger.info(
            f"Found {len(results)} similar documents for query"
        )

        return results

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 3,
    ) -> List[Tuple[Document, float]]:

        results = self._vector_store.similarity_search_with_score(
            query=query,
            k=k,
        )

        return results

    # ------------------------------------------------
    # Store Utilities
    # ------------------------------------------------

    def get_document_count(self) -> int:

        try:
            return self._vector_store._collection.count()
        except Exception as e:

            logger.warning(
                f"Could not get document count: {e}"
            )

            return 0

    def has_documents(self) -> bool:

        return self.get_document_count() > 0

    # ------------------------------------------------
    # Clearing Store
    # ------------------------------------------------

    def clear(self):

        try:

            collection = self._vector_store._collection

            all_data = collection.get()

            if all_data and all_data.get("ids"):

                ids = all_data["ids"]

                if ids:

                    collection.delete(ids=ids)

                    logger.info(
                        f"Deleted {len(ids)} documents from vector store"
                    )

            logger.info("Vector store cleared")

        except Exception as e:

            logger.error(
                f"Failed to clear vector store: {e}"
            )

            self._reinitialize()

    def _reinitialize(self):

        import os
        import shutil

        config = get_config()

        if os.path.exists(config.VECTOR_DB_PATH):

            shutil.rmtree(config.VECTOR_DB_PATH)

            logger.info(
                f"Deleted vector store directory: {config.VECTOR_DB_PATH}"
            )

        os.makedirs(config.VECTOR_DB_PATH, exist_ok=True)

        self._initialize()

        logger.info("Vector store reinitialized")


# ------------------------------------------------
# Global Singleton
# ------------------------------------------------

_vector_store_service: Optional[VectorStoreService] = None


def get_vector_store() -> VectorStoreService:

    global _vector_store_service

    if _vector_store_service is None:
        _vector_store_service = VectorStoreService()

    return _vector_store_service