# ADR-0003: Separate greeting composition from output

- **Status:** Superseded by [ADR-0009](0009-reduce-the-implementation-to-a-single-statement.md)
- **Date:** 2026-10-06
- **Deciders:** @maintainers
- **Related issues:** #95

## Context

Up to version 1.1.1, `greet()` both built the greeting and printed it. This coupling caused several problems:

- The greeting could not be reused programmatically (e.g. embedded in another string, logged or sent over the network).
- Testing the greeting required capturing stdout, which made tests slower and more complex.
- Calling `greet()` from a library had an unexpected side effect (#95).

## Decision

We will separate the **composition** of the greeting from its **output**:

- `greet() -> str` returns the greeting and has no side effect.
- `main() -> int` obtains the greeting from `greet()`, prints it and returns the exit code.

`main()` MUST call `greet()` rather than reference `GREETING` directly, so that the output always goes through the public composition API.

## Alternatives Considered

### Keep a single function that prints

- **Pros:** Fewer lines of code.
- **Cons:** Mixes pure logic and I/O, hard to test, side effect on every call (#95).

### Single `print("Hello, World!")` statement at module level

- **Pros:** Shortest possible implementation.
- **Cons:** Prints on import, cannot be tested without subprocesses, cannot be reused, provides no entry point for the console script, no exit code.

### Return the greeting from `main()` and print it in `__main__.py`

- **Pros:** `main()` becomes pure.
- **Cons:** The console script would no longer print anything, as `console_scripts` entry points only use the return value as the exit code.

## Consequences

### Positive

- `greet()` is pure and trivially testable.
- `main()` is a thin I/O shell, following the "functional core, imperative shell" pattern.
- The greeting can be reused by other applications.

### Negative

- Breaking change for users relying on `greet()` printing the greeting. A [migration guide](../migration/v1-to-v2.md) is provided.

### Neutral

- Released as version 2.0.0, following Semantic Versioning.
