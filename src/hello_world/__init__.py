"""Hello World: a robust, production-ready greeting application.

The implementation lives in :mod:`hello_world.hello_world`. It is
intentionally NOT imported here: executing it prints the greeting, and
importing the package must remain free of side effects (see #95).

Run the application with ``python -m hello_world``.
"""

from __future__ import annotations

# The package version, following Semantic Versioning 2.0.0 (https://semver.org).
# This is the single source of truth, read by the build backend (see pyproject.toml).
__version__ = "3.0.0"

__all__ = ["__version__"]
