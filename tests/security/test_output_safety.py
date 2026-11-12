"""Security tests: output safety and environment isolation.

The greeting is written to the user's terminal. A compromised or corrupted
greeting could clear the screen, rewrite previous output, change the window
title or hide content using bidirectional overrides. These tests guarantee
that the output is free of every known terminal injection vector, and that
it cannot be influenced by the environment.
"""

from __future__ import annotations

import pytest

from tests.helpers import run_in_process

pytestmark = pytest.mark.security

INJECTION_VECTORS = [
    pytest.param("\x1b[", id="ansi-csi"),
    pytest.param("\x1b[31m", id="ansi-color"),
    pytest.param("\x1b[2J", id="ansi-clear-screen"),
    pytest.param("\x1b[1;1H", id="ansi-cursor-move"),
    pytest.param("\x1b[1A", id="ansi-cursor-up"),
    pytest.param("\x1b[2K", id="ansi-erase-line"),
    pytest.param("\x1b]0;", id="osc-window-title"),
    pytest.param("\x1b]8;;", id="osc-hyperlink"),
    pytest.param("\x1bP", id="dcs"),
    pytest.param("\x9b", id="c1-csi"),
    pytest.param("\x00", id="null-byte"),
    pytest.param("\r", id="carriage-return"),
    pytest.param("\x08", id="backspace"),
    pytest.param("\x07", id="bell"),
    pytest.param("\x7f", id="delete"),
    pytest.param("\u202e", id="bidi-right-to-left-override"),
    pytest.param("\u2066", id="bidi-isolate"),
    pytest.param("\u200b", id="zero-width-space"),
    pytest.param("\u200d", id="zero-width-joiner"),
    pytest.param("\u2028", id="line-separator"),
    pytest.param("\u2029", id="paragraph-separator"),
    pytest.param("\ufeff", id="byte-order-mark"),
]

#: Every C0 control character, plus DEL. Only the final line feed is allowed.
CONTROL_CHARACTERS = [pytest.param(chr(code), id=f"U+{code:04X}") for code in [*range(0x20), 0x7F]]

#: Environment variables that commonly alter the behavior of terminal programs.
ENVIRONMENT_OVERRIDES = [
    pytest.param("LANG", "C", id="LANG"),
    pytest.param("LC_ALL", "tr_TR.UTF-8", id="LC_ALL"),
    pytest.param("LC_CTYPE", "C", id="LC_CTYPE"),
    pytest.param("TERM", "dumb", id="TERM"),
    pytest.param("NO_COLOR", "1", id="NO_COLOR"),
    pytest.param("FORCE_COLOR", "3", id="FORCE_COLOR"),
    pytest.param("CLICOLOR_FORCE", "1", id="CLICOLOR_FORCE"),
    pytest.param("COLUMNS", "5", id="COLUMNS"),
    pytest.param("TZ", "Pacific/Kiritimati", id="TZ"),
    pytest.param("HELLO_WORLD_RECIPIENT", "Mars", id="HELLO_WORLD_RECIPIENT"),
    pytest.param("HELLO_WORLD_GREETING", "\x1b[2JGoodbye", id="HELLO_WORLD_GREETING"),
]


class TestInjectionVectors:
    @pytest.mark.parametrize("vector", INJECTION_VECTORS)
    def test_greeting_does_not_contain_vector(self, greeting, vector):
        assert vector not in greeting


class TestControlCharacters:
    @pytest.mark.parametrize("character", CONTROL_CHARACTERS)
    def test_greeting_does_not_contain_control_character(self, greeting, character):
        assert character not in greeting

    def test_stdout_contains_no_control_character_besides_the_final_line_feed(self, stdout_text):
        assert stdout_text[:-1].isprintable()
        assert stdout_text[-1] == "\n"


class TestEnvironmentIsolation:
    @pytest.mark.parametrize(("variable", "value"), ENVIRONMENT_OVERRIDES)
    def test_output_is_not_affected_by(self, monkeypatch, variable, value):
        monkeypatch.setenv(variable, value)
        assert run_in_process() == "Hello, World!\n"
