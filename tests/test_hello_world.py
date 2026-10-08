"""Tests for the Hello World application."""

from __future__ import annotations

from hello_world import greet, main


def test_greet_returns_the_greeting():
    assert greet() == "Hello, World!"


def test_main_prints_the_greeting(capsys):
    main()
    assert capsys.readouterr().out == "Hello, World!\n"
