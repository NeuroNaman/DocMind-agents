"""
Tests for vector store service.
"""

from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from app.services.vector_store import VectorStoreService, get_vector_store


class TestVectorStoreService:
    """Tests for VectorStoreService class."""

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_singleton_pattern(self, mock_chroma, mock_embedding):
        """Test singleton pattern returns same instance."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        service1 = VectorStoreService()
        service2 = VectorStoreService()

        assert service1 is service2

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_store_property(self, mock_chroma_class, mock_embedding):
        """Test store property returns Chroma instance."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        mock_store = MagicMock()
        mock_chroma_class.return_value = mock_store

        service = VectorStoreService()
        result = service.store

        assert result is mock_store

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_add_documents_empty_list(self, mock_chroma, mock_embedding):
        """Test add_documents with empty list."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        service = VectorStoreService()
        result = service.add_documents([])

        assert result == 0

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_add_documents_with_documents(self, mock_chroma_class, mock_embedding):
        """Test add_documents with documents."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        mock_store = MagicMock()
        mock_chroma_class.return_value = mock_store

        service = VectorStoreService()
        documents = [
            Document(page_content="Test 1", metadata={}),
            Document(page_content="Test 2", metadata={}),
        ]
        result = service.add_documents(documents)

        assert result == 2
        mock_store.add_documents.assert_called_once_with(documents)

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_similarity_search(self, mock_chroma_class, mock_embedding):
        """Test similarity_search method."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        mock_store = MagicMock()
        mock_store.similarity_search.return_value = [
            Document(page_content="Result", metadata={})
        ]
        mock_chroma_class.return_value = mock_store

        service = VectorStoreService()
        result = service.similarity_search("test query", k=3)

        assert len(result) == 1
        mock_store.similarity_search.assert_called_once()

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_similarity_search_with_score(self, mock_chroma_class, mock_embedding):
        """Test similarity_search_with_score method."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        mock_store = MagicMock()
        mock_store.similarity_search_with_score.return_value = [
            (Document(page_content="Result", metadata={}), 0.95)
        ]
        mock_chroma_class.return_value = mock_store

        service = VectorStoreService()
        result = service.similarity_search_with_score("test", k=3)

        assert len(result) == 1

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_get_document_count(self, mock_chroma_class, mock_embedding):
        """Test get_document_count method."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        mock_collection = MagicMock()
        mock_collection.count.return_value = 5
        mock_store = MagicMock()
        mock_store._collection = mock_collection
        mock_chroma_class.return_value = mock_store

        service = VectorStoreService()
        result = service.get_document_count()

        assert result == 5

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_get_document_count_exception(self, mock_chroma_class, mock_embedding):
        """Test get_document_count handles exception."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        mock_store = MagicMock()
        mock_store._collection.count.side_effect = Exception("Error")
        mock_chroma_class.return_value = mock_store

        service = VectorStoreService()
        result = service.get_document_count()

        assert result == 0

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_has_documents_true(self, mock_chroma_class, mock_embedding):
        """Test has_documents returns True when documents exist."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        mock_collection = MagicMock()
        mock_collection.count.return_value = 5
        mock_store = MagicMock()
        mock_store._collection = mock_collection
        mock_chroma_class.return_value = mock_store

        service = VectorStoreService()
        result = service.has_documents()

        assert result is True

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_has_documents_false(self, mock_chroma_class, mock_embedding):
        """Test has_documents returns False when no documents."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_store = MagicMock()
        mock_store._collection = mock_collection
        mock_chroma_class.return_value = mock_store

        service = VectorStoreService()
        result = service.has_documents()

        assert result is False

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_clear(self, mock_chroma_class, mock_embedding):
        """Test clear method."""
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        mock_collection = MagicMock()
        mock_collection.get.return_value = {"ids": ["id1", "id2"]}
        mock_store = MagicMock()
        mock_store._collection = mock_collection
        mock_chroma_class.return_value = mock_store

        service = VectorStoreService()
        service.clear()

        mock_collection.delete.assert_called_once_with(ids=["id1", "id2"])


class TestGetVectorStore:
    """Tests for get_vector_store function."""

    @patch("app.services.vector_store.EmbeddingService")
    @patch("app.services.vector_store.Chroma")
    def test_returns_service_instance(self, mock_chroma, mock_embedding):
        """Test that function returns VectorStoreService instance."""
        import app.services.vector_store as vs

        vs._vector_store_service = None
        VectorStoreService._instance = None
        VectorStoreService._vector_store = None

        result = get_vector_store()

        assert isinstance(result, VectorStoreService)
