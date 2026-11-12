"""Property-based tests powered by Hypothesis.

Instead of checking a handful of hand-picked scenarios, these tests assert
invariants that must hold under *any* generated conditions: arbitrary
execution counts, environments, random seeds and command-line arguments.
"""

from __future__ import annotations

import random
import sys

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tests.helpers import ENTRY_POINTS, patched_environ, run_in_process

pytestmark = pytest.mark.property

#: Environment variable names, restricted to a dedicated prefix to stay hermetic.
env_names = st.from_regex(r"HW_TEST_[A-Z0-9_]{1,16}", fullmatch=True)

#: Environment variable values (no null bytes, which the OS cannot store).
env_values = st.text(
    st.characters(codec="utf-8", exclude_characters="\x00"),
    max_size=32,
)


@given(executions=st.integers(min_value=1, max_value=50))
def test_output_is_stable_across_any_number_of_executions(executions):
    assert {run_in_process() for _ in range(executions)} == {"Hello, World!\n"}


@given(entry_point=st.sampled_from(ENTRY_POINTS))
def test_output_is_identical_for_every_entry_point(entry_point):
    assert run_in_process(entry_point) == "Hello, World!\n"


@given(environment=st.dictionaries(env_names, env_values, max_size=10))
def test_output_is_independent_of_the_environment(environment):
    with patched_environ(environment):
        assert run_in_process() == "Hello, World!\n"


@given(seed=st.integers())
def test_output_is_independent_of_the_random_seed(seed):
    random.seed(seed)
    assert run_in_process() == "Hello, World!\n"


@given(argv=st.lists(st.text(st.characters(codec="utf-8", exclude_characters="\x00"))))
def test_output_is_independent_of_command_line_arguments(argv):
    original = sys.argv
    sys.argv = ["hello_world", *argv]
    try:
        output = run_in_process()
    finally:
        sys.argv = original
    assert output == "Hello, World!\n"
