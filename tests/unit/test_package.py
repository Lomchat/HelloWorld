"""Tests for package-level metadata, public API, layout and code hygiene."""

from __future__ import annotations

import importlib
import inspect
import re
import sys
from pathlib import Path

import pytest

import hello_world
from hello_world import hello_world as core
from tests.helpers import PROJECT_ROOT

pytestmark = pytest.mark.unit

PACKAGE_DIR = Path(hello_world.__file__).resolve().parent
MODULES = ["hello_world", "hello_world.__main__", "hello_world.hello_world"]
SOURCE_FILES = sorted(PACKAGE_DIR.glob("*.py"))

# Official SemVer 2.0.0 regular expression (https://semver.org).
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
)


def _pyproject() -> dict:
    tomllib = pytest.importorskip("tomllib")
    return tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))


class TestPublicApi:
    @pytest.mark.parametrize("name", hello_world.__all__)
    def test_exported_name_exists(self, name):
        assert hasattr(hello_world, name)

    def test_package_exports(self):
        assert hello_world.__all__ == ["GREETING", "__version__", "greet", "main"]

    def test_module_exports(self):
        assert core.__all__ == ["GREETING", "greet", "main"]

    @pytest.mark.parametrize("name", ["GREETING", "greet", "main"])
    def test_package_re_exports_the_module_objects(self, name):
        assert getattr(hello_world, name) is getattr(core, name)

    @pytest.mark.parametrize("exports", [hello_world.__all__, core.__all__])
    def test_exports_are_sorted(self, exports):
        assert exports == sorted(exports)

    @pytest.mark.parametrize("exports", [hello_world.__all__, core.__all__])
    def test_exports_have_no_duplicates(self, exports):
        assert len(exports) == len(set(exports))


class TestVersion:
    def test_version_is_a_string(self):
        assert isinstance(hello_world.__version__, str)

    def test_version_follows_semver(self):
        assert SEMVER_PATTERN.match(hello_world.__version__)

    def test_version_matches_the_latest_changelog_entry(self):
        changelog = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        released = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", changelog, flags=re.MULTILINE)
        assert released, "CHANGELOG.md must contain at least one released version"
        assert released[0] == hello_world.__version__


class TestPackaging:
    def test_source_tree_contains_only_the_expected_modules(self):
        assert [path.name for path in SOURCE_FILES] == [
            "__init__.py",
            "__main__.py",
            "hello_world.py",
        ]

    def test_py_typed_marker_is_present(self):
        assert (PACKAGE_DIR / "py.typed").is_file()

    def test_has_no_runtime_dependencies(self):
        assert _pyproject()["project"]["dependencies"] == []

    def test_console_script_points_to_main(self):
        target = _pyproject()["project"]["scripts"]["hello-world"]
        module_name, _, attribute = target.partition(":")
        assert getattr(importlib.import_module(module_name), attribute) is core.main

    def test_supported_python_version_is_declared(self):
        assert _pyproject()["project"]["requires-python"] == ">=3.10"

    def test_running_interpreter_is_supported(self):
        assert sys.version_info >= (3, 10)


class TestCodeHygiene:
    @pytest.mark.parametrize("module_name", MODULES)
    def test_every_module_has_a_docstring(self, module_name):
        assert inspect.getdoc(importlib.import_module(module_name))

    @pytest.mark.parametrize("function", [core.greet, core.main], ids=["greet", "main"])
    def test_every_public_function_has_a_docstring(self, function):
        assert inspect.getdoc(function)

    @pytest.mark.parametrize("path", SOURCE_FILES, ids=lambda path: path.name)
    def test_source_files_use_postponed_annotations(self, path):
        assert "from __future__ import annotations" in path.read_text(encoding="utf-8")

    @pytest.mark.parametrize("path", SOURCE_FILES, ids=lambda path: path.name)
    def test_source_files_end_with_a_newline(self, path):
        assert path.read_text(encoding="utf-8").endswith("\n")

    @pytest.mark.parametrize("path", SOURCE_FILES, ids=lambda path: path.name)
    def test_source_files_are_ascii_only(self, path):
        assert path.read_text(encoding="utf-8").isascii()

    @pytest.mark.parametrize("path", SOURCE_FILES, ids=lambda path: path.name)
    def test_source_files_have_no_trailing_whitespace(self, path):
        lines = path.read_text(encoding="utf-8").splitlines()
        assert [line for line in lines if line != line.rstrip()] == []
