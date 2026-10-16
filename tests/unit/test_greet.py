"""Unit tests for :func:`hello_world.hello_world.greet`."""

from __future__ import annotations

import inspect
import typing

import pytest

from hello_world import hello_world
from hello_world.hello_world import GREETING, greet

pytestmark = pytest.mark.unit


class TestReturnValue:
    def test_returns_the_canonical_greeting(self):
        assert greet() == "Hello, World!"

    def test_returns_exactly_a_str(self):
        assert type(greet()) is str

    def test_returns_the_greeting_constant(self):
        assert greet() == GREETING

    def test_returns_the_very_same_object_as_the_constant(self):
        assert greet() is GREETING

    def test_return_value_is_truthy(self):
        assert greet()

    def test_return_value_is_hashable(self):
        assert hash(greet()) == hash("Hello, World!")


class TestPurity:
    def test_writes_nothing_to_stdout_or_stderr(self, capsys):
        greet()
        assert capsys.readouterr() == ("", "")

    def test_is_deterministic(self):
        assert {greet() for _ in range(1_000)} == {"Hello, World!"}

    def test_is_idempotent(self):
        assert greet() == greet() == greet()

    def test_does_not_modify_module_globals(self):
        before = dict(vars(hello_world))
        greet()
        assert dict(vars(hello_world)) == before

    def test_does_not_depend_on_the_environment(self, monkeypatch):
        monkeypatch.setenv("HELLO_WORLD_RECIPIENT", "Mars")
        assert greet() == "Hello, World!"


class TestSignature:
    def test_takes_no_parameters(self):
        assert inspect.signature(greet).parameters == {}

    def test_rejects_positional_arguments(self):
        with pytest.raises(TypeError):
            greet("World")

    def test_rejects_keyword_arguments(self):
        with pytest.raises(TypeError):
            greet(recipient="World")

    def test_return_annotation_is_str(self):
        assert typing.get_type_hints(greet) == {"return": str}

    def test_is_a_plain_function(self):
        assert inspect.isfunction(greet)

    def test_is_not_a_coroutine_function(self):
        assert not inspect.iscoroutinefunction(greet)

    def test_is_not_a_generator_function(self):
        assert not inspect.isgeneratorfunction(greet)


class TestDocumentation:
    def test_has_a_docstring(self):
        assert inspect.getdoc(greet)

    def test_docstring_has_a_summary_line_ending_with_a_period(self):
        assert inspect.getdoc(greet).splitlines()[0].endswith(".")

    @pytest.mark.parametrize("section", ["Returns:", "Example:"])
    def test_docstring_has_section(self, section):
        assert section in inspect.getdoc(greet)
