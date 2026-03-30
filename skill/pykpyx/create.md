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

If `pyproject.toml` does not exist in the current working directory, create it:

```toml
[project]
name = "<game-directory-name>"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pyke-pyxel",
]
```

If `pyproject.toml` already exists, read it and check whether `pyke-pyxel` appears in the dependencies. If it does not, warn the human: *"`pyke-pyxel` is not listed as a dependency in pyproject.toml. Add it to your dependencies."*

### 4. Create run script

Write `scripts/run_game.sh`:

```bash
#!/bin/bash
cd "$(dirname "$0")/.." && python -m <game_directory>.main
```

Replace `<game_directory>` with the derived game directory name (snake_case).

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
