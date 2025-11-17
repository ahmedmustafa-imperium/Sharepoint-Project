"""
Comprehensive logging setup for the Todo API.
Provides structured logging with appropriate levels, formatters, and handlers.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional
from app.core.filter import ContextFilter

class LoggerSetup:
    """Configures and provides logger instances for the application."""

    _logger: Optional[logging.Logger] = None
    _configured = False

    @staticmethod
    def setup_logger(
        name: str = "todo_api",
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        max_bytes: int = 10485760,
        backup_count: int = 5,
    ) -> logging.Logger:
        """
        Configure and return a logger instance with console and optional file handlers.
 
        Args:
            name (str): Logger name.
            level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
            log_file (Optional[str]): Path to log file. If provided, file handler is added.
            max_bytes (int): Maximum size of log file before rotation (default: 10MB).
            backup_count (int): Number of backup log files to keep (default: 5).
 
        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(name)

        if LoggerSetup._configured:
            return logger
        logger.setLevel(level)

        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()

        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt="%(asctime)s - %(request_id)s - %(name)s - %(levelname)s - "
            "[%(filename)s:%(lineno)d] - %(funcName)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        simple_formatter = logging.Formatter(
            fmt="%(asctime)s - %(request_id)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        console_handler.addFilter(ContextFilter())
        logger.addHandler(console_handler)

        if log_file:
            try:
                file_handler = RotatingFileHandler(
                    log_file, maxBytes=max_bytes, backupCount=backup_count
                )
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(detailed_formatter)
                file_handler.addFilter(ContextFilter())
                logger.addHandler(file_handler)
            except OSError as e:
                logger.warning("Could not set up file logging: %s", str(e))

        logger.propagate = False

        LoggerSetup._configured = True
        LoggerSetup._logger = logger

        logging.getLogger("azure").setLevel(logging.ERROR)
        logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
            logging.ERROR
        )
        logging.getLogger("azure.storage").setLevel(logging.ERROR)
        logging.getLogger("azure.identity").setLevel(logging.ERROR)

        return logger

    @staticmethod
    def get_logger(name: str = "todo_api") -> logging.Logger:
        """
        Get the configured logger instance.
 
        Args:
            name (str): Logger name (default: "todo_api").
 
        Returns:
            logging.Logger: The logger instance.
        """
        if LoggerSetup._logger is None:
            return LoggerSetup.setup_logger(name)
        return LoggerSetup._logger

    @staticmethod
    def set_level(level: int) -> None:
        """
        Set the logging level for all handlers.
 
        Args:
            level (int): New logging level.
        """
        if LoggerSetup._logger:
            LoggerSetup._logger.setLevel(level)
            for handler in LoggerSetup._logger.handlers:
                handler.setLevel(level)


# Module-level convenience functions
def get_logger(name: str = "todo_api") -> logging.Logger:
    """Get or create the configured logger."""
    return LoggerSetup.get_logger(name)


def setup_logger(
    name: str = "todo_api",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Setup and return a configured logger."""
    return LoggerSetup.setup_logger(name, level, log_file)

