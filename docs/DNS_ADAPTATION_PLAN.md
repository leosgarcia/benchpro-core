# DNS Bench Pro Adaptation Plan

Status: Proposed

## Goal

Transform DNS Bench Pro into:

```text
Standalone Application + Integratable Module
```

without rewriting the product or breaking standalone behavior.

## Phase A: Create Integration Package

Add:

```text
src/integration/
├── __init__.py
└── module.py
```

Create `DNSBenchModule` metadata:

```python
module_id = "dns"
display_name = "DNS Bench Pro"
version = "1.0.0"
integration_api = 1
vendor = "WL Tech"
capabilities = {"benchmark", "diagnostics", "history", "reports", "charts"}
```

Rollback: remove the new `integration` package.

Risk: LOW.

## Phase B: Create DNSBenchWidget

Extract the central product workspace from `MainWindow` into:

```text
src/ui/widgets/dns_bench_widget.py
```

This widget should contain:

- Benchmark tab
- Servers tab
- History tab
- Analysis tab
- About tab if appropriate for standalone reuse
- benchmark controls
- progress handling
- engine signal wiring

Rollback: leave `MainWindow` as-is and remove the new widget.

Risk: HIGH because this touches the main UI.

## Phase C: Adapt StandaloneMainWindow

Refactor `MainWindow` or introduce `StandaloneMainWindow` so the standalone shell owns:

- menu bar
- status bar
- window title
- window icon
- close behavior

The shell hosts `DNSBenchWidget`.

Rollback: restore previous `MainWindow` implementation.

Risk: MEDIUM.

## Phase D: Add Entry Point

Update `pyproject.toml`:

```toml
[project.entry-points."benchpro.modules"]
dns = "integration.module:DNSBenchModule"
```

The exact import path should match the existing package/import layout.

Rollback: remove the entry point.

Risk: LOW.

## Phase E: Add Contract Tests

Add DNS-local contract tests verifying:

- metadata exists
- `integration_api == 1`
- no imports of `bench_pro_core`
- `initialize()` does not fail
- `create_widget()` returns `QWidget`
- `shutdown()` does not fail

Rollback: remove the new tests.

Risk: LOW.

## Phase F: Validate Standalone

Run:

```text
python src/main.py
pytest
```

or equivalent project commands.

Acceptance:

```text
DNS Standalone: PASS
DNS Tests: PASS
```

Risk: LOW.

## Phase G: Validate Future Integration

Use a minimal fake Core loader or Bench Pro Core contract tests to load the DNS entry point.

Acceptance:

```text
DNS Module: PASS
Core Loader: PASS
Standalone still PASS
```

Risk: MEDIUM.

## Release Rule

No DNS release is acceptable unless:

```text
Standalone PASS
Tests PASS
Integration Contract PASS
No bench_pro_core imports PASS
```

