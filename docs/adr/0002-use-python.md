# ADR-0002: Use Python

- **Status:** Accepted
- **Date:** 2026-09-15
- **Deciders:** @maintainers

## Context

We need to choose an implementation language for the Hello World application. The language must be widely available, easy to read, well-tooled for testing and static analysis, and suitable for command-line applications.

## Decision

We will implement the application in Python, targeting Python 3.10 and later, with full type annotations checked by mypy in strict mode.

## Alternatives Considered

### C

- **Pros:** Historical reference implementation (Kernighan & Ritchie). Minimal runtime overhead.
- **Cons:** Manual memory management, weaker testing ecosystem, no built-in packaging story.

### Rust

- **Pros:** Memory safety, excellent tooling, single static binary.
- **Cons:** Compilation step, steeper learning curve for contributors, longer build times in CI.

### Bash

- **Pros:** Available everywhere, no installation required.
- **Cons:** No type system, limited testability, error-prone quoting rules.

## Consequences

### Positive

- First-class testing tools: pytest, Hypothesis, coverage.py.
- Static guarantees through mypy `--strict`.
- Distribution through PyPI and a console script.

### Negative

- Interpreter cold start (~20 ms) is slower than a native binary. A performance budget test guards against regressions.

### Neutral

- Python 3.10 is the minimum version, to allow modern typing syntax.
