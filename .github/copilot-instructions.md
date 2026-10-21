# GitHub Copilot Instructions

Please follow the guidelines in [CLAUDE.md](../CLAUDE.md) and [AGENTS.md](../AGENTS.md). They apply to every AI coding assistant working on this repository.

Most important rules:

- The output MUST remain exactly `Hello, World!\n`.
- Do not create new modules in `src/` (ADR-0004).
- Do not inline `greet()` into `main()` (ADR-0003).
- Every change requires tests. Coverage must remain at 100%.
- Run `make check` before proposing a change.
