# Manual Test Checklist

Status: Core Shell hardening checklist

## Startup

- [ ] Application opens without traceback.
- [ ] Window title is `Bench Pro Core`.
- [ ] Status bar shows a short ready state.
- [ ] Menu `Arquivo` contains `Sair`.
- [ ] Menu `Ajuda` contains `Sobre o Bench Pro Core`.

## Discovery

- [ ] Installed compatible modules are discovered.
- [ ] DNS Bench Pro appears when installed via editable package.
- [ ] No placeholder modules such as SMTP/SSL/HTTP are shown unless actually installed.
- [ ] Unavailable modules, if any, appear under `Módulos indisponíveis`.

## Navigation

- [ ] Module selection is visually clear.
- [ ] Up/Down keyboard navigation works.
- [ ] Enter activates the highlighted module.
- [ ] Module tooltip shows version and Integration API.
- [ ] Unavailable module tooltip shows a summarized reason without traceback.

## DNS Mount

- [ ] Selecting `DNS Bench Pro` mounts the DNS module widget.
- [ ] DNS tabs shown in integrated mode are `Benchmark`, `Servidores`, `Histórico`, and `Análises`.
- [ ] DNS `Sobre` tab is not shown in integrated mode.
- [ ] Switching away and back reuses the same DNS widget instance during the session.

## DNS Benchmark

- [ ] Benchmark starts from inside Core.
- [ ] Progress updates incrementally.
- [ ] Results appear in the table.
- [ ] Final status is shown by the DNS widget.
- [ ] No Core-specific action is required for DNS worker/thread lifecycle.

## DNS History

- [ ] A completed DNS benchmark is saved in DNS Bench Pro history.
- [ ] History tab loads saved sessions.
- [ ] Core does not read DNS SQLite tables directly.

## DNS Charts

- [ ] Analysis tab renders DNS charts after a benchmark.
- [ ] Switching modules does not destroy chart state unexpectedly.

## Window Resize

- [ ] Window can be resized.
- [ ] Navigation width remains usable.
- [ ] Module container resizes cleanly.

## Window Restore

- [ ] Close and reopen restores previous window geometry.
- [ ] Maximized state restores correctly.
- [ ] Invalid settings fall back to a professional default size.

## Module Failure

- [ ] A broken module does not prevent Core startup.
- [ ] Broken module is shown under `Módulos indisponíveis`.
- [ ] Selecting it shows `Módulo indisponível` in the container.
- [ ] UI message contains no traceback, full local path, token, or credential.
- [ ] Technical details are present only in logs.

## About

- [ ] About dialog shows Bench Pro Core version.
- [ ] About dialog shows Integration API 1.
- [ ] Loaded modules are listed.
- [ ] Unavailable modules are listed only when present.

## Shutdown

- [ ] Closing Core calls `registry.shutdown_all()`.
- [ ] All loaded modules receive `shutdown()`.
- [ ] A shutdown failure in one module does not block window close.
- [ ] Window settings are saved.
- [ ] Logs are flushed.
