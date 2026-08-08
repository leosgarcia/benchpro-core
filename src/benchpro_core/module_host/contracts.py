"""Core-local module integration contract definitions."""

from typing import Protocol

BENCHPRO_ENTRY_POINT_GROUP = "benchpro.modules"
SUPPORTED_INTEGRATION_API = {1}
REQUIRED_METADATA = (
    "module_id",
    "display_name",
    "version",
    "integration_api",
    "vendor",
    "capabilities",
)
REQUIRED_METHODS = ("initialize", "create_widget", "shutdown")


class BenchProModuleContract(Protocol):
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
