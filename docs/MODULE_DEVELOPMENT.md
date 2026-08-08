# Guia de Desenvolvimento de Módulos Bench Pro

## Objetivo

Este guia orienta a criação de novas micro aplicações compatíveis com o Bench Pro Core.

## Princípio standalone first

Toda micro deve funcionar completamente sozinha antes de ser integrada.

Requisitos mínimos:

- `python -m nome_do_produto` funcional;
- executável próprio no futuro;
- banco próprio;
- configuração própria;
- testes próprios;
- README próprio;
- LICENSE próprio;
- CI própria.

## Estrutura recomendada

```text
src/
└── produto_bench_pro/
    ├── application/
    ├── domain/
    ├── engine/
    ├── persistence/
    ├── export/
    ├── security/
    ├── ui/
    ├── integration/
    ├── paths.py
    ├── version.py
    └── __main__.py
```

Nem todos os pacotes são obrigatórios no início, mas a separação entre UI, application services, engine e persistence deve ser preservada.

## Separação UI/lógica

Errado:

```text
MainWindow → abre socket → calcula estatística → salva banco
```

Correto:

```text
Widget → Application Service → Engine → Domain Models → Repository
```

Essa separação permite que o Core hospede o widget sem conhecer lógica interna.

## Integração opcional

Adicionar pacote:

```text
integration/
├── __init__.py
└── module.py
```

Exemplo conceitual:

```python
class ProdutoBenchModule:
    module_id = "produto"
    display_name = "Produto Bench Pro"
    version = __version__
    integration_api = 1
    vendor = "WL Tech"
    capabilities = frozenset({"benchmark", "history"})

    def initialize(self): ...
    def create_widget(self, parent=None): ...
    def shutdown(self): ...
```

## Entry point

```toml
[project.entry-points."benchpro.modules"]
produto = "produto_bench_pro.integration.module:ProdutoBenchModule"
```

## Testes obrigatórios

- contrato de integração;
- widget integrado sem tela Sobre;
- standalone continua funcionando;
- migrations de banco;
- fronteiras de segurança;
- regressão das principais features.

## Versionamento

A versão comercial segue SemVer.

A versão do Integration API é inteiro separado.

## Empacotamento

Cada micro deve gerar seu próprio executável. Empacotamento conjunto pelo Core é estratégia adicional, não substituição do standalone.
