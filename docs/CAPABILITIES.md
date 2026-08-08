# Bench Pro Capabilities

Capabilities are high-level product abilities exposed by a micro application through Integration API v1.
They are used for discovery, navigation, future dashboards, and compatibility decisions. They must not be
arbitrary labels for internal implementation details.

## Definitions

| Capability | Definition |
| --- | --- |
| benchmark | Executes repeated measurements and exposes timing/performance results. |
| diagnostics | Executes functional or protocol-level checks and exposes diagnostic findings. |
| history | Exposes a usable history feature to the user, not only raw persistence. |
| reports | Generates formal exportable reports intended for delivery or archival. |
| charts | Provides visual charting/graphical analysis of collected results. |
| security_audit | Performs explicit security checks and produces security findings. |

## Current Module Matrix

| Capability | DNS Bench Pro 1.0.0 | SMTP Bench Pro 0.1.0 | Notes |
| --- | --- | --- | --- |
| benchmark | yes | yes | Both execute repeated measurements. |
| diagnostics | yes | yes | SMTP currently covers banner, EHLO, STARTTLS/SMTPS, and TLS inspection. |
| history | yes | yes | SMTP has SQLite persistence and a basic visible History tab. |
| reports | yes | no | SMTP formal reports are out of scope for 0.1.0. |
| charts | yes | no | SMTP charts are out of scope for 0.1.0. |
| security_audit | no | no | SMTP TLS inspection exists, but no formal security audit yet. |
| tls | no | review | TLS is currently an SMTP internal diagnostic aspect, not a documented Core-level capability. |

## SMTP TLS Capability Review

SMTP Bench Pro 0.1.0 currently advertises `tls`. This is accurate as an implemented internal feature,
but it is not yet a standardized high-level capability in the Core contract. Before relying on `tls` in
Core behavior, the ecosystem should either promote it to a documented capability or fold it under
`diagnostics` / future `security_audit` semantics.
