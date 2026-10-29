"""Property-based tests powered by Hypothesis.

Instead of checking a handful of hand-picked scenarios, these tests assert
invariants that must hold under *any* generated conditions: arbitrary call
counts, environments, random seeds and command-line arguments.
"""

from __future__ import annotations

import contextlib
import io
import random
import sys

import pytest
from hypothesis import given
from hypothesis import strategies as st

from hello_world import GREETING, greet, main
from tests.helpers import patched_environ

pytestmark = pytest.mark.property

#: Environment variable names, restricted to a dedicated prefix to stay hermetic.
env_names = st.from_regex(r"HW_TEST_[A-Z0-9_]{1,16}", fullmatch=True)

#: Environment variable values (no null bytes, which the OS cannot store).
env_values = st.text(
    st.characters(codec="utf-8", exclude_characters="\x00"),
    max_size=32,
)


@given(calls=st.integers(min_value=1, max_value=100))
def test_greet_is_stable_across_any_number_of_calls(calls):
    assert {greet() for _ in range(calls)} == {GREETING}


@given(environment=st.dictionaries(env_names, env_values, max_size=10))
def test_greet_is_independent_of_the_environment(environment):
    with patched_environ(environment):
        assert greet() == "Hello, World!"


@given(seed=st.integers())
def test_greet_is_independent_of_the_random_seed(seed):
    random.seed(seed)
    assert greet() == "Hello, World!"


@given(argv=st.lists(st.text(st.characters(codec="utf-8", exclude_characters="\x00"))))
def test_main_output_is_independent_of_command_line_arguments(argv):
    original = sys.argv
    sys.argv = ["hello-world", *argv]
    try:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exit_code = main()
    finally:
        sys.argv = original
    assert buffer.getvalue() == "Hello, World!\n"
    assert exit_code == 0


@given(calls=st.integers(min_value=1, max_value=50))
def test_main_prints_exactly_one_line_per_call(calls):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        for _ in range(calls):
            main()
    assert buffer.getvalue().splitlines() == [GREETING] * calls
