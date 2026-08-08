"""UI-safe text helpers."""

from pathlib import Path
import re

_SECRET_PATTERN = re.compile(r"(?i)(password|passwd|token|secret|api[_-]?key)=([^\s;]+)")
_WINDOWS_PATH_PATTERN = re.compile(r"[A-Za-z]:\\[^\s]+")
_POSIX_PATH_PATTERN = re.compile(r"(?<!\w)/(?:[^\s/]+/)+[^\s]+")


def sanitize_error_message(message: object, max_length: int = 240) -> str:
    """Return a short user-facing error message without paths or obvious secrets."""
    text = str(message) if message else "Erro desconhecido."
    text = _SECRET_PATTERN.sub(r"\1=<redacted>", text)
    text = _WINDOWS_PATH_PATTERN.sub(lambda match: Path(match.group(0)).name or "<path>", text)
    text = _POSIX_PATH_PATTERN.sub(lambda match: Path(match.group(0)).name or "<path>", text)
    text = " ".join(text.split())
    if len(text) > max_length:
        text = text[: max_length - 1].rstrip() + "…"
    return text
