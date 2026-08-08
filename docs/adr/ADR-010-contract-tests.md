# ADR-010: Contract Tests

Status: Accepted

## Context

The ecosystem depends on modules honoring a small integration contract.

## Decision

Create contract tests that validate metadata, Integration API compatibility, widget creation, lifecycle methods, and failure isolation.

## Consequences

Modules can be adapted independently while Core compatibility remains testable.

## Alternatives Considered

- Manual validation only: rejected because integration breakage would be easy to miss.

