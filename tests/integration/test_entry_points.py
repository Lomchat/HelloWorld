"""Integration tests for the application entry points, run in-process."""

from __future__ import annotations

import runpy

import pytest

from tests.helpers import ENTRY_POINTS, MODULE_PATH, run_in_process

pytestmark = pytest.mark.integration

SUPPORT_FILES = sorted(p for p in MODULE_PATH.parent.glob("*.py") if p != MODULE_PATH)


@pytest.mark.parametrize("entry_point", ENTRY_POINTS)
def test_entry_point_prints_the_greeting(entry_point):
    assert run_in_process(entry_point) == "Hello, World!\n"


def test_every_entry_point_produces_the_same_output():
    assert len({run_in_process(entry_point) for entry_point in ENTRY_POINTS}) == 1


def test_dash_m_entry_point_does_not_exit_explicitly():
    # The process exit status is 0 because the module completes normally.
    assert runpy.run_module("hello_world", run_name="__main__") is not None


@pytest.mark.parametrize("path", SUPPORT_FILES, ids=lambda path: path.name)
def test_support_modules_have_no_side_effects_unless_run(capsys, path):
    # A run name other than "__main__" mimics a plain import, in a fresh namespace
    # that leaves sys.modules untouched.
    runpy.run_path(str(path), run_name="__not_main__")
    assert capsys.readouterr() == ("", "")
