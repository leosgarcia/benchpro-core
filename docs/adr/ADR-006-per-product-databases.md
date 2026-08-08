# ADR-006: Per-Product Databases

Status: Accepted

## Context

Each product must remain standalone and own its history/settings.

## Decision

Each product owns its SQLite database and data directory.

## Consequences

Core must not query micro databases directly. Unified history requires module-provided APIs.

## Alternatives Considered

- One shared SQLite database: rejected because it couples schema evolution across products.

