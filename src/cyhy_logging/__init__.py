"""The cyhy_logging library."""

# We disable the following Flake8 checks:
# - "Module level import not at top of file (E402)" here because the constants
#   need to be defined early to prevent a circular import issue.

CYHY_ROOT_LOGGER = "cyhy"


from ._version import __version__  # noqa: E402
from .cyhy_logging import setup_logging  # noqa: E402

__all__ = ["CYHY_ROOT_LOGGER", "setup_logging", "__version__"]
