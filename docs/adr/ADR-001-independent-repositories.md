# ADR-001: Independent Repositories

Status: Accepted

## Context

Bench Pro contains multiple commercial/open-source desktop products. Each product must have independent releases, issues, CI, documentation, and executables.

## Decision

Use one Git repository per product.

## Consequences

Products can evolve and release independently. Cross-product coordination requires explicit version and compatibility documentation.

## Alternatives Considered

- Monorepo: simpler workspace operations, but higher coupling risk.
- Git submodules: possible later, but unnecessary before the ecosystem stabilizes.

