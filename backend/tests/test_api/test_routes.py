"""
Tests for API routes.
"""

from unittest.mock import MagicMock, patch

import pytest


@pytest.mark.anyio
class TestHealthEndpoint:
    """Test health check endpoint."""

    async def test_health_check(self, client):
        """Test health check returns healthy status."""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data


@pytest.mark.anyio
class TestProcessEndpoint:
    """Test process API endpoint."""

    async def test_process_requires_query(self, client):
        """Test that query is required."""
        response = await client.post(
            "/api/process",
            data={
                "content_type": "text",
                "text": "Some text content that is long enough to pass validation test",
            },
        )

        # FastAPI returns 422 for validation errors
        assert response.status_code == 422

    async def test_process_validates_url(self, client):
        """Test URL validation."""
        response = await client.post(
            "/api/process",
            data={"query": "What is this about?", "content_type": "url", "url": ""},
        )

        assert response.status_code == 400

    async def test_process_file_no_file(self, client):
        """Test file content type with no file uploaded."""
        response = await client.post(
            "/api/process",
            data={"query": "What is this?", "content_type": "file"},
        )

        assert response.status_code == 400
        assert "file" in response.json()["detail"].lower()

    async def test_process_text_no_text(self, client):
        """Test text content type with no text provided."""
        response = await client.post(
            "/api/process",
            data={"query": "What is this?", "content_type": "text"},
        )

        assert response.status_code == 400

    async def test_process_invalid_content_type(self, client):
        """Test invalid content type."""
        response = await client.post(
            "/api/process",
            data={"query": "What is this?", "content_type": "invalid"},
        )

        assert response.status_code == 400
        assert "content type" in response.json()["detail"].lower()

    @patch("app.api.routes.process_query")
    @patch("app.services.vector_store.get_vector_store")
    async def test_process_url_success(self, mock_get_vs, mock_process, client):
        """Test successful URL processing."""
        mock_vs = MagicMock()
        mock_vs.get_document_count.return_value = 5
        mock_get_vs.return_value = mock_vs
        mock_process.return_value = ("Test answer", "rag")

        response = await client.post(
            "/api/process",
            data={
                "query": "What is this about?",
                "content_type": "url",
                "url": "https://example.com/page",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Test answer"
        assert data["source"] == "rag"

    @patch("app.api.routes.process_query")
    @patch("app.services.vector_store.get_vector_store")
    async def test_process_text_success(self, mock_get_vs, mock_process, client):
        """Test successful text processing."""
        mock_vs = MagicMock()
        mock_vs.get_document_count.return_value = 3
        mock_get_vs.return_value = mock_vs
        mock_process.return_value = ("Answer from text", "rag")

        response = await client.post(
            "/api/process",
            data={
                "query": "What does this say?",
                "content_type": "text",
                "text": "This is some test text content that is long enough.",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data

    @patch("app.api.routes.process_query")
    @patch("app.services.vector_store.get_vector_store")
    async def test_process_file_success(self, mock_get_vs, mock_process, client):
        """Test successful file processing."""
        mock_vs = MagicMock()
        mock_vs.get_document_count.return_value = 10
        mock_get_vs.return_value = mock_vs
        mock_process.return_value = ("File answer", "rag")

        # Create a test file
        from io import BytesIO

        test_file = BytesIO(b"Test file content")
        test_file.name = "test.txt"

        response = await client.post(
            "/api/process",
            data={"query": "What is in this file?", "content_type": "file"},
            files={"file": ("test.txt", test_file, "text/plain")},
        )

        assert response.status_code == 200

    @patch("app.api.routes.process_query")
    async def test_process_handles_application_error(self, mock_process, client):
        """Test handling of AutoDocThinkerError."""
        from app.exceptions import DocumentProcessingError

        mock_process.side_effect = DocumentProcessingError("Test error")

        response = await client.post(
            "/api/process",
            data={
                "query": "What is this?",
                "content_type": "text",
                "text": "Some text content for processing",
            },
        )

        assert response.status_code == 400

    @patch("app.api.routes.process_query")
    async def test_process_handles_unexpected_error(self, mock_process, client):
        """Test handling of unexpected exceptions."""
        mock_process.side_effect = Exception("Unexpected error")

        response = await client.post(
            "/api/process",
            data={
                "query": "What is this?",
                "content_type": "text",
                "text": "Some text content for processing",
            },
        )

        assert response.status_code == 500


@pytest.mark.anyio
class TestDocumentEndpoints:
    """Test document management endpoints."""

    @patch("app.services.vector_store.get_vector_store")
    async def test_get_document_count(self, mock_get_vs, client):
        """Test get document count endpoint."""
        mock_vs = MagicMock()
        mock_vs.get_document_count.return_value = 15
        mock_get_vs.return_value = mock_vs

        response = await client.get("/api/documents/count")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 15
        assert data["has_documents"] is True

    @patch("app.services.vector_store.get_vector_store")
    async def test_get_document_count_empty(self, mock_get_vs, client):
        """Test get document count when empty."""
        mock_vs = MagicMock()
        mock_vs.get_document_count.return_value = 0
        mock_get_vs.return_value = mock_vs

        response = await client.get("/api/documents/count")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["has_documents"] is False

    @patch("app.services.vector_store.get_vector_store")
    async def test_get_document_count_error(self, mock_get_vs, client):
        """Test get document count with error."""
        mock_get_vs.side_effect = Exception("Database error")

        response = await client.get("/api/documents/count")

        assert response.status_code == 500

    @patch("app.services.vector_store.get_vector_store")
    async def test_clear_documents(self, mock_get_vs, client):
        """Test clear documents endpoint."""
        mock_vs = MagicMock()
        mock_get_vs.return_value = mock_vs

        response = await client.post("/api/documents/clear")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        mock_vs.clear.assert_called_once()

    @patch("app.services.vector_store.get_vector_store")
    async def test_clear_documents_error(self, mock_get_vs, client):
        """Test clear documents with error."""
        mock_vs = MagicMock()
        mock_vs.clear.side_effect = Exception("Clear failed")
        mock_get_vs.return_value = mock_vs

        response = await client.post("/api/documents/clear")

        assert response.status_code == 500
