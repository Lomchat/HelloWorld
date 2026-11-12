# Testing Strategy

The output of hello-world is a public, byte-exact contract. Our testing strategy is designed to guarantee that this contract is never broken, from every angle: functional, structural, security, robustness and performance.

## Principles

1. **Every entry point is tested.** Properties of the greeting are verified through `python -m hello_world`, through the core module executed as a module, and through the core module executed as a script, using the parametrized `greeting` fixture.
2. **Behavior over implementation.** The suite verifies what the program prints. This is why it survived the reduction of the implementation to a single statement (ADR-0009) almost unchanged.
3. **Structure is verified too.** The source of the core module is parsed with `ast` to guarantee that it contains exactly one statement.
4. **Tests are hermetic and fast.** No network, no sleeping, no dependency on the environment. The full suite runs in about 2 seconds.
5. **Regression tests are forever.** A fixed bug gets a test, and that test is never deleted.
6. **Coverage is necessary, not sufficient.** 100% coverage is enforced ([ADR-0007](adr/0007-enforce-full-test-coverage.md)), and complemented by property-based, conformance and security tests.

## Test pyramid

```text
                 ▲
                / \          e2e (19)
               /   \         real subprocess, interpreter flags, environments
              /─────\
             /       \       integration (7)
            /         \      entry points, in-process
           /───────────\
          /             \    unit (77)
         /               \   behavior and structure of the core module, packaging
        /─────────────────\
       /                   \ conformance (127) · security (177) · regression (11)
      /                     \ property (5) · concurrency (3) · performance (3)
     ───────────────────────
```

## Categories

| Category      | Marker        | Tests | What it guarantees                                                                 |
| ------------- | ------------- | ----: | ---------------------------------------------------------------------------------- |
| Security      | `security`    |   177 | No injection vector or control character in the output; environment isolation     |
| Conformance   | `conformance` |   127 | Every character, every byte, structure, encoding and fingerprints of the output    |
| Unit          | `unit`        |    77 | Behavior, AST structure and documentation of the core module; packaging            |
| End-to-end    | `e2e`         |    19 | Real executable, under various interpreter flags and environments                  |
| Regression    | `regression`  |    11 | Previously fixed bugs (#42, #51, #57, #64, #73, #88, #95)                          |
| Integration   | `integration` |     7 | Entry points and absence of import side effects, in-process                        |
| Property      | `property`    |     5 | Stability under arbitrary executions, environments, seeds and arguments            |
| Performance   | `performance` |     3 | Latency budgets                                                                    |
| Concurrency   | `concurrency` |     3 | Thread and process safety                                                          |
| **Total**     |               | **429** |                                                                                  |

## Running the tests

```bash
make test                          # full suite
make coverage                      # with coverage (fails under 100%)
.venv/bin/pytest -m security       # a single category
.venv/bin/pytest -m "not e2e"      # skip subprocess-based tests
HYPOTHESIS_PROFILE=ci make test    # explore 300 examples per property
```

## Fixtures and helpers

| Name                | Location            | Purpose                                                          |
| ------------------- | ------------------- | ---------------------------------------------------------------- |
| `greeting`          | `tests/conftest.py` | The greeting, as printed through each in-process entry point     |
| `stdout_text`       | `tests/conftest.py` | The text written to stdout by `python -m hello_world`            |
| `stdout_bytes`      | `tests/conftest.py` | The raw bytes written to stdout by `python -m hello_world`       |
| `run_in_process()`  | `tests/helpers.py`  | Executes an entry point in-process and returns its output        |
| `run_hello_world()` | `tests/helpers.py`  | Runs the application in a subprocess                             |
| `patched_environ()` | `tests/helpers.py`  | Temporarily patches `os.environ` (Hypothesis-compatible)         |

## Adding a test

1. Pick the category using the table above.
2. Reuse the existing fixtures and helpers.
3. For any property of the output, use the `greeting` fixture so that it runs through every entry point.
4. Never import `hello_world.hello_world` directly: use `run_in_process()`.
5. For a bug fix, use the `/add-regression-test` command.
6. Run `make check`.
