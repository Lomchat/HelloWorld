"""Shared pytest fixtures and configuration for the whole test suite."""

from __future__ import annotations

import os
import runpy

import pytest
from hypothesis import settings as hypothesis_settings

from tests.helpers import ENTRY_POINTS, run_in_process

# ---------------------------------------------------------------------------
# Hypothesis profiles
# ---------------------------------------------------------------------------

# "dev" keeps the local feedback loop fast; "ci" explores more examples.
hypothesis_settings.register_profile("dev", max_examples=50, deadline=None)
hypothesis_settings.register_profile("ci", max_examples=300, deadline=None)
hypothesis_settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "dev"))

# ---------------------------------------------------------------------------
# Output fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(params=ENTRY_POINTS)
def greeting(request: pytest.FixtureRequest) -> str:
    """The greeting, as printed through each in-process entry point.

    Tests using this fixture run once per entry point, which guarantees that
    every property of the greeting holds regardless of how the application is
    executed. The trailing line feed is removed.
    """
    return run_in_process(request.param).removesuffix("\n")


@pytest.fixture
def stdout_text(capsys: pytest.CaptureFixture[str]) -> str:
    """The text written to stdout by ``python -m hello_world``."""
    runpy.run_module("hello_world", run_name="__main__")
    return capsys.readouterr().out


@pytest.fixture
def stdout_bytes(capsysbinary: pytest.CaptureFixture[bytes]) -> bytes:
    """The raw bytes written to stdout by ``python -m hello_world``."""
    runpy.run_module("hello_world", run_name="__main__")
    return capsysbinary.readouterr().out
