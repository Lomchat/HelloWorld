#!/usr/bin/env bash
# Stop hook: verify that the canonical greeting is intact before Claude stops.
#
# Exit codes (see https://docs.claude.com/en/docs/claude-code/hooks):
#   0 - the greeting is intact, Claude may stop.
#   2 - the greeting is broken, Claude is asked to fix it before stopping.

set -uo pipefail

payload="$(cat)"

# Avoid infinite loops: if Claude is already continuing because of this hook,
# let it stop.
if grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true' <<<"${payload}"; then
    exit 0
fi

project_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"
python_bin="${project_dir}/.venv/bin/python"
[[ -x "${python_bin}" ]] || python_bin="$(command -v python3 || true)"
[[ -n "${python_bin}" ]] || exit 0

# Compare the raw bytes, including the trailing newline (see #73).
expected="$(printf 'Hello, World!\n' | od -An -c)"
actual="$(cd "${project_dir}" && PYTHONPATH=src "${python_bin}" -m hello_world 2>&1 | od -An -c)"

if [[ "${actual}" != "${expected}" ]]; then
    {
        echo "Integrity check failed: the output is no longer exactly 'Hello, World!\\n'."
        echo "Expected bytes: ${expected}"
        echo "Actual bytes:   ${actual}"
        echo "This violates Critical Invariant #1 in CLAUDE.md. Fix it before finishing."
    } >&2
    exit 2
fi

exit 0
