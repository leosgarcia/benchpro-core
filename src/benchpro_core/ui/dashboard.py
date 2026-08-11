"""Pragmatic startup dashboard for Bench Pro Core."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from benchpro_core.module_host.contracts import SUPPORTED_INTEGRATION_API
from benchpro_core.module_host.loader import FailedModule
from benchpro_core.ui.text import sanitize_error_message
from benchpro_core.version import __version__


class CoreDashboardWidget(QWidget):
    """Shows available modules and Core-level operational context."""

    module_requested = Signal(str)

    def __init__(self, modules: list[Any], failed_modules: list[FailedModule], parent=None):
        super().__init__(parent)
        self.modules = list(modules)
        self.failed_modules = list(failed_modules)
        self.module_buttons: dict[str, QPushButton] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 22, 24, 22)
        outer.setSpacing(16)

        title = QLabel("Bench Pro Core")
        title.setObjectName("dashboardTitle")
        subtitle = QLabel("Suíte local de diagnósticos técnicos WL Tech")
        subtitle.setObjectName("dashboardSubtitle")
        subtitle.setWordWrap(True)
        outer.addWidget(title)
        outer.addWidget(subtitle)

        summary = QGroupBox("Resumo do Ecossistema")
        summary_layout = QGridLayout(summary)
        summary_layout.setHorizontalSpacing(18)
        summary_layout.setVerticalSpacing(6)
        summary_values = [
            ("Módulos disponíveis", str(len(self.modules))),
            ("Módulos carregados", str(len(self.modules))),
            ("Módulos indisponíveis", str(len(self.failed_modules))),
            ("Integration API suportada", ", ".join(str(api) for api in sorted(SUPPORTED_INTEGRATION_API))),
            ("Core", f"{__version__}"),
            ("Status geral", "Operacional" if not self.failed_modules else "Atenção"),
        ]
        for index, (label, value) in enumerate(summary_values):
            row = index // 3
            col = (index % 3) * 2
            summary_layout.addWidget(QLabel(f"{label}:"), row, col)
            value_label = QLabel(value)
            value_label.setObjectName("dashboardValue")
            summary_layout.addWidget(value_label, row, col + 1)
        outer.addWidget(summary)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        cards_host = QWidget()
        cards_layout = QGridLayout(cards_host)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(12)

        for index, module in enumerate(self.modules):
            cards_layout.addWidget(self._module_card(module), index // 2, index % 2)
        for index, failed in enumerate(self.failed_modules, start=len(self.modules)):
            cards_layout.addWidget(self._failed_card(failed), index // 2, index % 2)
        if not self.modules and not self.failed_modules:
            cards_layout.addWidget(self._empty_card(), 0, 0)

        scroll.setWidget(cards_host)
        outer.addWidget(scroll, 1)

        note = QLabel("Novos módulos serão exibidos automaticamente quando instalados.")
        note.setObjectName("dashboardNote")
        note.setWordWrap(True)
        outer.addWidget(note)

    def _module_card(self, module: Any) -> QGroupBox:
        card = QGroupBox(str(module.display_name))
        card.setObjectName("moduleCard")
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        layout.addWidget(QLabel(f"Versão: {module.version}"))
        layout.addWidget(QLabel("Status: Disponível"))
        capabilities = ", ".join(sorted(str(capability) for capability in module.capabilities)) or "-"
        capabilities_label = QLabel(f"Capacidades: {capabilities}")
        capabilities_label.setWordWrap(True)
        layout.addWidget(capabilities_label)
        button = QPushButton("Abrir módulo")
        button.setObjectName("primaryButton")
        button.clicked.connect(lambda _checked=False, module_id=module.module_id: self.module_requested.emit(module_id))
        self.module_buttons[module.module_id] = button
        layout.addWidget(button)
        layout.addStretch(1)
        return card

    def _failed_card(self, failed: FailedModule) -> QGroupBox:
        card = QGroupBox(str(failed.name))
        card.setObjectName("moduleCard")
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        layout.addWidget(QLabel("Status: Indisponível"))
        reason = QLabel(sanitize_error_message(failed.message))
        reason.setWordWrap(True)
        layout.addWidget(reason)
        return card

    def _empty_card(self) -> QGroupBox:
        card = QGroupBox("Nenhum módulo disponível")
        card.setObjectName("moduleCard")
        layout = QVBoxLayout(card)
        body = QLabel("Instale módulos compatíveis com benchpro.modules para começar.")
        body.setWordWrap(True)
        layout.addWidget(body)
        return card
