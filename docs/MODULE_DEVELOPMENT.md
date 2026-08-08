# Bench Pro Module Development Guide

Status: Draft v1.0

## Principle

Build every micro as a standalone product first. Integration is an additional capability.

The module should know its domain. Bench Pro Core should know how to host modules.

## Recommended Structure

```text
src/
└── smtp_bench_pro/
    ├── application/
    ├── domain/
    ├── engine/
    ├── persistence/
    ├── export/
    ├── reporting/
    ├── ui/
    │   ├── widgets/
    │   └── windows/
    ├── integration/
    │   ├── __init__.py
    │   └── module.py
    ├── settings/
    ├── utils/
    ├── version.py
    └── __main__.py
```

## Layering Rules

- UI widgets render state and collect user intent.
- Application services orchestrate workflows.
- Engines perform protocol-specific work.
- Persistence owns database access.
- Export/reporting receive structured data.
- Integration adapts the product to the Core contract.

Avoid putting protocol logic, statistics, persistence, or export orchestration directly inside `QMainWindow`.

## Standalone First

Each product must support:

```text
python -m product_package
Product-Name.exe
```

Standalone behavior must not depend on Bench Pro Core.

## Integration Package

The integration package should expose one module class.

Example:

```python
class SMTPBenchModule:
    module_id = "smtp"
    display_name = "SMTP Bench Pro"
    version = "1.0.0"
    integration_api = 1
    vendor = "WL Tech"
    capabilities = {"benchmark", "diagnostics", "security_audit", "history", "reports"}

    def initialize(self, context=None):
        ...

    def create_widget(self, parent=None):
        ...

    def shutdown(self):
        ...
```

## Entry Point

```toml
[project.entry-points."benchpro.modules"]
smtp = "smtp_bench_pro.integration.module:SMTPBenchModule"
```

## UI Integration

A module must return a root widget, not a standalone main window.

Preferred shape:

```text
StandaloneMainWindow
    |
    v
ProductWidget

Bench Pro Core
    |
    v
ProductWidget
```

## Data

Each product owns its data directory, SQLite database, settings, and logs.

Core must not query a product database directly.

## Required Tests

Minimum tests:

- engine unit tests
- application service tests
- persistence tests
- export tests
- UI smoke tests
- standalone startup test
- integration contract test
- architecture import test preventing `bench_pro_core` imports

## Packaging

Each micro builds its own executable and release artifact. The Core may bundle modules for v1, but this must not replace standalone packaging.

