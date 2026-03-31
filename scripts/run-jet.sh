#!/usr/bin/env bash
# Run games/rpg/main.py using uv.
# Usage: ./scripts/run-rpg.sh [extra pyxel args]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET="$REPO_ROOT/games/jet/main.py"

if [ ! -f "$TARGET" ]; then
  echo "Error: target script not found: $TARGET" >&2
  exit 2
fi

export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

exec uv run --project "$REPO_ROOT" pyxel run "$TARGET" "$@"
