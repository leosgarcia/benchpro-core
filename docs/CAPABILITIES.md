# Capabilities do Ecossistema Bench Pro

## Objetivo

Capabilities descrevem o que um módulo oferece ao Bench Pro Core. Elas não são rótulos de marketing; são declarações funcionais que o Core pode usar para montar navegação, dashboards, relatórios e fluxos futuros.

## Regra principal

Um módulo só deve declarar uma capability quando a funcionalidade existir de forma utilizável.

Não declarar capabilities futuras.

## Capabilities v1

| Capability | Definição |
| :--- | :--- |
| `benchmark` | Executa medições repetidas e produz resultados quantitativos. |
| `diagnostics` | Executa verificações funcionais/protocolares estruturadas. |
| `history` | Persiste e expõe histórico utilizável. |
| `reports` | Gera relatórios formais para usuário ou cliente. |
| `charts` | Possui visualizações gráficas dedicadas. |
| `security_audit` | Produz achados de segurança com severidade e evidência. |
| `dns_checks` | Executa consultas DNS auxiliares ao diagnóstico principal. |

## Exemplos atuais

DNS Bench Pro:

```text
benchmark
diagnostics
history
reports
charts
```

SMTP Bench Pro:

```text
benchmark
diagnostics
history
security_audit
```

## Cuidados

- `tls` não deve ser usado como capability se for apenas detalhe interno de diagnóstico.
- `history` exige visualização ou API de histórico utilizável.
- `security_audit` exige findings estruturados, não apenas mensagens de aviso.
- `reports` deve significar exportação formal, não apenas tela de resultados.

## Uso pelo Core

O Core pode usar capabilities para:

- exibir ou ocultar áreas futuras;
- montar dashboards;
- informar recursos disponíveis no Sobre;
- validar compatibilidade;
- direcionar fluxos integrados.

O Core não deve assumir que todos os módulos possuem as mesmas capabilities.
