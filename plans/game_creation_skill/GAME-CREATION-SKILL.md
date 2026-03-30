# Game Creation Skill — Design Plan

**Status:** Draft
**Date:** 2026-03-30

## Goal

Build a reusable Claude Code **skill** that generates working games from a markdown specification using the `pyke_pyxel` engine. The skill lives in this repository (`pyxel`) and generates code into the **current working directory** — wherever the human launches Claude Code. Once this skill is complete, the companion `claude_pyxel` repository will be deleted; this skill fully replaces it.

---

## 1. Skill Commands

The skill is split into **four user-invocable commands** that map to the natural workflow phases:

| Command            | Purpose                                                                                                                   | Trigger                                                  |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `/pykpyx-create`   | Scaffold a new game project — create required sub-folders and a named spec file from the template                         | Manual (`/pykpyx-create <game-name>`)                    |
| `/pykpyx-validate` | Validate a game definition markdown file against the template; iterate with the human until it is complete and consistent | Manual (`/pykpyx-validate path/to/spec.md`)              |
| `/pykpyx-generate` | Generate game code from a validated spec into a target directory                                                          | Manual (`/pykpyx-generate path/to/spec.md [target-dir]`) |
| `/pykpyx-update`   | Apply incremental changes to an existing game — either from an updated spec or from natural-language instructions         | Manual (`/pykpyx-update path/to/spec.md [target-dir]`)   |

All four are `disable-model-invocation: true` because they produce side-effects (file creation/modification) and the human should control when they run.

---

## 2. Folder Structure

### 2.1 Skill source (in this repo)

```
skill/
├── SKILL.md                    # /pykpyx — top-level entry point (shared context, sub-command routing)
├── docs/
│   ├── GAME-SPEC-TEMPLATE.md  # Stand-alone template for humans to copy and fill in
│   ├── SKILL-USAGE.md         # Human-readable usage guide for the skill
│   └── VALIDATION-CHECKLIST.md # Validation rules read by /pykpyx-validate at runtime
├── pykpyx-create/
│   └── SKILL.md                # /pykpyx-create — project scaffolding
├── pykpyx-validate/
│   └── SKILL.md                # /pykpyx-validate — validation & iteration
├── pykpyx-generate/
│   ├── SKILL.md                # /pykpyx-generate — code generation
│   ├── templates/
│   │   ├── base_main.py        # Boilerplate for Game-type games
│   │   ├── rpg_main.py         # Boilerplate for RPGGame
│   │   ├── rpg_game_loop.py    # RPG handler stubs
│   │   ├── rpg_game_load.py    # RPG loading stubs
│   │   └── cell_auto_main.py   # Boilerplate for CellAutoGame (deferred — see §9)
└── pykpyx-update/
    └── SKILL.md                # /pykpyx-update — incremental changes
```

The top-level `SKILL.md` serves as the `/pykpyx` command. It provides shared context (engine conventions, coordinate rules, signal patterns) and routes the human to the appropriate sub-command. When invoked without arguments it describes the available workflow.

> **Note:** The templates are *not* Jinja/string-interpolation files. They are complete, minimal, working Python files that Claude reads as a starting point and then modifies per the spec. This keeps them human-readable and testable.

### 2.2 How the skill is discovered

The skill directory is made available in the human's working directory via one of:

- **Symlink**: `.claude/skills/pykpyx-validate -> /path/to/pyxel/skill/pykpyx-validate` (repeat for each command)
- **Copy**: copy the `skill/` folder into the working directory's `.claude/skills/`

The recommended approach during development is **symlink** so edits in the engine repo are picked up immediately.

---

## 3. Human-side Folder Structure

The skill generates into the **current working directory** (wherever the human launches Claude Code). It expects this layout:

```
./                              # Human's working directory
├── .claude/
│   └── skills/ -> ...          # Symlinks or copies of skill/
├── specs/
│   ├── MY-GAME.md              # Primary game spec (per template)
│   └── MY-GAME-PHASE2.md       # Optional: incremental spec (see §5)
├── my_game/                    # Generated game code (name from spec title)
│   ├── main.py
│   ├── game_loop.py            # Signal handler implementations
│   ├── game_load.py            # Sprite factories and setup
│   └── sprites.py              # When sprite count warrants a separate file
├── assets/
│   └── resources.pyxres        # Pyxel resource file (human-provided)
├── scripts/
│   └── run_game.sh             # Game runner script
└── pyproject.toml              # Depends on pyke-pyxel
```

**Conventions enforced by the skill:**

- Spec markdown files use UPPERCASE filenames (e.g. `MY-GAME.md`, not `my-game.md`).
- Spec files live in `specs/` (or are passed as an explicit path).
- The game directory name is derived from the spec title (snake_cased).
- Assets are referenced by relative path from the game directory; the spec's `Resources` field is the source of truth.
- The skill will **not** create or modify `.pyxres` files — those are authored by the human in the Pyxel editor.

---

## 4. Workflow Detail

### Step 1: Scaffold (`/pykpyx-create`)

```
Human: /pykpyx-create "My Game"
```

The skill:

1. Creates the required sub-folders in the current working directory (if they don't already exist):
   - `specs/`
   - `assets/`
   - `scripts/`
2. Copies `GAME-SPEC-TEMPLATE.md` from `skill/docs/` into `specs/`, renamed to match the game name in UPPERCASE (e.g. `specs/MY-GAME.md`).
3. Creates `pyproject.toml` (if one doesn't already exist) with the game name and `pyke-pyxel` as a dependency. If one already exists, checks that `pyke-pyxel` is listed as a dependency and warns if it is missing.
4. Creates `scripts/run_game.sh` — a one-liner that runs the game's `main.py`.
5. Checks for a `.venv` directory. If none is found, prints a hint: *"Run `uv sync` to set up your environment."*
6. Reports the created structure and tells the human to fill in the spec file.

### Step 2: Write spec (`/pykpyx-validate`)

```
Human fills in specs/MY-GAME.md
Human: /pykpyx-validate specs/MY-GAME.md
```

The skill:

1. Reads `skill/docs/VALIDATION-CHECKLIST.md` to load the current set of validation rules.
2. Reads the spec file.
3. Applies each validation rule from the checklist against the spec.
4. Writes a validation report to `specs/` as a markdown file named after the spec with a `-VALIDATION` suffix (e.g. `specs/MY-GAME-VALIDATION.md`). The report contains:
   - Pass/fail status for each rule
   - Issues and suggested fixes
   - Summary of what will be generated (file list, sprite count, signal count) if all rules pass
5. Reports the location of the validation file to the human.

### Step 3: Generate (`/pykpyx-generate`)

```
Human: /pykpyx-generate specs/MY-GAME.md
```

The skill:

1. Checks whether game code already exists in the target directory. If it does, **stops** and tells the human to use `/pykpyx-update` instead (unless `--force` is passed — see §5.4).
2. Re-validates the spec (quick pass — errors abort).
3. Determines the game type and selects the matching template(s).
4. Reads the template files, `@docs/README.md`, and `@docs/pyke_pyxel_API.md` for API context.
5. Generates game code:
   - **`main.py`** — settings, game instantiation, signal wiring, `game.start()`
   - **`game_loop.py`** — handler implementations for all connected signals
   - **`game_load.py`** — sprite factory functions, setup
   - **`sprites.py`** — only created when the spec defines ≥ 4 sprites
6. Writes files to the target directory.
7. Attempts to syntax-check the output (`python -m py_compile`).
8. Reports what was created and how to run it.

### Step 4: Iterate (`/pykpyx-update`)

```
Human: /pykpyx-update specs/MY-GAME.md
  or
Human: /pykpyx-update "Add a scoring HUD that shows points in the top-left"
```

See §5 below for how incremental development works.

---

## 5. Incremental Development

### The core question

> Does the skill regenerate game code from scratch each time, or can enhancements be phased in?

**Answer: Incremental by default, regenerate on request.**

The `/pykpyx-update` command works as follows:

### 5.1 Spec-driven updates

The human edits the existing spec file (or adds a new one) and runs `/pykpyx-update`. The skill:

1. Checks for a corresponding validation report (e.g. `specs/MY-GAME-VALIDATION.md`). If none is found, or if the spec file is newer than the validation report, **warns** the human that the updated spec has not been validated and recommends running `/pykpyx-validate` first. Proceeds only if the human confirms.
2. Reads the **current game code** in the target directory.
2. Reads the **updated spec** (or a new supplementary spec — see §5.3).
3. Diffs the spec against what is already implemented (by reading the code, not by storing prior state).
4. Generates **edits** to the existing files — not a full rewrite.
5. If a change requires new files (e.g. adding enemies/ module), creates them.
6. Reports what changed.

### 5.2 Natural-language updates *(future consideration)*

> **Not in scope for initial implementation.** In a future iteration, `/pykpyx-update` could accept plain English instead of a spec file:
>
> ```
> Human: /pykpyx-update "Make the enemies move twice as fast after wave 3"
> ```
>
> The skill would read the current game code, apply the described change, and report what was modified.

### 5.3 Multi-file specs

The human **can** split requirements across multiple markdown files:

```
specs/
├── MY-GAME.md           # Primary spec — references the others
├── MY-GAME-ENEMIES.md   # Enemy types and AI behaviour
└── MY-GAME-HUD.md       # HUD layout and scoring
```

The primary spec references supplementary files using `@` or markdown hyperlinks, e.g.:

```markdown
## Enemies

See @specs/MY-GAME-ENEMIES.md for enemy types and AI behaviour.

## HUD

See [HUD spec](MY-GAME-HUD.md) for layout and scoring.
```

Rules:

- **One file must be the primary spec** — it contains the Game Type, Title, Settings, and Sprites sections.
- Supplementary files are discovered by following `@` references or hyperlinks in the primary spec.
- The skill only reads the primary spec file; it resolves supplementary files from the references within it.
- `/pykpyx-generate` and `/pykpyx-update` always take the primary spec as their argument.

### 5.4 Full regeneration

If the human wants a clean slate:

```
Human: /pykpyx-generate specs/MY-GAME.md --force
```

This overwrites all generated files. The human is warned before proceeding.

---

## 6. Skill Implementation Notes

### 6.1 Engine API context

The skill needs engine API knowledge to generate correct code. Rather than bundling a separate reference file, each skill's `SKILL.md` instructs Claude to read the authoritative docs at invocation time:

- `@docs/README.md` — usage guide with patterns and examples
- `@docs/pyke_pyxel_API.md` — auto-generated API reference

These two files are the single source of truth. No curated subset is maintained in the skill.

### 6.2 Template design

Templates are minimal, valid, runnable games. They follow the patterns established in the existing example games (`games/`):

- **base**: `main.py` + `game_loop.py` + `game_load.py` with `Game`, settings, two signal handlers.
- **rpg**: `main.py` + `game_loop.py` + `game_load.py` + `config.py` with `RPGGame` and all RPG signals pre-wired.
- **cell_auto**: `main.py` + `game_loop.py` + `game_load.py` with `CellAutoGame` and matrix setup. *(deferred — see §9)*

The skill reads the template, understands the structure, then **modifies** it per the spec. It does not do string substitution — Claude rewrites the code with full understanding.

#### 6.2.1 Research findings

These findings are derived from reverse-engineering the Simple (`games/simple/`) and RPG (`games/rpg/`) games. They inform decisions about the spec template and Python templates.

**Three-file split applies to all game types.** Every generated game uses `main.py` + `game_loop.py` + `game_load.py`. For the RPG, `config.py` is added as a fourth file (sprite catalogue). The split keeps the same responsibilities regardless of game type:

| File | Responsibility |
|---|---|
| `main.py` | Settings, game instantiation, signal wiring, `game.start()`. Almost entirely boilerplate — game-specific values are slotted in. |
| `game_loop.py` | Game state dataclass, `start()` and `update()` handlers, input handlers, signal handlers. Most game-specific logic lives here. |
| `game_load.py` | Sprite creation, positioning, adding sprites to the game. For RPG: room construction (walls, doors). Called from `game_loop.start()`. |
| `config.py` | *(RPG only)* Sprite catalogue — static factory methods that return configured sprite instances. Pure leaf module with no game imports. |

**No AnimationFactory or SpriteFactory in generated code.** These are convenience classes for manual coding. Generated code should create `Animation` instances and sprites directly — the skill has full context from the spec and doesn't benefit from the factory abstraction.

**Centralised state management.** Every game needs mutable state tracked across frames. The template should define a standard `GameState` dataclass in `game_loop.py` that holds all game state, including references to sprites created in `game_load.py`. This solves the sprite-reference-passing problem: `game_load.py` populates the state object, and `game_loop.py` reads from it.

```python
# game_loop.py
@dataclass
class GameState:
    # Game-specific fields from spec
    destination: coord = field(default_factory=lambda: coord(1, 1))
    text_colour: int = 0
    # Sprite references populated by game_load
    player_sprite: Sprite | None = None
    hud_text: TextSprite | None = None

STATE = GameState()
```

This pattern:
- Eliminates module-level `global` variables for sprite references
- Gives `game_loop.py` a single, typed object to work with
- Makes game state explicit and inspectable
- Works identically for base `Game` and `RPGGame`

**Keyboard signal registration belongs in `game_loop.start()`.** The `game.keyboard.signal_for_key()` call requires the game instance, so it must happen inside the `start()` handler, not at module level.

**Signal handler signatures vary by signal type.** The templates must generate correct signatures:
- `GAME.WILL_START`, `GAME.UPDATE`: `(game: Game)`
- `MOUSE.DOWN`, `MOUSE.MOVE`: `(game: Game, value: tuple[int, int])`
- `PLAYER.BLOCKED`: `(player: Player, value: Sprite | None)`
- `ENEMY.BLOCKED`: `(enemy: Enemy, value: Sprite)`
- Custom keyboard signals: `(game: Game)`

**RPG arrow-key movement is boilerplate.** The 16-line press/release pattern for directional movement repeats in every RPG. The `rpg_game_loop.py` template should include it by default.

#### 6.2.2 Spec template gaps identified

The following are areas where `GAME-SPEC-TEMPLATE.md` may need updates, to be resolved when the template is finalised:

1. **Game State** — No section for declaring mutable state fields. Every game needs this.
2. **Room / Map Layout** *(RPG)* — No way to describe wall/door placements with grid coordinates. Major gap for RPG games.
3. **Sprite types** — The flat Sprites section doesn't distinguish between `Sprite`, `MovableSprite`, and `OpenableSprite`. RPG games need: directional movable sprites, dual-frame openable sprites, animated projectiles, and static wall sprites.
4. **Settings completeness** — Missing fields for `fps.animation` and `debug`.
5. **Enemy / NPC behaviour** — The "AI" section is marked BoardGame-only, but RPG enemies also need behavioural descriptions.
6. **HUD text specifics** — The HUD section is too vague to capture `TextSprite` positioning and dynamic behaviour.
7. **Projectile definitions** — No field for defining projectile sprites, speed, or launch mechanics.

### 6.3 Validation rules (for `/pykpyx-validate`)

Validation rules are maintained in `skill/docs/VALIDATION-CHECKLIST.md` — a stand-alone file that the `/pykpyx-validate` skill reads at runtime. This allows the rules to be iterated on independently of the skill instructions.

See that file for the current set of checks.

### 6.4 Frontmatter for each skill

**`/pykpyx`** (top-level)
```yaml
name: pykpyx
description: pyke_pyxel game creation skill. Describes available sub-commands and shared engine conventions. Use when the user asks about creating a game with pyke_pyxel.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Glob, Grep
```

**`/pykpyx-create`**
```yaml
name: pykpyx-create
description: Scaffold a new pyke_pyxel game project. Creates required folders and a named spec file from the game definition template.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Bash, Glob
argument-hint: <game-name>
```

**`/pykpyx-validate`**
```yaml
name: pykpyx-validate
description: Validate a pyke_pyxel game specification markdown file. Use when reviewing or iterating on a game definition before code generation.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Glob, Grep
argument-hint: [spec-file]
```

**`/pykpyx-generate`**
```yaml
name: pykpyx-generate
description: Generate a pyke_pyxel game from a validated specification. Creates game directory with runnable Python code.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [spec-file] [target-dir]
```

**`/pykpyx-update`**
```yaml
name: pykpyx-update
description: Apply incremental changes to an existing pyke_pyxel game from an updated spec or natural-language description.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [spec-or-instruction] [target-dir]
```

---

## 7. Open Questions — Resolved

| Question                                | Resolution                                                                                                              |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| What commands should the skill support? | Three: `/pykpyx-validate`, `/pykpyx-generate`, `/pykpyx-update` (§1)                                                    |
| Folder structure of the skill?          | `skill/{pykpyx-validate,pykpyx-generate,pykpyx-update}/` with templates and reference docs in `pykpyx-generate/` (§2.1) |
| Folder structure required of the human? | `specs/` for specs, generated game in a named directory, `assets/` for `.pyxres` (§3)                                   |
| Incremental vs regenerate?              | Incremental by default via `/pykpyx-update`; full regenerate via `/pykpyx-generate --force` (§5)                        |
| Multi-file specs?                       | Supported — one primary + supplementary files, merged in filename order (§5.3)                                          |

---

## 8. Implementation Sequence

### Build Phase 1

1. **Create `skill/` directory structure** and write `SKILL.md` for each command
2. **Write templates** in `skill/pykpyx-generate/templates/` based on patterns from existing example games
3. **Implement `/pykpyx-validate`** — validation logic in the skill instructions
4. **Implement `/pykpyx-generate`** — generation instructions with template reading

### Test Phase 1

5. **Test end-to-end** — write a sample spec, validate it, generate a game, run it. Human will also perform manual testing.

### Build Phase 2

6. **Implement `/pykpyx-update`** — incremental edit instructions

### Test Phase 2

7. **Test incremental flow** — modify a spec, apply updates, verify game still runs

### Docs Phase

8. **Write `skill/docs/SKILL-USAGE.md`** — human-readable guide covering the full workflow, commands, folder conventions, and examples
9. **Document** — mention the skill in `docs/README.md` and reference `skill/docs/SKILL-USAGE.md` for full details
10. **Document** — move any un-implemented or future reference items to `plans/ROADMAP.md`

---

## 8.1 Status Tracking

> Update this checklist as each step is completed.

#### Build Phase 1
- [ ] 1. Create `skill/` directory structure and write `SKILL.md` for each command
- [ ] 2. Write templates in `skill/pykpyx-generate/templates/`
- [ ] 3. Implement `/pykpyx-validate`
- [ ] 4. Implement `/pykpyx-generate`

#### Test Phase 1
- [ ] 5. End-to-end test (sample spec → validate → generate → run)
- [ ] 5a. Human manual testing sign-off

#### Build Phase 2
- [ ] 6. Implement `/pykpyx-update`

#### Test Phase 2
- [ ] 7. Incremental flow test (modify spec → update → verify)
- [ ] 7a. Human manual testing sign-off

#### Docs Phase
- [ ] 8. Write `skill/docs/SKILL-USAGE.md`
- [ ] 9. Update `docs/README.md` with skill reference
- [ ] 10. Move deferred items to `plans/ROADMAP.md`

---

## 9. Dependencies and Assumptions

- **First iteration supports `Game` and `RPGGame` only.** Templates and generation for these two types will be implemented first.
- **CellAutoGame** support will be added in a later iteration once the initial skill is stable.
- **BoardGame type** is still in development (per git history). The `board` template will be added once the type is stable.
- The skill assumes the target project has `pyke-pyxel` installed (editable or from package).
- `.pyxres` asset files are created by the human — the skill does not generate or modify them.
- The skill does not handle game deployment, packaging, or distribution.
