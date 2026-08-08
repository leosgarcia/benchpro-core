"""Module loading and Integration API v1 validation."""

from dataclasses import dataclass, field
import logging
from typing import Any, cast

from benchpro_core.module_host.contracts import REQUIRED_METADATA, REQUIRED_METHODS, SUPPORTED_INTEGRATION_API
from benchpro_core.module_host.discovery import DiscoveredModule
from benchpro_core.module_host.errors import (
    InvalidModuleError,
    ModuleInitializationError,
    ModuleLoadError,
    UnsupportedIntegrationAPIError,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoadedModule:
    name: str
    module: Any
    distribution: str | None = None


@dataclass(frozen=True)
class FailedModule:
    name: str
    error_type: str
    message: str
    distribution: str | None = None


@dataclass(frozen=True)
class ModuleLoadResult:
    successful_modules: list[LoadedModule] = field(default_factory=list)
    failed_modules: list[FailedModule] = field(default_factory=list)


def validate_module_contract(module: object) -> None:
    missing_metadata = [name for name in REQUIRED_METADATA if not hasattr(module, name)]
    if missing_metadata:
        raise InvalidModuleError(f"Missing required metadata: {', '.join(sorted(missing_metadata))}")

    module_obj = cast(Any, module)

    if not isinstance(module_obj.module_id, str) or not module_obj.module_id.strip():
        raise InvalidModuleError("module_id must be a non-empty string")
    if not isinstance(module_obj.display_name, str) or not module_obj.display_name.strip():
        raise InvalidModuleError("display_name must be a non-empty string")
    if not isinstance(module_obj.version, str) or not module_obj.version.strip():
        raise InvalidModuleError("version must be a non-empty string")
    if not isinstance(module_obj.vendor, str) or not module_obj.vendor.strip():
        raise InvalidModuleError("vendor must be a non-empty string")
    if module_obj.integration_api not in SUPPORTED_INTEGRATION_API:
        raise UnsupportedIntegrationAPIError(f"Unsupported integration_api: {module_obj.integration_api}")

    try:
        iter(module_obj.capabilities)
    except TypeError as exc:
        raise InvalidModuleError("capabilities must be iterable") from exc

    for method_name in REQUIRED_METHODS:
        if not callable(getattr(module, method_name, None)):
            raise InvalidModuleError(f"Missing required method: {method_name}")


def load_module(
    discovered_module: DiscoveredModule,
    initialize: bool = False,
    context: object | None = None,
) -> LoadedModule:
    """Load, instantiate, validate, and optionally initialize a discovered module."""
    try:
        module_class = discovered_module.entry_point.load()
        module = module_class()
    except Exception as exc:
        logger.exception("Module load failed: %s", discovered_module.name)
        raise ModuleLoadError(f"Failed to load module {discovered_module.name}: {exc}") from exc

    validate_module_contract(module)

    if initialize:
        try:
            module.initialize()
        except Exception as exc:
            logger.exception("Module initialization failed: %s", discovered_module.name)
            raise ModuleInitializationError(f"Failed to initialize module {discovered_module.name}: {exc}") from exc

    logger.info("Module loaded: %s", module.module_id)
    return LoadedModule(name=discovered_module.name, module=module, distribution=discovered_module.distribution)


def load_modules(
    discovered_modules: list[DiscoveredModule],
    initialize: bool = False,
    context: object | None = None,
) -> ModuleLoadResult:
    """Load modules independently so one bad module does not stop the host."""
    successes: list[LoadedModule] = []
    failures: list[FailedModule] = []

    for discovered_module in discovered_modules:
        try:
            successes.append(load_module(discovered_module, initialize=initialize, context=context))
        except Exception as exc:
            failures.append(
                FailedModule(
                    name=discovered_module.name,
                    error_type=exc.__class__.__name__,
                    message=str(exc),
                    distribution=discovered_module.distribution,
                )
            )
            logger.warning("Module rejected: %s (%s)", discovered_module.name, exc.__class__.__name__)

    return ModuleLoadResult(successful_modules=successes, failed_modules=failures)

