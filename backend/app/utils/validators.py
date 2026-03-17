"""
Input validators for AutoDocThinker.
Provides validation functions for various input types.
"""

import os
import re
from typing import Optional, Set
from urllib.parse import urlparse

from app.exceptions import ValidationError

ALLOWED_EXTENSIONS: Set[str] = {"pdf", "docx", "txt"}
MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16MB
MAX_TEXT_LENGTH: int = 100000  # 100k characters
MAX_URL_LENGTH: int = 2048


def validate_file_extension(filename: str) -> bool:
    """
    Check if file has an allowed extension.

    Args:
        filename: Name of the file

    Returns:
        True if extension is allowed

    Raises:
        ValidationError: If extension is not allowed
    """
    if "." not in filename:
        raise ValidationError("File must have an extension")

    extension = filename.rsplit(".", 1)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"File type '{extension}' not allowed. "
            f"Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    return True


def validate_file_size(file_size: int) -> bool:
    """
    Check if file size is within limits.

    Args:
        file_size: Size of file in bytes

    Returns:
        True if size is valid

    Raises:
        ValidationError: If file is too large
    """
    if file_size > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        raise ValidationError(f"File size exceeds maximum allowed ({max_mb}MB)")

    return True


def validate_url(url: str) -> bool:
    """
    Validate URL format.

    Args:
        url: URL to validate

    Returns:
        True if URL is valid

    Raises:
        ValidationError: If URL is invalid
    """
    if not url or not url.strip():
        raise ValidationError("URL cannot be empty")

    if len(url) > MAX_URL_LENGTH:
        raise ValidationError(f"URL exceeds maximum length ({MAX_URL_LENGTH})")

    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValidationError("Invalid URL format")

        if result.scheme not in ("http", "https"):
            raise ValidationError("URL must use http or https protocol")

    except Exception as e:
        raise ValidationError(f"Invalid URL: {str(e)}")

    return True


def validate_text_input(text: str) -> bool:
    """
    Validate text input.

    Args:
        text: Text to validate

    Returns:
        True if text is valid

    Raises:
        ValidationError: If text is invalid
    """
    if not text or not text.strip():
        raise ValidationError("Text cannot be empty")

    if len(text) > MAX_TEXT_LENGTH:
        raise ValidationError(
            f"Text exceeds maximum length ({MAX_TEXT_LENGTH} characters)"
        )

    return True


def validate_query(query: str) -> bool:
    """
    Validate user query.

    Args:
        query: Query to validate

    Returns:
        True if query is valid

    Raises:
        ValidationError: If query is invalid
    """
    if not query or not query.strip():
        raise ValidationError("Please enter a question")

    if len(query) < 3:
        raise ValidationError("Query must be at least 3 characters")

    if len(query) > 5000:
        raise ValidationError("Query exceeds maximum length (5000 characters)")

    return True


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = os.path.basename(filename)

    # Replace special characters
    filename = re.sub(r"[^\w\s.-]", "", filename)

    # Replace spaces with underscores
    filename = filename.replace(" ", "_")

    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]

    return name + ext


def get_file_type(filename: str) -> Optional[str]:
    """
    Get file type from filename.

    Args:
        filename: Name of the file

    Returns:
        File type (extension) or None
    """
    if "." in filename:
        return filename.rsplit(".", 1)[1].lower()
    return None
