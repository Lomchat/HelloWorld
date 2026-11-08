# Testing Strategy

The output of hello-world is a public, byte-exact contract. Our testing strategy is designed to guarantee that this contract is never broken, from every angle: functional, structural, security, robustness and performance.

## Principles

1. **Every surface is tested.** Properties of the greeting are verified on `greet()`, on `GREETING` and on the stdout of `main()`, through the parametrized `greeting` fixture.
2. **Tests are hermetic.** No network, no sleeping, no dependency on the environment.
3. **Tests are fast.** The full suite runs in about 1.5 seconds.
4. **Regression tests are forever.** A fixed bug gets a test, and that test is never deleted.
5. **Coverage is necessary, not sufficient.** 100% coverage is enforced ([ADR-0007](adr/0007-enforce-full-test-coverage.md)), and complemented by property-based, conformance and security tests.

## Test pyramid

```text
                 ▲
                / \          e2e (19)
               /   \         real subprocess, interpreter flags, environments
              /─────\
             /       \       integration (6)
            /         \      entry points, in-process
           /───────────\
          /             \    unit (86) + doctests (4)
         /               \   greet(), main(), GREETING, packaging
        /─────────────────\
       /                   \ conformance (127) · security (177) · regression (10)
      /                     \ property (5) · concurrency (3) · performance (3)
     ───────────────────────
```

## Categories

| Category      | Marker        | Tests | What it guarantees                                                                 |
| ------------- | ------------- | ----: | ---------------------------------------------------------------------------------- |
| Security      | `security`    |   177 | No injection vector or control character in the output; environment isolation     |
| Conformance   | `conformance` |   127 | Every character, every byte, structure, encoding and fingerprints of the output    |
| Unit          | `unit`        |    86 | Behavior, signature and documentation of `greet()`, `main()` and `GREETING`       |
| End-to-end    | `e2e`         |    19 | Real executable, under various interpreter flags and environments                  |
| Regression    | `regression`  |    10 | Previously fixed bugs (#42, #51, #57, #64, #73, #88, #95)                          |
| Integration   | `integration` |     6 | `python -m`, script execution and import side effects, in-process                  |
| Property      | `property`    |     5 | Stability under arbitrary call counts, environments, seeds and arguments           |
| Doctests      | n/a           |     4 | Examples in docstrings                                                             |
| Performance   | `performance` |     3 | Latency budgets                                                                    |
| Concurrency   | `concurrency` |     3 | Thread safety                                                                      |
| **Total**     |               | **440** |                                                                                  |

## Running the tests

```bash
make test                          # full suite
make coverage                      # with coverage (fails under 100%)
.venv/bin/pytest -m security       # a single category
.venv/bin/pytest -m "not e2e"      # skip subprocess-based tests
HYPOTHESIS_PROFILE=ci make test    # explore 300 examples per property
```

## Fixtures and helpers

| Name                | Location            | Purpose                                                       |
| ------------------- | ------------------- | ------------------------------------------------------------- |
| `greeting`          | `tests/conftest.py` | The greeting, as observed through each public surface          |
| `stdout_text`       | `tests/conftest.py` | The text written to stdout by `main()`                        |
| `stdout_bytes`      | `tests/conftest.py` | The raw bytes written to stdout by `main()`                   |
| `run_hello_world()` | `tests/helpers.py`  | Runs the application in a subprocess                          |
| `patched_environ()` | `tests/helpers.py`  | Temporarily patches `os.environ` (Hypothesis-compatible)      |

## Adding a test

1. Pick the category using the table above.
2. Reuse the existing fixtures and helpers.
3. For any property of the output, use the `greeting` fixture so that it runs on every surface.
4. For a bug fix, use the `/add-regression-test` command.
5. Run `make check`.
