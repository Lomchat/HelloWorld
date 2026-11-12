# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`hello-world` is a production-grade Python implementation of the canonical "Hello, World!" program. The entire implementation is a single statement (ADR-0009).

- **Language:** Python 3.10+ (developed on 3.12)
- **Runtime dependencies:** none (not even an import). Keep it that way.
- **Current version:** see `__version__` in `src/hello_world/__init__.py`

## Commands

```bash
make install        # create .venv and install dev dependencies
make test           # run the full test suite
make coverage       # run tests with coverage (fails under 100%)
make lint           # ruff check + ruff format --check
make format         # auto-format with ruff
make typecheck      # mypy --strict
make check          # lint + typecheck + coverage + output verification (run this before finishing ANY task)
make bench          # run micro-benchmarks
```

Run a single test:

```bash
.venv/bin/pytest tests/unit/test_hello_world_module.py::TestStructure::test_contains_exactly_one_statement
```

Run a single category: `.venv/bin/pytest -m security` (markers: `unit`, `integration`, `e2e`, `property`, `regression`, `security`, `conformance`, `concurrency`, `performance`).

## Architecture

```
python -m hello_world ──► __main__.py ──► runpy ──┐
                                                  ├──► hello_world.py: print("Hello, World!") ──► stdout
python src/hello_world/hello_world.py ────────────┘
```

- The **entire implementation** is the single statement in `src/hello_world/hello_world.py` (ADR-0009).
- `__init__.py` only defines `__version__`. It MUST NOT import the core module (#95).
- `__main__.py` executes the core module with `runpy.run_module()`. It does not import it: a module only runs on its first import.
- **Do NOT create new modules in `src/`.** `tests/unit/test_package.py` enforces the exact list of source files (ADR-0004).
- Architectural decisions are documented in `docs/adr/`. Read them before changing anything.

## Critical Invariants

**IMPORTANT: These invariants MUST NEVER be broken. If a change would break one of them, STOP and ask.**

1. The program MUST write exactly `Hello, World!` followed by a single `\n` to stdout. Nothing else. Byte for byte. Nothing on stderr.
2. `src/hello_world/hello_world.py` MUST contain **exactly one statement**: `print("Hello, World!")`. No import, no variable, no function, no class, no docstring (ADR-0009). This is verified by parsing the source with `ast`.
3. Importing the `hello_world` package MUST NOT print anything (#95).
4. Test coverage MUST stay at **100%** (lines and branches).
5. `mypy --strict` MUST pass with zero errors.
6. Zero runtime dependencies.

You can verify invariant 1 at any time with `python -m hello_world | od -c`.

## Code Style

- The core module is documented **with comments only**. A docstring is an expression statement and would violate invariant 2.
- The core module comments MUST keep their sections: Overview, Execution, Design principles, Output contract, Security considerations, Error handling, Performance, Maintenance notes (enforced by the unit tests).
- Support modules (`__init__.py`, `__main__.py`) MUST have a docstring and start with `from __future__ import annotations`.
- `print()` is allowed ONLY in the core module, with its `# noqa: T201` justification comment (ADR-0008).
- Comments should explain *why*, not *what*.
- Source files MUST be ASCII-only, with no trailing whitespace.
- Line length: 100.

## Testing Rules

- Every change MUST come with tests. No exceptions.
- Every bug fix MUST come with a regression test in `tests/regression/test_known_issues.py`, named `test_issue_<number>_<description>` with a docstring referencing the issue.
- NEVER delete or weaken a regression, conformance or security test.
- Properties of the greeting must be tested through **every entry point** using the `greeting` fixture from `tests/conftest.py`.
- Use the helpers in `tests/helpers.py` (`run_in_process`, `run_hello_world`, `patched_environ`). Do NOT use `unittest.mock`.
- NEVER `import hello_world.hello_world` in tests: importing it executes it, and later `runpy` executions then emit a `RuntimeWarning` (treated as an error). Use `run_in_process()`.
- Hypothesis tests MUST NOT use function-scoped fixtures (`monkeypatch`, `capsys`...). Use `patched_environ` and `run_in_process` instead.
- Never write raw invisible characters in test files. Always use escape sequences (`"\u202e"`).
- The full suite must stay under 10 seconds.

## Common Pitfalls

- **Do NOT add a docstring to `hello_world.py`.** It would count as a second statement.
- **Do NOT reintroduce `greet()`, `main()` or `GREETING`** without a new ADR superseding ADR-0009.
- **Do NOT replace `print()` with `sys.stdout.write()`.** It requires an import (a second statement) and manual newline handling, which caused #73 (ADR-0008).
- Do NOT split the greeting into several arguments: `print()` inserts a space between them (#57).
- Do NOT append `"\n"` to the greeting: `print()` already terminates the line (#73).
- Do NOT import the core module from `__init__.py` (#95).
- Do NOT add argument parsing. The application ignores `sys.argv` by design.
- Do NOT remove the space after the comma (#42).

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
