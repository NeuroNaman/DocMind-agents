"""
Tests for document loader tool.
"""

from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from app.exceptions import DocumentProcessingError, UnsupportedFileTypeError
from app.tools.document_loader import DocumentLoader


class TestDocumentLoader:
    """Tests for DocumentLoader class."""

    def test_supported_types(self):
        """Test SUPPORTED_TYPES constant."""
        assert "pdf" in DocumentLoader.SUPPORTED_TYPES
        assert "docx" in DocumentLoader.SUPPORTED_TYPES
        assert "txt" in DocumentLoader.SUPPORTED_TYPES
        assert "url" in DocumentLoader.SUPPORTED_TYPES

    def test_load_unsupported_type_raises_error(self):
        """Test loading unsupported file type raises error."""
        with pytest.raises(UnsupportedFileTypeError):
            DocumentLoader.load("file.xyz", "xyz")

    def test_load_normalizes_file_type(self):
        """Test that file type is normalized to lowercase."""
        with pytest.raises(UnsupportedFileTypeError):
            DocumentLoader.load("file.XYZ", "XYZ")

    @patch("app.tools.document_loader.PyMuPDFLoader")
    def test_load_pdf(self, mock_loader_class):
        """Test PDF loading."""
        mock_loader = MagicMock()
        mock_loader.load.return_value = [Document(page_content="Test", metadata={})]
        mock_loader_class.return_value = mock_loader

        result = DocumentLoader.load_pdf("test.pdf")

        assert len(result) == 1
        assert result[0].metadata.get("source_type") == "pdf"
        assert result[0].metadata.get("page") == 1

    @patch("app.tools.document_loader.Docx2txtLoader")
    def test_load_docx(self, mock_loader_class):
        """Test DOCX loading."""
        mock_loader = MagicMock()
        mock_loader.load.return_value = [
            Document(page_content="Test DOCX", metadata={})
        ]
        mock_loader_class.return_value = mock_loader

        result = DocumentLoader.load_docx("test.docx")

        assert len(result) == 1
        assert result[0].metadata.get("source_type") == "docx"

    @patch("app.tools.document_loader.TextLoader")
    def test_load_txt(self, mock_loader_class):
        """Test TXT loading."""
        mock_loader = MagicMock()
        mock_loader.load.return_value = [Document(page_content="Test TXT", metadata={})]
        mock_loader_class.return_value = mock_loader

        result = DocumentLoader.load_txt("test.txt")

        assert len(result) == 1
        assert result[0].metadata.get("source_type") == "txt"

    @patch("app.tools.document_loader.WebBaseLoader")
    def test_load_url(self, mock_loader_class):
        """Test URL loading."""
        mock_loader = MagicMock()
        mock_loader.load.return_value = [
            Document(page_content="Web content", metadata={})
        ]
        mock_loader_class.return_value = mock_loader

        result = DocumentLoader.load_url("https://example.com")

        assert len(result) == 1
        assert result[0].metadata.get("source_type") == "url"
        assert result[0].metadata.get("url") == "https://example.com"

    def test_load_text_content(self):
        """Test loading direct text content."""
        text = "This is direct text content."
        result = DocumentLoader.load_text_content(text)

        assert len(result) == 1
        assert result[0].page_content == text
        assert result[0].metadata.get("source_type") == "text"
        assert result[0].metadata.get("source") == "direct_input"

    def test_load_text_content_with_custom_source(self):
        """Test loading text content with custom source."""
        result = DocumentLoader.load_text_content("Test", source="custom")
        assert result[0].metadata.get("source") == "custom"

    @patch("app.tools.document_loader.PyMuPDFLoader")
    def test_load_pdf_via_load_method(self, mock_loader_class):
        """Test loading PDF via main load method."""
        mock_loader = MagicMock()
        mock_loader.load.return_value = [Document(page_content="PDF", metadata={})]
        mock_loader_class.return_value = mock_loader

        result = DocumentLoader.load("test.pdf", "pdf")

        assert len(result) >= 1

    @patch("app.tools.document_loader.Docx2txtLoader")
    def test_load_docx_via_load_method(self, mock_loader_class):
        """Test loading DOCX via main load method."""
        mock_loader = MagicMock()
        mock_loader.load.return_value = [Document(page_content="DOCX", metadata={})]
        mock_loader_class.return_value = mock_loader

        result = DocumentLoader.load("test.docx", "docx")

        assert len(result) >= 1

    @patch("app.tools.document_loader.TextLoader")
    def test_load_txt_via_load_method(self, mock_loader_class):
        """Test loading TXT via main load method."""
        mock_loader = MagicMock()
        mock_loader.load.return_value = [Document(page_content="TXT", metadata={})]
        mock_loader_class.return_value = mock_loader

        result = DocumentLoader.load("test.txt", "txt")

        assert len(result) >= 1

    @patch("app.tools.document_loader.WebBaseLoader")
    def test_load_url_via_load_method(self, mock_loader_class):
        """Test loading URL via main load method."""
        mock_loader = MagicMock()
        mock_loader.load.return_value = [Document(page_content="URL", metadata={})]
        mock_loader_class.return_value = mock_loader

        result = DocumentLoader.load("https://example.com", "url")

        assert len(result) >= 1

    @patch("app.tools.document_loader.PyMuPDFLoader")
    def test_load_handles_exception(self, mock_loader_class):
        """Test that load handles exceptions properly."""
        mock_loader_class.side_effect = Exception("Load error")

        with pytest.raises(DocumentProcessingError):
            DocumentLoader.load("test.pdf", "pdf")
