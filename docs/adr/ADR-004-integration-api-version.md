# ADR-004 — Versionamento do Integration API

## Contexto

A versão comercial de um produto não representa necessariamente compatibilidade com o Core.

## Decisão

Criar `integration_api` como inteiro independente da versão do produto.

Exemplo:

```text
SMTP Bench Pro 0.2.5
Integration API 1
```

## Consequências

- Core valida contrato por API, não por SemVer do produto.
- Produtos podem evoluir features sem mudar contrato.
- Quebras de contrato exigem nova versão de API.

## Alternativas consideradas

- Usar apenas SemVer do produto.
- Criar range de versões por módulo.
- Não validar compatibilidade.

## Status

Aceito

