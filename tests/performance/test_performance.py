"""Performance budget tests.

Budgets are intentionally generous so that these tests remain reliable on
slow or heavily loaded CI runners. Their purpose is to catch accidental
order-of-magnitude regressions, not to benchmark. For precise measurements,
use ``make bench``.
"""

from __future__ import annotations

import contextlib
import io
import time

import pytest

from hello_world import greet, main
from tests.helpers import run_hello_world

pytestmark = pytest.mark.performance


def test_greet_average_latency_is_under_ten_microseconds():
    iterations = 100_000
    start = time.perf_counter()
    for _ in range(iterations):
        greet()
    assert (time.perf_counter() - start) / iterations < 10e-6


def test_main_average_latency_is_under_one_hundred_microseconds():
    iterations = 10_000
    with contextlib.redirect_stdout(io.StringIO()):
        start = time.perf_counter()
        for _ in range(iterations):
            main()
        elapsed = time.perf_counter() - start
    assert elapsed / iterations < 100e-6


def test_cold_start_is_under_two_seconds():
    start = time.perf_counter()
    result = run_hello_world()
    assert result.returncode == 0
    assert time.perf_counter() - start < 2.0
