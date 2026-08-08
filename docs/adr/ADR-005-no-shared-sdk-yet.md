# ADR-005 — Não criar SDK compartilhado ainda

## Contexto

Um SDK compartilhado poderia parecer conveniente, mas criaria dependência prematura entre micros e Core.

## Decisão

Não criar `benchpro-sdk`, `benchpro-common` ou pacote compartilhado nesta fase.

O Core valida módulos por contrato local e duck typing.

## Consequências

- Menor acoplamento inicial.
- Menos risco de framework interno prematuro.
- Possível duplicação pequena e aceitável no curto prazo.
- Extração futura seguirá Rule of Three.

## Alternativas consideradas

- SDK obrigatório desde v1.
- Pacote comum de UI/configuração.
- Compartilhar QSS e helpers por runtime dependency.

## Status

Aceito

