"""Thread-safety and parallelism tests.

The core module is stateless: it defines no variable, no function and no
class. Executing it concurrently must therefore always produce the same
result. These tests verify that claim under contention, both across threads
(sharing a single compiled code object) and across processes.
"""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

from tests.helpers import EXPECTED_STDOUT, MODULE_PATH, run_hello_world

pytestmark = pytest.mark.concurrency

WORKERS = 16
ITERATIONS = 1_000

#: The core module, compiled once and shared by every thread.
CODE = compile(MODULE_PATH.read_text(encoding="utf-8"), str(MODULE_PATH), "exec")


def _execute_with_captured_print() -> list[str]:
    """Execute the core module with a thread-local ``print`` capturing its output."""
    captured: list[str] = []

    def fake_print(*args: object, **_kwargs: object) -> None:
        captured.append(" ".join(map(str, args)))

    exec(CODE, {"__name__": "__main__", "print": fake_print})  # noqa: S102 - trusted, own source
    return captured


def test_concurrent_executions_print_the_same_greeting():
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(lambda _: _execute_with_captured_print(), range(ITERATIONS)))
    assert all(result == ["Hello, World!"] for result in results)


def test_simultaneous_start_under_a_barrier():
    barrier = threading.Barrier(WORKERS)
    results: list[list[str]] = []
    lock = threading.Lock()

    def worker() -> None:
        barrier.wait()
        output = _execute_with_captured_print()
        with lock:
            results.append(output)

    threads = [threading.Thread(target=worker) for _ in range(WORKERS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)
    assert results == [["Hello, World!"]] * WORKERS


def test_parallel_processes_print_the_same_greeting():
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda _: run_hello_world().stdout, range(4)))
    assert results == [EXPECTED_STDOUT] * 4
