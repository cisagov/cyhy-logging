"""Test the cyhy_logging module."""

# Standard Python Libraries
import logging
import os

# Third-Party Libraries
import pytest

# cisagov Libraries
from cyhy_logging import CYHY_ROOT_LOGGER, __version__, setup_logging
from cyhy_logging.log_filters import RedactPasswordFilter

# define sources of version strings
RELEASE_TAG = os.getenv("RELEASE_TAG")
PROJECT_VERSION = __version__


@pytest.mark.skipif(
    RELEASE_TAG in [None, ""], reason="this is not a release (RELEASE_TAG not set)"
)
def test_release_version():
    """Verify that release tag version agrees with the module version."""
    assert (
        RELEASE_TAG == f"v{PROJECT_VERSION}"
    ), "RELEASE_TAG does not match the project version"


def test_setup_logging_no_log_level():
    """Test with no log level."""
    setup_logging()
    root_logger = logging.getLogger()
    assert any(isinstance(handler, logging.Handler) for handler in root_logger.handlers)


def test_setup_logging_with_debug_level():
    """Test with a specific log level."""
    setup_logging("DEBUG")
    cyhy_logger = logging.getLogger(CYHY_ROOT_LOGGER)
    assert cyhy_logger.level == logging.DEBUG


def test_redact_password_filter_added():
    """Test if RedactPasswordFilter is added."""
    setup_logging()
    root_logger = logging.getLogger()
    assert any(
        isinstance(handler.filters[0], RedactPasswordFilter)
        for handler in root_logger.handlers
        if handler.filters
    )
