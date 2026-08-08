# Versionamento do Ecossistema Bench Pro

## Versão do produto

Cada produto possui SemVer independente.

Exemplos:

```text
DNS Bench Pro 1.0.0
SMTP Bench Pro 0.2.5
Bench Pro Core 0.1.0
```

A versão do produto comunica evolução funcional, correções, compatibilidade e releases.

## Integration API

A versão do contrato de integração é um inteiro independente.

Exemplo:

```text
SMTP Bench Pro 0.2.5
Integration API 1
```

O Core valida `integration_api`, não a versão comercial do produto.

## Quando mudar o Integration API

Mudar somente quando o contrato obrigatório mudar.

Exemplos de mudança que exigem nova API:

- novo método obrigatório;
- alteração de assinatura obrigatória;
- mudança semântica incompatível;
- remoção de metadado obrigatório.

Não exige nova API:

- nova feature interna do módulo;
- novo relatório;
- nova aba;
- nova versão comercial;
- nova capability opcional.

## Compatibilidade

Core 0.1.0 suporta:

```text
Integration API 1
```

Módulos com API incompatível devem ser rejeitados de forma amigável.
