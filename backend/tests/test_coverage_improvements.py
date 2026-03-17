from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app import app
from app.services.vector_store import VectorStoreService

client = TestClient(app)


def test_process_invalid_content_type():
    response = client.post(
        "/api/process", data={"query": "test", "content_type": "invalid"}
    )
    assert response.status_code == 400
    assert "Invalid content type" in response.json()["detail"]


def test_process_file_no_filename():
    # Simulate file without filename
    files = {"file": ("", b"content", "text/plain")}
    response = client.post(
        "/api/process", data={"query": "test", "content_type": "file"}, files=files
    )
    assert response.status_code == 422


@patch("app.api.routes.process_query")
def test_process_generic_exception(mock_process):
    mock_process.side_effect = Exception("Unexpected error")
    response = client.post(
        "/api/process",
        data={
            "query": "test",
            "content_type": "text",
            "text": "valid text content for processing check" * 10,
        },
    )
    assert response.status_code == 500
    assert "Unexpected error" in response.json()["detail"]


@patch("app.services.embedding_service.HuggingFaceEmbeddings")
@patch("app.services.vector_store.VectorStoreService.clear")
def test_clear_documents_error(mock_clear, mock_hf_embeddings):
    """Test handling of error during document clearing."""
    mock_clear.side_effect = Exception("Clear failed")
    response = client.post("/api/documents/clear")
    assert response.status_code == 500
    assert "Clear failed" in response.json()["detail"]


@patch("app.services.embedding_service.HuggingFaceEmbeddings")
@patch("app.services.vector_store.VectorStoreService.get_document_count")
def test_get_document_count_error(mock_count, mock_hf_embeddings):
    """Test handling of error during document count retrieval."""
    mock_count.side_effect = Exception("Count failed")
    response = client.get("/api/documents/count")
    assert response.status_code == 500


@patch("app.services.embedding_service.HuggingFaceEmbeddings")
def test_vector_store_get_document_count_error(mock_hf_embeddings):
    """Test error handling in VectorStoreService.get_document_count."""
    service = VectorStoreService()
    if not service._vector_store:
        try:
            service._initialize()
        except Exception:
            pass

    # Mock the internal vector_store and collection
    service._vector_store = MagicMock()
    service._vector_store._collection.count.side_effect = Exception("DB Error")

    count = service.get_document_count()
    assert count == 0


@patch("app.services.embedding_service.HuggingFaceEmbeddings")
def test_vector_store_clear_error_and_reinit(mock_hf_embeddings):
    """Test error handling and reinitialization in VectorStoreService.clear."""
    service = VectorStoreService()
    if not service._vector_store:
        try:
            service._initialize()
        except Exception:
            pass

    # Force mock vector store just in case
    service._vector_store = MagicMock()

    # Mock get() to raise exception to trigger reinitialize
    service._vector_store._collection.get.side_effect = Exception("Delete Error")

    # Mock _reinitialize to verify it's called
    with patch.object(service, "_reinitialize") as mock_reinit:
        service.clear()
        mock_reinit.assert_called_once()
