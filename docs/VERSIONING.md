# Bench Pro Versioning

Status: Draft v1.0

## Product Version

Every product uses independent Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

Examples:

```text
DNS Bench Pro 1.2.0
SMTP Bench Pro 1.0.0
Bench Pro Core 1.1.0
```

Product versions describe user-facing release compatibility, features, and fixes.

## Integration API Version

Integration compatibility is a separate integer:

```text
integration_api = 1
```

Example:

```text
SMTP Bench Pro 1.5.2
Integration API 1
```

Bench Pro Core validates `integration_api`, not the product version.

## Compatibility Rule

Core may load a module when:

- the module's `integration_api` is supported
- required metadata is valid
- required lifecycle methods exist

Core must reject unsupported Integration API versions with a clear diagnostic.

## Breaking Changes

Any breaking change to required metadata or required lifecycle methods increments the Integration API.

Non-breaking additions should be optional capabilities or optional methods.

