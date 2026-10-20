# Contributing to Hello World

First of all, thank you for taking the time to contribute! 🎉

This document describes how to set up your environment, our conventions, and the process for submitting changes. Please read it in full before opening a pull request.

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [Development Workflow](#-development-workflow)
- [Coding Standards](#-coding-standards)
- [Testing Requirements](#-testing-requirements)
- [Commit Messages](#-commit-messages)
- [Pull Request Process](#-pull-request-process)
- [Architecture Decisions](#-architecture-decisions)

## 🤝 Code of Conduct

This project adheres to the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later
- GNU Make
- Git

### Setup

```bash
git clone https://github.com/Lomchat/HelloWorld.git
cd HelloWorld
make install   # creates .venv and installs dev dependencies
make hooks     # installs the pre-commit hooks
make check     # verifies that everything works
```

## 🔄 Development Workflow

1. Open an issue to discuss the change before starting to work on it.
2. Fork the repository and create a branch from `main`:
   - `feat/<short-description>` for new features
   - `fix/<issue-number>-<short-description>` for bug fixes
   - `docs/<short-description>` for documentation
3. Make your changes, with tests.
4. Run `make check`.
5. Update `CHANGELOG.md` under `[Unreleased]`.
6. Open a pull request.

## 🎨 Coding Standards

- **Formatting and linting:** [Ruff](https://docs.astral.sh/ruff/), configured in `pyproject.toml`. Run `make format`.
- **Type checking:** [mypy](https://mypy.readthedocs.io/) in strict mode. Run `make typecheck`.
- **Docstrings:** Google style, with `Returns:` and `Example:` sections, for every module and function.
- **Layout:** the implementation lives in `src/hello_world/hello_world.py`. Do not add new modules (see [ADR-0004](docs/adr/0004-single-module-layout.md)).
- **Dependencies:** no runtime dependency may be added.

## 🧪 Testing Requirements

- Every change must be covered by tests. Coverage must remain at **100%**.
- Every bug fix must include a regression test in `tests/regression/`, referencing the issue number.
- Regression, conformance and security tests must never be deleted or weakened.
- The full suite must run in under 10 seconds.

See the [Testing Strategy](docs/testing-strategy.md) for details on test categories and fixtures.

## 📝 Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

| Type       | Usage                                            |
| ---------- | ------------------------------------------------ |
| `feat`     | A new feature                                    |
| `fix`      | A bug fix                                        |
| `docs`     | Documentation only                               |
| `test`     | Adding or updating tests                         |
| `refactor` | A change that neither fixes a bug nor adds a feature |
| `perf`     | A performance improvement                        |
| `build`    | Build system or dependencies                     |
| `ci`       | CI configuration                                 |
| `chore`    | Maintenance tasks                                |

Breaking changes must include `BREAKING CHANGE:` in the footer, or a `!` after the type (e.g. `feat!:`).

## 🔍 Pull Request Process

1. Fill in the pull request template completely.
2. Make sure all CI checks pass.
3. At least one approval from a maintainer is required. Changes to `src/hello_world/hello_world.py` require an approval from the code owners (see `.github/CODEOWNERS`).
4. Pull requests are merged using squash merge.

### Definition of Done

- [ ] `make check` passes
- [ ] Coverage is 100%
- [ ] Tests added for the change
- [ ] `CHANGELOG.md` updated
- [ ] Documentation updated
- [ ] ADR written, if the change affects the architecture

## 🏛️ Architecture Decisions

Significant design changes require an [Architecture Decision Record](docs/adr/). Use the template in [`docs/adr/0000-template.md`](docs/adr/0000-template.md) and submit the ADR in its own pull request, before the implementation.

---

Thank you for helping make Hello World better! 💙
