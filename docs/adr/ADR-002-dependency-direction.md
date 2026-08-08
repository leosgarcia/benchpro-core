# ADR-002: Dependency Direction

Status: Accepted

## Context

Micro applications must remain complete standalone products.

## Decision

Bench Pro Core may discover and load micro applications. Micro applications must never import or depend on Bench Pro Core.

## Consequences

The Core is an aggregator, not a base framework. Modules stay distributable alone.

## Alternatives Considered

- Shared Core dependency in every product: rejected because it would make standalone products dependent on the aggregator.

