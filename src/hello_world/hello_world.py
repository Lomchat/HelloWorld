"""Core implementation of the Hello World application."""

from __future__ import annotations

__all__ = ["greet"]


def greet() -> None:
    """Print the greeting to standard output.

    Example:
        >>> greet()
        Hello World!
    """
    # Print the greeting to standard output.
    print("Hello World!")
