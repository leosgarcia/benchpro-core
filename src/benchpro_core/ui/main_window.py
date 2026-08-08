"""Main window for the first functional Bench Pro Core shell."""

import logging

from PySide6.QtCore import QByteArray, QSettings
from PySide6.QtGui import QAction, QGuiApplication
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QMessageBox, QStatusBar, QWidget

from benchpro_core.module_host.discovery import discover_modules
from benchpro_core.module_host.errors import DuplicateModuleError
from benchpro_core.module_host.loader import FailedModule, LoadedModule, load_modules
from benchpro_core.module_host.registry import ModuleRegistry
from benchpro_core.ui.about import AboutDialog
from benchpro_core.ui.module_container import ModuleContainer
from benchpro_core.ui.navigation import ModuleNavigation
from benchpro_core.ui.text import sanitize_error_message

logger = logging.getLogger(__name__)

DEFAULT_WINDOW_SIZE = (1200, 800)
DEFAULT_NAV_WIDTH = 240


class BenchProMainWindow(QMainWindow):
    """Minimal Core shell that hosts module-provided widgets."""

    def __init__(
        self,
        registry: ModuleRegistry | None = None,
        loaded_modules: list[LoadedModule] | None = None,
        failed_modules: list[FailedModule] | None = None,
        settings: QSettings | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.settings = settings or QSettings("WL Tech", "Bench Pro Core")
        self.registry = registry or ModuleRegistry()
        self.failed_modules = list(failed_modules or [])
        self._widget_cache: dict[str, QWidget] = {}
        self._loaded_modules_injected = loaded_modules is not None

        self.setWindowTitle("Bench Pro Core")
        self.setMinimumSize(980, 620)

        self.navigation = ModuleNavigation(self)
        self.module_container = ModuleContainer(self)

        self._create_menu()
        self._create_layout()
        self._create_status_bar()
        self._apply_theme()
        self._restore_window_state()
        self._set_status("Inicializando Bench Pro Core...")
        self._load_startup_modules(loaded_modules)
        self._populate_navigation()
        self.module_container.show_empty_state(len(self.registry.list_modules()))
        self._set_ready_status()

    def _create_layout(self) -> None:
        central = QWidget(self)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.navigation)
        layout.addWidget(self.module_container, 1)
        self.setCentralWidget(central)
        self.navigation.module_selected.connect(self.activate_module)
        self.navigation.unavailable_selected.connect(self.show_unavailable_module)

    def _create_status_bar(self) -> None:
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self._set_status("Inicializando Bench Pro Core...")

    def _create_menu(self) -> None:
        file_menu = self.menuBar().addMenu("&Arquivo")
        exit_action = QAction("&Sair", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = self.menuBar().addMenu("&Ajuda")
        about_action = QAction("&Sobre o Bench Pro Core", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def _apply_theme(self) -> None:
        self.setStyleSheet(
            "QMainWindow { background: #27272a; }"
            "QMenuBar { background: #18181b; color: #f4f4f5; }"
            "QMenuBar::item:selected { background: #27272a; }"
            "QMenu { background: #18181b; color: #f4f4f5; border: 1px solid #3f3f46; }"
            "QMenu::item:selected { background: #2563eb; }"
            "QStatusBar { background: #18181b; color: #d4d4d8; }"
        )

    def _restore_window_state(self) -> None:
        restored = False
        geometry = self.settings.value("window/geometry")
        if isinstance(geometry, QByteArray) and not geometry.isEmpty():
            restored = self.restoreGeometry(geometry)

        if restored:
            maximized = self.settings.value("window/maximized", False, type=bool)
            if maximized:
                self.showMaximized()
        else:
            self.resize(*DEFAULT_WINDOW_SIZE)
            self._center_on_screen()

        nav_width = self.settings.value("window/navigation_width", DEFAULT_NAV_WIDTH, type=int)
        if nav_width and nav_width > 0:
            self.navigation.setMinimumWidth(nav_width)

    def _center_on_screen(self) -> None:
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            return
        available = screen.availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(available.center())
        self.move(frame.topLeft())

    def _save_window_state(self) -> None:
        self.settings.setValue("window/geometry", self.saveGeometry())
        self.settings.setValue("window/maximized", self.isMaximized())
        self.settings.setValue("window/navigation_width", self.navigation.width())
        self.settings.sync()

    def _load_startup_modules(self, loaded_modules: list[LoadedModule] | None) -> None:
        logger.info("Bench Pro Core startup")
        modules_to_register = loaded_modules
        if modules_to_register is None:
            self._set_status("Procurando módulos...")
            discovered = discover_modules()
            logger.info("Discovery count: %d", len(discovered))
            result = load_modules(discovered, initialize=True)
            modules_to_register = result.successful_modules
            self.failed_modules.extend(result.failed_modules)

        for loaded_module in modules_to_register:
            try:
                self.registry.register(loaded_module)
            except DuplicateModuleError as exc:
                logger.exception("Duplicate module rejected: %s", loaded_module.name)
                self.failed_modules.append(
                    FailedModule(
                        name=loaded_module.name,
                        error_type=exc.__class__.__name__,
                        message=str(exc),
                        distribution=loaded_module.distribution,
                    )
                )

    def _populate_navigation(self) -> None:
        self.navigation.set_modules(self.registry.list_modules(), self.failed_modules)

    def _set_status(self, message: str) -> None:
        if hasattr(self, "status_bar"):
            self.status_bar.showMessage(message)

    def _set_ready_status(self) -> None:
        loaded_count = len(self.registry.list_modules())
        failed_count = len(self.failed_modules)
        loaded_text = f"{loaded_count} módulo carregado" if loaded_count == 1 else f"{loaded_count} módulos carregados"
        if failed_count:
            failed_text = (
                f"{failed_count} módulo indisponível"
                if failed_count == 1
                else f"{failed_count} módulos indisponíveis"
            )
            self._set_status(f"Pronto | {loaded_text} | {failed_text}")
        else:
            self._set_status(f"Pronto | {loaded_text}")

    def activate_module(self, module_id: str) -> None:
        module = self.registry.get(module_id)
        if module is None:
            self.module_container.show_error("Módulo indisponível", "Não foi possível carregar este módulo.")
            self._set_status(f"Falha ao carregar módulo {module_id}")
            return

        try:
            if module_id not in self._widget_cache:
                logger.info("Creating widget for module: %s", module_id)
                self._set_status(f"Carregando {module.display_name}...")
                self._widget_cache[module_id] = module.create_widget(parent=self.module_container)
            self.module_container.show_module(self._widget_cache[module_id])
            self._set_status(f"{module.display_name} ativo")
            logger.info("Module activated: %s", module_id)
        except Exception as exc:
            logger.exception("Module widget creation failed: %s", module_id)
            safe_reason = sanitize_error_message(exc)
            self.module_container.show_error(
                f"Falha ao carregar {module.display_name}.",
                "Não foi possível carregar este módulo.",
                safe_reason,
            )
            self._set_status(f"Falha ao carregar módulo {module.display_name}")
            QMessageBox.warning(
                self,
                "Falha ao carregar módulo",
                f"Falha ao carregar {module.display_name}.\n\nConsulte os logs para detalhes técnicos.",
            )

    def show_unavailable_module(self, failed_module: FailedModule) -> None:
        safe_reason = sanitize_error_message(failed_module.message)
        self.module_container.show_error(
            "Módulo indisponível",
            "Não foi possível carregar este módulo.",
            safe_reason,
        )
        self._set_status("1 módulo indisponível")

    def show_about(self) -> None:
        dialog = AboutDialog(
            modules=self.registry.list_modules(),
            failed_modules=self.failed_modules,
            parent=self,
        )
        dialog.exec()

    def closeEvent(self, event) -> None:
        logger.info("Bench Pro Core shutdown")
        self._set_status("Finalizando módulos...")
        self._save_window_state()
        errors = self.registry.shutdown_all()
        for error in errors:
            logger.error("Module shutdown error: %s", error)
        for handler in logging.getLogger().handlers:
            handler.flush()
        event.accept()


