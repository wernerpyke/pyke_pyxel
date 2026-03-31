# Validation Checklist

Rules for validating a game spec against `GAME-SPEC-TEMPLATE.md`. The `/pykpyx validate` command reads this file and applies each rule to the spec. Mark each rule PASS or FAIL in the validation report.

---

## Structure Rules

- [ ] **"Game Type"** section exists
- [ ] **"Title and Assets"** section exists
- [ ] **"Settings"** section exists
- [ ] **"Game State"** section exists
- [ ] **"Entities"** section exists with at least one entity defined
- [ ] **"Sprites"** section exists with at least one sprite defined (static or animated)
- [ ] **"Input"** section exists with at least one input method (Keyboard or Mouse)
- [ ] **"Game Start"** section exists with setup description
- [ ] **"Game Update"** section exists with per-frame logic description

---

## Game Type Rules

- [ ] Game Type value is exactly `Game` or `RPGGame`
- [ ] If Game Type is `RPGGame`, the **"RPG"** section exists with required sub-sections (RPG Sprites, Room Layout)
- [ ] If Game Type is `Game`, the **"RPG"** section is absent or deleted

---

## Title and Assets Rules

- [ ] Title is non-empty
- [ ] Resources path is specified and ends in `.pyxres`
- [ ] The `.pyxres` file exists at the specified path (resolved relative to the project root)
- [ ] Sprite transparency colour, if specified, is a valid `COLOURS` constant name (e.g. BEIGE, BLACK, WHITE, RED, BLUE, GREEN, BROWN, PURPLE, ORANGE, YELLOW, GREY, PINK, BLUE_DARK, BLUE_SKY, BLUE_LIGHT, GREEN_MINT)

---

## Settings Rules

- [ ] Window size, if specified, is a positive integer
- [ ] Tile size, if specified, is a positive integer that divides window size evenly
- [ ] FPS (game), if specified, is a positive integer
- [ ] FPS (animation), if specified, is a positive integer
- [ ] Mouse enabled, if specified, is `yes` or `no`
- [ ] Debug, if specified, is `yes` or `no`
- [ ] Display smoothing, if specified, is `yes` or `no`
- [ ] Full screen, if specified, is `yes` or `no`

---

## Game State Rules

- [ ] Each declared field has a name, type, and default value
- [ ] Types are valid Python type expressions
- [ ] No duplicate field names
- [ ] No sprite reference fields declared (these are inferred automatically from Entities)

---

## Entity Rules

- [ ] At least one entity is defined
- [ ] Each entity has a **Sprite** field that references a sprite name defined in the Sprites section
- [ ] Entity speed, if specified, is a positive integer followed by `px per second`
- [ ] Each entity has a **Description** field with a non-empty value

---

## Sprite Rules

- [ ] Each sprite has a unique name
- [ ] Static sprites have a Frame specified as `colrow(<col>,<row>)`
- [ ] Animated sprites have a Default frame specified as `colrow(<col>,<row>)`
- [ ] Animated sprites have at least one Animation entry
- [ ] Animation entries specify position as `colrow(<col>,<row>)` and frame count (positive integer)
- [ ] All coordinate values in sprite definitions are positive integers (1-indexed — no zeros)
- [ ] No movement speed is defined in the Sprites section (speed belongs in Entities)

---

## Input Rules

- [ ] At least one of Keyboard or Mouse sub-sections is populated
- [ ] Keyboard entries use the bulleted format: key name, then **Pressed** and **Released** sub-items
- [ ] Each keyboard entry has at least one of Pressed or Released with a non-empty value (use `none` for no action)
- [ ] Keyboard actions reference entities defined in the Entities section (not raw sprite names)
- [ ] Mouse entries, if present, have both Event and Action columns filled
- [ ] If Mouse input is defined, Settings must have `Mouse enabled: yes`

---

## HUD Rules *(apply only when HUD section is present)*

- [ ] Each HUD element has a Type (text, score, or indicator)
- [ ] Each HUD element has a Position specified as `colrow(<col>,<row>)` with positive integers
- [ ] Each HUD element has an Initial value
- [ ] A corresponding `GameState` field exists for each dynamic HUD element

---

## Consistency and Redundancy Rules

> These rules detect information that is stated in more than one section, or references that don't match. When a redundancy is found, the validation report must identify which sections conflict and recommend which section should own the information.

- [ ] Movement speed is defined only in Entities, not duplicated in Sprites, Input, or Game Update
- [ ] Entity behaviour is described only in Entities and/or Game Update, not duplicated across both with conflicting detail
- [ ] Input actions reference entities by their entity name (e.g. "Player"), not by sprite name (e.g. "Ship")
- [ ] Game Start and Game Update reference only entity names and sprite names that are defined in their respective sections
- [ ] No property or behaviour is described with conflicting values across sections

---

## RPG-specific Rules *(apply only when Game Type is `RPGGame`)*

### Player

- [ ] Player sub-section exists with Default frame, Speed, Frames per direction, and Directions
- [ ] Player Speed is a positive integer (pixels per second)
- [ ] Player Directions lists all four: UP, DOWN, LEFT, RIGHT with `colrow(<col>,<row>)` coordinates
- [ ] All player frame coordinates are positive integers (1-indexed)

### Room Layout

- [ ] Room Layout section exists
- [ ] **Player Start** position is specified as `colrow(<col>,<row>)` with positive integers
- [ ] **Walls** sub-section has at least one wall placement
- [ ] All Room Layout coordinates use `colrow(<col>,<row>)` format with positive integers (1-indexed)
- [ ] Wall ranges (horizontal/vertical) have start ≤ end

### Openable Sprites

- [ ] Each openable sprite has both a Closed frame and an Open frame
- [ ] Frame coordinates use `colrow(<col>,<row>)` format with positive integers (1-indexed)

### Movable Sprites *(if defined)*

- [ ] Each movable sprite has Speed (positive integer) and all four Directions
- [ ] Frame coordinates use `colrow(<col>,<row>)` format with positive integers (1-indexed)

### Projectile Sprites *(if defined)*

- [ ] Each projectile has a Frame or Animation defined
- [ ] Each projectile has a Speed (positive integer)

### Enemy Behaviour *(if enemies defined in Room Layout)*

- [ ] Each enemy placed in Room Layout has a corresponding Enemy Behaviour entry
- [ ] Each behaviour entry has a Movement description
