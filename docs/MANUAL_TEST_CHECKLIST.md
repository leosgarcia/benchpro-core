# Checklist de Teste Manual

## Objetivo

Este checklist valida a experiência integrada do Bench Pro Core com módulos reais instalados em modo editable.

## Preparação

Workspace esperado:

```text
BENCHPRO/
├── benchpro-core/
├── dns-bench-pro/
└── smtp-bench-pro/
```

Instalação:

```bash
cd benchpro-core
python -m pip install -e .
python -m pip install -e ..\dns-bench-pro
python -m pip install -e ..\smtp-bench-pro
```

## Discovery

Executar:

```bash
python -m benchpro_core --list-modules
```

Esperado:

```text
DNS Bench Pro 1.0.0 [API 1]
SMTP Bench Pro 0.2.5 [API 1]
```

## Core GUI

Executar:

```bash
python -m benchpro_core
```

Validar:

- janela abre com título Bench Pro Core;
- navegação lateral aparece;
- módulos descobertos aparecem dinamicamente;
- estado vazio é exibido antes da seleção;
- menu Arquivo/Sair funciona;
- Sobre lista módulos carregados.

## DNS integrado

Validar:

- DNS aparece na navegação;
- selecionar DNS monta widget;
- abas funcionais aparecem;
- não há menu standalone duplicado;
- não há aba Sobre do DNS no modo integrado;
- benchmark continua responsivo.

## SMTP integrado

Validar:

- SMTP aparece na navegação;
- selecionar SMTP monta widget;
- abas Benchmark, Diagnóstico, Segurança e Histórico aparecem;
- exportação histórica permanece local ao SMTP;
- comparação histórica permanece local ao SMTP;
- não há aba Sobre no modo integrado.

## Troca de módulos

Executar sequência:

```text
DNS → SMTP → DNS → SMTP
```

Validar:

- widgets são reutilizados;
- estado interno não é perdido desnecessariamente;
- nenhum módulo interfere no outro;
- Core permanece responsivo.

## Shutdown

Fechar Core.

Validar:

- `shutdown()` é chamado nos módulos;
- exceções não fecham abruptamente a aplicação;
- logs são gravados pelo Core.

## Standalone após integração

Executar fora do Core:

```bash
python -m smtp_bench_pro
python src/main.py  # no DNS Bench Pro
```

Ambos devem continuar funcionando como produtos independentes.
