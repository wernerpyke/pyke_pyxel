#!/usr/bin/env bash
# Run pytest tests using the project's .venv.
# Usage: ./scripts/run-tests.sh [pytest args]
# Examples:
#   ./scripts/run-tests.sh              # Run all tests
#   ./scripts/run-tests.sh -v           # Verbose output
#   ./scripts/run-tests.sh tests/test_coord.py  # Run specific file

set -euo pipefail

# Resolve repo root (script is located in scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TESTS_DIR="$REPO_ROOT/tests"

if [ ! -d "$TESTS_DIR" ]; then
  echo "Error: tests directory not found: $TESTS_DIR" >&2
  exit 2
fi

# Ensure the repository root is on PYTHONPATH so local packages (like pyke_pyxel) can be imported
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

# Auto-activate the project's virtualenv if an activate script exists.
ACTIVATE="$REPO_ROOT/.venv/bin/activate"
if [ -f "$ACTIVATE" ]; then
  # shellcheck source=/dev/null
  source "$ACTIVATE"
fi

# Prefer the project's venv pytest
VENV_PYTEST="$REPO_ROOT/.venv/bin/pytest"

if [ -x "$VENV_PYTEST" ]; then
  exec "$VENV_PYTEST" "$TESTS_DIR" "$@"
fi

# Fallback to system pytest
if command -v pytest >/dev/null 2>&1; then
  exec pytest "$TESTS_DIR" "$@"
fi

# Fallback to python -m pytest
VENV_PYTHON="$REPO_ROOT/.venv/bin/python"
if [ -x "$VENV_PYTHON" ]; then
  exec "$VENV_PYTHON" -m pytest "$TESTS_DIR" "$@"
fi

if command -v python3 >/dev/null 2>&1; then
  exec python3 -m pytest "$TESTS_DIR" "$@"
fi

echo "No suitable pytest found. Install pytest: pip install pytest" >&2
exit 3
