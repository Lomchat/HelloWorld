"""Tests for the Hello World application."""

from __future__ import annotations

from hello_world import greet


def test_greet_prints_the_greeting(capsys):
    greet()
    assert capsys.readouterr().out == "Hello, World!\n"
