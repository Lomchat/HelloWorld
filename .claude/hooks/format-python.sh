#!/usr/bin/env bash
# PostToolUse hook: format and auto-fix Python files after every edit.
#
# Reads the hook payload from stdin, extracts the edited file path and runs
# `ruff format` and `ruff check --fix` on it. The hook never blocks: if ruff is
# unavailable or the file is not a Python file, it exits successfully.

set -euo pipefail

# Extract the edited file path from the JSON payload.
file_path="$(python3 -c 'import json, sys; print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))' 2>/dev/null || true)"

# Only Python files are formatted.
[[ "${file_path}" == *.py ]] || exit 0
[[ -f "${file_path}" ]] || exit 0

# Prefer the project virtual environment, fall back to a global installation.
ruff_bin="${CLAUDE_PROJECT_DIR:-.}/.venv/bin/ruff"
if [[ ! -x "${ruff_bin}" ]]; then
    ruff_bin="$(command -v ruff || true)"
fi
[[ -n "${ruff_bin}" ]] || exit 0

"${ruff_bin}" format --quiet "${file_path}" || true
"${ruff_bin}" check --fix --quiet "${file_path}" || true
exit 0
