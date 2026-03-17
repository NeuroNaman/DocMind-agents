"""
Tests for logger utility.
"""

import logging
from unittest.mock import MagicMock

from app.utils.logger import get_logger, setup_logging


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_without_app(self):
        """Test setup_logging without app parameter."""
        # Clear any existing handlers
        logger = logging.getLogger("autodocthinker")
        logger.handlers = []

        result = setup_logging()

        assert result is not None
        assert result.name == "autodocthinker"
        assert len(result.handlers) >= 1

    def test_setup_logging_with_app_config(self):
        """Test setup_logging with app config."""
        # Clear any existing handlers
        logger = logging.getLogger("autodocthinker")
        logger.handlers = []

        mock_app = MagicMock()
        # Make config a dict so isinstance(config, dict) is True
        mock_app.config = {
            "LOG_FILE": "test.log",
            "LOG_LEVEL": "DEBUG",
        }

        result = setup_logging(mock_app)
        assert result is not None

    def test_setup_logging_prevents_duplicate_handlers(self):
        """Test that duplicate handlers are prevented."""
        logger = logging.getLogger("autodocthinker")
        logger.handlers = []

        setup_logging()
        initial_count = len(logger.handlers)

        setup_logging()
        assert len(logger.handlers) == initial_count

    def test_setup_logging_sets_log_level(self):
        """Test that log level is set correctly."""
        logger = logging.getLogger("autodocthinker")
        logger.handlers = []

        result = setup_logging()
        assert result.level == logging.INFO


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_with_name(self):
        """Test get_logger with name parameter."""
        logger = get_logger("test_module")
        assert logger.name == "autodocthinker.test_module"

    def test_get_logger_without_name(self):
        """Test get_logger without name parameter."""
        logger = get_logger()
        assert logger.name == "autodocthinker"

    def test_get_logger_with_none(self):
        """Test get_logger with None parameter."""
        logger = get_logger(None)
        assert logger.name == "autodocthinker"

    def test_get_logger_returns_logger_instance(self):
        """Test that get_logger returns a Logger instance."""
        logger = get_logger("test")
        assert isinstance(logger, logging.Logger)
