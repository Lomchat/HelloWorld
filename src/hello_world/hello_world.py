"""Core implementation of the Hello World application."""

from __future__ import annotations

__all__ = ["greet", "main"]


def greet() -> str:
    """Return the greeting.

    Returns:
        The greeting.
    """
    # Return the greeting.
    return "Hello, World!"


def main() -> int:
    """Print the greeting to standard output.

    Returns:
        The process exit code. ``0`` indicates success.
    """
    # Print the greeting to standard output.
    print(greet())  # noqa: T201 - Printing the greeting is the purpose of this application.

    # Return 0 to indicate successful execution.
    return 0
