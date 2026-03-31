# /pykpyx generate

You are executing the `generate` sub-command. This generates working game code from a validated spec using the `pyke_pyxel` engine.

## Arguments

- `[path/to/spec.md]` (required) — path to the game spec file.
- `[target-dir]` (optional) — output directory for generated code. Default: derived from the spec **filename** (lowercase, snake_case, e.g. `MY-GAME.md` → `my_game/`). This matches the directory name used by the `create` command.
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
- At least one entity is defined in the Entities section
- At least one sprite is defined (static or animated)
- Resources path is specified
- The `.pyxres` file exists at the specified path (resolved relative to the project root)

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

### Important: Interpreting `colrow()` notation

The spec uses `colrow(<col>,<row>)` notation (e.g. `colrow(3,5)`) to make it unambiguous that the first value is a **column** and the second is a **row**. When generating code:

- Strip the `colrow(` prefix and `)` suffix to extract the two integer values.
- The first value is the column, the second is the row.
- Map `colrow(c,r)` to `coord(c, r)` in generated code.
- Also accept bare `(<col>,<row>)` as valid (backwards compatibility), interpreting the first value as column and the second as row.

### Important: Interpreting empty values

The human may express "no action" or "not applicable" in several equivalent ways. Treat all of the following as meaning **no value / not applicable**:

- `none`
- `n/a`
- Empty value (key present but blank, e.g. `- **Released:**`)
- Absent key (sub-item omitted entirely)

When generating code, skip these — do not generate a handler or logic for a field that has no value.

### 6. Clarify ambiguity

Before generating code, review the spec's natural-language sections (**Game Start**, **Game Update**, **Entity descriptions**) for ambiguity. If any requirement could be interpreted multiple ways, **stop and ask the human** before proceeding. Do not guess.

Examples that require clarification:
- Positions described in relative terms without coordinates (e.g. "centre of the screen") — ask for exact `colrow(<col>,<row>)` or confirm you should calculate from window/tile size
- Vague timing or conditions (e.g. "after a while", "sometimes") — ask for specific frame counts or conditions
- References to concepts not defined in the spec

If the validation report exists and contains ambiguity warnings, address those specifically.

After all clarifications are resolved, **write them to the spec's "Claude Clarifications" section**. For each clarification, append an entry:

```markdown
### <short topic>
- **Question:** <the question you asked>
- **Answer:** <the human's answer>
- **Applied to:** <which spec section/field this affects>
```

This ensures the spec is a complete record of all design decisions, including those resolved during generation.

### 7. Generate code

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

1. Generate `GameState` dataclass:
   - Include all human-declared fields from the spec's **Game State** section with their types and defaults.
   - For each entity defined in the **Entities** section, automatically add a `<entity_name>_sprite: Sprite | None = None` field. The human does not declare these — the skill infers them.
   - Add any other internal state fields needed by the generated logic (e.g. timers, flags).
2. Create module-level `STATE = GameState()`.
3. Generate `start()` handler:
   - Call `game_load.load(game, STATE)` (or RPG-specific load functions).
   - Register keyboard signal handlers using `game.keyboard.signal_for_key()` for each key in the spec's **Input > Keyboard** section. For keys that have both **Pressed** and **Released** actions, register separate handlers for each event.
   - Set any initial state from the **Game Start** section.
4. Generate `update()` handler:
   - Implement per-frame logic from the **Game Update** section.
   - For RPGGame: include the arrow-key movement boilerplate (press/release pattern for UP, DOWN, LEFT, RIGHT).
5. Generate input handlers:
   - For each keyboard key, generate up to two handlers based on the spec's **Pressed** and **Released** sub-items:
     - `<key>_pressed(game)` — logic from the **Pressed** action. Omit if Pressed is `none`.
     - `<key>_released(game)` — logic from the **Released** action. Omit if Released is `none`.
   - Input actions reference entities by name (e.g. "Player"). Use the entity's sprite reference from `STATE` (e.g. `STATE.player_sprite`) and the entity's speed from the Entities section to implement the action.
   - Mouse handlers (`mouse_down`, `mouse_move`) if mouse input is defined.
6. For RPGGame: generate `player_blocked()` and `enemy_blocked()` from the **Collision and Blocking** section.
7. Add any additional signal handlers described in the spec.

#### `game_load.py`

Starting from the template:

**For `Game` type:**

1. Generate a `load(game: Game, state)` function that:
   - Creates each sprite defined in the spec (using `Sprite`, `Animation`, `TextSprite` as appropriate). When creating `Animation` instances, set `loop=True` by default. If the spec marks an animation as `no-loop`, set `loop=False`.
   - Positions sprites using `coord()`.
   - Adds sprites to the game via `game.add_sprite()`. **Exception:** `TextSprite` instances used for HUD elements must be added via `game.hud.add_text()`, not `game.add_sprite()` or `game.hud.add_sprite()`. Only `Sprite` and `CompoundSprite` go through `game.hud.add_sprite()`.
   - For each entity in the **Entities** section, assign the created sprite to the corresponding `state.<entity_name>_sprite` field. Use the entity's **Sprite** field to find the matching sprite.
   - Apply entity properties: use the entity's **Speed** (from the Entities section) when configuring movement for the sprite.

**For `RPGGame` type:**

1. Generate `player_sprite()` — returns the player's `MovableSprite` with directional animations set up per the spec's **RPG > Player** section.
2. Generate `build_room(room: Room)` — creates walls, doors, and obstacles per the **Room Layout** section. Places enemies per the **Enemies** sub-section.
3. Generate `set_player_position(player: Player)` — sets starting position from **Player Start**.
4. Generate any additional sprite factory functions needed.

#### HUD elements

If the spec has a **HUD** section, generate HUD setup in `game_load.py` (inside the `load()` function):

1. For each HUD element with type **text** or **score**: create a `TextSprite` and add it via `game.hud.add_text()`.
2. For each HUD element with type **indicator** backed by a `Sprite`: add it via `game.hud.add_sprite()`.
3. Position each element using `coord()` from the spec's `colrow()` value.
4. Store references in `state` fields so `game_loop.py` can update them dynamically.

**Critical:** Never pass a `TextSprite` to `game.hud.add_sprite()` or `game.add_sprite()` — always use `game.hud.add_text()`.

#### `sprites.py` (conditional)

Only create this file when the spec defines **4 or more sprites**. In that case:

1. Move sprite creation logic out of `game_load.py` into `sprites.py`.
2. Export sprite factory functions (one per sprite or logical group).
3. Have `game_load.py` import from `sprites` and call the factory functions.

### 8. Write files

1. Create the target directory if it doesn't exist.
2. Write each generated file to the target directory.
3. Add an `__init__.py` file (empty) so the directory is importable as a Python module.

### 9. Syntax check

Run `python -m py_compile <file>` on each generated `.py` file using the Bash tool. Report any syntax errors. If errors are found, fix them before proceeding.

### 10. Report

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

- [ ] All `colrow()` spec values correctly mapped to `coord()` calls with 1-indexed positive integers
- [ ] All signal handler signatures match the table in SKILL.md
- [ ] `GameState` uses `@dataclass` with typed fields and defaults
- [ ] No `AnimationFactory` or `SpriteFactory` usage
- [ ] Keyboard signals registered in `start()`, not at module level
- [ ] Imports follow standard order: stdlib → third-party → local
- [ ] No unused imports
- [ ] Never access `game.settings` — `Game` has no public `settings` attribute. Use `GameSettings.get()` to read settings at runtime
- [ ] RPG games include arrow-key movement boilerplate
- [ ] Resources path uses `Path(__file__).parent.parent.resolve()` to resolve relative to the project root (not the game package directory)
