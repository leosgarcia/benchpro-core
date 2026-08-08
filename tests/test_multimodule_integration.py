"""Multi-module host validation for DNS + SMTP."""

import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from benchpro_core.module_host.discovery import discover_modules
from benchpro_core.module_host.loader import load_modules
from benchpro_core.ui.main_window import BenchProMainWindow


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def settings(tmp_path):
    settings_obj = QSettings(str(tmp_path / "benchpro-core-multimodule.ini"), QSettings.IniFormat)
    settings_obj.clear()
    return settings_obj


@pytest.mark.integration
def test_real_dns_and_smtp_are_hosted_together(qapp, settings):
    discovered = discover_modules()
    selected = [module for module in discovered if module.name in {"dns", "smtp"}]
    names = {module.name for module in selected}
    if names != {"dns", "smtp"}:
        pytest.skip("DNS and SMTP Bench Pro entry points are not both installed in this Python environment")

    result = load_modules(selected, initialize=True)
    assert result.failed_modules == []
    assert [loaded.module.module_id for loaded in result.successful_modules] == ["dns", "smtp"]

    window = BenchProMainWindow(loaded_modules=result.successful_modules, settings=settings)
    items = [window.navigation.list_widget.item(index).text() for index in range(window.navigation.list_widget.count())]
    assert items == ["DNS Bench Pro", "SMTP Bench Pro"]

    window.activate_module("dns")
    dns_widget_first = window.module_container.current_widget
    window.activate_module("smtp")
    smtp_widget_first = window.module_container.current_widget
    window.activate_module("dns")
    dns_widget_second = window.module_container.current_widget
    window.activate_module("smtp")
    smtp_widget_second = window.module_container.current_widget

    assert dns_widget_first is dns_widget_second
    assert smtp_widget_first is smtp_widget_second
    assert dns_widget_first is not smtp_widget_first
    assert set(window._widget_cache) == {"dns", "smtp"}
    assert window.status_bar.currentMessage() == "SMTP Bench Pro ativo"

    smtp_labels = [smtp_widget_first.tab_widget.tabText(index) for index in range(smtp_widget_first.tab_widget.count())]
    assert "Sobre" not in smtp_labels

    window.close()
    qapp.processEvents()


class FakeDist:
    metadata = {"Name": "fake-dist"}


class FakeEntryPoint:
    def __init__(self, name, target=None, error=None):
        self.name = name
        self._target = target
        self._error = error
        self.dist = FakeDist()

    def load(self):
        if self._error:
            raise self._error
        return self._target


class FakeEntryPoints(list):
    def select(self, group=None):
        return self if group == "benchpro.modules" else []


class ProductModule:
    version = "1.0.0"
    integration_api = 1
    vendor = "WL Tech"
    capabilities = {"benchmark"}

    def initialize(self):
        self.initialized = True

    def create_widget(self, parent=None):
        return None

    def shutdown(self):
        self.shutdown_called = True


class DNSModule(ProductModule):
    module_id = "dns"
    display_name = "DNS Bench Pro"


class SMTPModule(ProductModule):
    module_id = "smtp"
    display_name = "SMTP Bench Pro"
    version = "0.1.0"


def test_smtp_failure_does_not_block_dns(monkeypatch):
    entry_points = FakeEntryPoints([
        FakeEntryPoint("dns", DNSModule),
        FakeEntryPoint("smtp", error=ImportError("smtp exploded")),
    ])
    monkeypatch.setattr("benchpro_core.module_host.discovery.metadata.entry_points", lambda: entry_points)

    result = load_modules(discover_modules(), initialize=True)

    assert [loaded.module.module_id for loaded in result.successful_modules] == ["dns"]
    assert len(result.failed_modules) == 1
    assert result.failed_modules[0].name == "smtp"


def test_dns_failure_does_not_block_smtp(monkeypatch):
    entry_points = FakeEntryPoints([
        FakeEntryPoint("dns", error=ImportError("dns exploded")),
        FakeEntryPoint("smtp", SMTPModule),
    ])
    monkeypatch.setattr("benchpro_core.module_host.discovery.metadata.entry_points", lambda: entry_points)

    result = load_modules(discover_modules(), initialize=True)

    assert [loaded.module.module_id for loaded in result.successful_modules] == ["smtp"]
    assert len(result.failed_modules) == 1
    assert result.failed_modules[0].name == "dns"
