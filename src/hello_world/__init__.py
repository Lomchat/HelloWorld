"""Hello World: a robust, production-ready greeting application.

This package exposes the public API of the application. All implementation
details live in :mod:`hello_world.hello_world`.

Example:
    >>> from hello_world import greet
    >>> greet()
    'Hello, World!'
"""

from __future__ import annotations

from hello_world.hello_world import GREETING, greet, main

# The package version, following Semantic Versioning 2.0.0 (https://semver.org).
# This is the single source of truth, read by the build backend (see pyproject.toml).
__version__ = "2.1.0"

__all__ = ["GREETING", "__version__", "greet", "main"]
