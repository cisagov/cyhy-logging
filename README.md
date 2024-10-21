# cyhy-logging 🪵 #

[![GitHub Build Status](https://github.com/cisagov/cyhy-logging/workflows/build/badge.svg)](https://github.com/cisagov/cyhy-logging/actions)
[![CodeQL](https://github.com/cisagov/cyhy-logging/workflows/CodeQL/badge.svg)](https://github.com/cisagov/cyhy-logging/actions/workflows/codeql-analysis.yml)
[![Coverage Status](https://coveralls.io/repos/github/cisagov/cyhy-logging/badge.svg?branch=develop)](https://coveralls.io/github/cisagov/cyhy-logging?branch=develop)
[![Known Vulnerabilities](https://snyk.io/test/github/cisagov/cyhy-logging/develop/badge.svg)](https://snyk.io/test/github/cisagov/cyhy-logging)

This is a Python package that provides a standard logging configuration which is
used by the Cyber Hygiene (CyHy) system.

The logging setup uses the
[`RichHandler`](https://rich.readthedocs.io/en/stable/logging.html) to provide
visually appealing and informative log outputs, including enhanced tracebacks
when debugging.  Additionally, default filters like the
[`RedactPasswordFilter`](src/cyhy_logging/log_filters.py) are applied to all log
handlers to automatically filter and redact sensitive information.

To ensure that all logs across different parts of the CyHy system are properly
grouped under a single root, the `CYHY_ROOT_LOGGER` constant is used. By using
this constant when configuring loggers (`CYHY_ROOT_LOGGER` as the root logger),
all log messages are consistently organized under the same logging namespace,
which simplifies log management and makes it easier to locate all related logs.
Additionally, using `CYHY_ROOT_LOGGER` allows the verbosity of CyHy logs to be
increased independently without affecting the verbosity of other packages that
use the logging system.

## Pre-requisites ##

- [Python 3.12](https://www.python.org/downloads/) or newer

## Example Usage ##

```python
from cyhy_logging import CYHY_ROOT_LOGGER, setup_logging
import logging

# Set up logging
logger = logging.getLogger(f"{CYHY_ROOT_LOGGER}.{__name__}")
setup_logging("DEBUG")

# Use the logger
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

# The logger will redact sensitive information by default
logger.info("Logging into database at https://admin:password@example.com/secret")

# Raise an exception to demonstrate the enhanced traceback
raise Exception("This is an exception")

# Shutdown logging
logging.shutdown()
```

Output:

```console
[13:37:28] DEBUG    This is a debug message                   <python-input-0>:9
           INFO     This is an info message                  <python-input-0>:10
           WARNING  This is a warning message                <python-input-0>:11
           ERROR    This is an error message                 <python-input-0>:12
           CRITICAL This is a critical message               <python-input-0>:13
           INFO     Logging into database at                 <python-input-0>:16
                    https://admin:****@example.com/secret
╭───────────────────── Traceback (most recent call last) ──────────────────────╮
│ in <module>:18                                                               │
│ ╭───────────────────────────────── locals ─────────────────────────────────╮ │
│ │ CYHY_ROOT_LOGGER = 'cyhy'                                                │ │
│ │           logger = <Logger cyhy.__main__ (DEBUG)>                        │ │
│ │          logging = <module 'logging' from                                │ │
│ │                    '/Users/lemmy/.pyenv/versions/3.13.0/lib/python3.13/… │ │
│ ╰──────────────────────────────────────────────────────────────────────────╯ │
╰──────────────────────────────────────────────────────────────────────────────╯
Exception: This is an exception
```

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
