# ADR-0007: Enforce full test coverage

- **Status:** Accepted
- **Date:** 2026-10-27
- **Deciders:** @maintainers

## Context

The project previously required 95% line coverage. Given the size of the codebase, 95% left room for an entire function to go untested. As the output is a byte-exact public contract, any untested line is a risk.

## Decision

We will require **100% line and branch coverage**, enforced by `fail_under = 100` in `pyproject.toml` and checked on every pull request by the CI workflow.

Lines that can only be exercised in a subprocess (the `if __name__ == "__main__":` guards) are excluded from coverage measurement, and are instead covered by the end-to-end test suite.

## Alternatives Considered

### Keep the 95% threshold

- **Pros:** Less friction for contributors.
- **Cons:** Allows untested code paths in a codebase where every line matters.

### Mutation testing instead of coverage

- **Pros:** Measures test effectiveness rather than execution.
- **Cons:** Slow. Still planned as a complement, not a replacement.

## Consequences

### Positive

- Every statement and branch is executed by at least one test.
- Coverage regressions block the merge.

### Negative

- Contributors must write tests for every change, however small.

### Neutral

- Coverage is a necessary but not sufficient condition. It is complemented by conformance, security and property-based tests.
