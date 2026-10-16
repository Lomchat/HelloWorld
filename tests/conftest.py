"""Shared pytest fixtures and configuration for the whole test suite."""

from __future__ import annotations

import os

import pytest
from hypothesis import settings as hypothesis_settings

from hello_world import GREETING, greet, main

# ---------------------------------------------------------------------------
# Hypothesis profiles
# ---------------------------------------------------------------------------

# "dev" keeps the local feedback loop fast; "ci" explores more examples.
hypothesis_settings.register_profile("dev", max_examples=50, deadline=None)
hypothesis_settings.register_profile("ci", max_examples=300, deadline=None)
hypothesis_settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "dev"))

# ---------------------------------------------------------------------------
# Output surfaces
# ---------------------------------------------------------------------------

#: Every public surface through which the greeting can be observed.
SURFACES = ["greet()", "GREETING", "main() stdout"]


@pytest.fixture(params=SURFACES)
def greeting(request: pytest.FixtureRequest) -> str:
    """The greeting, as observed through each public surface.

    Tests using this fixture run once per surface, which guarantees that every
    property of the greeting holds regardless of how it is obtained.
    """
    if request.param == "greet()":
        return greet()
    if request.param == "GREETING":
        return GREETING
    capsys = request.getfixturevalue("capsys")
    main()
    return capsys.readouterr().out.removesuffix("\n")


@pytest.fixture
def stdout_text(capsys: pytest.CaptureFixture[str]) -> str:
    """The text written to stdout by :func:`main`."""
    main()
    return capsys.readouterr().out


@pytest.fixture
def stdout_bytes(capsysbinary: pytest.CaptureFixture[bytes]) -> bytes:
    """The raw bytes written to stdout by :func:`main`."""
    main()
    return capsysbinary.readouterr().out
