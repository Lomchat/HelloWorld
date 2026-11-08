<div align="center">

# 🌍 Hello World

**A robust, production-ready Hello World application for Python.**

[![CI](https://github.com/Lomchat/HelloWorld/actions/workflows/ci.yml/badge.svg)](https://github.com/Lomchat/HelloWorld/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](docs/testing-strategy.md)
[![Tests](https://img.shields.io/badge/tests-440%20passing-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](pyproject.toml)
[![Typed: mypy --strict](https://img.shields.io/badge/typed-mypy%20--strict-blue)](https://mypy.readthedocs.io/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Dependencies: 0](https://img.shields.io/badge/runtime%20dependencies-0-success)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

[Features](#-features) •
[Quick Start](#-quick-start) •
[Architecture](#️-architecture) •
[Testing](#-testing) •
[FAQ](#-faq) •
[Contributing](#-contributing)

</div>

---

## 📖 Overview

**Hello World** is a modern, production-grade implementation of the canonical
"Hello, World!" program. Built on clean code principles, it provides a solid,
battle-tested foundation for greeting the world reliably, securely and
consistently, on every platform.

```console
$ hello-world
Hello, World!
```

## ✨ Features

- 🎯 **Separation of Concerns**: greeting composition (`greet()`) is fully decoupled from output (`main()`).
- 🧱 **Single Source of Truth**: the greeting is defined exactly once, as a `Final` constant.
- 🧪 **Thoroughly Tested**: 440 tests across 10 categories, 100% line and branch coverage.
- 🛡️ **Secure by Design**: output verified against 22 terminal injection vectors and every control character.
- 🔒 **Hermetic**: output is guaranteed to be independent of locale, terminal settings, environment variables and command-line arguments.
- 🔍 **Fully Typed**: passes `mypy --strict` and ships a `py.typed` marker.
- ⚡ **Fast**: under 10 µs per greeting, with performance budgets enforced in CI.
- 🧵 **Thread-Safe**: `greet()` is pure and returns an immutable value.
- 📦 **Zero Runtime Dependencies**: only the Python standard library.
- 🐳 **Container Ready**: multi-stage, non-root Docker image with a health check.
- 📚 **Documented Decisions**: every design choice is recorded in an [ADR](docs/adr/).

## 🚀 Quick Start

### Requirements

- Python 3.10 or later

### Installation

```bash
pip install git+https://github.com/Lomchat/HelloWorld.git
```

Or from source:

```bash
git clone https://github.com/Lomchat/HelloWorld.git
cd HelloWorld
make install
```

### Command line

```console
$ hello-world
Hello, World!

$ python -m hello_world
Hello, World!
```

### Python API

```python
from hello_world import greet

greeting = greet()  # "Hello, World!"
```

`greet()` is pure: it never writes to stdout and always returns the same value,
which makes it safe to call from any context.

To print the greeting from your own code, use `main()`:

```python
from hello_world import main

exit_code = main()  # prints "Hello, World!" and returns 0
```

### Docker

```bash
docker build -t hello-world .
docker run --rm hello-world
```

## 📚 API Reference

| Symbol                  | Type         | Description                                                       |
| ----------------------- | ------------ | ----------------------------------------------------------------- |
| `GREETING`              | `Final[str]` | The canonical greeting, `"Hello, World!"`.                        |
| `greet()`               | `() -> str`  | Returns the greeting. Pure, no side effects.                      |
| `main()`                | `() -> int`  | Prints the greeting to stdout and returns the exit code (`0`).    |
| `__version__`           | `str`        | The package version, following Semantic Versioning.               |

### Exit codes

| Code | Meaning                     |
| ---- | --------------------------- |
| `0`  | The greeting was printed.   |

## 🏗️ Architecture

Hello World follows a deliberately simple, single-module architecture
([ADR-0004](docs/adr/0004-single-module-layout.md)), with a strict separation
between the composition of the greeting and its output
([ADR-0003](docs/adr/0003-separate-greeting-composition-from-output.md)).

```mermaid
flowchart LR
    Script["hello-world<br/>(console script)"] --> Main
    Module["python -m hello_world<br/>(__main__.py)"] --> Main
    Main["main()"] -->|composes via| Greet["greet()"]
    Greet -->|returns| Greeting[["GREETING<br/>Final[str]"]]
    Main -->|prints to| Stdout[("stdout")]
```

See [docs/architecture.md](docs/architecture.md) for a detailed walkthrough and
[docs/adr/](docs/adr/) for the reasoning behind each design decision.

## 📁 Project Structure

```text
hello-world/
├── src/hello_world/
│   ├── __init__.py          # Public API and version
│   ├── __main__.py          # `python -m hello_world` entry point
│   ├── hello_world.py       # Core implementation
│   └── py.typed             # PEP 561 marker
├── tests/                   # 440 tests (see below)
├── benchmarks/              # Micro-benchmarks
├── docs/
│   ├── adr/                 # Architecture Decision Records
│   ├── migration/           # Migration guides
│   ├── architecture.md
│   └── testing-strategy.md
├── scripts/                 # Maintenance scripts
├── .claude/                 # Claude Code configuration
└── .github/                 # CI/CD workflows and templates
```

## 🧪 Testing

```bash
make test        # run the full suite
make coverage    # run with coverage (fails under 100%)
make check       # lint + typecheck + tests, as in CI
```

| Category       | Location             | Tests   | Purpose                                         |
| -------------- | -------------------- | ------: | ----------------------------------------------- |
| Security       | `tests/security/`    |     177 | Terminal injection and environment isolation    |
| Conformance    | `tests/conformance/` |     127 | Byte-exact output contract on every surface     |
| Unit           | `tests/unit/`        |      86 | `greet()`, `main()`, `GREETING`, packaging      |
| End-to-end     | `tests/e2e/`         |      19 | Real executable in a subprocess                 |
| Regression     | `tests/regression/`  |      10 | Previously fixed bugs                           |
| Integration    | `tests/integration/` |       6 | Entry points, in-process                        |
| Property-based | `tests/property/`    |       5 | Invariants under generated conditions           |
| Doctests       | `src/`               |       4 | Examples in docstrings stay correct             |
| Performance    | `tests/performance/` |       3 | Latency budgets                                 |
| Concurrency    | `tests/concurrency/` |       3 | Thread safety                                   |
| **Total**      |                      | **440** |                                                 |

The full suite runs in about 1.5 seconds. Run a single category with its
marker, e.g. `pytest -m security`. See
[docs/testing-strategy.md](docs/testing-strategy.md) for details.

## 🗺️ Roadmap

- [x] Core greeting engine
- [x] `python -m` support
- [x] Separation of composition and output
- [x] Single source of truth for the greeting
- [x] Security and conformance test suites
- [x] 100% test coverage
- [x] Docker image
- [ ] Internationalization (see [ADR-0005](docs/adr/0005-defer-internationalization.md))
- [ ] Asynchronous API (`agreet()`)
- [ ] OpenTelemetry instrumentation

## ❓ FAQ

<details>
<summary><b>Why not simply use <code>print("Hello, World!")</code>?</b></summary>

That is essentially what `main()` does. However, keeping the composition of the
greeting (`greet()`) separate from its output (`main()`) keeps the core logic
pure, reusable and testable without capturing stdout. The rationale is detailed
in [ADR-0003](docs/adr/0003-separate-greeting-composition-from-output.md).

</details>

<details>
<summary><b>Why is everything in a single module?</b></summary>

The current scope does not justify a multi-module layout. Splitting the code
prematurely would add indirection without any benefit (YAGNI). The decision
will be revisited if the module grows beyond 500 lines. See
[ADR-0004](docs/adr/0004-single-module-layout.md).

</details>

<details>
<summary><b>Why does <code>hello-world --help</code> print the greeting?</b></summary>

The application takes no arguments by design: command-line arguments are
ignored, and the output is always the canonical greeting. This behavior is
covered by the end-to-end and property-based test suites.

</details>

<details>
<summary><b>Does it support other languages?</b></summary>

Not yet. Internationalization has been carefully evaluated and deliberately
deferred. See [ADR-0005](docs/adr/0005-defer-internationalization.md).

</details>

<details>
<summary><b>Is it thread-safe?</b></summary>

Yes. `greet()` is a pure function returning an immutable constant. Thread
safety is covered by a dedicated test suite.

</details>

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and
our [Code of Conduct](CODE_OF_CONDUCT.md) before opening a pull request.

To report a vulnerability, please follow [SECURITY.md](SECURITY.md) instead of
opening a public issue.

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Brian Kernighan, for the original `hello, world` example (1972).
- The Python community and the maintainers of pytest, Hypothesis, Ruff and mypy.
- All our [contributors](https://github.com/Lomchat/HelloWorld/graphs/contributors).

<div align="center">

Made with ❤️ by the Hello World team

</div>
