# ADR-009 — Módulos embarcados na distribuição v1

## Contexto

O Core poderá no futuro suportar módulos instaláveis separadamente, mas a primeira distribuição integrada precisa reduzir variáveis operacionais.

## Decisão

A estratégia preferencial para v1 é uma distribuição completa com módulos aprovados embarcados.

A arquitetura, porém, permanece compatível com instalação modular futura via entry points.

## Consequências

- Menos risco de incompatibilidade para usuário final.
- Build inicial mais previsível.
- Pipeline de release do Core deve validar módulos incluídos.
- Instalação modular pode ser adicionada depois sem mudar o contrato v1.

## Alternativas consideradas

- Marketplace de plugins desde v1.
- Instalação manual de módulos pelo usuário.
- Core distribuído vazio.

## Status

Aceito

