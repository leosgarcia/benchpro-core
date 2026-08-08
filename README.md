# Bench Pro Core

Status: Early Architecture / Pre-Alpha

Bench Pro Core is the aggregator application for the WL Tech Bench Pro ecosystem.

It is designed to discover and host compatible Bench Pro modules inside a unified desktop experience, without becoming a dependency of the individual products.

## Ecosystem

Planned and existing products include:

- DNS Bench Pro
- SMTP Bench Pro
- SSL Bench Pro
- HTTP Bench Pro

Each micro application is a complete standalone product with its own repository, release lifecycle, database, settings, documentation, CI, and executable.

## Architectural Rule

Bench Pro Core may discover and load micro applications.

Micro applications must never depend on Bench Pro Core.

```text
Bench Pro Core
      |
      v
Compatible modules
```

Never:

```text
Micro application
      |
      v
Bench Pro Core
```

## Integration API v1

Bench Pro Core uses Integration API v1 to validate optional module capabilities.

Required metadata:

- `module_id`
- `display_name`
- `version`
- `integration_api`
- `vendor`
- `capabilities`

Required methods:

- `initialize()`
- `create_widget()`
- `shutdown()`

Modules are discovered through Python entry points:

```toml
[project.entry-points."benchpro.modules"]
dns = "integration.module:DNSBenchModule"
```

## Current State

This repository currently contains:

- architecture documentation
- Integration Contract v1 documentation
- module lifecycle documentation
- ADRs
- initial contract tests
- minimal Python package skeleton

It does not yet contain:

- a module loader
- a GUI shell
- a dashboard
- PyInstaller build configuration
- bundled module integration

## Development

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run checks:

```bash
pytest
ruff check .
bandit -r src/
```

## License

MIT License.

Copyright (c) 2026 WL Tech.

