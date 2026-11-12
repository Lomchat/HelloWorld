# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Internationalization support (deferred, see [ADR-0005](docs/adr/0005-defer-internationalization.md)).
- Re-evaluate the single-module layout once `hello_world.py` exceeds 500 lines (see [ADR-0004](docs/adr/0004-single-module-layout.md)).

## [3.0.0] - 2026-11-12

### Changed

- **BREAKING:** The implementation has been reduced to a single statement, `print("Hello, World!")` (see [ADR-0009](docs/adr/0009-reduce-the-implementation-to-a-single-statement.md)). See the [migration guide](docs/migration/v2-to-v3.md).
- The core module is now documented exclusively with comments, as a module docstring would count as a second statement.
- `python -m hello_world` now executes the core module with `runpy`, so that the greeting is printed on every invocation.
- Importing the `hello_world` package no longer imports the core module, and therefore remains free of side effects ([#95]).

### Removed

- **BREAKING:** `greet()`, `main()` and `GREETING`.
- **BREAKING:** The `hello-world` console script. Use `python -m hello_world` instead.
- Doctests, as the source code no longer contains any docstring example.

## [2.3.1] - 2026-11-07

### Fixed

- Fixed a double newline at the end of the output: `main()` called `print(greet() + "\n")` ([#73]).

## [2.3.0] - 2026-10-30

### Added

- Property-based test suite powered by Hypothesis.
- Thread-safety test suite.
- Performance budget test suite.
- Multi-stage `Dockerfile` running as a non-root user, with a health check.
- `make bench` target and `benchmarks/` directory.

### Changed

- Raised the minimum coverage threshold from 95% to 100% (see [ADR-0007](docs/adr/0007-enforce-full-test-coverage.md)).

## [2.2.0] - 2026-10-23

### Security

- Added a security test suite verifying that the output is free of 22 known terminal injection vectors and of every C0 control character.
- Added environment isolation tests guaranteeing that the output cannot be influenced by locale, terminal or color settings.

### Added

- Byte-exact conformance test suite, including MD5, SHA-1, SHA-256 and CRC32 fingerprints and a snapshot of the canonical output.

## [2.1.0] - 2026-10-16

### Added

- `GREETING` module-level constant, annotated as `Final[str]`, as the single source of truth for the greeting (see [ADR-0006](docs/adr/0006-define-the-greeting-as-a-module-level-constant.md)).
- Explicit `__all__` declarations in every public module.

### Changed

- `greet()` now returns `GREETING` instead of a string literal.

### Fixed

- A diverging copy of the greeting literal produced a duplicated exclamation mark ([#88]).

## [2.0.1] - 2026-10-10

### Fixed

- `main()` now returns `0` instead of `None`, so that `raise SystemExit(main())` reports success unambiguously ([#51]).

## [2.0.0] - 2026-10-08

### Added

- `main()`, the new entry point of the application, which prints the greeting.

### Changed

- **BREAKING:** `greet()` now returns the greeting instead of printing it ([#95], see [ADR-0003](docs/adr/0003-separate-greeting-composition-from-output.md)). See the [migration guide](docs/migration/v1-to-v2.md).
- **BREAKING:** The `hello-world` console script now points to `hello_world.hello_world:main`.

## [1.1.1] - 2026-09-29

### Fixed

- Removed the space before the exclamation mark: the greeting was rendered as `Hello, World !` ([#57]).
- The `__main__` module now propagates the exit code ([#64]).

## [1.1.0] - 2026-09-25

### Added

- Support for `python -m hello_world` through a `__main__.py` module ([#64]).
- `hello-world` console script.

## [1.0.1] - 2026-09-22

### Fixed

- Restored the comma between `Hello` and `World` ([#42]).
- Restored the space after the comma, which went missing in the first fix for [#42].

## [1.0.0] - 2026-09-18

### Added

- First stable release.
- `greet()` public function.
- Full type annotations and `py.typed` marker (PEP 561).

## [0.1.0] - 2026-09-15

### Added

- Initial proof of concept.

[Unreleased]: https://github.com/Lomchat/HelloWorld/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/Lomchat/HelloWorld/compare/v2.3.1...v3.0.0
[2.3.1]: https://github.com/Lomchat/HelloWorld/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/Lomchat/HelloWorld/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/Lomchat/HelloWorld/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/Lomchat/HelloWorld/compare/v2.0.1...v2.1.0
[2.0.1]: https://github.com/Lomchat/HelloWorld/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/Lomchat/HelloWorld/compare/v1.1.1...v2.0.0
[1.1.1]: https://github.com/Lomchat/HelloWorld/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/Lomchat/HelloWorld/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/Lomchat/HelloWorld/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/Lomchat/HelloWorld/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/Lomchat/HelloWorld/releases/tag/v0.1.0
[#42]: https://github.com/Lomchat/HelloWorld/issues/42
[#51]: https://github.com/Lomchat/HelloWorld/issues/51
[#57]: https://github.com/Lomchat/HelloWorld/issues/57
[#64]: https://github.com/Lomchat/HelloWorld/issues/64
[#73]: https://github.com/Lomchat/HelloWorld/issues/73
[#88]: https://github.com/Lomchat/HelloWorld/issues/88
[#95]: https://github.com/Lomchat/HelloWorld/issues/95
