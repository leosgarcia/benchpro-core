# Ciclo de Vida dos Módulos

## Lifecycle v1

O lifecycle mínimo do Bench Pro Core é:

```text
discover → validate → load → initialize → create_widget → shutdown
```

## discover

O Core consulta entry points do grupo `benchpro.modules`.

Falhas de discovery devem ser registradas em log e isoladas.

## validate

O Core valida:

- metadados obrigatórios;
- `integration_api` suportado;
- métodos mínimos;
- formato de capabilities.

Módulos inválidos não devem derrubar o Core.

## load

O Core importa e instancia a classe exposta pelo entry point.

Falhas de import devem ser capturadas e exibidas como módulo indisponível.

## initialize

O módulo prepara seu estado interno.

A operação deve ser idempotente sempre que possível.

Não deve executar rede automaticamente.

## create_widget

O módulo entrega um `QWidget` funcional para o container do Core.

O Core não deve recriar o widget a cada troca de navegação. A instância pode ser cacheada durante a sessão.

## shutdown

O Core chama shutdown ao fechar a aplicação.

Regras:

- falha em um módulo não impede shutdown dos demais;
- exceções são registradas;
- a aplicação deve fechar normalmente;
- workers internos pertencem ao módulo.

## Rollback e falhas

Se `initialize` falhar, o módulo não deve ser ativado.

Se `create_widget` falhar, o Core deve mostrar erro amigável e manter outros módulos funcionais.

Se `shutdown` falhar, o Core registra a falha e continua encerrando.

## Responsabilidade dos módulos

Cada módulo controla:

- workers;
- sockets;
- locks;
- banco próprio;
- configurações internas;
- logs próprios;
- estado funcional.

O Core hospeda. O módulo executa.
