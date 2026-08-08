"""Application paths for Bench Pro Core."""

from __future__ import annotations

import os
from pathlib import Path

VENDOR_NAME = "WL Tech"
APP_NAME = "Bench Pro Core"


def app_data_dir() -> Path:
    """Return the product-owned application data directory for Bench Pro Core."""
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    path = base / VENDOR_NAME / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def logs_dir() -> Path:
    """Return the Core log directory, creating it when possible."""
    path = app_data_dir() / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def settings_dir() -> Path:
    """Return the Core settings directory, creating it when possible."""
    path = app_data_dir() / "settings"
    path.mkdir(parents=True, exist_ok=True)
    return path
