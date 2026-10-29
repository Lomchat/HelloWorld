"""End-to-end tests running the real program in a subprocess.

These tests treat the application as a black box: they only observe the
bytes written to stdout and stderr, and the process exit code.
"""

from __future__ import annotations

import pytest

from tests.helpers import EXPECTED_STDOUT, run_hello_world

pytestmark = pytest.mark.e2e


class TestModuleExecution:
    def test_outputs_the_exact_expected_bytes(self):
        assert run_hello_world().stdout == EXPECTED_STDOUT

    def test_exits_successfully(self):
        assert run_hello_world().returncode == 0

    def test_writes_nothing_to_stderr(self):
        assert run_hello_world().stderr == b""


class TestScriptExecution:
    def test_outputs_the_exact_expected_bytes(self):
        assert run_hello_world(script=True).stdout == EXPECTED_STDOUT

    def test_exits_successfully(self):
        assert run_hello_world(script=True).returncode == 0


class TestRobustness:
    @pytest.mark.parametrize("args", [["--help"], ["--version"], ["-v"], ["extra", "args"]])
    def test_ignores_command_line_arguments(self, args):
        result = run_hello_world(*args)
        assert (result.returncode, result.stdout) == (0, EXPECTED_STDOUT)

    @pytest.mark.parametrize(
        "flags",
        [("-O",), ("-OO",), ("-B",), ("-X", "utf8"), ("-X", "dev"), ("-W", "error")],
        ids=[
            "optimize",
            "optimize-docstrings",
            "no-bytecode",
            "utf8-mode",
            "dev-mode",
            "warnings-as-errors",
        ],
    )
    def test_supports_interpreter_flags(self, flags):
        result = run_hello_world(interpreter_flags=flags)
        assert (result.returncode, result.stdout, result.stderr) == (0, EXPECTED_STDOUT, b"")

    @pytest.mark.parametrize(
        "env",
        [{"LANG": "C"}, {"LC_ALL": "C.UTF-8"}, {"TERM": "dumb"}, {"NO_COLOR": "1"}],
        ids=["LANG=C", "LC_ALL=C.UTF-8", "TERM=dumb", "NO_COLOR=1"],
    )
    def test_output_is_stable_across_environments(self, env):
        assert run_hello_world(env=env).stdout == EXPECTED_STDOUT
