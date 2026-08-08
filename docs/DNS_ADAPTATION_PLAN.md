# Plano de Adaptação do DNS Bench Pro

## Objetivo

Adaptar o DNS Bench Pro existente para integração com o Bench Pro Core com o menor conjunto de alterações possível.

## Fase A — Criar pacote de integração

Adicionar:

```text
src/integration/
├── __init__.py
└── module.py
```

Responsabilidade:

- expor metadados;
- implementar Integration API v1;
- criar widget integrado;
- preservar standalone.

## Fase B — Criar widget reutilizável

Extrair o conteúdo funcional para:

```text
src/ui/widgets/dns_bench_widget.py
```

Este widget deve conter a experiência operacional principal, sem menu global e sem tela Sobre obrigatória.

## Fase C — Adaptar janela standalone

A MainWindow standalone passa a compor `DNSBenchWidget`.

Não remover menus, status bar, ajuda e Sobre do modo standalone.

## Fase D — Configurar entry point

Adicionar ao `pyproject.toml`:

```toml
[project.entry-points."benchpro.modules"]
dns = "integration.module:DNSBenchModule"
```

## Fase E — Testes de contrato

Validar:

- metadata completa;
- `integration_api == 1`;
- `create_widget()` retorna `QWidget`;
- widget integrado não é `QMainWindow`;
- shutdown não falha.

## Fase F — Validar standalone

Executar:

```bash
pytest
python src/main.py
```

A aplicação standalone deve continuar igual para o usuário.

## Fase G — Validar integração futura

Instalar em modo editable ao lado do Core:

```bash
python -m pip install -e ..\dns-bench-pro
python -m benchpro_core --list-modules
```

O Core deve descobrir DNS Bench Pro sem tratamento especial.

## Rollback

Cada fase é reversível:

- remover entry point;
- remover pacote integration;
- retornar MainWindow ao estado anterior;
- manter banco e schema intactos.

## Risco principal

O maior risco é misturar lógica de Core dentro do DNS. Isso deve ser evitado com adapter pattern e contrato mínimo.
