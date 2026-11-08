# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`hello-world` is a production-grade, fully typed Python implementation of the canonical "Hello, World!" program.

- **Language:** Python 3.10+ (developed on 3.12)
- **Runtime dependencies:** none (standard library only). Keep it that way.
- **Current version:** see `__version__` in `src/hello_world/__init__.py`

## Commands

```bash
make install        # create .venv and install dev dependencies
make test           # run the full test suite
make coverage       # run tests with coverage (fails under 100%)
make lint           # ruff check + ruff format --check
make format         # auto-format with ruff
make typecheck      # mypy --strict
make check          # lint + typecheck + coverage (run this before finishing ANY task)
make bench          # run micro-benchmarks
```

Run a single test:

```bash
.venv/bin/pytest tests/unit/test_greet.py::TestReturnValue::test_returns_the_canonical_greeting
```

Run a single category: `.venv/bin/pytest -m security` (markers: `unit`, `integration`, `e2e`, `property`, `regression`, `security`, `conformance`, `concurrency`, `performance`).

## Architecture

```
hello-world (console script) ──┐
                               ├──► main() ──► greet() ──► GREETING
python -m hello_world ─────────┘      │
                                      └──► print() ──► stdout
```

- The **entire implementation** lives in `src/hello_world/hello_world.py` (see ADR-0004).
- `__init__.py` only re-exports the public API and defines `__version__`.
- `__main__.py` only calls `main()`.
- **Do NOT create new modules in `src/`.** `tests/unit/test_package.py` enforces the exact list of source files.
- Architectural decisions are documented in `docs/adr/`. Read them before changing anything.

## Critical Invariants

**IMPORTANT: These invariants MUST NEVER be broken. If a change would break one of them, STOP and ask.**

1. The program MUST write exactly `Hello, World!` followed by a single `\n` to stdout. Nothing else. Byte for byte. Nothing on stderr.
2. `greet()` MUST be pure: no side effects, no I/O, always the same return value.
3. `main()` MUST return `0` (an `int`, not `None`, not `True`) (#51).
4. The string `"Hello, World!"` MUST be defined exactly once in `src/`, as `GREETING` (ADR-0006).
5. Test coverage MUST stay at **100%** (lines and branches).
6. `mypy --strict` MUST pass with zero errors.
7. Zero runtime dependencies.

You can verify invariant 1 at any time with `python -m hello_world | od -c`.

## Code Style

- Every module and function MUST have a Google-style docstring with `Returns:` and `Example:` sections.
- Every function MUST be fully type-annotated.
- Every module MUST start with `from __future__ import annotations`.
- Every public module MUST declare `__all__`, sorted.
- `print()` is allowed ONLY in `main()`, with its `# noqa: T201` justification comment (ADR-0008).
- Comments should explain *why*, not *what*.
- Source files MUST be ASCII-only, with no trailing whitespace.
- Line length: 100.

## Testing Rules

- Every change MUST come with tests. No exceptions.
- Every bug fix MUST come with a regression test in `tests/regression/test_known_issues.py`, named `test_issue_<number>_<description>` with a docstring referencing the issue.
- NEVER delete or weaken a regression, conformance or security test.
- Properties of the greeting must be tested on **every surface** using the `greeting` fixture from `tests/conftest.py` (`greet()`, `GREETING` and the stdout of `main()`).
- Use the helpers in `tests/helpers.py` (`run_hello_world`, `patched_environ`). Do NOT use `unittest.mock`.
- Hypothesis tests MUST NOT use function-scoped fixtures (`monkeypatch`, `capsys`...). Use `patched_environ` and `contextlib.redirect_stdout` instead.
- Never write raw invisible characters in test files. Always use escape sequences (`"‮"`).
- The full suite must stay under 10 seconds.

## Common Pitfalls

- **Do NOT inline `greet()` into `main()`.** The separation between composition and output is intentional (ADR-0003).
- **Do NOT replace `print()` with `sys.stdout.write()`.** It requires manual newline handling, which caused #73 (ADR-0008).
- Do NOT add argument parsing. `main()` takes no arguments and ignores `sys.argv` by design.
- Do NOT add a second occurrence of the greeting string in `src/`. Reference `GREETING` instead.
- Do NOT remove the space after the comma (#42), nor add one before the exclamation mark (#57).
- Do NOT add `print(greet() + "\n")`: `print()` already appends a newline (#73).

## Workflow

1. Read the relevant ADRs in `docs/adr/` before any change to `src/`.
2. For any design change, write a new ADR first (use `/new-adr` or `docs/adr/0000-template.md`).
3. Implement the change with tests.
4. Update `CHANGELOG.md` under `[Unreleased]` (Keep a Changelog format).
5. Run `make check`. All checks MUST pass before you report the task as done.
6. Use Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).

## Claude Code Configuration

- Slash commands live in `.claude/commands/` (`/verify-greeting`, `/review`, `/release`, `/add-regression-test`, `/new-adr`).
- Subagents live in `.claude/agents/` (`greeting-integrity-reviewer`, `test-engineer`, `architecture-guardian`).
- A PostToolUse hook formats Python files after every edit, and a Stop hook verifies the output before you finish.
- Editing `src/hello_world/hello_world.py` requires explicit approval (see `.claude/settings.json`).

## When in Doubt

Ask before changing `src/`. Prefer consistency with existing patterns over novelty.
