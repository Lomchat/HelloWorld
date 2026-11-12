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

from tests.helpers import MODULE_PATH, run_hello_world

pytestmark = pytest.mark.performance

CODE = compile(MODULE_PATH.read_text(encoding="utf-8"), str(MODULE_PATH), "exec")


def test_executing_the_core_module_takes_under_one_hundred_microseconds():
    iterations = 10_000
    with contextlib.redirect_stdout(io.StringIO()):
        start = time.perf_counter()
        for _ in range(iterations):
            exec(CODE, {"__name__": "__main__"})  # noqa: S102 - trusted, own source
        elapsed = time.perf_counter() - start
    assert elapsed / iterations < 100e-6


def test_compiling_the_core_module_takes_under_ten_milliseconds():
    source = MODULE_PATH.read_text(encoding="utf-8")
    start = time.perf_counter()
    compile(source, str(MODULE_PATH), "exec")
    assert time.perf_counter() - start < 10e-3


def test_cold_start_is_under_two_seconds():
    start = time.perf_counter()
    result = run_hello_world()
    assert result.returncode == 0
    assert time.perf_counter() - start < 2.0
