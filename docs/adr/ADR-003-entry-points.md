# ADR-003 — Discovery por entry points

## Contexto

O Core precisa descobrir módulos instalados sem registry manual e sem exigir que as micros conheçam o host.

## Decisão

Usar `importlib.metadata.entry_points` com o grupo:

```text
benchpro.modules
```

## Consequências

- Mecanismo padrão do Python.
- Funciona com instalações editable.
- Testável em CI.
- Não exige arquivo de manifesto externo na v1.

## Alternativas consideradas

- Manifestos JSON.
- Registry explícito mantido pelo Core.
- Busca por diretórios locais.

## Status

Aceito

