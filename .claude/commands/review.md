---
description: Review the current changes against the project invariants and conventions
argument-hint: "[optional focus area]"
allowed-tools: Bash(git status), Bash(git diff:*), Bash(git log:*), Bash(make check)
---

Review the current changes (`git diff` and `git diff --cached`). Focus area: $ARGUMENTS

Check every item below and report findings grouped by severity (🔴 blocking, 🟠 major, 🟡 minor, 🔵 nit).

## Invariants (blocking)

- [ ] The output is still exactly `Hello, World!\n` on stdout, with nothing on stderr.
- [ ] `src/hello_world/hello_world.py` still contains exactly one statement: `print("Hello, World!")`.
- [ ] Importing the `hello_world` package still prints nothing.
- [ ] No new module was added to `src/`.
- [ ] No runtime dependency was added.

## Quality

- [ ] Every new or modified function has a Google-style docstring with `Returns:` and `Example:` sections.
- [ ] Every new or modified function is fully type-annotated.
- [ ] Comments explain *why*, not *what*.
- [ ] Every change is covered by tests, and coverage remains at 100%.
- [ ] Bug fixes include a regression test referencing the issue number.
- [ ] No regression, conformance or security test was deleted or weakened.

## Documentation

- [ ] `CHANGELOG.md` is updated under `[Unreleased]`.
- [ ] An ADR was added for any design change.
- [ ] `README.md`, `CLAUDE.md` and `AGENTS.md` are consistent with the change.

Finish by running `make check` and include the summary line in your report.
