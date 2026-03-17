"""
Tests for embedding service.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.services.embedding_service import EmbeddingService, get_embedding_service


class TestEmbeddingService:
    """Tests for EmbeddingService class."""

    @patch("app.services.embedding_service.HuggingFaceEmbeddings")
    def test_singleton_pattern(self, mock_embeddings):
        """Test singleton pattern returns same instance."""
        # Reset singleton for testing
        EmbeddingService._instance = None
        EmbeddingService._embeddings = None

        service1 = EmbeddingService()
        service2 = EmbeddingService()

        assert service1 is service2

    @patch("app.services.embedding_service.HuggingFaceEmbeddings")
    def test_get_embeddings(self, mock_embeddings_class):
        """Test get_embeddings returns model."""
        EmbeddingService._instance = None
        EmbeddingService._embeddings = None

        mock_embeddings = MagicMock()
        mock_embeddings_class.return_value = mock_embeddings

        service = EmbeddingService()
        result = service.get_embeddings()

        assert result is mock_embeddings

    @patch("app.services.embedding_service.HuggingFaceEmbeddings")
    def test_embed_text(self, mock_embeddings_class):
        """Test embed_text returns vector."""
        EmbeddingService._instance = None
        EmbeddingService._embeddings = None

        mock_embeddings = MagicMock()
        mock_embeddings.embed_query.return_value = [0.1, 0.2, 0.3]
        mock_embeddings_class.return_value = mock_embeddings

        service = EmbeddingService()
        result = service.embed_text("Test text")

        assert result == [0.1, 0.2, 0.3]
        mock_embeddings.embed_query.assert_called_once_with("Test text")

    @patch("app.services.embedding_service.HuggingFaceEmbeddings")
    def test_embed_documents(self, mock_embeddings_class):
        """Test embed_documents returns vectors."""
        EmbeddingService._instance = None
        EmbeddingService._embeddings = None

        mock_embeddings = MagicMock()
        mock_embeddings.embed_documents.return_value = [[0.1, 0.2], [0.3, 0.4]]
        mock_embeddings_class.return_value = mock_embeddings

        service = EmbeddingService()
        result = service.embed_documents(["Text 1", "Text 2"])

        assert len(result) == 2
        mock_embeddings.embed_documents.assert_called_once_with(["Text 1", "Text 2"])

    @patch("app.services.embedding_service.HuggingFaceEmbeddings")
    def test_initialization_failure(self, mock_embeddings_class):
        """Test initialization failure raises exception."""
        EmbeddingService._instance = None
        EmbeddingService._embeddings = None

        mock_embeddings_class.side_effect = Exception("Model not found")

        with pytest.raises(Exception):
            EmbeddingService()


class TestGetEmbeddingService:
    """Tests for get_embedding_service function."""

    @patch("app.services.embedding_service.HuggingFaceEmbeddings")
    def test_returns_service_instance(self, mock_embeddings_class):
        """Test that function returns EmbeddingService instance."""
        import app.services.embedding_service as es

        es._embedding_service = None
        EmbeddingService._instance = None
        EmbeddingService._embeddings = None

        result = get_embedding_service()

        assert isinstance(result, EmbeddingService)

    @patch("app.services.embedding_service.HuggingFaceEmbeddings")
    def test_singleton_global(self, mock_embeddings_class):
        """Test global singleton pattern."""
        import app.services.embedding_service as es

        es._embedding_service = None
        EmbeddingService._instance = None
        EmbeddingService._embeddings = None

        service1 = get_embedding_service()
        service2 = get_embedding_service()

        assert service1 is service2
