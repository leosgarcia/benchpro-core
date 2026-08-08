"""Vertical module navigation for Bench Pro Core."""

from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QVBoxLayout, QWidget

from benchpro_core.ui.text import sanitize_error_message


class ModuleNavigation(QWidget):
    """Lists loaded and unavailable modules."""

    module_selected = Signal(str)
    unavailable_selected = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_widget = QListWidget(self)
        self.list_widget.currentItemChanged.connect(self._on_current_item_changed)
        self.list_widget.itemActivated.connect(self._on_item_activated)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        heading = QLabel("Módulos")
        heading.setObjectName("navHeading")
        layout.addWidget(heading)
        layout.addWidget(self.list_widget)

        self.setMinimumWidth(220)
        self.setMaximumWidth(320)
        self.setStyleSheet(
            "QWidget { background: #18181b; color: #e4e4e7; }"
            "QLabel#navHeading { font-weight: 600; color: #fafafa; }"
            "QListWidget { border: 1px solid #3f3f46; background: #202024; outline: 0; }"
            "QListWidget::item { padding: 8px; border-bottom: 1px solid #2f2f35; }"
            "QListWidget::item:selected { background: #2563eb; color: white; }"
        )

    def set_modules(self, modules: list[Any], failed_modules: list[Any]) -> None:
        self.list_widget.clear()
        for module in modules:
            item = QListWidgetItem(module.display_name)
            item.setData(Qt.UserRole, {"kind": "module", "module_id": module.module_id})
            item.setToolTip(
                f"{module.display_name}\nVersion {module.version}\nIntegration API {module.integration_api}"
            )
            self.list_widget.addItem(item)

        if failed_modules:
            header = QListWidgetItem("Módulos indisponíveis")
            header.setFlags(Qt.NoItemFlags)
            header.setForeground(QBrush(QColor("#a1a1aa")))
            self.list_widget.addItem(header)
            for failed_module in failed_modules:
                reason = sanitize_error_message(failed_module.message)
                item = QListWidgetItem(f"{failed_module.name}\nEstado: Indisponível")
                item.setData(Qt.UserRole, {"kind": "failed", "failed_module": failed_module})
                item.setToolTip(reason)
                item.setForeground(QBrush(QColor("#fca5a5")))
                self.list_widget.addItem(item)

    def _on_current_item_changed(self, current: QListWidgetItem | None, previous: QListWidgetItem | None) -> None:
        if current is not None:
            self._emit_item(current)

    def _on_item_activated(self, item: QListWidgetItem) -> None:
        self._emit_item(item)

    def _emit_item(self, item: QListWidgetItem) -> None:
        payload = item.data(Qt.UserRole)
        if not payload:
            return
        if payload.get("kind") == "module":
            self.module_selected.emit(payload["module_id"])
        elif payload.get("kind") == "failed":
            self.unavailable_selected.emit(payload["failed_module"])
