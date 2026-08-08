"""Logging setup for Bench Pro Core."""

import logging
from logging.handlers import RotatingFileHandler
import sys

from benchpro_core.paths import logs_dir

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"


def configure_logging() -> None:
    """Configure console logging and best-effort rotating file logging."""
    root = logging.getLogger()
    if root.handlers:
        return

    root.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    try:
        file_handler = RotatingFileHandler(
            logs_dir() / "bench-pro-core.log",
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
    except OSError as exc:
        root.warning("File logging unavailable; continuing with console logging: %s", exc)
