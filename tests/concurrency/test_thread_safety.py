"""Thread-safety tests.

``greet()`` is a pure function returning an immutable constant, so it should
be safe to call from multiple threads. These tests verify that claim under
contention.
"""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

from hello_world import greet

pytestmark = pytest.mark.concurrency

WORKERS = 16
ITERATIONS = 1_000


def test_concurrent_calls_return_the_same_greeting():
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(lambda _: greet(), range(ITERATIONS)))
    assert set(results) == {"Hello, World!"}


def test_concurrent_calls_return_the_same_object():
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(lambda _: greet(), range(ITERATIONS)))
    assert len({id(result) for result in results}) == 1


def test_simultaneous_start_under_a_barrier():
    barrier = threading.Barrier(WORKERS)
    results: list[str] = []
    lock = threading.Lock()

    def worker() -> None:
        barrier.wait()
        greeting = greet()
        with lock:
            results.append(greeting)

    threads = [threading.Thread(target=worker) for _ in range(WORKERS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)
    assert results == ["Hello, World!"] * WORKERS
