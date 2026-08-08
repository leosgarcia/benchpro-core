# ADR-003: Entry Points for Module Discovery

Status: Accepted

## Context

Bench Pro Core needs a standard and testable way to discover installed modules.

## Decision

Use `importlib.metadata.entry_points` with group `benchpro.modules`.

## Consequences

Discovery follows Python packaging standards and requires no custom registry in v1.

## Alternatives Considered

- JSON manifests: useful for future external distribution, but less native for Python packages.
- Manual registry: simple but brittle and less discoverable.

