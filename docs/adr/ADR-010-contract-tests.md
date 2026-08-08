# ADR-010 — Testes de contrato

## Contexto

Módulos evoluem em repositórios separados. O Core precisa de garantias automáticas de que módulos compatíveis continuam respeitando o contrato.

## Decisão

Criar testes de contrato para validar módulos Bench Pro.

Validações mínimas:

- metadata obrigatória;
- `integration_api` suportado;
- `create_widget()` retorna `QWidget`;
- `shutdown()` não derruba o host;
- módulo inválido é rejeitado;
- falha de módulo não derruba registry/Core.

## Consequências

- Menor risco em integrações futuras.
- CI do Core pode testar módulos fake e módulos reais instalados.
- Micros podem copiar testes de contrato localmente.

## Alternativas consideradas

- Validar manualmente apenas pela GUI.
- Confiar somente em documentação.
- Criar SDK obrigatório com classes base.

## Status

Aceito

