"""Core implementation of the Hello World application.

This module exposes a small, stable public API:

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

__all__ = ["greet", "main"]


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
    return "Hello, World!!"


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
    print(greet())  # noqa: T201 - Printing the greeting is the purpose of this application.

    # Return 0 to indicate successful execution.
    return 0
