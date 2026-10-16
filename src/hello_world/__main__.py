"""Module entry point, enabling ``python -m hello_world``."""

from __future__ import annotations

from hello_world.hello_world import main

if __name__ == "__main__":  # pragma: no cover - exercised by the end-to-end suite
    # Propagate the exit code to the operating system.
    raise SystemExit(main())
