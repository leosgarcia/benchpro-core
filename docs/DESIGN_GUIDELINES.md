# Bench Pro Design Guidelines

Status: Draft v1.0

## Goal

All Bench Pro products should feel like members of the same professional desktop suite while remaining independently implemented and packaged.

Do not create a shared visual runtime library in v1. This document defines visual and interaction guidance only.

## Current DNS Bench Pro Baseline

Observed DNS Bench Pro patterns:

- PySide6 desktop UI
- Main navigation by `QTabWidget`
- tabs named `Benchmark`, `Servidores`, `Historico`, `Analises`, `Sobre`
- compact top configuration area
- grouped controls with `QGroupBox`
- primary action button using blue background
- result-heavy views based on tables
- status bar with concise execution state
- help menu with guide, shortcuts, online docs, GitHub, issues, and about
- charts using dark plot background and protocol-specific colors

## Navigation

Standalone products may use tabs for primary product workflows.

Bench Pro Core should use dynamic module navigation and embed each module in a contained workspace.

Common standalone tabs:

- Benchmark
- Servers or Targets
- History
- Analysis
- Reports
- Settings
- About

## Tables

Tables should be dense, readable, and sortable where useful.

Recommended behavior:

- no inline editing unless the table is explicitly a configuration editor
- row selection for detail views
- numeric columns aligned consistently
- status columns use semantic color sparingly

## Status Bar

Every standalone product should expose:

- ready state
- active execution state
- completion summary
- failure summary
- current session identifier when available

## Menus

Recommended menus:

- File
- Tools, when product-specific utilities exist
- Help

Common actions:

- start benchmark
- export report
- open user guide
- open online documentation
- open GitHub repository
- report issue
- quit

## About

About views should include:

- product name
- product version
- vendor
- website
- repository
- license
- Python version
- PySide6/Qt version
- OS information

## Help

Help should be available offline for basic usage and online for full documentation.

Avoid making tooltips the only source of important guidance.

## Actions

Primary actions:

- visually stronger
- concise labels
- disabled while unsafe or unavailable

Destructive actions:

- require confirmation
- use clear object names, for example `Delete session #42`
- never run implicitly during navigation

## Colors

Semantic colors:

```text
success: green
warning: yellow/amber
danger: red
info: blue
neutral: gray
```

DNS chart baseline:

```text
UDP: cyan
TCP: lime
DOH: amber
DOT: violet
```

Use semantic color for meaning, not decoration.

## Spacing

Desktop tool surfaces should be compact:

- outer margins around 8-10 px
- internal group spacing around 6-10 px
- avoid oversized marketing-style hero layouts inside tools

## Tooltips

Tooltips should clarify controls whose effect is not obvious.

Do not put long documentation in tooltips.

## Dialogs

Dialogs should be modal only when a decision is required.

Use non-blocking status updates for routine progress.

## Charts

Charts should:

- preserve protocol identity by color
- use readable axis labels
- avoid over-animation
- keep dark plot styling only when it improves contrast with the rest of the product

