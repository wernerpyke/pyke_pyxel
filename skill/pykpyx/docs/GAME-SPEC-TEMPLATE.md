# Game Spec Template

**Purpose:** Use this template to describe the requirements for a game built with `pyke_pyxel`. Fill in each section to give Claude Code the information needed to generate a working game.

Delete any sections that don't apply to your game type. Sections marked *(optional)* can be omitted entirely if not needed. If your game type is `Game`, delete the entire **RPG** section.

---

## Game Type

> Which engine game type does this game use?

- **Type:** `Game` | `RPGGame`

---

## Title and Assets

> The game's display title and resource file.

- **Title:** `<game title>`
- **Resources:** `<path to .pyxres file>`
- **Sprite transparency colour:** `<colour name>` *(e.g. BEIGE, BLACK — omit for engine default)*

---

## Settings

> Window, frame rate, input, and display settings. Only list settings that differ from engine defaults.

| Setting              | Value       |
| -------------------- | ----------- |
| Window size (px)     |             |
| Tile size (px)       |             |
| Background colour    |             |
| FPS (game)           |             |
| FPS (animation)      |             |
| Mouse enabled        | yes / no    |
| Debug                | yes / no    |
| Display smoothing    | yes / no    |
| Full screen          | yes / no    |

---

## Game State

> Declare the mutable state the game tracks across frames for gameplay purposes (score, lives, wave number, etc.). Each field becomes part of a centralised `GameState` dataclass.
>
> **Note:** You do not need to declare sprite references here. The skill automatically adds sprite references and internal state fields based on the Entities and Sprites sections.

| Field          | Type          | Default     | Description                |
| -------------- | ------------- | ----------- | -------------------------- |
| `<field_name>` | `<data type>` | `<default>` | `<what this field tracks>` |

*Example:*

| Field         | Type     | Default        | Description                        |
| ------------- | -------- | -------------- | ---------------------------------- |
| `score`       | `int`    | `0`            | Current player score               |
| `lives`       | `int`    | `3`            | Remaining player lives             |
| `target`      | `string` | `enemy_boss`   | The current target of the player   |
| `destination` | `colrow` | `colrow(10,5)` | The next destination of the player |

---

## Entities

> Map logical game roles to sprites and declare per-entity properties. Each entity connects a name used in Input, Game Start, and Game Update to a specific sprite defined in the Sprites section.
>
> Speed is an entity property — do not duplicate it in the Sprites section.

### `<entity_name>`

- **Sprite:** `<sprite_name>` *(must match a name in the Sprites section)*
- **Speed:** `<n> px per second` *(optional — omit for static entities)*
- **Description:** `<natural-language description of this entity's role and behaviour>`

*Example:*

### `Player`

- **Sprite:** `Ship`
- **Speed:** `10 px per second`
- **Description:** The player-controlled ship. Moves in four directions via keyboard. Cannot leave the screen boundaries.

### `Enemy`

- **Sprite:** `Alien`
- **Speed:** `5 px per second`
- **Description:** Descends from the top of the screen. Destroyed on collision with a projectile.

---

## Sprites

> Define each sprite's visual data — frames and animations. Do not include movement speed here; speed belongs in the Entities section.
>
> All frame positions use `colrow(<col>,<row>)` format with 1-indexed positive integers. The `colrow()` wrapper makes it explicit that the first value is a column and the second is a row.

### Static Sprites

> Sprites with no animations — walls, obstacles, decorations.

#### `<sprite_name>`

- **Frame:** `colrow(<col>,<row>)`

### Animated Sprites

> Sprites with one or more animations.

#### `<sprite_name>`

- **Default frame:** `colrow(<col>,<row>)`
- **Animations:**
  - `<name>`: at `colrow(<col>,<row>)`, `<n>` frames
  - `<name>`: at `colrow(<col>,<row>)`, `<n>` frames, flipped
  - `<name>`: at `colrow(<col>,<row>)`, `<n>` frames, no-loop

> Animations loop by default. Add `no-loop` to play the animation once and stop on the last frame.

---

## Input

> How does the player interact with the game? Describe each input method and what it does.

### Keyboard *(optional)*

> List each key with its pressed and released actions. Use `none` if nothing happens on release.

- `<KEY>`:
  - **Pressed:** `<what happens when key is pressed>`
  - **Released:** `<what happens when key is released>`

*Example:*

- `UP`:
  - **Pressed:** Start Player 'idle' animation, move Player towards the top of the screen
  - **Released:** Stop Player movement

- `SPACE`:
  - **Pressed:** Fire projectile from Player position
  - **Released:** none

### Mouse *(optional)*

| Event        | Action                           |
| ------------ | -------------------------------- |
| Click        | `<what it does>`                 |
| Move         | `<what it does>`                 |

---

## HUD

> Describe on-screen text and status displays. All positions use `colrow(<col>,<row>)` format.

### `<element_name>`

- **Type:** text | score | indicator
- **Position:** `colrow(<col>,<row>)`
- **Initial value:** `<text or number>`
- **Dynamic behaviour:** `<how it changes (e.g. "updates on score change", "cycles colour each frame")>`

---

## Game Start

> What happens when the game starts? Describe initial setup: creating sprites, placing them, setting initial state. Natural language is fine — the skill will ask for clarification if anything is ambiguous.

---

## Game Update

> Describe per-frame logic. Use the sub-sections that apply.

### Movement

> How sprites move each frame (e.g. "move 1px/frame toward destination", "patrol between waypoints").

### Scoring *(optional)*

> How and when points are earned or lost.

### State Transitions *(optional)*

> Conditions that change the game's mode or phase (e.g. "when all enemies defeated, advance to next wave").

### Win / Lose Conditions *(optional)*

> When and how the game ends.

---
## RPG

> **Delete this entire section if Game Type is `Game`.**
>
> Everything below is specific to `RPGGame`. It covers RPG sprite types, room layout, collision handling, and enemy behaviour.

### RPG Sprites

> RPG-specific sprite types. Static and animated sprites shared with `Game` are defined in the **Sprites** section above.
>
> All frame positions use `colrow(<col>,<row>)` format with 1-indexed positive integers.

#### Player

> The player sprite. Created via `game.set_player()` — exactly one per RPGGame. Arrow-key movement is included by default.

- **Default frame:** `colrow(<col>,<row>)`
- **Speed:** `<pixels per second>`
- **Frames per direction:** `<n>`
- **Directions:**
  - UP: `colrow(<col>,<row>)`
  - DOWN: `colrow(<col>,<row>)`
  - LEFT: `colrow(<col>,<row>)`, flipped *(or own frames)*
  - RIGHT: `colrow(<col>,<row>)`

#### Movable Sprites *(optional)*

> Other sprites that move on the grid with directional animations (e.g. NPCs, companions). Does not include the player (above) or enemies (see Enemy Behaviour below).

##### `<sprite_name>`

- **Default frame:** `colrow(<col>,<row>)`
- **Speed:** `<pixels per second>`
- **Frames per direction:** `<n>`
- **Directions:**
  - UP: `colrow(<col>,<row>)`
  - DOWN: `colrow(<col>,<row>)`
  - LEFT: `colrow(<col>,<row>)`, flipped *(or own frames)*
  - RIGHT: `colrow(<col>,<row>)`

#### Openable Sprites

> Sprites with two states (e.g. doors, chests).

##### `<sprite_name>`

- **Closed frame:** `colrow(<col>,<row>)`
- **Open frame:** `colrow(<col>,<row>)`

#### Projectile Sprites *(optional)*

> Sprites launched by the player or enemies.

##### `<sprite_name>`

- **Frame:** `colrow(<col>,<row>)`
- **Animation:** at `colrow(<col>,<row>)`, `<n>` frames *(looping)*
- **Speed:** `<pixels per second>`

### Room Layout

> Describe the room contents and their grid positions. All coordinates use `colrow(<col>,<row>)` format, 1-indexed.

#### Walls

> List each wall placement. Use ranges for horizontal or vertical runs.

- `<sprite_name>` at `colrow(<col>,<row>)`
- `<sprite_name>` horizontal from `colrow(<col>,<row>)` to `colrow(<col>,<row>)`
- `<sprite_name>` vertical from `colrow(<col>,<row>)` to `colrow(<col>,<row>)`

#### Doors *(optional)*

- `<sprite_name>` at `colrow(<col>,<row>)`, initially open | closed

#### Player Start

- Position: `colrow(<col>,<row>)`

#### Enemies *(optional)*

- `<sprite_name>` at `colrow(<col>,<row>)`

### Collision and Blocking *(optional)*

> What happens when sprites collide or are blocked? Maps to `PLAYER.BLOCKED` and `ENEMY.BLOCKED` signal handlers.

| Event              | Behaviour                                   |
| ------------------ | ------------------------------------------- |
| Player blocked by  | `<what happens>`                            |
| Enemy blocked by   | `<what happens>`                            |

### Enemy Behaviour *(optional)*

> Describe how enemies act.

#### `<enemy_name>`

- **Movement:** `<how it moves (e.g. random direction, patrol, chase player)>`
- **On blocked:** `<what happens when movement is blocked>`

---

## Claude Clarifications

> **Do not fill in this section yourself.** This section is written by the `generate` command when it encounters ambiguous or unclear requirements and asks you (the human) to clarify. Each entry records the question asked and the answer given, so the spec remains a complete record of all design decisions.
>
> If this section is empty or absent, no clarifications were needed.

<!-- Example entry (written by generate):

### Movement speed units
- **Question:** Entity "Enemy" speed is "slow" — what speed in px per second?
- **Answer:** 3 px per second
- **Applied to:** Entities > Enemy > Speed

-->
