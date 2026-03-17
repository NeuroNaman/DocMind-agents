"""
Document loader tool for processing various file types.
Supports PDF, DOCX, TXT, and URL content extraction.
"""

from typing import List

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyMuPDFLoader,
    TextLoader,
    WebBaseLoader,
)
from langchain_core.documents import Document

from app.exceptions import DocumentProcessingError, UnsupportedFileTypeError
from app.utils.logger import get_logger

logger = get_logger("document_loader")


class DocumentLoader:
    """
    Unified document loader for multiple file types.
    Provides a consistent interface for loading documents.
    """

    SUPPORTED_TYPES = {"pdf", "docx", "txt", "url"}

    @staticmethod
    def load(file_path: str, file_type: str) -> List[Document]:
        """
        Load document based on file type.

        Args:
            file_path: Path to file or URL
            file_type: Type of content (pdf, docx, txt, url)

        Returns:
            List of LangChain documents

        Raises:
            UnsupportedFileTypeError: If file type not supported
            DocumentProcessingError: If loading fails
        """
        file_type = file_type.lower()

        if file_type not in DocumentLoader.SUPPORTED_TYPES:
            raise UnsupportedFileTypeError(file_type)

        try:
            if file_type == "pdf":
                return DocumentLoader.load_pdf(file_path)
            elif file_type == "docx":
                return DocumentLoader.load_docx(file_path)
            elif file_type == "txt":
                return DocumentLoader.load_txt(file_path)
            elif file_type == "url":
                return DocumentLoader.load_url(file_path)
        except UnsupportedFileTypeError:
            raise
        except Exception as e:
            logger.error(f"Document loading failed: {e}")
            raise DocumentProcessingError(f"Failed to load {file_type}: {str(e)}")

    @staticmethod
    def load_pdf(file_path: str) -> List[Document]:
        """
        Load PDF file.

        Args:
            file_path: Path to PDF file

        Returns:
            List of documents
        """
        logger.info(f"Loading PDF: {file_path}")
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()

        # Add metadata
        for i, doc in enumerate(documents):
            doc.metadata["source_type"] = "pdf"
            doc.metadata["page"] = i + 1

        logger.info(f"Loaded {len(documents)} pages from PDF")
        return documents

    @staticmethod
    def load_docx(file_path: str) -> List[Document]:
        """
        Load DOCX file.

        Args:
            file_path: Path to DOCX file

        Returns:
            List of documents
        """
        logger.info(f"Loading DOCX: {file_path}")
        loader = Docx2txtLoader(file_path)
        documents = loader.load()

        for doc in documents:
            doc.metadata["source_type"] = "docx"

        logger.info("Loaded DOCX document")
        return documents

    @staticmethod
    def load_txt(file_path: str) -> List[Document]:
        """
        Load TXT file.

        Args:
            file_path: Path to TXT file

        Returns:
            List of documents
        """
        logger.info(f"Loading TXT: {file_path}")
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()

        for doc in documents:
            doc.metadata["source_type"] = "txt"

        logger.info("Loaded TXT document")
        return documents

    @staticmethod
    def load_url(url: str) -> List[Document]:
        """
        Load content from URL.

        Args:
            url: Web URL to load

        Returns:
            List of documents
        """
        logger.info(f"Loading URL: {url}")
        loader = WebBaseLoader(url)
        documents = loader.load()

        for doc in documents:
            doc.metadata["source_type"] = "url"
            doc.metadata["url"] = url

        logger.info("Loaded content from URL")
        return documents

    @staticmethod
    def load_text_content(text: str, source: str = "direct_input") -> List[Document]:
        """
        Create document from direct text input.

        Args:
            text: Text content
            source: Source identifier

        Returns:
            List with single document
        """
        document = Document(
            page_content=text, metadata={"source": source, "source_type": "text"}
        )
        logger.info("Created document from direct text input")
        return [document]
