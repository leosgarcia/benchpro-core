"""PySide6 smoke and hardening tests for the Bench Pro Core GUI shell."""

import pytest
from PySide6.QtCore import QByteArray, QSettings, Qt
from PySide6.QtWidgets import QApplication, QLabel

from benchpro_core.module_host.loader import FailedModule, LoadedModule
from benchpro_core.module_host.registry import ModuleRegistry
from benchpro_core.ui.about import AboutDialog
from benchpro_core.ui.dashboard import CoreDashboardWidget
from benchpro_core.ui.empty_state import EmptyStateWidget
from benchpro_core.ui.main_window import BenchProMainWindow
from benchpro_core.ui.module_container import ModuleContainer
from benchpro_core.ui.text import sanitize_error_message


class FakeModule:
    def __init__(self, module_id="fake", display_name="Fake Bench Pro"):
        self.module_id = module_id
        self.display_name = display_name
        self.version = "1.0.0"
        self.integration_api = 1
        self.vendor = "WL Tech"
        self.capabilities = {"benchmark"}
        self.create_widget_calls = 0
        self.shutdown_called = False

    def initialize(self, context=None):
        pass

    def create_widget(self, parent=None):
        self.create_widget_calls += 1
        return QLabel(f"{self.display_name} widget", parent)

    def shutdown(self):
        self.shutdown_called = True


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def settings(tmp_path):
    settings_obj = QSettings(str(tmp_path / "benchpro-core-test.ini"), QSettings.IniFormat)
    settings_obj.clear()
    return settings_obj


def loaded(module: FakeModule) -> LoadedModule:
    return LoadedModule(name=module.module_id, module=module)


def test_main_window_instantiates(qapp, settings):
    window = BenchProMainWindow(loaded_modules=[], settings=settings)

    assert window.windowTitle() == "Bench Pro Core"
    assert window.navigation is not None
    assert window.module_container is not None

    window.close()


def test_dashboard_appears_on_startup(qapp, settings):
    window = BenchProMainWindow(loaded_modules=[], settings=settings)

    assert isinstance(window.module_container.current_widget, CoreDashboardWidget)

    window.close()


def test_empty_state_zero_modules_text(qapp):
    widget = EmptyStateWidget(module_count=0)
    labels = "\n".join(label.text() for label in widget.findChildren(QLabel))

    assert "Nenhum módulo compatível encontrado." in labels
    assert "Verifique a instalação dos módulos Bench Pro." in labels


def test_valid_module_appears_in_navigation(qapp, settings):
    module = FakeModule(module_id="dns", display_name="DNS Bench Pro")
    window = BenchProMainWindow(loaded_modules=[loaded(module)], settings=settings)

    payload = window.navigation.list_widget.item(0).data(Qt.UserRole)

    assert window.navigation.list_widget.count() == 1
    assert window.navigation.list_widget.item(0).text() == "DNS Bench Pro"
    assert payload == {"kind": "module", "module_id": "dns"}

    window.close()


def test_failed_module_does_not_crash_main_window(qapp, settings):
    failed = FailedModule(name="smtp", error_type="ModuleLoadError", message="simulated failure")
    window = BenchProMainWindow(loaded_modules=[], failed_modules=[failed], settings=settings)

    assert window.navigation.list_widget.count() == 2
    assert window.navigation.list_widget.item(0).text() == "Módulos indisponíveis"
    assert "Estado: Indisponível" in window.navigation.list_widget.item(1).text()

    window.close()


def test_unavailable_module_selection_shows_sanitized_error(qapp, settings):
    failed = FailedModule(
        name="smtp",
        error_type="ModuleLoadError",
        message="token=abc123 failed at C:\\secret\\smtp_module.py",
    )
    window = BenchProMainWindow(loaded_modules=[], failed_modules=[failed], settings=settings)

    window.navigation.list_widget.setCurrentRow(1)
    qapp.processEvents()
    labels = "\n".join(label.text() for label in window.module_container.findChildren(QLabel))

    assert "Módulo indisponível" in labels
    assert "Não foi possível carregar este módulo." in labels
    assert "token=<redacted>" in labels
    assert "C:\\secret" not in labels

    window.close()


def test_clicking_module_creates_and_mounts_widget(qapp, settings):
    module = FakeModule(module_id="dns", display_name="DNS Bench Pro")
    window = BenchProMainWindow(loaded_modules=[loaded(module)], settings=settings)

    window.navigation.list_widget.setCurrentRow(0)
    qapp.processEvents()

    assert module.create_widget_calls == 1
    assert isinstance(window.module_container.current_widget, QLabel)
    assert window.module_container.current_widget.text() == "DNS Bench Pro widget"

    window.close()


def test_widget_is_reused_when_switching_modules(qapp, settings):
    dns = FakeModule(module_id="dns", display_name="DNS Bench Pro")
    ssl = FakeModule(module_id="ssl", display_name="SSL Bench Pro")
    window = BenchProMainWindow(loaded_modules=[loaded(dns), loaded(ssl)], settings=settings)

    window.navigation.list_widget.setCurrentRow(0)
    window.navigation.list_widget.setCurrentRow(1)
    window.navigation.list_widget.setCurrentRow(0)
    qapp.processEvents()

    assert dns.create_widget_calls == 1
    assert ssl.create_widget_calls == 1
    assert window.module_container.current_widget.text() == "DNS Bench Pro widget"

    window.close()


def test_shutdown_all_called_on_close(qapp, settings):
    module = FakeModule(module_id="dns", display_name="DNS Bench Pro")
    registry = ModuleRegistry()
    registry.register(loaded(module))
    window = BenchProMainWindow(registry=registry, loaded_modules=[], settings=settings)

    window.close()
    qapp.processEvents()

    assert module.shutdown_called is True


def test_about_shows_core_version_api_and_modules(qapp):
    module = FakeModule(module_id="dns", display_name="DNS Bench Pro")
    failed = FailedModule(name="smtp", error_type="ModuleLoadError", message="C:\\tmp\\broken.py password=123")
    dialog = AboutDialog(modules=[module], failed_modules=[failed])

    labels = "\n".join(label.text() for label in dialog.findChildren(QLabel))

    assert "Bench Pro Core" in labels
    assert "Version 0.1.0" in labels
    assert "Integration API 1" in labels
    assert "DNS Bench Pro 1.0.0" in labels
    assert "Módulos indisponíveis" in labels
    assert "password=<redacted>" in labels
    assert "C:\\tmp" not in labels

    dialog.close()


def test_multiple_fake_modules_appear(qapp, settings):
    dns = FakeModule(module_id="dns", display_name="DNS Bench Pro")
    ssl = FakeModule(module_id="ssl", display_name="SSL Bench Pro")
    window = BenchProMainWindow(loaded_modules=[loaded(dns), loaded(ssl)], settings=settings)

    items = [window.navigation.list_widget.item(index).text() for index in range(window.navigation.list_widget.count())]

    assert items == ["DNS Bench Pro", "SSL Bench Pro"]

    window.close()


def test_settings_save_geometry_on_close(qapp, settings):
    window = BenchProMainWindow(loaded_modules=[], settings=settings)
    window.resize(1111, 711)

    window.close()
    qapp.processEvents()

    assert isinstance(settings.value("window/geometry"), QByteArray)
    assert settings.value("window/navigation_width", type=int) > 0


def test_settings_restore_geometry(qapp, settings):
    first = BenchProMainWindow(loaded_modules=[], settings=settings)
    first.resize(1111, 711)
    first.close()
    qapp.processEvents()

    second = BenchProMainWindow(loaded_modules=[], settings=settings)

    assert second.size().width() >= 980
    assert second.size().height() >= 620

    second.close()


def test_invalid_settings_fallback(qapp, settings):
    settings.setValue("window/geometry", QByteArray(b"invalid"))
    settings.setValue("window/navigation_width", -5)

    window = BenchProMainWindow(loaded_modules=[], settings=settings)

    assert window.size().width() >= 980
    assert window.size().height() >= 620

    window.close()


def test_status_bar_startup_final(qapp, settings):
    module = FakeModule(module_id="dns", display_name="DNS Bench Pro")
    window = BenchProMainWindow(loaded_modules=[loaded(module)], settings=settings)

    assert window.status_bar.currentMessage() == "Pronto | 1 módulo carregado"

    window.close()


def test_shutdown_persists_settings(qapp, settings):
    window = BenchProMainWindow(loaded_modules=[], settings=settings)

    window.close()
    qapp.processEvents()

    assert settings.contains("window/geometry")
    assert settings.contains("window/maximized")


def test_error_sanitization_removes_paths_and_secrets():
    message = sanitize_error_message("password=hunter2 failed at C:\\Users\\name\\secret.py")

    assert "password=<redacted>" in message
    assert "C:\\Users" not in message


def test_module_container_error_reason(qapp):
    container = ModuleContainer()

    container.show_error("Módulo indisponível", "Não foi possível carregar este módulo.", "erro resumido")
    labels = "\n".join(label.text() for label in container.findChildren(QLabel))

    assert "Módulo indisponível" in labels
    assert "erro resumido" in labels


def test_dashboard_lists_modules_versions_and_opens_module(qapp, settings):
    module = FakeModule(module_id="dns", display_name="DNS Bench Pro")
    window = BenchProMainWindow(loaded_modules=[loaded(module)], settings=settings)

    dashboard = window.module_container.current_widget
    assert isinstance(dashboard, CoreDashboardWidget)
    labels = "\n".join(label.text() for label in dashboard.findChildren(QLabel))
    assert "dns" in dashboard.module_buttons
    assert "Versão: 1.0.0" in labels
    assert "Status: Disponível" in labels
    assert "HTTP Bench Pro" not in labels

    dashboard.module_buttons["dns"].click()
    qapp.processEvents()

    assert module.create_widget_calls == 1
    assert window.module_container.current_widget.text() == "DNS Bench Pro widget"
    assert "Versão 1.0.0" in window.module_container._subtitle.text()

    window.close()


def test_dashboard_shows_failed_module_as_unavailable(qapp, settings):
    failed = FailedModule(name="smtp", error_type="ModuleLoadError", message="simulated failure")
    window = BenchProMainWindow(loaded_modules=[], failed_modules=[failed], settings=settings)

    dashboard = window.module_container.current_widget
    assert isinstance(dashboard, CoreDashboardWidget)
    labels = "\n".join(label.text() for label in dashboard.findChildren(QLabel))
    assert "Status: Indisponível" in labels
    assert "simulated failure" in labels

    window.close()


def test_navigation_tooltip_contains_generic_metadata(qapp, settings):
    module = FakeModule(module_id="smtp", display_name="SMTP Bench Pro")
    window = BenchProMainWindow(loaded_modules=[loaded(module)], settings=settings)

    tooltip = window.navigation.list_widget.item(0).toolTip()
    assert "SMTP Bench Pro" in tooltip
    assert "Versão 1.0.0" in tooltip
    assert "Integration API 1" in tooltip
    assert "Capacidades: benchmark" in tooltip

    window.close()
