#!/usr/bin/env bash
# Generate API documentation using pydoc-markdown via uv.
# Usage: ./scripts/update-docs.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

uv run --project "$REPO_ROOT" pydoc-markdown > "$REPO_ROOT/docs/pyke_pyxel_API.md"
