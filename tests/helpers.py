"""Shared test helpers.

Helpers are kept in a dedicated module rather than redefined in each test
file, to guarantee consistent behavior across the whole suite.
"""

from __future__ import annotations

import contextlib
import os
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping

#: Root directory of the repository.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

#: Directory containing the ``hello_world`` package.
SRC_DIR = PROJECT_ROOT / "src"

#: Path to the core module, runnable as a standalone script.
MODULE_PATH = SRC_DIR / "hello_world" / "hello_world.py"

#: The exact bytes the program must write to stdout.
EXPECTED_STDOUT = b"Hello, World!\n"


def run_hello_world(
    *args: str,
    env: Mapping[str, str] | None = None,
    interpreter_flags: tuple[str, ...] = (),
    script: bool = False,
) -> subprocess.CompletedProcess[bytes]:
    """Run the application in a subprocess.

    Args:
        *args: Command-line arguments passed to the application.
        env: Extra environment variables.
        interpreter_flags: Flags passed to the Python interpreter (e.g. ``-O``).
        script: Run ``hello_world.py`` directly instead of ``python -m hello_world``.

    Returns:
        The completed process, with stdout and stderr captured as bytes.
    """
    environment = {**os.environ, "PYTHONPATH": str(SRC_DIR), **(env or {})}
    target = [str(MODULE_PATH)] if script else ["-m", "hello_world"]
    return subprocess.run(
        [sys.executable, *interpreter_flags, *target, *args],
        capture_output=True,
        env=environment,
        check=False,
        timeout=30,
    )


@contextlib.contextmanager
def patched_environ(values: Mapping[str, str]) -> Iterator[None]:
    """Temporarily add variables to ``os.environ``.

    Unlike pytest's ``monkeypatch`` fixture, this helper can be used inside
    Hypothesis tests, which must not depend on function-scoped fixtures.

    Args:
        values: The variables to set.

    Yields:
        Nothing. The original environment is restored on exit.
    """
    original = os.environ.copy()
    os.environ.update(values)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original)
