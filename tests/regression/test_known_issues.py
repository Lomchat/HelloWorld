"""Regression tests for previously fixed bugs.

Every test in this module references the issue that motivated it. These
tests must never be deleted, even if they look redundant with other tests:
their purpose is to guarantee that a given bug never comes back.
"""

from __future__ import annotations

import ast
import importlib
import importlib.util

import pytest

import hello_world
from tests.helpers import MODULE_PATH, run_hello_world, run_in_process

pytestmark = pytest.mark.regression


def test_issue_42_comma_between_hello_and_world():
    """#42: The comma between "Hello" and "World" was missing."""
    assert run_in_process()[5] == ","


def test_issue_42_space_after_comma():
    """#42 (follow-up): The space after the comma went missing in the first fix."""
    assert run_in_process()[5:7] == ", "


def test_issue_51_process_exits_with_status_zero():
    """#51: main() returned None, so the exit status of the process was ambiguous."""
    assert run_hello_world().returncode == 0


def test_issue_57_no_whitespace_before_the_exclamation_mark():
    """#57: The greeting was rendered as "Hello, World !"."""
    assert " !" not in run_in_process()


def test_issue_57_print_receives_a_single_argument():
    """#57 (root cause): print("Hello, World", "!") inserted a space between its arguments."""
    statement = ast.parse(MODULE_PATH.read_text(encoding="utf-8")).body[0]
    assert isinstance(statement, ast.Expr)
    assert isinstance(statement.value, ast.Call)
    assert len(statement.value.args) == 1


def test_issue_57_no_trailing_whitespace_on_stdout(stdout_text):
    """#57 (follow-up): stdout ended with "Hello, World! \\n"."""
    assert stdout_text == stdout_text.rstrip() + "\n"


def test_issue_64_package_is_runnable_with_dash_m():
    """#64: `python -m hello_world` failed with "No module named hello_world.__main__"."""
    assert importlib.util.find_spec("hello_world.__main__") is not None


def test_issue_64_dash_m_entry_point_prints_the_greeting():
    """#64 (follow-up): The __main__ module did not print anything."""
    assert run_in_process("python -m hello_world") == "Hello, World!\n"


def test_issue_73_output_ends_with_exactly_one_newline(stdout_text):
    """#73: The greeting was followed by two newlines (print(greet() + "\\n"))."""
    assert stdout_text.endswith("\n")
    assert not stdout_text.endswith("\n\n")


def test_issue_88_exclamation_mark_is_not_duplicated():
    """#88: The greeting was rendered as "Hello, World!!"."""
    assert run_in_process().count("!") == 1


def test_issue_95_importing_the_package_has_no_side_effects(capsys):
    """#95: Using the package from a library printed the greeting unexpectedly."""
    importlib.reload(hello_world)
    assert capsys.readouterr().out == ""
