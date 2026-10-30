#!/usr/bin/env bash
# =============================================================================
# verify_output.sh - Verify the output of hello-world byte by byte.
# =============================================================================
#
# Usage:
#   ./scripts/verify_output.sh
#
# Exit codes:
#   0 - The output is exactly "Hello, World!\n" and stderr is empty.
#   1 - The output deviates from the expected bytes.

set -euo pipefail

readonly PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly EXPECTED_HEX="48656c6c6f2c20576f726c64210a"

# Prefer the project virtual environment when available.
if [[ -x "${PROJECT_DIR}/.venv/bin/python" ]]; then
    PYTHON="${PROJECT_DIR}/.venv/bin/python"
else
    PYTHON="$(command -v python3)"
fi

stderr_file="$(mktemp)"
trap 'rm -f "${stderr_file}"' EXIT

# Capture stdout as hex and stderr separately.
actual_hex="$(PYTHONPATH="${PROJECT_DIR}/src" "${PYTHON}" -m hello_world 2>"${stderr_file}" | od -An -tx1 | tr -d ' \n')"

status=0

if [[ "${actual_hex}" == "${EXPECTED_HEX}" ]]; then
    echo "✅ stdout: exactly 'Hello, World!\\n' (14 bytes)"
else
    echo "❌ stdout: unexpected bytes"
    echo "   expected: ${EXPECTED_HEX}"
    echo "   actual:   ${actual_hex}"
    status=1
fi

if [[ ! -s "${stderr_file}" ]]; then
    echo "✅ stderr: empty"
else
    echo "❌ stderr: not empty"
    sed 's/^/   /' "${stderr_file}"
    status=1
fi

exit "${status}"
