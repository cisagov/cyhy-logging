"""Tests for log_filters.py."""

# Standard Python Libraries
import logging

# cisagov Libraries
from cyhy_logging.log_filters import RedactPasswordFilter


def test_redact_password_filter_no_password():
    """Test that URLs without passwords are not modified."""
    log_record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=1,
        msg="Accessing https://example.com/resource",
        args=None,
        exc_info=None,
    )

    # Create the filter instance
    redact_filter = RedactPasswordFilter()

    # Apply the filter
    result = redact_filter.filter(log_record)

    # The log record should remain unchanged
    assert result is True
    assert log_record.msg == "Accessing https://example.com/resource"


def test_redact_password_filter_with_password():
    """Test that URLs with passwords are redacted."""
    log_record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=1,
        msg="Accessing https://user:secret@example.com/resource",
        args=None,
        exc_info=None,
    )

    # Create the filter instance
    redact_filter = RedactPasswordFilter()

    # Apply the filter
    new_record = redact_filter.filter(log_record)

    # The password should be redacted
    assert new_record.msg == "Accessing https://user:****@example.com/resource"


def test_redact_password_filter_multiple_urls():
    """Test that multiple URLs with passwords in a log message are all redacted."""
    log_record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=1,
        msg="Accessing https://user:secret@example.com/resource and https://admin:password@admin.example.com/admin",
        args=None,
        exc_info=None,
    )

    # Create the filter instance
    redact_filter = RedactPasswordFilter()

    # Apply the filter
    new_record = redact_filter.filter(log_record)

    # Both passwords should be redacted
    assert new_record.msg == (
        "Accessing https://user:****@example.com/resource and https://admin:****@admin.example.com/admin"
    )


def test_redact_password_filter_non_url_text():
    """Test that non-URL text is not affected."""
    log_record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=1,
        msg="This is a regular log message without URLs.",
        args=None,
        exc_info=None,
    )

    # Create the filter instance
    redact_filter = RedactPasswordFilter()

    # Apply the filter
    result = redact_filter.filter(log_record)

    # The log message should remain unchanged
    assert result is True
    assert log_record.msg == "This is a regular log message without URLs."


def test_redact_password_filter_empty_message():
    """Test that an empty log message doesn't raise an error."""
    log_record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=1,
        msg="",
        args=None,
        exc_info=None,
    )

    # Create the filter instance
    redact_filter = RedactPasswordFilter()

    # Apply the filter
    result = redact_filter.filter(log_record)

    # The empty log message should remain unchanged
    assert result is True
    assert log_record.msg == ""
