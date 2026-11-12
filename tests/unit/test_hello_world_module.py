"""Unit tests for the core module, :mod:`hello_world.hello_world`.

The core module must contain exactly one statement (ADR-0009). These tests
verify both its behavior and its structure, by parsing its source code.
"""

from __future__ import annotations

import ast
import io
import tokenize

import pytest

from tests.helpers import MODULE_PATH, run_in_process

pytestmark = pytest.mark.unit

SOURCE = MODULE_PATH.read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)
STATEMENT = TREE.body[0]

#: Statement types that must never appear in the core module.
FORBIDDEN_NODES = [
    ast.Import,
    ast.ImportFrom,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Assign,
    ast.AnnAssign,
    ast.AugAssign,
    ast.If,
    ast.For,
    ast.While,
    ast.Try,
    ast.With,
    ast.Return,
    ast.Raise,
    ast.Global,
    ast.Lambda,
]


def _comment_lines() -> list[str]:
    tokens = tokenize.generate_tokens(io.StringIO(SOURCE).readline)
    return [token.string for token in tokens if token.type == tokenize.COMMENT]


class TestBehavior:
    def test_prints_the_canonical_greeting(self):
        assert run_in_process("hello_world.hello_world") == "Hello, World!\n"

    def test_prints_exactly_one_line(self):
        assert len(run_in_process("hello_world.hello_world").splitlines()) == 1

    def test_writes_nothing_to_stderr(self, capsys):
        run_in_process("hello_world.hello_world")
        assert capsys.readouterr().err == ""

    def test_prints_the_greeting_on_every_execution(self):
        outputs = [run_in_process("hello_world.hello_world") for _ in range(3)]
        assert outputs == ["Hello, World!\n"] * 3

    def test_source_compiles(self):
        assert compile(SOURCE, str(MODULE_PATH), "exec")


class TestStructure:
    def test_contains_exactly_one_statement(self):
        assert len(TREE.body) == 1

    def test_the_statement_is_an_expression(self):
        assert isinstance(STATEMENT, ast.Expr)

    def test_the_expression_is_a_function_call(self):
        assert isinstance(STATEMENT.value, ast.Call)

    def test_the_called_function_is_print(self):
        assert isinstance(STATEMENT.value.func, ast.Name)
        assert STATEMENT.value.func.id == "print"

    def test_print_receives_exactly_one_argument(self):
        assert len(STATEMENT.value.args) == 1

    def test_print_receives_no_keyword_argument(self):
        assert STATEMENT.value.keywords == []

    def test_the_argument_is_a_string_literal(self):
        assert isinstance(STATEMENT.value.args[0], ast.Constant)
        assert isinstance(STATEMENT.value.args[0].value, str)

    def test_the_argument_is_the_canonical_greeting(self):
        assert STATEMENT.value.args[0].value == "Hello, World!"

    def test_has_no_module_docstring(self):
        assert ast.get_docstring(TREE) is None

    @pytest.mark.parametrize("node_type", FORBIDDEN_NODES, ids=lambda node: node.__name__)
    def test_contains_no(self, node_type):
        assert not any(isinstance(node, node_type) for node in ast.walk(TREE))


class TestDocumentation:
    def test_every_non_blank_line_but_one_is_a_comment(self):
        lines = [line.strip() for line in SOURCE.splitlines() if line.strip()]
        code_lines = [line for line in lines if not line.startswith("#")]
        assert len(code_lines) == 1

    def test_is_thoroughly_commented(self):
        assert len(_comment_lines()) >= 50

    def test_the_statement_is_preceded_by_an_explanatory_comment(self):
        lines = SOURCE.splitlines()
        statement_index = STATEMENT.lineno - 1
        assert lines[statement_index - 1].startswith("#")

    def test_the_lint_suppression_is_justified(self):
        statement_line = SOURCE.splitlines()[STATEMENT.lineno - 1]
        assert "# noqa: T201 - " in statement_line

    @pytest.mark.parametrize(
        "section",
        [
            "Overview",
            "Execution",
            "Design principles",
            "Output contract",
            "Security considerations",
            "Error handling",
            "Performance",
            "Maintenance notes",
        ],
    )
    def test_documents_section(self, section):
        assert f"# {section}" in SOURCE

    @pytest.mark.parametrize("reference", ["ADR-0008", "ADR-0009", "#57", "#73"])
    def test_references(self, reference):
        assert reference in SOURCE
