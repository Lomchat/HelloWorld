# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/Lomchat/HelloWorld/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/Lomchat/HelloWorld/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/Lomchat/HelloWorld/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/Lomchat/HelloWorld/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/Lomchat/HelloWorld/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/Lomchat/HelloWorld/releases/tag/v0.1.0
[#42]: https://github.com/Lomchat/HelloWorld/issues/42
[#57]: https://github.com/Lomchat/HelloWorld/issues/57
[#64]: https://github.com/Lomchat/HelloWorld/issues/64
