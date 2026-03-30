# /pykpyx generate

You are executing the `generate` sub-command. This generates working game code from a validated spec using the `pyke_pyxel` engine.

## Arguments

- `[path/to/spec.md]` (required) — path to the game spec file.
- `[target-dir]` (optional) — output directory for generated code. Default: derived from the spec's Title field (snake_case, e.g. `"My Game"` → `my_game/`).
- `--force` (optional flag) — overwrite existing game code if present.

If no spec path is provided, use the same auto-discovery logic as the validate command (look in `specs/`, excluding `*-VALIDATION.md`).

## Workflow

### 1. Check for existing code

Check whether the target directory exists and contains `.py` files.

- **Without `--force`:** Stop and tell the human: *"Game code already exists in `<target-dir>/`. Use `/pykpyx update` to apply changes, or `/pykpyx generate --force` to regenerate from scratch."*
- **With `--force`:** Warn the human that all `.py` files in the target directory will be overwritten, then proceed.

### 2. Quick validation

Read the spec file and check these critical rules (abort on failure):

- Game Type section exists and value is `Game` or `RPGGame`
- Title is non-empty
- At least one sprite is defined (static or animated)
- Resources path is specified

If any of these fail, stop and tell the human to fix the spec. Recommend running `/pykpyx validate` first.

### 3. Resolve supplementary specs

Check the spec for `@specs/` references or markdown hyperlinks to other `.md` files. If found, read those files to gather the full requirements.

### 4. Select templates

Based on the Game Type:

- **`Game`** — read the three template files from `<skill-dir>/templates/game/`
- **`RPGGame`** — read the three template files from `<skill-dir>/templates/rpg/`

Read all three template files: `main.py`, `game_loop.py`, `game_load.py`.

### 5. Load engine documentation

Read these two files for API context. They live in the `pyke_pyxel` repository at `<skill-dir>/../../docs/`:

- `<skill-dir>/../../docs/README.md` — usage guide with lifecycle, patterns, and examples
- `<skill-dir>/../../docs/pyke_pyxel_API.md` — auto-generated API reference

These are essential for generating correct code. If either file cannot be found, warn the human but continue — use the shared context from `SKILL.md` as a fallback.

### 6. Generate code

Use the templates as your starting point. Read each template, understand its structure, then **rewrite** it with the spec's requirements filled in. Do not use string substitution — write complete, correct Python code.

#### `main.py`

Starting from the template:

1. Apply all **Settings** from the spec to a `GameSettings()` object.
2. Set the game **Title** and **Resources** path.
3. Set sprite transparency colour if specified.
4. Wire all required **signals** using `Signals.connect()`:
   - Always: `GAME.WILL_START` → `game_loop.start`, `GAME.UPDATE` → `game_loop.update`
   - If mouse input defined: `MOUSE.DOWN`, `MOUSE.MOVE`, `MOUSE.UP` as needed → corresponding `game_loop` handlers
   - If RPGGame: `PLAYER.BLOCKED` → `game_loop.player_blocked`, `ENEMY.BLOCKED` → `game_loop.enemy_blocked`
5. For RPGGame: include `game_load.build_room()`, `game.set_player()`, and `game_load.set_player_position()` calls before `game.start()`.
6. End with `game.start()`.

#### `game_loop.py`

Starting from the template:

1. Generate `GameState` dataclass from the spec's **Game State** section. Include all declared fields with their types and defaults.
2. Create module-level `STATE = GameState()`.
3. Generate `start()` handler:
   - Call `game_load.load(game, STATE)` (or RPG-specific load functions).
   - Register keyboard signal handlers using `game.keyboard.signal_for_key()` for each key in the spec's **Input > Keyboard** section.
   - Set any initial state from the **Game Start** section.
4. Generate `update()` handler:
   - Implement per-frame logic from the **Game Update** section.
   - For RPGGame: include the arrow-key movement boilerplate (press/release pattern for UP, DOWN, LEFT, RIGHT).
5. Generate input handlers:
   - One function per keyboard key that has game logic (connected via `signal_for_key` in `start()`).
   - Mouse handlers (`mouse_down`, `mouse_move`) if mouse input is defined.
6. For RPGGame: generate `player_blocked()` and `enemy_blocked()` from the **Collision and Blocking** section.
7. Add any additional signal handlers described in the spec.

#### `game_load.py`

Starting from the template:

**For `Game` type:**

1. Generate a `load(game: Game, state)` function that:
   - Creates each sprite defined in the spec (using `Sprite`, `Animation`, `TextSprite` as appropriate).
   - Positions sprites using `coord()`.
   - Adds sprites to the game via `game.add_sprite()`.
   - Populates sprite references on `state` (e.g. `state.player_sprite = sprite`).

**For `RPGGame` type:**

1. Generate `player_sprite()` — returns the player's `MovableSprite` with directional animations set up per the spec's **RPG > Player** section.
2. Generate `build_room(room: Room)` — creates walls, doors, and obstacles per the **Room Layout** section. Places enemies per the **Enemies** sub-section.
3. Generate `set_player_position(player: Player)` — sets starting position from **Player Start**.
4. Generate any additional sprite factory functions needed.

#### `sprites.py` (conditional)

Only create this file when the spec defines **4 or more sprites**. In that case:

1. Move sprite creation logic out of `game_load.py` into `sprites.py`.
2. Export sprite factory functions (one per sprite or logical group).
3. Have `game_load.py` import from `sprites` and call the factory functions.

### 7. Write files

1. Create the target directory if it doesn't exist.
2. Write each generated file to the target directory.
3. Add an `__init__.py` file (empty) so the directory is importable as a Python module.

### 8. Syntax check

Run `python -m py_compile <file>` on each generated `.py` file using the Bash tool. Report any syntax errors. If errors are found, fix them before proceeding.

### 9. Report

Tell the human what was generated:

```
Generated game "<title>" in <target-dir>/:

  <target-dir>/main.py        — settings, signals, game start
  <target-dir>/game_loop.py   — game state, handlers, input
  <target-dir>/game_load.py   — sprite creation and setup
  <target-dir>/__init__.py    — package init

Run with:
  ./scripts/run_game.sh
  — or —
  python -m <target-dir>.main

To make changes, edit specs/<SPEC-NAME>.md and run:
  /pykpyx update specs/<SPEC-NAME>.md
```

Include `sprites.py` in the listing if it was created.

## Code Quality Checklist

Before writing the final files, verify your generated code against these rules:

- [ ] All `coord()` values use 1-indexed positive integers
- [ ] All signal handler signatures match the table in SKILL.md
- [ ] `GameState` uses `@dataclass` with typed fields and defaults
- [ ] No `AnimationFactory` or `SpriteFactory` usage
- [ ] Keyboard signals registered in `start()`, not at module level
- [ ] Imports follow standard order: stdlib → third-party → local
- [ ] No unused imports
- [ ] RPG games include arrow-key movement boilerplate
- [ ] Resources path uses `Path(__file__).parent.resolve()` for portability
