---
name: pykpyx
description: "pyke_pyxel game creation skill. Sub-commands: create, validate, generate, update. Use /pykpyx <command> to scaffold, validate, generate, or update games."
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: <command> [args...]
---

# pykpyx — pyke_pyxel Game Creation Skill

You are the `pykpyx` skill. You help the human scaffold, validate, generate, and update games built with the `pyke_pyxel` engine.

**Important:** Before executing any sub-command, note the path to this skill directory (the directory containing this `SKILL.md` file). You will need it to locate templates, docs, and sub-command instruction files. References to `<skill-dir>` below mean this directory.

---

## Engine Conventions

All sub-commands must respect these rules when generating or validating code.

### Coordinate system

- Grid coordinates use `coord(col, row)` and are **1-indexed** — `coord(1, 1)` is the top-left tile.
- Never use `0` for `col` or `row` in `coord()` or `area()`.
- Pixel coordinates (`x`, `y`) are 0-indexed and used internally by Pyxel — game specs and generated code use grid coordinates.

### Signal-driven architecture

- Games wire logic through `Signals.connect(signal, handler)` — not through inheritance.
- Do not subclass `Game` or `RPGGame`.
- All game-specific logic lives in handler functions connected to signals.

### Three-file structure

Every generated game consists of exactly three files (plus optional `sprites.py` for games with many sprites):

| File | Responsibility |
|------|---------------|
| `main.py` | Settings, game instantiation, signal wiring, `game.start()` |
| `game_loop.py` | `GameState` dataclass, `start()` and `update()` handlers, input handlers, signal handlers |
| `game_load.py` | Sprite creation, positioning, adding to game. For RPG: room construction, player sprite factory |

### GameState pattern

- Define `@dataclass class GameState` in `game_loop.py` with all mutable game state.
- Create a module-level `STATE = GameState()` instance.
- Sprite references that handlers need use the `Type | None = None` pattern (e.g. `player_sprite: Sprite | None = None`).
- `game_load` populates sprite references on `STATE`; `game_loop` reads them.
- Do not use module-level `global` variables for sprite references.

### Signal handler signatures

| Signal | Handler signature |
|--------|------------------|
| `Signals.GAME.WILL_START` | `(game: Game)` |
| `Signals.GAME.UPDATE` | `(game: Game)` |
| `Signals.MOUSE.DOWN` | `(game: Game, value: tuple[int, int])` |
| `Signals.MOUSE.MOVE` | `(game: Game, value: tuple[int, int])` |
| `Signals.MOUSE.UP` | `(game: Game, value: tuple[int, int])` |
| `Signals.PLAYER.BLOCKED` | `(player: Player, value: Sprite \| None)` |
| `Signals.PLAYER.MOVED` | `(player: Player)` |
| `Signals.ENEMY.BLOCKED` | `(enemy: Enemy, value: Sprite)` |
| `Signals.ENEMY.STOPPED` | `(enemy: Enemy)` |
| Custom keyboard signals | `(game: Game)` |

### Sprite hierarchy

- `Sprite` — base animated entity (all game types)
- `TextSprite` — text rendered via Pyxel font (for HUD elements)
- `CompoundSprite` — multi-tile grid sprite
- `MovableSprite` — 4-directional movement with animations (RPG only)
- `OpenableSprite` — two-state objects like doors and chests (RPG only)

### Code generation rules

- Do **not** use `AnimationFactory` or `SpriteFactory` — create `Animation` instances directly. The skill has full context from the spec.
- Keyboard signal registration (`game.keyboard.signal_for_key()`) must happen inside the `start()` handler — it needs the `game` instance and cannot be done at module level.
- RPG games always include the arrow-key movement boilerplate in `update()`.
- Sprites are added to the game via `game.add_sprite()` or `Signals.send_add_sprite()`.

---

## Sub-command Routing

Parse the first argument after `/pykpyx` to determine the sub-command. Pass remaining arguments through to the sub-command.

- **`create`** — Read [create.md](create.md) and follow its instructions.
- **`validate`** — Read [validate.md](validate.md) and follow its instructions.
- **`generate`** — Read [generate.md](generate.md) and follow its instructions.
- **`update`** — Read [update.md](update.md) and follow its instructions.

If no argument is provided, or the argument is not recognised, display this help:

```
pykpyx — pyke_pyxel Game Creation Skill

Available commands:

  /pykpyx create <game-name>            Scaffold a new game project
  /pykpyx validate [path/to/spec.md]    Validate a game spec
  /pykpyx generate [path/to/spec.md]    Generate game code from a validated spec
  /pykpyx update [path/to/spec.md]      Apply incremental changes to an existing game

Workflow:
  1. /pykpyx create "My Game"           — creates folders and spec template
  2. Fill in specs/MY-GAME.md           — describe your game
  3. /pykpyx validate specs/MY-GAME.md  — check spec for errors
  4. /pykpyx generate specs/MY-GAME.md  — generate working game code
  5. /pykpyx update specs/MY-GAME.md    — apply changes after editing the spec
```
