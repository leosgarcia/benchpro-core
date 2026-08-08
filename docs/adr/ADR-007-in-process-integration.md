# ADR-007: In-Process Integration

Status: Accepted

## Context

Core should embed module UI and workflows naturally.

## Decision

Prefer in-process Python integration for v1.

## Consequences

The user experience is coherent and avoids subprocess coordination. Core must isolate failures around module boundaries.

## Alternatives Considered

- Launch micro executables via subprocess: rejected for normal integration because it is not a real embedded module model.

