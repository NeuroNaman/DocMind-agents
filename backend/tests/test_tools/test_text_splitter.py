"""
Tests for text splitter tool.
"""

from langchain_core.documents import Document

from app.tools.text_splitter import TextSplitterTool, get_text_splitter


class TestTextSplitterTool:
    """Tests for TextSplitterTool class."""

    def test_init_with_defaults(self):
        """Test initialization with default values from config."""
        splitter = TextSplitterTool()
        assert splitter.chunk_size > 0
        assert splitter.chunk_overlap >= 0

    def test_init_with_custom_values(self):
        """Test initialization with custom values."""
        splitter = TextSplitterTool(chunk_size=500, chunk_overlap=50)
        assert splitter.chunk_size == 500
        assert splitter.chunk_overlap == 50

    def test_split_documents_empty_list(self):
        """Test split_documents with empty list."""
        splitter = TextSplitterTool()
        result = splitter.split_documents([])
        assert result == []

    def test_split_documents_adds_metadata(self):
        """Test that split_documents adds chunk metadata."""
        splitter = TextSplitterTool(chunk_size=100, chunk_overlap=10)
        documents = [Document(page_content="This is a test document " * 20)]

        result = splitter.split_documents(documents)

        assert len(result) > 0
        for i, chunk in enumerate(result):
            assert chunk.metadata.get("chunk_index") == i
            assert chunk.metadata.get("total_chunks") == len(result)

    def test_split_documents_preserves_content(self):
        """Test that content is preserved in chunks."""
        splitter = TextSplitterTool(chunk_size=1000, chunk_overlap=100)
        original_text = "Test content for splitting."
        documents = [Document(page_content=original_text)]

        result = splitter.split_documents(documents)

        assert len(result) >= 1
        assert original_text in result[0].page_content

    def test_split_text(self):
        """Test split_text method."""
        splitter = TextSplitterTool(chunk_size=50, chunk_overlap=10)
        text = "This is a longer text that should be split into multiple chunks. " * 5

        result = splitter.split_text(text)

        assert isinstance(result, list)
        assert len(result) >= 1
        assert all(isinstance(chunk, str) for chunk in result)

    def test_get_chunk_count(self):
        """Test get_chunk_count estimation."""
        splitter = TextSplitterTool(chunk_size=100, chunk_overlap=20)
        text = "x" * 500

        result = splitter.get_chunk_count(text)

        assert result >= 1
        assert isinstance(result, int)

    def test_get_chunk_count_minimum_one(self):
        """Test get_chunk_count returns minimum 1."""
        splitter = TextSplitterTool(chunk_size=1000, chunk_overlap=100)
        text = "short"

        result = splitter.get_chunk_count(text)

        assert result == 1


class TestGetTextSplitter:
    """Tests for get_text_splitter function."""

    def test_returns_splitter_instance(self):
        """Test that function returns TextSplitterTool instance."""
        result = get_text_splitter()
        assert isinstance(result, TextSplitterTool)

    def test_singleton_pattern(self):
        """Test singleton pattern returns same instance."""
        splitter1 = get_text_splitter()
        splitter2 = get_text_splitter()
        assert splitter1 is splitter2
