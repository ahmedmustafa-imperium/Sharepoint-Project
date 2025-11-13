"""
Logging configuration for the SharePoint project.

Sets up root logger, stream handler, and formatting based on settings.
"""
import logging
import sys
from app.core.config import settings

def configure_logging() -> None:
    """
    Configure root logger with level, handler, and formatter.

    Uses LOG_LEVEL from core.config.settings.
    """
    level = getattr(logging, settings.LOG_LEVEL, logging.DEBUG)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout
    )

configure_logging()
logger = logging.getLogger(__name__)
logger.propagate = True  # ensure it bubbles to root logger
