# Bench Pro Integration Contract v1

Status: Draft v1.0

## Goal

Integration API v1 defines the minimum surface a micro application exposes so Bench Pro Core can discover, validate, initialize, and embed it.

The contract is intentionally small. It is an optional capability of each micro application, not a runtime dependency on Bench Pro Core.

## No Shared SDK in v1

Micro applications must not import `bench_pro_core`.

Bench Pro Core may define a local `Protocol` for validation, but that protocol belongs to Core only.

Conceptual Core-side protocol:

```python
from typing import Protocol


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
```

This is not a shared SDK. It is a validation shape used by Core.

## Required Metadata

Required:

| Field | Type | Requirement |
| --- | --- | --- |
| `module_id` | `str` | Stable lowercase identifier, for example `dns` or `smtp`. |
| `display_name` | `str` | Human readable product name. |
| `version` | `str` | Product SemVer string. |
| `integration_api` | `int` | Integration contract version. v1 uses `1`. |
| `vendor` | `str` | Product vendor, normally `WL Tech`. |
| `capabilities` | `set[str]` or equivalent iterable | Supported feature flags. |

Optional:

| Field | Type | Notes |
| --- | --- | --- |
| `description` | `str` | Optional in v1 because Core can operate without it. |
| `icon` | `str` or path-like | Optional in v1 because packaging paths vary by product. |

## Required Methods

### initialize(context=None)

Prepares the module for integrated use.

Rules:

- Must be safe to call once.
- Should be idempotent when practical.
- Must not require Core-specific classes.
- May accept `None`.
- May ignore unknown context attributes.

### create_widget(parent=None)

Returns a PySide6 `QWidget` suitable for embedding inside Core.

Rules:

- Must not return a standalone `QMainWindow`.
- Must not create a second `QApplication`.
- Must not assume it owns the process menu bar.
- Must keep module-specific persistence and settings.

### shutdown()

Releases resources owned by the module.

Rules:

- Must be safe even if initialization partially failed.
- Must not raise during normal shutdown.
- Should stop module-owned workers.
- Should not close Bench Pro Core.

## Capabilities

Known capability names for v1:

```text
benchmark
diagnostics
security_audit
history
reports
charts
export
dns_checks
```

Capabilities are descriptive. Core must not assume all modules support the same feature set.

## Discovery Entry Point

Micro applications may expose an entry point:

```toml
[project.entry-points."benchpro.modules"]
dns = "dns_bench_pro.integration.module:DNSBenchModule"
```

The standalone product must continue working if this entry point is never used.

## Validation Rules

Core should reject a module when:

- required metadata is missing
- `module_id` is empty or invalid
- `integration_api` is unsupported
- required methods are missing
- `capabilities` is not iterable
- loading raises an import error

Core should mark the module as failed, not crash.

## Future Extensions

The following are intentionally not required in v1:

- `health_check()`
- `activate()`
- `deactivate()`
- unified history API
- unified reporting API
- Core-managed logging adapter

They may be introduced by Integration API v2 or optional capabilities.

