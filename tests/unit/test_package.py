"""Tests for package-level metadata, layout and code hygiene."""

from __future__ import annotations

import importlib
import inspect
import re
import sys
from pathlib import Path

import pytest

import hello_world
from tests.helpers import PROJECT_ROOT

pytestmark = pytest.mark.unit

PACKAGE_DIR = Path(hello_world.__file__).resolve().parent
SOURCE_FILES = sorted(PACKAGE_DIR.glob("*.py"))

#: Modules that contain Python code besides the core statement.
SUPPORT_FILES = [path for path in SOURCE_FILES if path.name != "hello_world.py"]

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
    def test_package_exports_only_the_version(self):
        assert hello_world.__all__ == ["__version__"]

    @pytest.mark.parametrize("name", ["greet", "main", "GREETING"])
    def test_removed_names_are_not_exported(self, name):
        assert not hasattr(hello_world, name)

    def test_importing_the_package_has_no_side_effects(self, capsys):
        importlib.reload(hello_world)
        assert capsys.readouterr() == ("", "")


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

    def test_declares_no_console_script(self):
        assert "scripts" not in _pyproject()["project"]

    def test_supported_python_version_is_declared(self):
        assert _pyproject()["project"]["requires-python"] == ">=3.10"

    def test_running_interpreter_is_supported(self):
        assert sys.version_info >= (3, 10)


class TestCodeHygiene:
    @pytest.mark.parametrize("module_name", ["hello_world", "hello_world.__main__"])
    def test_support_modules_have_a_docstring(self, module_name):
        assert inspect.getdoc(importlib.import_module(module_name))

    @pytest.mark.parametrize("path", SUPPORT_FILES, ids=lambda path: path.name)
    def test_support_modules_use_postponed_annotations(self, path):
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

    @pytest.mark.parametrize("path", SOURCE_FILES, ids=lambda path: path.name)
    def test_print_is_called_at_most_once(self, path):
        lines = path.read_text(encoding="utf-8").splitlines()
        code = [line for line in lines if not line.lstrip().startswith("#")]
        assert "\n".join(code).count("print(") <= 1
