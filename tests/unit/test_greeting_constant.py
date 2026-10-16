"""Unit tests for :data:`hello_world.hello_world.GREETING`."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import hello_world as package
from hello_world import hello_world
from hello_world.hello_world import GREETING

pytestmark = pytest.mark.unit


def test_value():
    assert GREETING == "Hello, World!"


def test_is_a_str():
    assert type(GREETING) is str


def test_length():
    assert len(GREETING) == 13


def test_is_annotated_as_final():
    assert hello_world.__annotations__["GREETING"] == "Final[str]"


def test_name_follows_the_constant_naming_convention():
    assert "GREETING".isupper()


def test_is_exported_by_the_module():
    assert "GREETING" in hello_world.__all__


def test_is_re_exported_by_the_package():
    assert package.GREETING is GREETING


def test_is_assigned_exactly_once_in_the_source():
    tree = ast.parse(Path(hello_world.__file__).read_text(encoding="utf-8"))
    assignments = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.AnnAssign | ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "GREETING"
            for target in (node.targets if isinstance(node, ast.Assign) else [node.target])
        )
    ]
    assert len(assignments) == 1


def test_is_the_only_string_literal_containing_the_greeting():
    tree = ast.parse(Path(hello_world.__file__).read_text(encoding="utf-8"))
    literals = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and node.value == "Hello, World!"
    ]
    assert literals == ["Hello, World!"]
