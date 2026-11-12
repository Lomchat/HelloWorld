"""Shared test helpers.

Helpers are kept in a dedicated module rather than redefined in each test
file, to guarantee consistent behavior across the whole suite.
"""

from __future__ import annotations

import contextlib
import io
import os
import runpy
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Mapping

#: Root directory of the repository.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

#: Directory containing the ``hello_world`` package.
SRC_DIR = PROJECT_ROOT / "src"

#: Path to the core module, runnable as a standalone script.
MODULE_PATH = SRC_DIR / "hello_world" / "hello_world.py"

#: The exact bytes the program must write to stdout when run as a process.
#: In a subprocess, stdout is opened in text mode, so the line feed is translated
#: to the platform line separator ("\r\n" on Windows). In-process tests, which
#: capture stdout without translation, always observe "\n".
EXPECTED_STDOUT = f"Hello, World!{os.linesep}".encode("ascii")

#: Every way of executing the application in-process, by name.
_RUNNERS: dict[str, Callable[[], object]] = {
    "python -m hello_world": lambda: runpy.run_module("hello_world", run_name="__main__"),
    "hello_world.hello_world": lambda: runpy.run_module(
        "hello_world.hello_world",
        run_name="__main__",
    ),
    "hello_world.py": lambda: runpy.run_path(str(MODULE_PATH), run_name="__main__"),
}

#: The names of the in-process entry points, used to parametrize tests.
ENTRY_POINTS = tuple(_RUNNERS)


def run_in_process(entry_point: str = "python -m hello_world") -> str:
    """Execute the application in the current process and return its output.

    The module is executed (not imported), so that the greeting is printed on
    every call, regardless of what is already in ``sys.modules``.

    Args:
        entry_point: One of :data:`ENTRY_POINTS`.

    Returns:
        Everything the application wrote to stdout.
    """
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        _RUNNERS[entry_point]()
    return buffer.getvalue()


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
