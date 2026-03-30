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

> Declare the mutable state the game tracks across frames. Each field becomes part of a centralised `GameState` dataclass. Include sprite references that handlers need access to.

| Field            | Type            | Default         | Description                         |
| ---------------- | --------------- | --------------- | ----------------------------------- |
| `<field_name>`   | `<python type>` | `<default>`     | `<what this field tracks>`          |

*Example:*

| Field           | Type             | Default       | Description                       |
| --------------- | ---------------- | ------------- | --------------------------------- |
| `destination`   | `coord`          | `coord(1, 1)` | Where the player sprite is moving |
| `score`         | `int`            | `0`           | Current player score              |
| `player_sprite` | `Sprite \| None` | `None`        | Reference to the player sprite    |

---

## Sprites

> Define each sprite used in the game. For RPGGame-specific sprite types (movable, openable, projectile), see the **RPG** section below.

### Static Sprites

> Sprites with no animations — walls, obstacles, decorations.

#### `<sprite_name>`

- **Frame:** `<col>,<row>` *(1-indexed position in the sprite sheet)*

### Animated Sprites

> Sprites with one or more animations.

#### `<sprite_name>`

- **Default frame:** `<col>,<row>`
- **Animations:**
  - `<name>`: at `<col>,<row>`, `<n>` frames
  - `<name>`: at `<col>,<row>`, `<n>` frames, flipped

---

## Input

> How does the player interact with the game? Describe each input method and what it does.

### Keyboard *(optional)*

| Key       | Action                              |
| --------- | ----------------------------------- |
| `<key>`   | `<what it does>`                    |

### Mouse *(optional)*

| Event        | Action                           |
| ------------ | -------------------------------- |
| Click        | `<what it does>`                 |
| Move         | `<what it does>`                 |

---

## HUD

> Describe on-screen text and status displays.

### `<element_name>`

- **Type:** text | score | indicator
- **Position:** `(<col>,<row>)`
- **Initial value:** `<text or number>`
- **Dynamic behaviour:** `<how it changes (e.g. "updates on score change", "cycles colour each frame")>`

---

## Game Start

> What happens when the game starts? Describe initial setup: creating sprites, placing them, setting initial state.

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

#### Player

> The player sprite. Created via `game.set_player()` — exactly one per RPGGame. Arrow-key movement is included by default.

- **Default frame:** `<col>,<row>`
- **Speed:** `<pixels per second>`
- **Frames per direction:** `<n>`
- **Directions:**
  - UP: `<col>,<row>`
  - DOWN: `<col>,<row>`
  - LEFT: `<col>,<row>`, flipped *(or own frames)*
  - RIGHT: `<col>,<row>`

#### Movable Sprites *(optional)*

> Other sprites that move on the grid with directional animations (e.g. NPCs, companions). Does not include the player (above) or enemies (see Enemy Behaviour below).

##### `<sprite_name>`

- **Default frame:** `<col>,<row>`
- **Speed:** `<pixels per second>`
- **Frames per direction:** `<n>`
- **Directions:**
  - UP: `<col>,<row>`
  - DOWN: `<col>,<row>`
  - LEFT: `<col>,<row>`, flipped *(or own frames)*
  - RIGHT: `<col>,<row>`

#### Openable Sprites

> Sprites with two states (e.g. doors, chests).

##### `<sprite_name>`

- **Closed frame:** `<col>,<row>`
- **Open frame:** `<col>,<row>`

#### Projectile Sprites *(optional)*

> Sprites launched by the player or enemies.

##### `<sprite_name>`

- **Frame:** `<col>,<row>`
- **Animation:** at `<col>,<row>`, `<n>` frames *(looping)*
- **Speed:** `<pixels per second>`

### Room Layout

> Describe the room contents and their grid positions. All coordinates are 1-indexed (col, row).

#### Walls

> List each wall placement. Use ranges for horizontal or vertical runs.

- `<sprite_name>` at `(<col>,<row>)`
- `<sprite_name>` horizontal from `(<col>,<row>)` to `(<col>,<row>)`
- `<sprite_name>` vertical from `(<col>,<row>)` to `(<col>,<row>)`

#### Doors *(optional)*

- `<sprite_name>` at `(<col>,<row>)`, initially open | closed

#### Player Start

- Position: `(<col>,<row>)`

#### Enemies *(optional)*

- `<sprite_name>` at `(<col>,<row>)`

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
