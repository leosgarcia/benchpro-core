# Bench Pro Core

<p align="center">
  <strong>Aplicação agregadora do ecossistema Bench Pro da WL Tech</strong>
</p>

<p align="center">
  <a href="https://github.com/leosgarcia/benchpro-core"><img src="https://img.shields.io/badge/Reposit%C3%B3rio-benchpro--core-111827?style=for-the-badge&logo=github" alt="Repositório benchpro-core" /></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-blue.svg?style=for-the-badge" alt="Licença MIT" /></a>
  <a href="https://github.com/leosgarcia/benchpro-core/actions"><img src="https://img.shields.io/github/actions/workflow/status/leosgarcia/benchpro-core/ci.yml?branch=main&style=for-the-badge&label=CI" alt="Status da CI" /></a>
</p>

## Visão geral

**Bench Pro Core** é a aplicação desktop agregadora do ecossistema **Bench Pro**, desenvolvido pela **WL Tech**. Seu papel é descobrir, validar e hospedar módulos compatíveis, como DNS Bench Pro e SMTP Bench Pro, em uma experiência unificada.

O Core não é uma biblioteca obrigatória para as aplicações micro. Cada produto continua independente, com repositório, versão, banco SQLite, configuração, CI, distribuição e ciclo de release próprios.

## Regra arquitetural central

A dependência sempre aponta do Core para os módulos:

```text
Bench Pro Core
      ↓
Aplicações micro compatíveis
```

Nunca o inverso:

```text
Aplicação micro
      ↓
Bench Pro Core
```

Isso garante que DNS Bench Pro, SMTP Bench Pro e futuros produtos continuem funcionando como aplicações standalone completas.

## Recursos atuais

- Descoberta de módulos via `importlib.metadata.entry_points`.
- Validação do Integration API v1.
- Carregamento, inicialização e shutdown de módulos.
- Isolamento de falhas durante discovery, load, widget creation e shutdown.
- Shell desktop em PySide6 com navegação lateral e container genérico de módulos.
- Hospedagem de widgets fornecidos por módulos sem conhecer detalhes internos dos produtos.
- Testes de contrato, lifecycle, UI shell, discovery e integração multimódulo.
- Documentação arquitetural, ADRs e guia de desenvolvimento de módulos.

## Produtos do ecossistema

| Produto | Tipo | Estado | Repositório |
| :--- | :--- | :--- | :--- |
| DNS Bench Pro | Micro aplicação | Integrado | https://github.com/leosgarcia/dns-bench-pro |
| SMTP Bench Pro | Micro aplicação | Integrado | https://github.com/leosgarcia/smtp-bench-pro |
| Bench Pro Core | Agregador | Pre-alpha | https://github.com/leosgarcia/benchpro-core |
| SSL / HTTP / SSH Bench Pro | Micro aplicações futuras | Planejado | A definir |

## Uso

### Instalação em modo desenvolvimento

```bash
git clone https://github.com/leosgarcia/benchpro-core.git
cd benchpro-core
python -m pip install -e ".[dev]"
```

Para testar integração real com módulos locais:

```bash
python -m pip install -e ..\dns-bench-pro
python -m pip install -e ..\smtp-bench-pro
```

### Interface gráfica

```bash
python -m benchpro_core
```

### Listar módulos descobertos

```bash
python -m benchpro_core --list-modules
```

Exemplo:

```text
Bench Pro Core 0.1.0

Discovered modules:
DNS Bench Pro 1.0.0 [API 1]
SMTP Bench Pro 0.4.0 [API 1]
```

## Estrutura do projeto

```text
benchpro-core/
├── docs/                         # Arquitetura, contrato, ciclo de vida e ADRs
├── src/benchpro_core/            # Código-fonte da aplicação Core
│   ├── module_host/              # Discovery, loader, contrato e registry
│   ├── ui/                       # MainWindow, navegação, container e estados vazios
│   ├── logging_config.py         # Configuração de logging
│   ├── paths.py                  # Diretórios por plataforma
│   ├── version.py                # Versão do produto
│   └── __main__.py               # Entrada GUI/CLI
├── tests/                        # Testes unitários, UI e integração
├── pyproject.toml                # Metadados e configuração de ferramentas
└── requirements-dev.txt          # Dependências de desenvolvimento
```

## Documentação

- [Arquitetura](docs/ARCHITECTURE.md)
- [Contrato de Integração](docs/INTEGRATION_CONTRACT.md)
- [Ciclo de Vida dos Módulos](docs/MODULE_LIFECYCLE.md)
- [Guia de Desenvolvimento de Módulos](docs/MODULE_DEVELOPMENT.md)
- [Versionamento](docs/VERSIONING.md)
- [Capabilities](docs/CAPABILITIES.md)
- [Design Guidelines](docs/DESIGN_GUIDELINES.md)
- [Checklist de Teste Manual](docs/MANUAL_TEST_CHECKLIST.md)
- [ADRs](docs/adr/)

## Qualidade

```bash
pytest
ruff check .
bandit -r src
```

Estado atual validado:

- `pytest`: 48 testes passando
- `ruff`: sem violações no Core
- `bandit`: sem achados relevantes no Core

## Roadmap

- Dashboard operacional do ecossistema.
- Relatórios integrados de infraestrutura.
- Empacotamento com módulos embarcados.
- Estratégia de instalação modular futura.
- Histórico e relatórios unificados sem acoplamento ao schema interno das micros.
- Contratos de compatibilidade para novas Integration APIs.

## Segurança

O Core não coleta senhas, tokens, certificados privados ou credenciais das aplicações micro. Credenciais, quando existirem, pertencem ao contexto específico do módulo e devem respeitar o princípio de menor privilégio.

## Licença

Bench Pro Core é distribuído sob a [Licença MIT](LICENSE).

© 2026 WL Tech. Website: https://wltech.com.br

