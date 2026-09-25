"""Module entry point, enabling ``python -m hello_world``."""

from __future__ import annotations

from hello_world.hello_world import greet

if __name__ == "__main__":
    greet()
