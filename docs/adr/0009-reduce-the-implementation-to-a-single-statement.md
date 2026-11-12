# ADR-0009: Reduce the implementation to a single statement

- **Status:** Accepted
- **Date:** 2026-11-12
- **Deciders:** @maintainers
- **Supersedes:** [ADR-0003](0003-separate-greeting-composition-from-output.md), [ADR-0006](0006-define-the-greeting-as-a-module-level-constant.md)

## Context

As of version 2.3.1, the core module contained 15 statements: a constant (`GREETING`), a pure function (`greet()`), an output function (`main()`), an `if __name__ == "__main__":` guard, an `__all__` declaration and their imports.

A review of the codebase against its actual usage showed that:

- `greet()` had exactly one caller: `main()`.
- `GREETING` had exactly one reader: `greet()`.
- No downstream consumer of the Python API (`greet()`, `main()`, `GREETING`) has ever been identified.
- Each statement had to be documented, type-checked, linted and covered by tests, which made it a maintenance liability rather than an asset.
- The byte-exact output contract is verified through stdout by the conformance, security and end-to-end test suites. None of these guarantees relied on the internal structure of the module.

In other words, the abstractions introduced by ADR-0003 and ADR-0006 provided indirection without any consumer (YAGNI).

## Decision

The core module, `src/hello_world/hello_world.py`, will contain **exactly one statement**:

```python
print("Hello, World!")
```

- The module is documented exclusively with comments. A module docstring is an expression statement, and would therefore violate this decision.
- `__main__.py` executes the core module with `runpy.run_module()`, rather than importing it, so that the greeting is printed on every invocation, even if the module has already been imported.
- The package `__init__.py` does not import the core module, so that importing the package remains free of side effects (#95).
- The `hello-world` console script is removed, as console script entry points require a callable.

This decision is enforced by `tests/unit/test_hello_world_module.py`, which parses the source code and verifies its structure statement by statement.

## Alternatives Considered

### Keep the functional core / imperative shell (ADR-0003)

- **Pros:** The greeting can be tested without capturing stdout. A Python API is available for reuse.
- **Cons:** No consumer of the API exists. The output must be tested through stdout regardless, as it is the actual contract.

### `sys.stdout.write("Hello, World!\n")`

- **Pros:** Explicit about the destination.
- **Cons:** Requires an import, hence two statements. Manual newline handling caused #73 (see ADR-0008).

### `__import__("sys").stdout.write("Hello, World!\n")`

- **Pros:** A single statement, without `print()`.
- **Cons:** Unreadable. Manual newline handling (#73).

## Consequences

### Positive

- The entire implementation can be read in a single line.
- The number of statements drops from 15 to 1.
- The module has no state, no function and no class. Thread safety is guaranteed by construction.
- The test suite required almost no change to its assertions, which confirms that it verifies behavior rather than implementation details.

### Negative

- Breaking change for users of `greet()`, `main()` and `GREETING`. A [migration guide](../migration/v2-to-v3.md) is provided.
- The `hello-world` console script is no longer available. Use `python -m hello_world`.
- Importing `hello_world.hello_world` directly prints the greeting. This is documented and mitigated by the package `__init__.py`.

### Neutral

- Released as version 3.0.0, following Semantic Versioning.
- The single statement still relies on `print()`, in accordance with ADR-0008.
