"""Empty state widget for Bench Pro Core."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class EmptyStateWidget(QWidget):
    """Simple empty state shown before a module is selected."""

    def __init__(self, module_count: int = 0, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)

        title = QLabel("Bench Pro Core")
        title.setObjectName("emptyTitle")
        title.setAlignment(Qt.AlignCenter)

        if module_count == 0:
            message_text = "Nenhum módulo compatível encontrado."
            count_text = "Verifique a instalação dos módulos Bench Pro."
        else:
            message_text = "Selecione um módulo para começar."
            count_text = (
                f"{module_count} módulo disponível"
                if module_count == 1
                else f"{module_count} módulos disponíveis"
            )

        message = QLabel(message_text)
        message.setAlignment(Qt.AlignCenter)

        count = QLabel(count_text)
        count.setAlignment(Qt.AlignCenter)
        count.setObjectName("emptyCount")

        layout.addWidget(title)
        layout.addWidget(message)
        layout.addWidget(count)

        self.setStyleSheet(
            "QLabel#emptyTitle { font-size: 22px; font-weight: 600; color: #f4f4f5; }"
            "QLabel { color: #d4d4d8; }"
            "QLabel#emptyCount { color: #a1a1aa; }"
        )

