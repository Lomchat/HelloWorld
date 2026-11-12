"""Micro-benchmarks for the Hello World application.

Usage:
    make bench

Results are printed as a table. They are indicative only and depend on the
machine, the Python version and the system load.
"""

from __future__ import annotations

import contextlib
import io
import platform
import runpy
import statistics
import timeit
from pathlib import Path

from hello_world import __version__

#: Path to the core module.
MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "hello_world" / "hello_world.py"

#: The core module, compiled once.
CODE = compile(MODULE_PATH.read_text(encoding="utf-8"), str(MODULE_PATH), "exec")

#: Number of executions per measurement.
NUMBER = 10_000

#: Number of measurements per benchmark.
REPEAT = 7


def _exec_compiled() -> None:
    exec(CODE, {"__name__": "__main__"})  # noqa: S102 - trusted, own source


def _runpy_module() -> None:
    runpy.run_module("hello_world.hello_world", run_name="__main__")


BENCHMARKS = {
    "exec (precompiled code)": _exec_compiled,
    "runpy.run_module (core module)": _runpy_module,
}


def run() -> None:
    """Run every benchmark and print a summary table."""
    print(f"hello-world {__version__} on Python {platform.python_version()} ({platform.machine()})")
    print(f"{NUMBER:,} executions x {REPEAT} repetitions, stdout redirected\n")
    print(f"{'Benchmark':<32} {'best':>10} {'median':>10} {'stdev':>10}")
    print("-" * 65)
    for name, func in BENCHMARKS.items():
        # Redirect stdout so that the benchmark measures the execution, not the terminal.
        with contextlib.redirect_stdout(io.StringIO()):
            timings = [t / NUMBER for t in timeit.repeat(func, number=NUMBER, repeat=REPEAT)]
        print(
            f"{name:<32} "
            f"{min(timings) * 1e6:>8.2f}µs "
            f"{statistics.median(timings) * 1e6:>8.2f}µs "
            f"{statistics.stdev(timings) * 1e6:>8.2f}µs",
        )


if __name__ == "__main__":
    run()
