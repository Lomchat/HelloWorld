# GitHub Copilot Instructions

Please follow the guidelines in [CLAUDE.md](../CLAUDE.md) and [AGENTS.md](../AGENTS.md). They apply to every AI coding assistant working on this repository.

Most important rules:

- The output MUST remain exactly `Hello, World!\n`.
- Do not create new modules in `src/` (ADR-0004).
- The core module must contain exactly one statement: `print("Hello, World!")` (ADR-0009).
- Every change requires tests. Coverage must remain at 100%.
- Run `make check` before proposing a change.
