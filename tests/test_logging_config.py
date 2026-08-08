"""Tests for Core logging setup."""

import logging

from benchpro_core import logging_config


class BrokenRotatingFileHandler:
    def __init__(self, *args, **kwargs):
        raise OSError("cannot create log file")


def test_logging_fallback_when_file_handler_fails(monkeypatch):
    root = logging.getLogger()
    original_handlers = list(root.handlers)
    original_level = root.level
    root.handlers.clear()

    monkeypatch.setattr(logging_config, "RotatingFileHandler", BrokenRotatingFileHandler)

    try:
        logging_config.configure_logging()
        assert root.handlers
        assert any(isinstance(handler, logging.StreamHandler) for handler in root.handlers)
    finally:
        root.handlers.clear()
        root.handlers.extend(original_handlers)
        root.setLevel(original_level)

