"""Small registry for loaded Bench Pro modules."""

import logging
from typing import Any

from benchpro_core.module_host.errors import DuplicateModuleError, ModuleShutdownError
from benchpro_core.module_host.loader import LoadedModule

logger = logging.getLogger(__name__)


class ModuleRegistry:
    """Registry for loaded modules keyed by module_id."""

    def __init__(self):
        self._modules: dict[str, LoadedModule] = {}

    def register(self, loaded_module: LoadedModule) -> None:
        module_id = loaded_module.module.module_id
        if module_id in self._modules:
            raise DuplicateModuleError(f"Duplicate module_id: {module_id}")
        self._modules[module_id] = loaded_module
        logger.info("Module registered: %s", module_id)

    def get(self, module_id: str) -> Any | None:
        loaded_module = self._modules.get(module_id)
        return loaded_module.module if loaded_module else None

    def list_modules(self) -> list[Any]:
        return [loaded.module for loaded in self._modules.values()]

    def shutdown_all(self) -> list[ModuleShutdownError]:
        errors: list[ModuleShutdownError] = []
        for module_id, loaded_module in list(self._modules.items()):
            try:
                loaded_module.module.shutdown()
                logger.info("Module shutdown complete: %s", module_id)
            except Exception as exc:
                error = ModuleShutdownError(f"Failed to shutdown module {module_id}: {exc}")
                errors.append(error)
                logger.exception("Module shutdown failed: %s", module_id)
        self._modules.clear()
        return errors
