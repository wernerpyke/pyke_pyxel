# Validation Checklist

Rules for validating a game spec against `GAME-SPEC-TEMPLATE.md`. The `/pykpyx validate` command reads this file and applies each rule to the spec. Mark each rule PASS or FAIL in the validation report.

---

## Structure Rules

- [ ] **"Game Type"** section exists
- [ ] **"Title and Assets"** section exists
- [ ] **"Settings"** section exists
- [ ] **"Game State"** section exists
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
- [ ] Sprite reference fields use the `Type | None` pattern with default `None`
- [ ] No duplicate field names

---

## Sprite Rules

- [ ] Each sprite has a unique name
- [ ] Static sprites have a Frame specified as `col,row`
- [ ] Animated sprites have a Default frame specified as `col,row`
- [ ] Animated sprites have at least one Animation entry
- [ ] Animation entries specify position (`col,row`) and frame count (positive integer)
- [ ] All coordinate values in sprite definitions are positive integers (1-indexed — no zeros)

---

## Input Rules

- [ ] At least one of Keyboard or Mouse sub-sections is populated
- [ ] Keyboard entries, if present, have both Key and Action columns filled
- [ ] Mouse entries, if present, have both Event and Action columns filled
- [ ] If Mouse input is defined, Settings must have `Mouse enabled: yes`

---

## HUD Rules *(apply only when HUD section is present)*

- [ ] Each HUD element has a Type (text, score, or indicator)
- [ ] Each HUD element has a Position specified as `(col,row)` with positive integers
- [ ] Each HUD element has an Initial value
- [ ] A corresponding `GameState` field or sprite reference exists for each dynamic HUD element

---

## RPG-specific Rules *(apply only when Game Type is `RPGGame`)*

### Player

- [ ] Player sub-section exists with Default frame, Speed, Frames per direction, and Directions
- [ ] Player Speed is a positive integer (pixels per second)
- [ ] Player Directions lists all four: UP, DOWN, LEFT, RIGHT with `col,row` coordinates
- [ ] All player frame coordinates are positive integers (1-indexed)

### Room Layout

- [ ] Room Layout section exists
- [ ] **Player Start** position is specified as `(col,row)` with positive integers
- [ ] **Walls** sub-section has at least one wall placement
- [ ] All Room Layout coordinates are positive integers (1-indexed)
- [ ] Wall ranges (horizontal/vertical) have start ≤ end

### Openable Sprites

- [ ] Each openable sprite has both a Closed frame and an Open frame
- [ ] Frame coordinates are positive integers (1-indexed)

### Movable Sprites *(if defined)*

- [ ] Each movable sprite has Speed (positive integer) and all four Directions
- [ ] Frame coordinates are positive integers (1-indexed)

### Projectile Sprites *(if defined)*

- [ ] Each projectile has a Frame or Animation defined
- [ ] Each projectile has a Speed (positive integer)

### Enemy Behaviour *(if enemies defined in Room Layout)*

- [ ] Each enemy placed in Room Layout has a corresponding Enemy Behaviour entry
- [ ] Each behaviour entry has a Movement description
