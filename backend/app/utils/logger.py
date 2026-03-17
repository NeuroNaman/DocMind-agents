"""
Logging configuration for AutoDocThinker.
Sets up structured logging with file and console handlers.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler


def setup_logging(app=None) -> logging.Logger:
    """
    Configure application logging.

    Args:
        app: Application instance (optional)

    Returns:
        Configured logger instance
    """
    # Get configuration
    if app and hasattr(app, "config"):
        # Handle both dict-like and object-like config
        if isinstance(app.config, dict):
            log_file = app.config.get("LOG_FILE", "logs/app.log")
            log_level = app.config.get("LOG_LEVEL", "INFO")
        else:
            log_file = getattr(app.config, "LOG_FILE", "logs/app.log")
            log_level = getattr(app.config, "LOG_LEVEL", "INFO")
    else:
        log_file = "logs/app.log"
        log_level = "INFO"

    # Create logger
    logger = logging.getLogger("autodocthinker")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if log_level == "DEBUG" else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (will be prefixed with 'autodocthinker.')

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"autodocthinker.{name}")
    return logging.getLogger("autodocthinker")
