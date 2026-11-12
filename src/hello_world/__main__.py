"""Module entry point, enabling ``python -m hello_world``."""

from __future__ import annotations

import runpy

if __name__ == "__main__":
    # Execute the core module rather than importing it: a module is only executed
    # on its first import, whereas this entry point must print the greeting every
    # time it runs (see ADR-0009).
    runpy.run_module("hello_world.hello_world", run_name="__main__")
