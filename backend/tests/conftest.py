"""
Pytest configuration and fixtures.
Provides shared fixtures for all tests.
"""

import os
import sys
import tempfile
from typing import Generator

import pytest
from httpx import ASGITransport, AsyncClient

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    """Create async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return """
    AutoDocThinker is an AI-powered document intelligence platform.
    It enables users to extract insights from uploaded files through natural language queries.
    The system uses a multi-agent workflow to process documents intelligently.
    """


@pytest.fixture
def sample_query():
    """Sample query for testing."""
    return "What is AutoDocThinker?"


@pytest.fixture
def temp_text_file(sample_text: str) -> Generator[str, None, None]:
    """Create a temporary text file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(sample_text)
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def initial_state(sample_query: str):
    """Create initial agent state for testing."""
    return {
        "input": sample_query,
        "file_content": None,
        "file_type": None,
        "context": None,
        "answer": None,
        "history": [],
        "source": None,
        "error": None,
        "metadata": None,
    }
