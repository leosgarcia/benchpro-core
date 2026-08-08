# ADR-001 — Repositórios independentes

## Contexto

O ecossistema Bench Pro contém múltiplos produtos com ciclos de vida diferentes. DNS Bench Pro, SMTP Bench Pro e Bench Pro Core precisam evoluir, versionar e publicar releases sem bloquear uns aos outros.

## Decisão

Cada produto terá repositório Git próprio.

Exemplos:

- `dns-bench-pro`
- `smtp-bench-pro`
- `benchpro-core`
- futuros `ssl-bench-pro`, `http-bench-pro`, `ssh-bench-pro`

## Consequências

- Releases independentes.
- Issues e CI por produto.
- Menor acoplamento organizacional.
- Necessidade de validar integração entre repositórios.

## Alternativas consideradas

- Monorepo único para toda a suíte.
- Submodules Git.
- Repositório pai sem estratégia formal.

## Status

Aceito

