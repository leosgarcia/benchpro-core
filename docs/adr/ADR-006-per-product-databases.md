# ADR-006 — Bancos por produto

## Contexto

Cada micro aplicação possui histórico, schema e regras de persistência próprias. Um banco único criaria acoplamento entre produtos e dificultaria evolução independente.

## Decisão

Cada produto mantém seu próprio banco SQLite.

Exemplos:

- `bench-pro-core.db`
- `dns-bench-pro.db`
- `smtp-bench-pro.db`

## Consequências

- Schema de cada produto evolui separadamente.
- Core não executa SQL direto em banco de micro.
- Integração de histórico deve usar API/repository do módulo.
- Backups e troubleshooting ficam isolados por produto.

## Alternativas consideradas

- Banco único para toda a suíte.
- Core como dono do schema de todas as micros.
- Replicação automática de dados para o Core.

## Status

Aceito

