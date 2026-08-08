# ADR-005: No Shared SDK Yet

Status: Accepted

## Context

A shared SDK could reduce duplication but also create premature framework coupling.

## Decision

Do not create `benchpro-sdk`, `benchpro-common`, or similar packages in v1.

## Consequences

The first modules use metadata, duck typing, and Core-local protocols. Shared code may be extracted later under the Rule of Three.

## Alternatives Considered

- Create SDK immediately: rejected as premature.

