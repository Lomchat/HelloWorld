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
import statistics
import timeit

from hello_world import GREETING, __version__, greet, main

#: Number of calls per measurement.
NUMBER = 100_000

#: Number of measurements per benchmark.
REPEAT = 7


def _bench_main() -> None:
    # Redirect stdout so that the benchmark measures the call, not the terminal.
    with contextlib.redirect_stdout(io.StringIO()):
        main()


BENCHMARKS = {
    "GREETING (constant access)": lambda: GREETING,
    "greet()": greet,
    "main() (redirected stdout)": _bench_main,
}


def run() -> None:
    """Run every benchmark and print a summary table."""
    print(f"hello-world {__version__} on Python {platform.python_version()} ({platform.machine()})")
    print(f"{NUMBER:,} calls x {REPEAT} repetitions\n")
    print(f"{'Benchmark':<30} {'best':>10} {'median':>10} {'stdev':>10}")
    print("-" * 63)
    for name, func in BENCHMARKS.items():
        timings = [t / NUMBER for t in timeit.repeat(func, number=NUMBER, repeat=REPEAT)]
        print(
            f"{name:<30} "
            f"{min(timings) * 1e9:>8.1f}ns "
            f"{statistics.median(timings) * 1e9:>8.1f}ns "
            f"{statistics.stdev(timings) * 1e9:>8.1f}ns",
        )


if __name__ == "__main__":
    run()
