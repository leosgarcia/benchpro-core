# ADR-004: Integration API Version

Status: Accepted

## Context

Product versions and integration compatibility change at different speeds.

## Decision

Use a separate integer `integration_api`.

## Consequences

Core validates compatibility without tying itself to commercial product versions.

## Alternatives Considered

- Use SemVer product version for compatibility: rejected because product releases may include unrelated changes.

