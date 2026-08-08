# Bench Pro Design Guidelines

## Objetivo

Este documento define diretrizes visuais e de experiência para produtos Bench Pro. Ele orienta consistência entre DNS Bench Pro, SMTP Bench Pro, Bench Pro Core e futuras aplicações, sem criar dependência runtime compartilhada.

## Princípios

- Interface profissional, objetiva e densa o suficiente para uso técnico.
- Prioridade para clareza operacional, não aparência promocional.
- Estados e ações visíveis, previsíveis e auditáveis.
- Cores semânticas acompanhadas de texto.
- Módulos independentes, mas visualmente familiares.

## Estrutura comum

Aplicações standalone devem conter:

- janela principal;
- menu mínimo;
- abas ou navegação clara;
- status bar;
- tela Sobre;
- ajuda contextual quando aplicável.

Modo integrado deve evitar:

- menu próprio;
- status bar própria conflitante;
- botão Sair;
- janela interna;
- aba Sobre duplicada.

## Navegação

Preferir:

- abas para áreas principais dentro de uma micro;
- lista lateral para módulos no Core;
- master/detail para histórico;
- diálogos read-only para comparações e relatórios técnicos.

## Tabelas

Tabelas devem:

- ter colunas úteis e estáveis;
- evitar excesso de campos;
- ser redimensionáveis;
- manter textos de status claros;
- não depender apenas de cor.

## Ações

Ações primárias:

- devem estar próximas do contexto;
- devem ter texto claro;
- devem ficar desabilitadas quando não forem aplicáveis.

Ações destrutivas:

- exigem confirmação;
- devem explicar consequência;
- devem evitar ambiguidade.

## Severidade

Padrão textual:

- Critical
- High
- Medium
- Low
- Info

Cores podem reforçar a leitura, mas o texto é obrigatório.

## Estados vazios

Estados vazios devem explicar o que falta e qual ação cria dados.

Exemplos:

```text
Nenhuma execução disponível.
Execute um benchmark ou diagnóstico para criar histórico.
```

```text
Selecione uma execução para visualizar os detalhes.
```

## Relatórios

Relatórios exportados devem:

- ser técnicos e neutros;
- preservar evidências;
- identificar versão do produto;
- separar timestamp de execução e timestamp de exportação;
- escapar dados fornecidos por servidores;
- evitar conclusões exageradas.

## Sobre

A tela Sobre deve conter:

- nome do produto;
- versão;
- fornecedor;
- copyright;
- propósito curto;
- módulos carregados, no caso do Core.

## Independência de implementação

Estas diretrizes não exigem QSS, biblioteca visual ou pacote compartilhado. Cada produto pode implementar localmente, desde que respeite a experiência comum.
