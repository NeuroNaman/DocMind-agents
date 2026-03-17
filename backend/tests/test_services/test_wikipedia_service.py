"""
Tests for Wikipedia service.
"""

from unittest.mock import MagicMock, patch

from app.services.wikipedia_service import WikipediaService, get_wikipedia_service


class TestWikipediaService:
    """Tests for WikipediaService class."""

    @patch("app.services.wikipedia_service.WikipediaQueryRun")
    @patch("app.services.wikipedia_service.WikipediaAPIWrapper")
    def test_singleton_pattern(self, mock_wrapper, mock_query_run):
        """Test singleton pattern returns same instance."""
        # Reset singleton for testing
        WikipediaService._instance = None
        WikipediaService._wikipedia = None

        service1 = WikipediaService()
        service2 = WikipediaService()

        assert service1 is service2

    @patch("app.services.wikipedia_service.WikipediaQueryRun")
    @patch("app.services.wikipedia_service.WikipediaAPIWrapper")
    def test_search_success(self, mock_wrapper, mock_query_run):
        """Test successful Wikipedia search."""
        # Reset singleton
        WikipediaService._instance = None
        WikipediaService._wikipedia = None

        mock_run_instance = MagicMock()
        mock_run_instance.run.return_value = "Python is a programming language."
        mock_query_run.return_value = mock_run_instance

        service = WikipediaService()
        result = service.search("Python programming")

        assert result == "Python is a programming language."
        mock_run_instance.run.assert_called_once_with("Python programming")

    @patch("app.services.wikipedia_service.WikipediaQueryRun")
    @patch("app.services.wikipedia_service.WikipediaAPIWrapper")
    def test_search_failure(self, mock_wrapper, mock_query_run):
        """Test Wikipedia search failure."""
        WikipediaService._instance = None
        WikipediaService._wikipedia = None

        mock_run_instance = MagicMock()
        mock_run_instance.run.side_effect = Exception("API error")
        mock_query_run.return_value = mock_run_instance

        service = WikipediaService()
        result = service.search("Test query")

        assert "failed" in result.lower()

    @patch("app.services.wikipedia_service.WikipediaQueryRun")
    @patch("app.services.wikipedia_service.WikipediaAPIWrapper")
    def test_get_summary_calls_search(self, mock_wrapper, mock_query_run):
        """Test get_summary calls search method."""
        WikipediaService._instance = None
        WikipediaService._wikipedia = None

        mock_run_instance = MagicMock()
        mock_run_instance.run.return_value = "Summary text"
        mock_query_run.return_value = mock_run_instance

        service = WikipediaService()
        result = service.get_summary("Python")

        assert result == "Summary text"


class TestGetWikipediaService:
    """Tests for get_wikipedia_service function."""

    @patch("app.services.wikipedia_service.WikipediaQueryRun")
    @patch("app.services.wikipedia_service.WikipediaAPIWrapper")
    def test_returns_service_instance(self, mock_wrapper, mock_query_run):
        """Test that function returns WikipediaService instance."""
        # Reset globals
        import app.services.wikipedia_service as ws

        ws._wikipedia_service = None
        WikipediaService._instance = None
        WikipediaService._wikipedia = None

        result = get_wikipedia_service()

        assert isinstance(result, WikipediaService)

    @patch("app.services.wikipedia_service.WikipediaQueryRun")
    @patch("app.services.wikipedia_service.WikipediaAPIWrapper")
    def test_singleton_global(self, mock_wrapper, mock_query_run):
        """Test global singleton pattern."""
        import app.services.wikipedia_service as ws

        ws._wikipedia_service = None
        WikipediaService._instance = None
        WikipediaService._wikipedia = None

        service1 = get_wikipedia_service()
        service2 = get_wikipedia_service()

        assert service1 is service2
