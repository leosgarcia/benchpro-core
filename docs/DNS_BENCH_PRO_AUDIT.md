# Auditoria Técnica do DNS Bench Pro

## Objetivo

Esta auditoria registra a análise do DNS Bench Pro existente para torná-lo compatível com o Bench Pro Core sem reescrever o produto e sem quebrar o modo standalone.

## Resultado executivo

O DNS Bench Pro já possuía uma base funcional sólida, com engine, persistência, exportação, histórico e UI. A adaptação recomendada foi incremental, usando adapter pattern e extração mínima de UI reutilizável.

O objetivo não foi reorganizar o projeto inteiro, e sim permitir duas formas de uso:

```text
Standalone Application
+
Integratable Module
```

## Pontos auditados

| Área | Responsabilidade atual | Acoplamento | Alteração necessária | Risco |
| :--- | :--- | :---: | :--- | :---: |
| Entry point | Inicia aplicação standalone | Baixo | Preservar comportamento atual | LOW |
| MainWindow | Composição da GUI standalone | Médio | Delegar conteúdo principal para widget reutilizável | MEDIUM |
| Benchmark engine | Execução de testes DNS | Baixo | Reutilizar sem alteração estrutural | LOW |
| Models | Representação de resultados | Baixo | Manter API atual | LOW |
| Persistence | SQLite e histórico | Médio | Expor leitura via repository, sem acesso direto pelo Core | MEDIUM |
| Exporters | PDF/CSV/JSON | Baixo | Manter standalone | LOW |
| Charts | Visualizações da aplicação | Médio | Reutilizar dentro do widget principal | MEDIUM |
| Settings | Configurações próprias | Médio | Não migrar para settings do Core | LOW |
| Logging | Logger próprio | Baixo | Manter namespace próprio | LOW |
| Threading | Workers internos | Médio | Core não acessa workers diretamente | MEDIUM |

## Acoplamentos relevantes

- Conteúdo funcional originalmente concentrado na janela principal.
- Histórico e relatórios pertencem ao DNS, não ao Core.
- O Core não deve abrir o banco DNS diretamente.
- A UI integrada não deve exibir menu, status bar ou Sobre standalone.

## Estratégia adotada

Criar um widget raiz reutilizável:

```text
DNSBenchWidget
```

E manter:

```text
StandaloneMainWindow
    ↓
DNSBenchWidget

Bench Pro Core
    ↓
DNSBenchWidget
```

## Contrato proposto

```python
class DNSBenchModule:
    module_id = "dns"
    display_name = "DNS Bench Pro"
    version = __version__
    integration_api = 1
    vendor = "WL Tech"
    capabilities = frozenset({"benchmark", "diagnostics", "history", "reports", "charts"})
```

## Critérios de aceitação

- DNS standalone continua funcionando.
- DNS integrado retorna `QWidget`, não `QMainWindow`.
- Core não importa classes internas específicas fora do entry point.
- Banco DNS continua no namespace do DNS.
- Testes de contrato passam.
- Testes essenciais de benchmark passam.
