# ADR-002 — Direção de dependência

## Contexto

As aplicações micro devem continuar funcionando sozinhas. Se dependessem do Core, o ecossistema perderia autonomia e distribuição independente.

## Decisão

A dependência permitida é:

```text
Bench Pro Core → Micro aplicações
```

É proibido:

```text
Micro aplicação → Bench Pro Core
```

## Consequências

- Micros não importam `benchpro_core`.
- Core valida módulos por contrato local.
- Standalone permanece protegido.
- Integração é capacidade adicional, não requisito.

## Alternativas consideradas

- Criar SDK obrigatório.
- Fazer as micros herdarem classes do Core.
- Compartilhar banco/configuração via Core.

## Status

Aceito

