"""About dialog for Bench Pro Core."""

from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

from benchpro_core.module_host.contracts import SUPPORTED_INTEGRATION_API
from benchpro_core.ui.text import sanitize_error_message
from benchpro_core.version import __version__


class AboutDialog(QDialog):
    """Simple product about dialog."""

    def __init__(self, modules: list[object] | None = None, failed_modules: list[object] | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sobre o Bench Pro Core")
        self.setMinimumWidth(400)

        modules = modules or []
        failed_modules = failed_modules or []
        api_versions = ", ".join(str(version) for version in sorted(SUPPORTED_INTEGRATION_API))
        module_lines = "\n".join(f"- {module.display_name} {module.version}" for module in modules)
        if not module_lines:
            module_lines = "Nenhum módulo carregado."

        failed_lines = "\n".join(
            f"- {module.name}: {sanitize_error_message(module.message)}" for module in failed_modules
        )

        layout = QVBoxLayout(self)
        title = QLabel(f"<b>Bench Pro Core</b><br/>Version {__version__}<br/>Integration API {api_versions}")
        description = QLabel("Host e agregador do ecossistema Bench Pro.")
        vendor = QLabel("WL Tech<br/>© 2026 WL Tech")
        loaded_modules = QLabel(f"<b>Módulos carregados</b><br/><pre>{module_lines}</pre>")
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.accept)

        for label in (title, description, vendor, loaded_modules):
            label.setWordWrap(True)
            layout.addWidget(label)

        if failed_lines:
            failed_label = QLabel(f"<b>Módulos indisponíveis</b><br/><pre>{failed_lines}</pre>")
            failed_label.setWordWrap(True)
            layout.addWidget(failed_label)

        layout.addWidget(close_button)
