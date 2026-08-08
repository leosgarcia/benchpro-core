# ADR-009: Bundled Modules for Core v1

Status: Accepted

## Context

PyInstaller, plugin discovery, dependency resolution, and support are easier when the first Core release is controlled.

## Decision

Bench Pro Core v1 should prefer a complete bundled distribution containing supported modules.

## Consequences

Initial QA and support are simpler. Future installable modules remain possible.

## Alternatives Considered

- Separately installable modules from day one: deferred until the integration model is proven.

## Packaging Risk Notes

Bench Pro Core discovers modules through `importlib.metadata.entry_points`. Editable installs work for local development,
but a PyInstaller build may not automatically preserve distribution metadata for each bundled module. The v1 build strategy
must explicitly include module packages and their entry point metadata, or provide a generated registry produced at build time
from the same entry point source of truth.

For v1, the preferred release shape remains a complete bundled distribution. Separately installable modules should wait until
metadata discovery, dependency conflicts, and update semantics are validated in packaged builds.
