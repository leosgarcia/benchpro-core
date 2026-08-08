"""Optional integration smoke test using the real SMTP Bench Pro entry point."""

import pytest
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from benchpro_core.module_host.discovery import discover_modules
from benchpro_core.module_host.loader import load_module
from smtp_bench_pro.version import __version__ as smtp_version


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.mark.integration
def test_real_smtp_module_contract_and_widget_smoke(qapp):
    discovered = discover_modules()
    smtp_module = next((module for module in discovered if module.name == "smtp"), None)
    if smtp_module is None:
        pytest.skip("SMTP Bench Pro entry point is not installed in this Python environment")

    loaded = load_module(smtp_module, initialize=True)
    module = loaded.module
    widget = module.create_widget()

    assert module.module_id == "smtp"
    assert module.display_name == "SMTP Bench Pro"
    assert module.version == smtp_version
    assert module.integration_api == 1
    assert module.vendor == "WL Tech"
    assert "benchmark" in module.capabilities
    assert "diagnostics" in module.capabilities
    assert isinstance(widget, QWidget)
    assert not isinstance(widget, QMainWindow)

    labels = [widget.tab_widget.tabText(index) for index in range(widget.tab_widget.count())]
    assert labels == ["Benchmark", "Diagnóstico", "Segurança", "Histórico"]
    assert "Sobre" not in labels

    module.shutdown()
    qapp.processEvents()


