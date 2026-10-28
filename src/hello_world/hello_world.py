"""Core implementation of the Hello World application.

This module contains the complete business logic of the application and
exposes a small, stable public API:

* :data:`GREETING`: the canonical greeting, defined once as the single source
  of truth (see ADR-0006);
* :func:`greet`: returns the greeting, without any side effect;
* :func:`main`: prints the greeting to standard output and returns an exit
  code.

Separating the composition of the greeting (:func:`greet`) from its output
(:func:`main`) keeps the core logic pure and easy to test (see ADR-0003).

Example:
    >>> greet()
    'Hello, World!'
"""

from __future__ import annotations

from typing import Final

__all__ = ["GREETING", "greet", "main"]

# The canonical greeting displayed by the application.
# IMPORTANT: This value is part of the public contract of the application.
# Any change MUST be reflected in the conformance test suite (tests/conformance/).
GREETING: Final[str] = "Hello, World!"


def greet() -> str:
    """Return the canonical greeting.

    This function is pure: it has no side effects and always returns the same
    value, which makes it safe to call from any context.

    Returns:
        The canonical greeting, ``"Hello, World!"``.

    Example:
        >>> greet()
        'Hello, World!'
    """
    # Return the greeting.
    return GREETING


def main() -> int:
    """Print the greeting to standard output.

    This is the main entry point of the application. It is invoked by the
    ``hello-world`` console script and by ``python -m hello_world``.

    Returns:
        The process exit code. ``0`` indicates success.

    Example:
        >>> main()
        Hello, World!
        0
    """
    # Print the greeting to standard output.
    print(greet() + "\n")  # noqa: T201 - Printing the greeting is the purpose of this application.

    # Return 0 to indicate successful execution.
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised by the end-to-end suite
    # Propagate the exit code to the operating system.
    raise SystemExit(main())
