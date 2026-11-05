# ADR-0008: Use `print()` for output

- **Status:** Accepted
- **Date:** 2026-11-05
- **Deciders:** @maintainers
- **Related issues:** #73

## Context

`main()` must write the greeting, followed by a single line feed, to standard output. Python offers several ways to do so. In version 2.3.0, `main()` called `print(greet() + "\n")`, which produced two line feeds (#73). The fix prompted a review of the available options.

## Decision

We will use the built-in `print()` function, with its default arguments:

```python
print(greet())
```

`print()` is the only place in `src/` where output is produced. The corresponding Ruff rule (`T201`) is suppressed on that single line, with an inline justification.

## Alternatives Considered

### `sys.stdout.write(greet() + "\n")`

- **Pros:** Explicit about the destination and the line terminator.
- **Cons:** Requires manual newline handling, which is exactly what caused #73. Requires importing `sys`.

### `logging`

- **Pros:** Configurable handlers and levels.
- **Cons:** Logs go to stderr by default and include metadata. Logging is meant for diagnostics, not program output.

### `os.write(1, ...)`

- **Pros:** Bypasses Python buffering.
- **Cons:** Low-level, bytes-only, ignores `sys.stdout` redirections (which breaks `contextlib.redirect_stdout` and pytest's `capsys`).

## Consequences

### Positive

- Idiomatic, readable and impossible to get the line terminator wrong.
- Honors `sys.stdout` redirections, which keeps `main()` testable in-process.

### Negative

- A `noqa` comment is required to satisfy the linter.

### Neutral

- The trailing line feed is verified byte by byte by the conformance test suite.
