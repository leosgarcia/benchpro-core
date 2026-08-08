"""Optional integration smoke test using the real DNS Bench Pro entry point."""

import pytest
from PySide6.QtWidgets import QApplication, QWidget

from benchpro_core.module_host.discovery import discover_modules
from benchpro_core.module_host.loader import load_module


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.mark.integration
def test_real_dns_module_widget_smoke(qapp):
    discovered = discover_modules()
    dns_module = next((module for module in discovered if module.name == "dns"), None)
    if dns_module is None:
        pytest.skip("DNS Bench Pro entry point is not installed in this Python environment")

    loaded = load_module(dns_module, initialize=True)
    widget = loaded.module.create_widget()

    assert loaded.module.module_id == "dns"
    assert isinstance(widget, QWidget)
    assert widget.tab_widget.count() == 4
    assert widget.tab_widget.tabText(0) == "Benchmark"
    assert widget.tab_widget.tabText(1) == "Servidores"
    assert widget.tab_widget.tabText(2) == "Histórico"
    assert widget.tab_widget.tabText(3) == "Análises"

    loaded.module.shutdown()
    qapp.processEvents()
