"""Integration tests for the application entry points, run in-process."""

from __future__ import annotations

import runpy

import pytest

from hello_world import greet, main
from tests.helpers import MODULE_PATH

pytestmark = pytest.mark.integration


def test_main_prints_what_greet_returns(capsys):
    main()
    assert capsys.readouterr().out == f"{greet()}\n"


def test_dash_m_entry_point(capsys):
    with pytest.raises(SystemExit) as excinfo:
        runpy.run_module("hello_world", run_name="__main__")
    assert excinfo.value.code == 0
    assert capsys.readouterr().out == "Hello, World!\n"


def test_script_entry_point(capsys):
    with pytest.raises(SystemExit) as excinfo:
        runpy.run_path(str(MODULE_PATH), run_name="__main__")
    assert excinfo.value.code == 0
    assert capsys.readouterr().out == "Hello, World!\n"


@pytest.mark.parametrize(
    "path",
    sorted(MODULE_PATH.parent.glob("*.py")),
    ids=lambda path: path.name,
)
def test_executing_a_module_without_running_it_has_no_side_effects(capsys, path):
    # A run name other than "__main__" mimics a plain import, in a fresh namespace
    # that leaves sys.modules untouched.
    runpy.run_path(str(path), run_name="__not_main__")
    assert capsys.readouterr() == ("", "")
