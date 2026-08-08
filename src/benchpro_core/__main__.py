"""Command-line entry point for Bench Pro Core."""

import sys

from PySide6.QtWidgets import QApplication

from benchpro_core.logging_config import configure_logging
from benchpro_core.module_host.discovery import discover_modules
from benchpro_core.module_host.loader import load_modules
from benchpro_core.ui.main_window import BenchProMainWindow
from benchpro_core.version import __version__


def list_modules() -> None:
    print(f"Bench Pro Core {__version__}")
    result = load_modules(discover_modules())
    print()
    print("Discovered modules:")
    if not result.successful_modules:
        print("No compatible modules discovered.")
    for loaded_module in result.successful_modules:
        module = loaded_module.module
        print(f"{module.display_name} {module.version} [API {module.integration_api}]")
    for failed_module in result.failed_modules:
        print(f"{failed_module.name}: {failed_module.error_type}: {failed_module.message}")


def run_gui() -> int:
    configure_logging()
    app = QApplication.instance() or QApplication(sys.argv)
    app.setOrganizationName("WL Tech")
    app.setApplicationName("Bench Pro Core")
    window = BenchProMainWindow()
    window.show()
    return app.exec()


def main() -> None:
    if "--list-modules" in sys.argv:
        list_modules()
        return
    raise SystemExit(run_gui())


if __name__ == "__main__":
    main()
