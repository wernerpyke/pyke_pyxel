# Board Drawing — Design Plan

**Status:** Draft
**Related:** [BOARD-GAME-TYPE.md](BOARD-GAME-TYPE.md) — parent design plan

---

## 1. Problem

`BoardGame._draw()` inserts board rendering between background and sprites:

```
1. Background
2. Board cells
3. Highlights (selected piece, valid targets, etc.)
4. Sprites (pieces)
5. HUD
6. FX
```

Games need control over how individual cells look — colours, borders, grid lines — and this varies significantly across game types. Chess has alternating dark/light cells with no grid lines. Scrabble has ~60 bonus cells across 5 colour categories with thin grid lines. Tic-tac-toe has uniform cells with thick lines.

The question: how should games configure cell appearance in a way that is consistent with how `Game`, `RPGGame`, and `CellAutoGame` handle visual customisation?

---

## 2. Options Considered

### Option A — Board-level properties

Set visual properties on the `Board` instance directly, similar to how `Rect` exposes `set_border(colour, width)`.

```python
game.board.set_grid_lines(colour=GREY, width=1)
game.board.set_cell_colour(colour=BEIGE)
```

**Assessment:**
- Works for uniform boards (tic-tac-toe).
- Fails for position-dependent styling (chess alternating colours, scrabble bonus cells). Would require per-cell setter calls for every cell, which is effectively a worse version of a factory pattern.

**Verdict:** Only viable for trivially uniform boards. Rejected.

### Option B — Extend `GameSettings.colours`

Add board-specific entries to the global `GameSettings` singleton.

```python
settings.colours.board_grid = COLOURS.GREY
settings.colours.board_cell = COLOURS.BEIGE
```

**Assessment:**
- Same per-cell limitation as Option A.
- Pollutes the global singleton with board-specific config. Neither `RPGGame` nor `CellAutoGame` extend `GameSettings` — they handle visual config at the component level.
- Wrong level of abstraction: board visuals are a component concern, not a game-wide setting.

**Verdict:** Inconsistent with existing patterns and still can't handle per-cell variation. Rejected.

### Option C — `BoardCellFactory` (selected)

A factory that `Board` calls during initialisation to produce a `BoardCell` for each position. The game controls per-cell appearance by providing a custom factory.

**Why this is consistent with the engine:**
- **Like `CellAutoGame`:** its `Matrix` owns a grid of `Cell` objects with individual `.colour`. `BoardCellFactory` is the same idea — a grid of cells with individual visual properties — but controlled via a factory at initialisation rather than direct mutation.
- **Like `Rect`:** drawables own their own visual properties (`set_border`, `set_background`). `BoardCell` owns its own fill/border config rather than reading from a global setting.
- **Like `AI`:** the factory is a concrete class with a sensible default. Simple games don't need to touch it; complex games subclass.
- **Component-level config:** set on `Board`, not on `GameSettings` — consistent with how `CellAutoGame` and drawables handle visual config.

---

## 3. Design

### 3.1 `BoardCell`

```python
@dataclass
class BoardCell:
    """Visual properties for a single board cell."""
    fill: int | None       # fill colour (Pyxel palette index), None = transparent
    border: int | None     # border colour, None = no border
    border_width: int      # border width in pixels (default: 1)
```

`BoardCell` is a pure data object describing how a cell looks. It is created by the factory and stored by the `Board`. The `Board._draw()` method reads these properties when rendering.

### 3.2 `BoardCellFactory`

```python
class BoardCellFactory:
    """Creates BoardCell instances for each board position.

    Default implementation produces uniform cells. Subclass and override
    create_cell() for position-dependent styling (e.g. alternating chess
    colours, scrabble bonus cells).
    """

    def create_cell(self, col: int, row: int) -> BoardCell: ...
```

- Concrete class with a default implementation (uniform cells).
- `Board` calls `factory.create_cell(col, row)` for every position during `__init__` and stores the results.
- Games provide a custom factory by passing it to `BoardGame` (or setting it on `Board`).

### 3.3 Highlight layer

Highlights (selected piece, valid move targets, check indicators) are a **separate draw layer** between board cells and sprites. They are not part of `BoardCell` or the factory.

**Rationale:** Cell appearance (from the factory) is static — it describes the board's base look and doesn't change during play. Highlights are transient runtime state driven by game logic (user selection, move validation results, check detection). Mixing the two would force the factory to be aware of game state, or require mutating `BoardCell` objects each frame.

Draw order:

```
1. Background
2. Board cells          ← BoardCell fill + borders (from factory)
3. Highlights           ← transient overlays (selection, valid targets, etc.)
4. Sprites (pieces)
5. HUD
6. FX
```

Highlight API design is out of scope for this document and will be addressed separately.

---

## 4. Real-World Examples

### 4.1 Chess (8×8, alternating cells, no grid lines)

```python
class ChessCellFactory(BoardCellFactory):
    def create_cell(self, col, row):
        is_light = (col + row) % 2 == 0
        return BoardCell(
            fill=BEIGE if is_light else BROWN,
            border=None,
            border_width=0
        )
```

- Cells have alternating fill colours based on position.
- No borders or grid lines — cells abut directly.
- Highlights (separate layer): selected piece cell, valid move targets, king in check.

### 4.2 Scrabble (15×15, bonus cells, thin grid lines)

```python
class ScrabbleCellFactory(BoardCellFactory):
    BONUS_COLOURS = {
        "DL": LIGHT_BLUE,    # double letter
        "TL": BLUE,          # triple letter
        "DW": PINK,          # double word
        "TW": RED,           # triple word
        "★":  PINK,          # center star
    }

    BONUS_MAP = {
        (1, 1): "TW", (1, 4): "DL", (1, 8): "TW",
        # ... all bonus positions
    }

    def create_cell(self, col, row):
        bonus = self.BONUS_MAP.get((col, row))
        return BoardCell(
            fill=self.BONUS_COLOURS.get(bonus, TAN),
            border=GREY,
            border_width=1
        )
```

- Most cells are plain (TAN fill); ~60 bonus cells use position-dependent colours.
- Thin uniform grid lines via border on every cell.
- Highlights (separate layer): valid placement positions, selected tile.

### 4.3 Tic-tac-toe (3×3, uniform cells, thick grid lines)

```python
class TicTacToeCellFactory(BoardCellFactory):
    def create_cell(self, col, row):
        return BoardCell(
            fill=None,
            border=BLACK,
            border_width=3
        )
```

- No cell fill (transparent background shows through).
- Thick black borders form the classic `#` grid shape.
- Could also use the default factory if uniform thin lines are acceptable.
- Highlights (separate layer): winning line.

---

## 5. Integration with `BOARD-GAME-TYPE.md`

Once this design is finalised, the following sections in `BOARD-GAME-TYPE.md` should be updated:

- **Section 2.2 (Module Layout):** add `_cell.py` for `BoardCell` and `BoardCellFactory`
- **Section 2.3 (`BoardGame`):** document how the factory is passed/set
- **Section 2.3 (`Board`):** reference `BoardCellFactory` in `Board.__init__`; update `Board._draw()` description
- **Section 2.3 (`_draw()` order):** update to show the highlight layer between board and sprites

---

## 6. Open Questions

1. **Factory injection** — should the factory be passed to `BoardGame.__init__`, or set via a property (like `AI`)? Leaning toward `__init__` since cell appearance is fundamental to the board's identity and unlikely to change at runtime.

2. **Highlight API** — how should games manage transient highlights? Possible directions:
   - `Board.set_highlight(position, colour)` / `Board.clear_highlights()`
   - A `HighlightLayer` object with its own draw method
   - Signal-driven: game emits highlight intent, board renders it

3. **Cell mutation at runtime** — should `BoardCell` properties be immutable after creation, or can games update them (e.g. Scrabble removing a bonus after first use)? If mutable, the factory establishes initial state and games mutate as needed. If immutable, games would need to rebuild cells.
