"""Tests for the Bench Pro Core module host."""

import pytest

from benchpro_core.module_host.discovery import DiscoveredModule, discover_modules
from benchpro_core.module_host.errors import (
    DuplicateModuleError,
    InvalidModuleError,
    ModuleInitializationError,
    ModuleLoadError,
    ModuleShutdownError,
    UnsupportedIntegrationAPIError,
)
from benchpro_core.module_host.loader import load_module, load_modules, validate_module_contract
from benchpro_core.module_host.registry import ModuleRegistry


class FakeEntryPoint:
    def __init__(self, name, target=None, error=None):
        self.name = name
        self._target = target
        self._error = error
        self.dist = None

    def load(self):
        if self._error:
            raise self._error
        return self._target


class FakeEntryPoints(list):
    def select(self, group=None):
        return self if group == "benchpro.modules" else []


class ValidModule:
    module_id = "valid"
    display_name = "Valid Bench Pro"
    version = "1.0.0"
    integration_api = 1
    vendor = "WL Tech"
    capabilities = {"benchmark"}

    def __init__(self):
        self.initialized = False
        self.shutdown_called = False

    def initialize(self, context=None):
        self.initialized = True

    def create_widget(self, parent=None):
        return object()

    def shutdown(self):
        self.shutdown_called = True


class SecondValidModule(ValidModule):
    module_id = "second"
    display_name = "Second Bench Pro"


class NoContextInitializeModule(ValidModule):
    module_id = "no_context"
    display_name = "No Context Bench Pro"

    def initialize(self):
        self.initialized = True


class MissingMetadataModule:
    module_id = "missing"
    display_name = "Missing Metadata"
    version = "1.0.0"
    integration_api = 1
    vendor = "WL Tech"

    def initialize(self, context=None):
        pass

    def create_widget(self, parent=None):
        return object()

    def shutdown(self):
        pass


class MissingMethodModule(ValidModule):
    create_widget = None


class UnsupportedApiModule(ValidModule):
    integration_api = 999


class InitErrorModule(ValidModule):
    def initialize(self, context=None):
        raise RuntimeError("init exploded")


class ShutdownErrorModule(ValidModule):
    module_id = "shutdown_error"

    def shutdown(self):
        raise RuntimeError("shutdown exploded")


class ConstructorErrorModule(ValidModule):
    def __init__(self):
        raise RuntimeError("constructor exploded")


def test_discover_modules_when_no_entry_points(monkeypatch):
    monkeypatch.setattr("benchpro_core.module_host.discovery.metadata.entry_points", lambda: FakeEntryPoints())

    assert discover_modules() == []


def test_discover_modules_returns_descriptors(monkeypatch):
    entry_points = FakeEntryPoints([FakeEntryPoint("valid", ValidModule), FakeEntryPoint("second", SecondValidModule)])
    monkeypatch.setattr("benchpro_core.module_host.discovery.metadata.entry_points", lambda: entry_points)

    discovered = discover_modules()

    assert [module.name for module in discovered] == ["second", "valid"]


def test_load_valid_module():
    discovered = DiscoveredModule("valid", FakeEntryPoint("valid", ValidModule))

    loaded = load_module(discovered, initialize=True)

    assert loaded.module.module_id == "valid"
    assert loaded.module.initialized is True


def test_load_module_uses_v1_initialize_without_context():
    discovered = DiscoveredModule("no-context", FakeEntryPoint("no-context", NoContextInitializeModule))

    loaded = load_module(discovered, initialize=True)

    assert loaded.module.initialized is True


def test_load_multiple_valid_modules():
    result = load_modules(
        [
            DiscoveredModule("valid", FakeEntryPoint("valid", ValidModule)),
            DiscoveredModule("second", FakeEntryPoint("second", SecondValidModule)),
        ]
    )

    assert [loaded.module.module_id for loaded in result.successful_modules] == ["valid", "second"]
    assert result.failed_modules == []


def test_missing_metadata_is_rejected():
    with pytest.raises(InvalidModuleError, match="Missing required metadata"):
        validate_module_contract(MissingMetadataModule())


def test_missing_required_method_is_rejected():
    with pytest.raises(InvalidModuleError, match="Missing required method"):
        validate_module_contract(MissingMethodModule())


def test_unsupported_integration_api_is_rejected():
    with pytest.raises(UnsupportedIntegrationAPIError, match="Unsupported integration_api"):
        validate_module_contract(UnsupportedApiModule())


def test_duplicate_module_id_is_rejected():
    registry = ModuleRegistry()
    first = load_module(DiscoveredModule("valid-a", FakeEntryPoint("valid-a", ValidModule)))
    second = load_module(DiscoveredModule("valid-b", FakeEntryPoint("valid-b", ValidModule)))

    registry.register(first)

    with pytest.raises(DuplicateModuleError, match="Duplicate module_id"):
        registry.register(second)


def test_import_error_is_wrapped():
    discovered = DiscoveredModule("broken", FakeEntryPoint("broken", error=ImportError("missing dep")))

    with pytest.raises(ModuleLoadError, match="Failed to load module broken"):
        load_module(discovered)


def test_constructor_error_is_wrapped():
    discovered = DiscoveredModule("broken-init", FakeEntryPoint("broken-init", ConstructorErrorModule))

    with pytest.raises(ModuleLoadError, match="Failed to load module broken-init"):
        load_module(discovered)


def test_initialize_error_is_wrapped():
    discovered = DiscoveredModule("init-error", FakeEntryPoint("init-error", InitErrorModule))

    with pytest.raises(ModuleInitializationError, match="Failed to initialize module init-error"):
        load_module(discovered, initialize=True)


def test_registry_shutdown():
    registry = ModuleRegistry()
    loaded = load_module(DiscoveredModule("valid", FakeEntryPoint("valid", ValidModule)))

    registry.register(loaded)
    errors = registry.shutdown_all()

    assert errors == []
    assert registry.list_modules() == []
    assert loaded.module.shutdown_called is True


def test_registry_shutdown_collects_errors():
    registry = ModuleRegistry()
    loaded = load_module(DiscoveredModule("shutdown-error", FakeEntryPoint("shutdown-error", ShutdownErrorModule)))

    registry.register(loaded)
    errors = registry.shutdown_all()

    assert len(errors) == 1
    assert isinstance(errors[0], ModuleShutdownError)
    assert registry.list_modules() == []


def test_failure_of_one_module_does_not_interrupt_other_modules():
    result = load_modules(
        [
            DiscoveredModule("valid", FakeEntryPoint("valid", ValidModule)),
            DiscoveredModule("broken", FakeEntryPoint("broken", error=ImportError("missing dep"))),
            DiscoveredModule("second", FakeEntryPoint("second", SecondValidModule)),
        ]
    )

    assert [loaded.module.module_id for loaded in result.successful_modules] == ["valid", "second"]
    assert len(result.failed_modules) == 1
    assert result.failed_modules[0].error_type == "ModuleLoadError"
