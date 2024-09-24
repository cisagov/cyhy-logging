"""cyhy_logging Python library and tool."""

# Standard Python Libraries
import logging
from typing import Optional

# Third-Party Libraries
from rich.logging import RichHandler
from rich.traceback import install as install_rich_tracebacks

from . import CYHY_ROOT_LOGGER
from .log_filters import RedactPasswordFilter


def setup_logging(log_level: Optional[str] = None) -> None:
    """Set up logging for the CyHy namespace."""
    # If a log_level is provided, ensure it is uppercase
    if log_level:
        log_level = log_level.upper()

    logging.basicConfig(
        datefmt="[%X]",
        force=True,
        format="%(message)s",
        handlers=[RichHandler()],
    )

    # Install the Rich traceback handler
    if log_level == "DEBUG":
        install_rich_tracebacks(show_locals=True)

    # Add a filter to redact passwords from URLs to all handlers of the root logger
    password_redact_filter = RedactPasswordFilter()
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.addFilter(password_redact_filter)

    # Set the log level for the CyHy namespace
    if log_level:
        cyhy_logger = logging.getLogger(CYHY_ROOT_LOGGER)
        cyhy_logger.setLevel(log_level)
