"""Unit tests for :func:`hello_world.hello_world.main`."""

from __future__ import annotations

import contextlib
import inspect
import io
import typing

import pytest

from hello_world import hello_world
from hello_world.hello_world import main

pytestmark = pytest.mark.unit


class TestOutput:
    def test_prints_the_canonical_greeting(self, capsys):
        main()
        assert capsys.readouterr().out == "Hello, World!\n"

    def test_writes_nothing_to_stderr(self, capsys):
        main()
        assert capsys.readouterr().err == ""

    def test_prints_exactly_one_line(self, stdout_text):
        assert len(stdout_text.splitlines()) == 1

    def test_writes_to_the_current_sys_stdout(self):
        target = io.StringIO()
        with contextlib.redirect_stdout(target):
            main()
        assert target.getvalue() == "Hello, World!\n"

    def test_prints_one_greeting_per_call(self, capsys):
        for _ in range(3):
            main()
        assert capsys.readouterr().out == "Hello, World!\n" * 3

    def test_delegates_composition_to_greet(self, monkeypatch, capsys):
        monkeypatch.setattr(hello_world, "greet", lambda: "delegated")
        main()
        assert capsys.readouterr().out == "delegated\n"

    def test_ignores_command_line_arguments(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.argv", ["hello-world", "--recipient", "Mars"])
        main()
        assert capsys.readouterr().out == "Hello, World!\n"


class TestExitCode:
    def test_returns_zero(self):
        assert main() == 0

    def test_returns_exactly_an_int(self):
        assert type(main()) is int

    def test_exit_code_is_a_valid_process_status(self):
        assert 0 <= main() <= 255


class TestSignature:
    def test_takes_no_parameters(self):
        assert inspect.signature(main).parameters == {}

    def test_rejects_arguments(self):
        with pytest.raises(TypeError):
            main(["--help"])

    def test_return_annotation_is_int(self):
        assert typing.get_type_hints(main) == {"return": int}


class TestDocumentation:
    def test_has_a_docstring(self):
        assert inspect.getdoc(main)

    @pytest.mark.parametrize("section", ["Returns:", "Example:"])
    def test_docstring_has_section(self, section):
        assert section in inspect.getdoc(main)
