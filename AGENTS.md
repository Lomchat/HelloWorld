# AGENTS.md

Instructions for AI coding agents (Codex, Cursor, Copilot, Gemini, Claude...) working on this repository.

> [!NOTE]
> The canonical, most detailed version of these guidelines is [CLAUDE.md](CLAUDE.md).
> This file is a summary. Keep both files in sync when updating either of them.

## Setup

```bash
make install
```

## Before finishing any task

```bash
make check
```

All checks (ruff, mypy `--strict`, pytest with 100% coverage, output verification) MUST pass.

## Non-negotiable rules

1. The output MUST be exactly `Hello, World!\n` on stdout, and nothing on stderr.
2. `src/hello_world/hello_world.py` contains exactly one statement: `print("Hello, World!")`. Comments only around it, no docstring (ADR-0009).
3. Importing the `hello_world` package prints nothing (#95).
4. No new modules in `src/` (ADR-0004).
5. Coverage stays at 100%. No runtime dependencies.
6. Every bug fix comes with a regression test referencing the issue number.

## Where things are

| Concern              | Location                              |
| -------------------- | ------------------------------------- |
| Implementation       | `src/hello_world/hello_world.py`      |
| `python -m` entry    | `src/hello_world/__main__.py`         |
| Version              | `src/hello_world/__init__.py`         |
| Architecture records | `docs/adr/`                           |
| Test fixtures        | `tests/conftest.py`                   |
| Test helpers         | `tests/helpers.py`                    |
