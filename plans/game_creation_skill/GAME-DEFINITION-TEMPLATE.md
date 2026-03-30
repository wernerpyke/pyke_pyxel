# Game Definition Template

**Purpose:** Use this template to describe the requirements for a game built with `pyke_pyxel`. Fill in each section to give Claude Code the information needed to generate a working game.

Delete any sections that don't apply to your game type. Sections marked *(optional)* can be omitted entirely if not needed.

---

## Game Type

> Which engine game type does this game use?

- **Type:** `Game` | `RPGGame` | `CellAutoGame` | `BoardGame`

---

## Title and Assets

> The game's display title and resource file.

- **Title:** `<game title>`
- **Resources:** `<path to .pyxres file>`
- **Sprite transparency colour:** `<colour name>` *(e.g. BEIGE, BLACK)*

---

## Settings

> Window, frame rate, input, and display settings. Only list settings that differ from engine defaults.

| Setting              | Value       |
| -------------------- | ----------- |
| Window size (px)     |             |
| Background colour    |             |
| FPS                  |             |
| Mouse enabled        | yes / no    |
| Display smoothing    | yes / no    |
| Full screen          | yes / no    |

---

## Sprites

> Define each sprite used in the game. For each sprite, specify its default frame and any animations.

### `<sprite_name>`

- **Default frame:** `<col>,<row>` *(1-indexed position in the sprite sheet)*
- **Animations:** *(list each animation with its direction/name, starting frame, frame count, and any flags)*
  - `<DIRECTION/NAME>`: at `<col>,<row>`, `<n>` frames
  - `<DIRECTION/NAME>`: at `<col>,<row>`, `<n>` frames, flipped

---

## Board *(BoardGame only)*

> Define the board layout, dimensions, and cell appearance.

- **Layout:** `GRID` *(the board layout enum value)*
- **Columns:** `<n>`
- **Rows:** `<n>`

### Cell Appearance *(optional)*

> Describe how board cells should look (colours, alternating patterns, highlights, etc.)

---

## Pieces *(BoardGame only)*

> Define the game pieces, their ownership, and their sprites.

### `<piece_kind>`

- **Player:** HUMAN | AI | both
- **Sprite:** `<sprite_name>`
- **Count:** `<n>` per player *(or describe initial placement)*

### Starting Positions

> Describe where pieces are placed at the start of the game. Use board coordinates (1-indexed col, row).

---

## Game Start

> What happens when the game starts? Describe initial setup: creating sprites/pieces, placing them, setting initial state.

---

## Game Update

> What happens each frame (or each turn for BoardGame)? Describe per-frame or per-turn logic.

---

## Input

> How does the player interact with the game? Describe each input method and what it does.

### Mouse *(optional)*

> Describe mouse interactions (click, drag, hover).

### Keyboard *(optional)*

> Describe keyboard controls (keys and their actions).

---

## Turn Rules *(BoardGame only)*

> Describe the turn structure and move mechanics.

- **First player:** HUMAN | AI
- **Move description:** *(what constitutes a valid move)*

### Move Validation

> Describe the rules that determine whether a move is legal.

### Turn Sequence

> Describe what happens during each turn, step by step.

---

## AI *(BoardGame only, optional)*

> Describe the AI behaviour. Omit this section to use the default random AI.

- **Strategy:** `<description of AI decision-making>`

---

## Win Condition *(BoardGame only)*

> How does the game end? Describe win, loss, and draw conditions.

---

## Game Rules

> Describe all gameplay rules — collisions, scoring, boundaries, state transitions, and any other logic that governs the game.

---

## HUD *(optional)*

> Describe any on-screen status displays: score, turn indicator, health, etc.

---

## Sound and Music *(optional)*

> Describe any sound effects or background music triggers.

---

## Notes *(optional)*

> Any additional context, edge cases, or clarifications.
