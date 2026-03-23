#!/usr/bin/env bash
# Run pytest tests using uv.
# Usage: ./scripts/run-tests.sh [pytest args]
# Examples:
#   ./scripts/run-tests.sh              # Run all tests
#   ./scripts/run-tests.sh -v           # Verbose output
#   ./scripts/run-tests.sh tests/test_coord.py  # Run specific file

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

exec uv run --project "$REPO_ROOT" pytest "$REPO_ROOT/tests" "$@"
