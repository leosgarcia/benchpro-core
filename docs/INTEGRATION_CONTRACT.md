# Integration Contract v1

## Objetivo

O Integration Contract v1 define o contrato mínimo para que uma aplicação Bench Pro possa ser hospedada pelo Bench Pro Core sem depender dele.

O contrato é pequeno por decisão arquitetural. Ele deve permitir integração real, mas evitar que o Core se transforme em framework obrigatório.

## Regra absoluta

A micro aplicação não importa `benchpro_core`.

O Core valida o módulo por duck typing, Protocol local e metadados.

## Metadados obrigatórios

| Campo | Tipo esperado | Descrição |
| :--- | :--- | :--- |
| `module_id` | `str` | Identificador curto e estável. Ex.: `dns`, `smtp`. |
| `display_name` | `str` | Nome exibido ao usuário. |
| `version` | `str` | Versão comercial do produto. |
| `integration_api` | `int` | Versão do contrato de integração. |
| `vendor` | `str` | Fornecedor do módulo. |
| `capabilities` | `set[str]` ou compatível | Recursos funcionais oferecidos. |

## Métodos obrigatórios

```python
def initialize() -> None:
    ...

def create_widget(parent=None):
    ...

def shutdown() -> None:
    ...
```

### initialize

Prepara estado interno mínimo.

Não deve:

- abrir janela principal;
- iniciar benchmark automaticamente;
- executar rede sem ação do usuário;
- acessar Core internamente.

### create_widget

Retorna um `QWidget` integrável.

Não deve retornar:

- `QMainWindow`;
- janela standalone completa;
- tela Sobre duplicada;
- menu próprio de aplicação.

### shutdown

Libera recursos internos do módulo.

Deve ser seguro chamar durante fechamento do Core. Falhas devem ser tratadas pelo Core sem impedir shutdown dos demais módulos.

## Discovery

Grupo de entry points:

```toml
[project.entry-points."benchpro.modules"]
dns = "integration.module:DNSBenchModule"
smtp = "smtp_bench_pro.integration.module:SMTPBenchModule"
```

## Compatibilidade

O Core valida `integration_api`, não a versão comercial.

Exemplo:

```text
SMTP Bench Pro 0.2.5
Integration API 1
```

## Extensões futuras

Não fazem parte do v1 obrigatório:

- `health_check()`;
- `activate()`;
- `deactivate()`;
- APIs de histórico unificado;
- APIs de relatório unificado.

Essas extensões só devem entrar em nova versão de contrato após necessidade real.
