# ADR-007 — Integração em processo

## Contexto

O Core precisa hospedar módulos de forma real, compartilhando a experiência desktop, sem simplesmente abrir executáveis externos.

## Decisão

A integração v1 será em processo, via import Python e widget Qt retornado pelo módulo.

Subprocessos ficam reservados para cenários futuros de isolamento forte.

## Consequências

- Experiência visual integrada.
- Comunicação simples por contrato Python.
- Necessidade de isolamento de falhas em boundaries.
- Módulos continuam responsáveis por seus workers e recursos.

## Alternativas consideradas

- Abrir `DNS-Bench-Pro.exe` por subprocess.
- RPC local.
- Processo separado por módulo desde v1.

## Status

Aceito

