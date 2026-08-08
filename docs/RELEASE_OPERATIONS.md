# Operações de Release do Bench Pro Core

Estes procedimentos documentam o fluxo operacional de release do Bench Pro Core.

## Versão atual

```text
Bench Pro Core v0.1.0
```

Notas públicas da versão:

```text
docs/releases/v0.1.0.md
```

## Remote oficial

```bash
git remote set-url origin https://github.com/leosgarcia/benchpro-core.git
git remote -v
```

## Metadados do repositório

```bash
gh repo edit leosgarcia/benchpro-core --homepage https://wltech.com.br --description "Bench Pro Core — aplicação agregadora do ecossistema Bench Pro da WL Tech."
```

## Validação antes de release

```bash
pytest
ruff check .
bandit -r src
python -m benchpro_core --list-modules
```

Validações manuais recomendadas:

- abrir GUI do Core;
- verificar navegação lateral;
- carregar DNS Bench Pro;
- carregar SMTP Bench Pro;
- alternar entre módulos;
- fechar aplicação e validar shutdown.

## Criar tag

```bash
git fetch --tags
git tag -a v0.1.0 -m "Bench Pro Core v0.1.0"
git push origin main
git push origin v0.1.0
```

## Criar release manualmente

```bash
gh release create v0.1.0 \
  --repo leosgarcia/benchpro-core \
  --title "Bench Pro Core v0.1.0" \
  --notes-file docs/releases/v0.1.0.md
```

## Artefatos futuros

O Core ainda não publica executável PyInstaller oficial.

Quando o empacotamento for habilitado, a distribuição v1 deve preferencialmente incluir os módulos aprovados embarcados, mantendo a arquitetura preparada para módulos instaláveis no futuro.
