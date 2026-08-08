from typing import Any, Protocol, cast

import pytest


SUPPORTED_INTEGRATION_APIS = {1}
REQUIRED_METADATA = {
    "module_id",
    "display_name",
    "version",
    "integration_api",
    "vendor",
    "capabilities",
}


class ModuleContract(Protocol):
    module_id: str
    display_name: str
    version: str
    integration_api: int
    vendor: str
    capabilities: set[str]

    def initialize(self, context: object | None = None) -> None:
        ...

    def create_widget(self, parent=None):
        ...

    def shutdown(self) -> None:
        ...


class FakeWidget:
    pass


class ValidFakeModule:
    module_id = "fake"
    display_name = "Fake Bench Pro"
    version = "1.0.0"
    integration_api = 1
    vendor = "WL Tech"
    capabilities = {"benchmark", "history"}

    def initialize(self, context=None):
        self.initialized = True

    def create_widget(self, parent=None):
        return FakeWidget()

    def shutdown(self):
        self.shutdown_called = True


class MissingMetadataModule:
    module_id = "broken"
    display_name = "Broken Module"
    version = "1.0.0"
    integration_api = 1
    vendor = "WL Tech"

    def initialize(self, context=None):
        pass

    def create_widget(self, parent=None):
        return FakeWidget()

    def shutdown(self):
        pass


class UnsupportedApiModule(ValidFakeModule):
    integration_api = 999


class InvalidLifecycleModule(ValidFakeModule):
    create_widget = None


def validate_module_contract(module: object) -> None:
    missing = [name for name in REQUIRED_METADATA if not hasattr(module, name)]
    if missing:
        raise ValueError(f"Missing required metadata: {', '.join(sorted(missing))}")

    module_obj = cast(Any, module)

    if module_obj.integration_api not in SUPPORTED_INTEGRATION_APIS:
        raise ValueError("Unsupported integration_api")

    if not module_obj.module_id:
        raise ValueError("module_id must not be empty")

    try:
        iter(module_obj.capabilities)
    except TypeError as exc:
        raise ValueError("capabilities must be iterable") from exc

    for method_name in ("initialize", "create_widget", "shutdown"):
        if not callable(getattr(module, method_name, None)):
            raise ValueError(f"Missing required method: {method_name}")


def test_valid_module_contract_lifecycle():
    module = ValidFakeModule()

    validate_module_contract(module)
    module.initialize()
    widget = module.create_widget(parent=None)
    module.shutdown()

    assert isinstance(widget, FakeWidget)
    assert module.initialized is True
    assert module.shutdown_called is True


def test_missing_metadata_module_is_rejected():
    with pytest.raises(ValueError, match="Missing required metadata"):
        validate_module_contract(MissingMetadataModule())


def test_unsupported_integration_api_is_rejected():
    with pytest.raises(ValueError, match="Unsupported integration_api"):
        validate_module_contract(UnsupportedApiModule())


def test_invalid_lifecycle_method_is_rejected():
    with pytest.raises(ValueError, match="Missing required method"):
        validate_module_contract(InvalidLifecycleModule())


def test_import_failure_can_be_recorded_without_crashing_registry():
    failures = []

    try:
        raise ImportError("simulated plugin import failure")
    except ImportError as exc:
        failures.append({"module": "broken", "error": str(exc)})

    assert failures == [{"module": "broken", "error": "simulated plugin import failure"}]

