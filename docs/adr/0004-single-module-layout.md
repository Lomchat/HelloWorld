# ADR-0004: Single-module layout

- **Status:** Accepted
- **Date:** 2026-10-06
- **Deciders:** @maintainers

## Context

With the introduction of `main()` (ADR-0003), we evaluated how the source code should be organized. Several layouts were proposed during the design review, ranging from a single module to a layered architecture with dedicated modules for configuration, composition, output and error handling.

## Decision

We will keep the entire implementation in a single module, `src/hello_world/hello_world.py`. The package contains only:

- `__init__.py`: re-exports the public API and defines `__version__`;
- `__main__.py`: enables `python -m hello_world`;
- `hello_world.py`: the implementation.

This layout is enforced by `tests/unit/test_package.py::TestPackaging::test_source_tree_contains_only_the_expected_modules`.

## Alternatives Considered

### Layered architecture (ports and adapters)

Separate modules for the domain (`core/`), output adapters (`output/`), configuration (`config.py`), validation, exceptions and a composition root.

- **Pros:** Highly extensible. Each concern is isolated. Output destinations can be swapped through dependency injection.
- **Cons:** Around 400 statements and 20 modules for a single line of output. Significant indirection. Extensibility that no current requirement calls for (YAGNI).

### Flat module at the root of `src/` (no package)

- **Pros:** Even simpler.
- **Cons:** No `python -m hello_world` support, no room for `py.typed`, non-standard layout.

## Consequences

### Positive

- The whole implementation can be read in under a minute.
- No indirection between the entry point and the output.

### Negative

- Future features (see ADR-0005) may require revisiting this decision.

### Neutral

- This decision will be re-evaluated if `hello_world.py` exceeds 500 lines.
