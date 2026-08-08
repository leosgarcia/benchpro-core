# DNS Bench Pro Technical Audit

Status: Initial audit

Repository inspected: `C:\projetos\BENCHPRO\dns-bench-pro`

Product version observed: `1.0.0`

## Summary

DNS Bench Pro is already functional and has useful separation between engine, models, persistence, exporters, widgets, and tests.

The main integration blocker is that `ui.main_window.MainWindow` currently acts as both standalone shell and product workspace. It owns menu/status behavior and also wires benchmark controls, tabs, engine signals, history, export, and charts.

The recommended adaptation is incremental: introduce a reusable `DNSBenchWidget` and make both standalone and Core integration host that widget.

No schema rewrite, namespace rename, or large package move is needed.

## Findings Table

| File | Current Responsibility | Coupling | Required Change | Risk |
| --- | --- | --- | --- | --- |
| `src/main.py` | CLI and GUI entry point; creates `QApplication`, `DNSRepository`, and `MainWindow`. | Couples startup to `MainWindow`. | Keep intact initially. Later switch GUI startup to `StandaloneMainWindow` if created. | LOW |
| `src/ui/main_window.py` | Standalone shell, tab workspace, benchmark orchestration, status bar, menu, export actions. | Strong UI shell/workspace coupling. | Extract central tabs and benchmark UI into `DNSBenchWidget`; keep menu/status in standalone shell. | HIGH |
| `src/core/benchmark_engine.py` | Concurrent DNS benchmark engine using Qt signals and `QThreadPool`. | Depends on Qt threading/signals, but not on `MainWindow`. | No change for initial integration. Module widget can own/use it. | LOW |
| `src/core/models.py` | Dataclasses for DNS servers and test results. | Low; pure domain data. | No change. | NONE |
| `src/core/statistics.py` | Latency metrics. | Low. | No change. | NONE |
| `src/core/server_catalog.py` | Built-in and custom server catalog access. | Depends on repository optionally. | No change. | LOW |
| `src/core/resolvers/*` | Protocol-specific DNS resolvers. | Low UI coupling. | No change. | NONE |
| `src/persistence/database.py` | SQLite connection and schema migrations. | Owns default app data path. | No schema change. Keep DNS-owned database. | LOW |
| `src/persistence/repository.py` | DNS history, server states, comparison and trends. | Used by CLI and widgets. | No direct Core access. Optionally expose read methods through module later. | LOW |
| `src/export/*` | PDF, JSON, CSV exporters. | Called by CLI and UI. | No change. | LOW |
| `src/ui/widgets/results_table.py` | Results table widget. | Depends on DNS models. | Reuse inside `DNSBenchWidget`. | NONE |
| `src/ui/widgets/server_manager.py` | Server management widget. | Depends on DNS repository. | Reuse inside `DNSBenchWidget`. | LOW |
| `src/ui/widgets/history_view.py` | History UI, comparison dialog, export actions. | Depends on repository and exporters; uses dialogs. | Reuse initially. Consider moving export orchestration later only if needed. | MEDIUM |
| `src/ui/widgets/charts.py` | Charts and trend visualization. | Depends on repository and DNS models. | Reuse inside `DNSBenchWidget`. | LOW |
| `src/ui/widgets/about.py` | Product about widget. | Standalone product metadata. | Reuse standalone; Core may show module metadata separately. | LOW |
| `src/utils/config.py` | Product constants and version. | Central product identity. | Use for module metadata. | LOW |
| `src/utils/platform_utils.py` | App data, database and log paths. | Owns DNS data namespace. | Keep unchanged. Integrated mode should keep using this namespace. | LOW |
| `src/utils/logger.py` | DNS logger configuration. | Owns DNS logs. | Keep unchanged. Core may log lifecycle separately. | LOW |
| `tests/test_ui.py` | MainWindow smoke tests. | Assumes five tabs on `MainWindow`. | Add tests for `DNSBenchWidget` during adaptation; update MainWindow tests only after shell refactor. | MEDIUM |
| `tests/test_benchmark_engine.py` | Engine tests with Qt core app. | Some network-dependent behavior may be environment sensitive. | No change for integration contract. | LOW |
| `tests/test_repository.py` | SQLite repository tests. | Uses temp DB. | No change. | NONE |
| `pyproject.toml` | Packaging metadata, dependencies, pytest settings. | No entry points for Bench Pro modules yet. | Later add `benchpro.modules` entry point. | LOW |

## Existing Entry Points

The observed GUI/CLI entry point is `src/main.py` with a `main()` function.

The package currently uses top-level imports such as `from core...`, `from ui...`, and `from persistence...` with `pythonpath = ["src"]`.

This should not be changed during the first integration adaptation.

## Existing Lifecycle

Current implicit standalone lifecycle:

```text
start process
create QApplication
create DNSRepository
create MainWindow
user starts benchmark
BenchmarkEngine runs QThreadPool workers
repository stores history
window closes
process exits
```

No explicit integration lifecycle exists yet.

## Current Couplings

The important coupling is not between engine and UI. It is between the standalone `MainWindow` shell and the product workspace.

`MainWindow` currently contains:

- tab creation
- benchmark form
- benchmark action handling
- progress handling
- export handling
- history/chart refresh
- menu bar
- status bar

This is acceptable for a standalone v1, but integration needs a reusable root widget.

## Minimal Adaptation Target

Add:

```text
src/integration/
├── __init__.py
└── module.py
```

Introduce:

```text
DNSBenchWidget(QWidget)
```

Then:

```text
StandaloneMainWindow(QMainWindow)
    hosts DNSBenchWidget

DNSBenchModule.create_widget(parent)
    returns DNSBenchWidget(parent)
```

## Constraints

- Do not move all files.
- Do not rename imports globally.
- Do not alter SQLite schema.
- Do not remove CLI.
- Do not break `MainWindow` tests until replacement tests exist.
- Do not make DNS import `bench_pro_core`.

