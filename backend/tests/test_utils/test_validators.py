"""
Tests for input validators.
"""

import pytest

from app.exceptions import ValidationError
from app.utils.validators import (
    get_file_type,
    sanitize_filename,
    validate_file_extension,
    validate_file_size,
    validate_query,
    validate_text_input,
    validate_url,
)


class TestValidateFileExtension:
    """Tests for validate_file_extension."""

    def test_valid_pdf(self):
        """Test valid PDF file."""
        assert validate_file_extension("document.pdf") is True

    def test_valid_docx(self):
        """Test valid DOCX file."""
        assert validate_file_extension("document.docx") is True

    def test_valid_txt(self):
        """Test valid TXT file."""
        assert validate_file_extension("document.txt") is True

    def test_uppercase_extension(self):
        """Test uppercase extension."""
        assert validate_file_extension("document.PDF") is True

    def test_no_extension_raises_error(self):
        """Test file without extension raises error."""
        with pytest.raises(ValidationError) as exc_info:
            validate_file_extension("filename")
        assert "extension" in str(exc_info.value).lower()

    def test_invalid_extension_raises_error(self):
        """Test invalid extension raises error."""
        with pytest.raises(ValidationError) as exc_info:
            validate_file_extension("document.xyz")
        assert "not allowed" in str(exc_info.value).lower()


class TestValidateFileSize:
    """Tests for validate_file_size."""

    def test_valid_size(self):
        """Test valid file size."""
        assert validate_file_size(1024) is True

    def test_max_size(self):
        """Test at max size limit."""
        assert validate_file_size(16 * 1024 * 1024) is True

    def test_too_large_raises_error(self):
        """Test file too large raises error."""
        with pytest.raises(ValidationError) as exc_info:
            validate_file_size(17 * 1024 * 1024)
        assert "exceeds" in str(exc_info.value).lower()


class TestValidateUrl:
    """Tests for validate_url."""

    def test_valid_https_url(self):
        """Test valid HTTPS URL."""
        assert validate_url("https://example.com") is True

    def test_valid_http_url(self):
        """Test valid HTTP URL."""
        assert validate_url("http://example.com") is True

    def test_url_with_path(self):
        """Test URL with path."""
        assert validate_url("https://example.com/page/article") is True

    def test_empty_url_raises_error(self):
        """Test empty URL raises error."""
        with pytest.raises(ValidationError):
            validate_url("")

    def test_whitespace_url_raises_error(self):
        """Test whitespace URL raises error."""
        with pytest.raises(ValidationError):
            validate_url("   ")

    def test_invalid_format_raises_error(self):
        """Test invalid URL format raises error."""
        with pytest.raises(ValidationError):
            validate_url("not-a-url")

    def test_ftp_protocol_raises_error(self):
        """Test non-http/https protocol raises error."""
        with pytest.raises(ValidationError) as exc_info:
            validate_url("ftp://example.com")
        assert "http" in str(exc_info.value).lower()

    def test_too_long_url_raises_error(self):
        """Test URL exceeding max length raises error."""
        long_url = "https://example.com/" + "a" * 2100
        with pytest.raises(ValidationError):
            validate_url(long_url)


class TestValidateTextInput:
    """Tests for validate_text_input."""

    def test_valid_text(self):
        """Test valid text input."""
        assert validate_text_input("Hello, this is some text.") is True

    def test_empty_text_raises_error(self):
        """Test empty text raises error."""
        with pytest.raises(ValidationError):
            validate_text_input("")

    def test_whitespace_text_raises_error(self):
        """Test whitespace-only text raises error."""
        with pytest.raises(ValidationError):
            validate_text_input("   ")

    def test_too_long_text_raises_error(self):
        """Test text exceeding max length raises error."""
        long_text = "a" * 100001
        with pytest.raises(ValidationError):
            validate_text_input(long_text)


class TestValidateQuery:
    """Tests for validate_query."""

    def test_valid_query(self):
        """Test valid query."""
        assert validate_query("What is Python?") is True

    def test_empty_query_raises_error(self):
        """Test empty query raises error."""
        with pytest.raises(ValidationError) as exc_info:
            validate_query("")
        assert "enter a question" in str(exc_info.value).lower()

    def test_too_short_query_raises_error(self):
        """Test query too short raises error."""
        with pytest.raises(ValidationError) as exc_info:
            validate_query("ab")
        assert "at least 3" in str(exc_info.value).lower()

    def test_too_long_query_raises_error(self):
        """Test query too long raises error."""
        long_query = "a" * 5001
        with pytest.raises(ValidationError):
            validate_query(long_query)


class TestSanitizeFilename:
    """Tests for sanitize_filename."""

    def test_normal_filename(self):
        """Test normal filename passes through."""
        result = sanitize_filename("document.pdf")
        assert result == "document.pdf"

    def test_removes_path_components(self):
        """Test path components are removed."""
        result = sanitize_filename("/path/to/document.pdf")
        assert result == "document.pdf"

    def test_replaces_spaces(self):
        """Test spaces are replaced with underscores."""
        result = sanitize_filename("my document.pdf")
        assert result == "my_document.pdf"

    def test_removes_special_characters(self):
        """Test special characters are removed."""
        result = sanitize_filename("doc@#$%ument.pdf")
        assert "@" not in result
        assert "#" not in result

    def test_truncates_long_names(self):
        """Test long filenames are truncated."""
        long_name = "a" * 150 + ".pdf"
        result = sanitize_filename(long_name)
        name, ext = result.rsplit(".", 1)
        assert len(name) <= 100


class TestGetFileType:
    """Tests for get_file_type."""

    def test_pdf_extension(self):
        """Test PDF file type detection."""
        assert get_file_type("document.pdf") == "pdf"

    def test_uppercase_extension(self):
        """Test uppercase extension is lowercased."""
        assert get_file_type("document.PDF") == "pdf"

    def test_no_extension(self):
        """Test file without extension returns None."""
        assert get_file_type("filename") is None

    def test_multiple_dots(self):
        """Test file with multiple dots."""
        assert get_file_type("file.name.txt") == "txt"
