# ADR-008: UI Logic Separation

Status: Accepted

## Context

Core integration requires reuse of product functionality without reusing a full standalone window.

## Decision

Business logic must live outside PySide6 widgets where practical. Standalone windows should host reusable product widgets.

## Consequences

Modules can expose widgets to Core without duplicating functional UI.

## Alternatives Considered

- Keep all behavior in `QMainWindow`: rejected because it blocks clean embedding.

