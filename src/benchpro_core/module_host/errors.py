"""Module host exceptions."""


class ModuleHostError(Exception):
    """Base exception for module host failures."""


class ModuleLoadError(ModuleHostError):
    """Raised when a module entry point cannot be loaded or instantiated."""


class InvalidModuleError(ModuleHostError):
    """Raised when a module does not satisfy Integration API v1."""


class UnsupportedIntegrationAPIError(InvalidModuleError):
    """Raised when a module uses an unsupported Integration API version."""


class DuplicateModuleError(ModuleHostError):
    """Raised when a registry receives duplicate module IDs."""


class ModuleInitializationError(ModuleHostError):
    """Raised when module initialization fails."""


class ModuleShutdownError(ModuleHostError):
    """Raised when module shutdown fails."""
