"""Container used to host module-provided widgets."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from benchpro_core.ui.empty_state import EmptyStateWidget


class ModuleContainer(QWidget):
    """Displays the currently selected module widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_widget: QWidget | None = None
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.show_empty_state()

    def clear(self) -> None:
        if self._current_widget is not None:
            self._layout.removeWidget(self._current_widget)
            self._current_widget.hide()
            self._current_widget = None

    def show_module(self, widget: QWidget) -> None:
        self.clear()
        self._current_widget = widget
        if widget.parent() is None:
            widget.setParent(self)
        self._layout.addWidget(widget)
        widget.show()

    def show_empty_state(self, module_count: int = 0) -> None:
        self.clear()
        self.show_module(EmptyStateWidget(module_count=module_count, parent=self))

    def show_error(self, title: str, message: str, reason: str | None = None) -> None:
        self.clear()
        error_widget = QWidget(self)
        layout = QVBoxLayout(error_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)

        heading = QLabel(title)
        heading.setObjectName("errorTitle")
        heading.setAlignment(Qt.AlignCenter)

        body = QLabel(message)
        body.setAlignment(Qt.AlignCenter)
        body.setWordWrap(True)

        layout.addWidget(heading)
        layout.addWidget(body)

        if reason:
            reason_label = QLabel(f"Motivo:\n{reason}")
            reason_label.setObjectName("errorReason")
            reason_label.setAlignment(Qt.AlignCenter)
            reason_label.setWordWrap(True)
            layout.addWidget(reason_label)

        footer = QLabel("Consulte os logs para detalhes técnicos.")
        footer.setObjectName("errorFooter")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        error_widget.setStyleSheet(
            "QLabel#errorTitle { font-size: 18px; font-weight: 600; color: #fca5a5; }"
            "QLabel#errorReason { color: #f4f4f5; }"
            "QLabel#errorFooter { color: #a1a1aa; }"
            "QLabel { color: #d4d4d8; }"
        )
        self.show_module(error_widget)

    @property
    def current_widget(self) -> QWidget | None:
        return self._current_widget
