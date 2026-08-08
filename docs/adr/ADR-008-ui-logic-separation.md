# ADR-008 — Separação entre UI e lógica

## Contexto

Para que uma micro seja integrável, a lógica funcional não pode viver diretamente na janela principal standalone.

## Decisão

Cada micro deve separar UI, application services, engine, domain models, persistence e integration adapter.

A janela standalone compõe o widget funcional. O Core hospeda esse mesmo widget em modo integrado.

## Consequências

- Menos duplicação de UI.
- Standalone e integrado usam a mesma base funcional.
- Testes de engine e service ficam mais simples.
- Refatorações devem preservar comportamento standalone.

## Alternativas consideradas

- Duplicar tela integrada no Core.
- Reutilizar `QMainWindow` inteira dentro do Core.
- Manter lógica de negócio nos widgets principais.

## Status

Aceito

