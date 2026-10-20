"""Regression tests for previously fixed bugs.

Every test in this module references the issue that motivated it. These
tests must never be deleted, even if they look redundant with other tests:
their purpose is to guarantee that a given bug never comes back.
"""

from __future__ import annotations

import importlib.util
import runpy

import pytest

from hello_world import greet, main

pytestmark = pytest.mark.regression


def test_issue_42_comma_between_hello_and_world():
    """#42: The comma between "Hello" and "World" was missing."""
    assert greet()[5] == ","


def test_issue_42_space_after_comma():
    """#42 (follow-up): The space after the comma went missing in the first fix."""
    assert greet()[5:7] == ", "


def test_issue_51_main_returns_an_integer_exit_code():
    """#51: main() returned None, so `raise SystemExit(main())` was ambiguous."""
    assert main() == 0


def test_issue_57_no_whitespace_before_the_exclamation_mark():
    """#57: The greeting was rendered as "Hello, World !"."""
    assert " !" not in greet()


def test_issue_57_no_trailing_whitespace_on_stdout(stdout_text):
    """#57 (follow-up): stdout ended with "Hello, World! \\n"."""
    assert stdout_text == stdout_text.rstrip() + "\n"


def test_issue_64_package_is_runnable_with_dash_m():
    """#64: `python -m hello_world` failed with "No module named hello_world.__main__"."""
    assert importlib.util.find_spec("hello_world.__main__") is not None


def test_issue_64_dash_m_entry_point_exits_successfully(capsys):
    """#64 (follow-up): The __main__ module did not propagate the exit code."""
    with pytest.raises(SystemExit) as excinfo:
        runpy.run_module("hello_world", run_name="__main__")
    assert excinfo.value.code == 0
    assert capsys.readouterr().out == "Hello, World!\n"


def test_issue_73_output_ends_with_exactly_one_newline(stdout_text):
    """#73: The greeting was followed by two newlines (print(greet() + "\\n"))."""
    assert stdout_text.endswith("\n")
    assert not stdout_text.endswith("\n\n")


def test_issue_88_exclamation_mark_is_not_duplicated():
    """#88: The greeting was rendered as "Hello, World!!"."""
    assert greet().count("!") == 1


def test_issue_95_greet_has_no_side_effects(capsys):
    """#95: greet() printed the greeting instead of returning it (fixed in 2.0.0)."""
    result = greet()
    assert result == "Hello, World!"
    assert capsys.readouterr().out == ""
