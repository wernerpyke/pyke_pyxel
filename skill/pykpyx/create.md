# /pykpyx create

You are executing the `create` sub-command. This scaffolds a new game project in the human's current working directory.

## Arguments

- `<game-name>` (required) — the human-readable game name, e.g. `"My Game"` or `"Space Invaders"`.

If no game name is provided, ask the human for one.

## Name Derivation

From the game name, derive two forms:

- **Spec filename** — UPPERCASE, hyphenated: `"My Game"` → `MY-GAME.md`
- **Game directory** — lowercase, snake_case: `"My Game"` → `my_game`

## Workflow

Execute these steps in order:

### 1. Create directories

Create these directories in the current working directory if they don't already exist:

- `specs/`
- `assets/`
- `scripts/`

### 2. Copy spec template

1. Read `GAME-SPEC-TEMPLATE.md` from `<skill-dir>/docs/GAME-SPEC-TEMPLATE.md`.
2. In the template content, replace `<game title>` in the **Title and Assets** section with the provided game name.
3. Write the result to `specs/<SPEC-FILENAME>` (e.g. `specs/MY-GAME.md`).

If a file already exists at that path, **do not overwrite it**. Warn the human and skip this step.

### 3. Create pyproject.toml

If `pyproject.toml` does not exist in the current working directory, create it with the following steps:

#### 3a. Ask for pyke_pyxel location

Before writing the file, ask the human where `pyke_pyxel` is installed. Present the question like this:

> **Where is pyke_pyxel?** I need this to set up the dependency source.
>
> 1. Local path (editable install) — e.g. `../pyxel` or `/Users/you/Dark/pyxel`
> 2. Git URL — e.g. `https://github.com/user/pyxel.git`
> 3. Skip — I'll configure this myself later
>
> Enter a path, URL, or choice number:

**Default heuristic:** Before asking, check whether a directory exists at `../pyxel` (relative to the current working directory) that contains a `pyke_pyxel/` subdirectory. If it does, offer it as the default:

> Found `pyke_pyxel` at `../pyxel`. Use this? (Y/path/URL/skip)

#### 3b. Write the file

Write `pyproject.toml` with the dependency and source configuration:

```toml
[project]
name = "<game-name>"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pyke-pyxel",
]

[tool.uv.sources]
pyke-pyxel = { path = "<local-path>", editable = true }
```

Adjust the `[tool.uv.sources]` section based on the human's answer:

- **Local path**: `pyke-pyxel = { path = "<path>", editable = true }` — use the path exactly as provided (relative or absolute).
- **Git URL**: `pyke-pyxel = { git = "<url>" }` — no `editable` key.
- **Skip**: Omit the `[tool.uv.sources]` section entirely.

#### 3c. Existing pyproject.toml

If `pyproject.toml` already exists, read it and check whether `pyke-pyxel` appears in the dependencies. If it does not, warn the human: *"`pyke-pyxel` is not listed as a dependency in pyproject.toml. Add it to your dependencies."*

### 4. Create run script

Write `scripts/run_game.sh`:

```bash
#!/usr/bin/env bash
# Run <game_directory>/main.py using uv.
# Usage: ./scripts/run_game.sh [extra pyxel args]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET="$REPO_ROOT/<game_directory>/main.py"

if [ ! -f "$TARGET" ]; then
  echo "Error: target script not found: $TARGET" >&2
  exit 2
fi

export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

exec uv run --project "$REPO_ROOT" pyxel run "$TARGET" "$@"
```

Replace `<game_directory>` with the derived game directory name (snake_case). Also replace it in the comment on line 2.

Make the file executable (`chmod +x`).

If the file already exists, **do not overwrite it**. Skip this step.

### 5. Check for virtual environment

Check whether a `.venv/` directory exists in the current working directory. If it does not, print this hint:

> Run `uv sync` to set up your virtual environment.

### 6. Report

Tell the human what was created. Use this format:

```
Created game project "<game-name>":

  specs/<SPEC-FILENAME>    — game spec (fill this in next)
  assets/                  — place your .pyxres file here
  scripts/run_game.sh      — run script
  pyproject.toml           — project config

Next steps:
  1. Fill in specs/<SPEC-FILENAME> with your game requirements
  2. Run /pykpyx validate specs/<SPEC-FILENAME>
```

Adjust the report if any files were skipped (already existed).
