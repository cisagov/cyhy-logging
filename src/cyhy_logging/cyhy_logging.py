"""cyhy_logging Python library and tool."""

# Standard Python Libraries
import logging
from typing import Optional

# Third-Party Libraries
from rich.logging import RichHandler

from . import CYHY_ROOT_LOGGER
from .log_filters import RedactPasswordFilter


def setup_logging(log_level: Optional[str] = None) -> None:
    """Set up logging for the CyHy namespace."""
    # If a log_level is provided, ensure it is uppercase
    if log_level:
        log_level = log_level.upper()

    is_debug = log_level == logging.DEBUG

    logging.basicConfig(
        datefmt="[%X]",
        format="%(message)s",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                show_path=is_debug,
                tracebacks_show_locals=is_debug,
            )
        ],
    )

    # Add a filter to redact passwords from URLs to all handlers of the root logger
    password_redact_filter = RedactPasswordFilter()
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.addFilter(password_redact_filter)

    # Set the log level for the CyHy namespace
    if log_level:
        cyhy_logger = logging.getLogger(CYHY_ROOT_LOGGER)
        cyhy_logger.setLevel(log_level)
