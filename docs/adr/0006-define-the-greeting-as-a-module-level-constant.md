# ADR-0006: Define the greeting as a module-level constant

- **Status:** Accepted
- **Date:** 2026-10-15
- **Deciders:** @maintainers
- **Related issues:** #88

## Context

Until version 2.0.1, the greeting was a string literal inside `greet()`. A copy of the same literal had also appeared in the docstrings, in the tests and, briefly, in `main()`. During a refactoring, one of these copies was modified independently, which led to an inconsistent greeting (#88).

## Decision

We will define the greeting exactly once, as a module-level constant:

```python
GREETING: Final[str] = "Hello, World!"
```

- `greet()` returns `GREETING`.
- `GREETING` is part of the public API and is re-exported by the package.
- `typing.Final` signals to type checkers that it must never be reassigned.
- `tests/unit/test_greeting_constant.py` verifies, by parsing the source with `ast`, that `GREETING` is assigned exactly once and that no other string literal contains the greeting.

## Alternatives Considered

### Keep the literal inside `greet()`

- **Pros:** Locality.
- **Cons:** Not reusable without calling the function. Encourages duplication (#88).

### Enum

- **Pros:** Strongly typed.
- **Cons:** `Greeting.HELLO_WORLD.value` is verbose for a single value. Enums are designed for sets of values.

### Configuration file

- **Pros:** Changeable without modifying the code.
- **Cons:** Adds I/O and failure modes to a pure function. Breaks the byte-exact output contract.

## Consequences

### Positive

- Single source of truth, verified statically by mypy and by the test suite.
- Consumers can reference `hello_world.GREETING` directly.

### Negative

- None identified.

### Neutral

- `greet()` and `GREETING` return the very same object, which is verified by the unit tests.
