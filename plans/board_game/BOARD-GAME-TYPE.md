# BoardGame — Design Plan

**Status:** PAUSED
**Goal:** Add a new `BoardGame` game type to `pyke_pyxel` that supports turn-based, player-vs-AI board games on a grid layout.

---

## 1. Overview

`BoardGame` is a new game type that extends the base `Game` class, following the same pattern as `RPGGame` and `CellAutoGame`. It introduces:

- **Turn-based play** — discrete turns rather than real-time updates
- **Player vs AI** — a human player and a game-specific AI opponent
- **Board layouts** — selectable from a set of enumerated board representations (initially: Grid)

### Design Principles

- **Exactly two players.** `BoardGame` always has exactly two players (`Player.HUMAN` and `Player.AI`) — never more. This is a hard constraint, not a default. The engine does not need to generalise for N players.
- **Do not duplicate base engine logic.** If the engine already provides functionality (e.g. `coord.with_xy` for pixel-to-grid conversion, `Map` for spatial queries), `BoardGame` should delegate to it rather than reimplement it.

### Scope

| Feature                               | In scope (v1) | Future |
| ------------------------------------- | ------------- | ------ |
| Turn style: sequential (Chess-like)   | Yes           |        |
| Turn style: simultaneous (Poker-like) |               | Yes    |
| Board layout: Grid                    | Yes           |        |
| Board layout: Hex, radial, etc.       |               | Yes    |
| AI: default random + custom subclass   | Yes           |        |
| Multiplayer (human vs human)          |               | Yes    |

---

## 2. Architecture

### 2.1 Class Hierarchy

```
Game (base)
├── RPGGame
├── CellAutoGame
└── BoardGame          # new
```

`BoardGame` inherits from `Game` and adds:

- A `Board` selected from an enumerated set of layouts (initially: `BoardLayout.GRID`)
- A `TurnManager` to orchestrate turn flow
- A default `AI` (random valid move) replaceable via a setter property

### 2.2 Module Layout

```
pyke_pyxel/
  board/
    __init__.py            # public exports: BoardGame, BoardLayout, Board, BoardPieceSprite, TurnManager, AI, Player
    game.py                # BoardGame class
    _turn_manager.py       # TurnManager — orchestrates turn lifecycle
    _board.py              # Board class + BoardLayout enum
    _sprites.py            # BoardPieceSprite and any future board-specific sprite subclasses
    _ai.py                 # AI class (concrete, default picks random valid move)
```

### 2.3 Key Classes

#### `BoardGame(Game)`

The game type subclass. Manages the board, players, and turn lifecycle.

```python
class BoardGame(Game):
    def __init__(self, settings, title, resources, *,
                 layout: BoardLayout, cols: int, rows: int): ...

    @property
    def board(self) -> Board: ...      # created internally from layout enum

    @property
    def turn_manager(self) -> TurnManager: ...

    @property
    def current_player(self) -> Player: ...   # Player.HUMAN or Player.AI

    @property
    def ai(self) -> AI: ...            # default: AI() (random valid move)

    @ai.setter
    def ai(self, value: AI) -> None: ...  # replace with custom AI

    def is_valid(self, move: Move, board: Board, turn_manager: TurnManager) -> bool:
        """Validate whether a move is legal under game rules. Default: any in-bounds move
        is valid. Override in subclass for game-specific rules (e.g. legal chess moves)."""
        ...

    def enumerate_moves(self, player: Player, board: Board, turn_manager: TurnManager) -> list[Move]:
        """Return all legal moves for a player. Default: all in-bounds moves.
        Override in subclass for game-specific move generation."""
        ...
```

**Lifecycle overrides:**

- `_update()` — replaces real-time game loop with turn-aware logic:
  1. Keyboard/mouse input (always)
  2. If paused, return
  3. Timers
  4. `GAME.UPDATE` signal
  5. **Turn processing** — if it's the AI's turn, request and apply AI move
  6. FX, animations

- `_draw()` — inserts board rendering between background and sprites:
  1. Background
  2. **Board** (grid lines, cell highlights, etc.), see [Board drawing](BOARD-DRAW.md)
  3. Sprites (pieces)
  4. HUD (turn indicator, captured pieces, etc.)
  5. FX

#### `BoardLayout` (Enum) / `Board`

Board layouts are selected via an enum rather than subclassed. The engine provides all layouts; games choose one.

```python
class BoardLayout(Enum):
    GRID = "grid"          # rectangular grid (chess, checkers, scrabble)
    # HEX = "hex"          # future: hexagonal
    # RADIAL = "radial"    # future: radial/circular

class Board:
    """Board with a specific layout. Created internally by BoardGame based on the chosen layout."""

    def __init__(self, layout: BoardLayout, cols: int, rows: int): ...

    @property
    def layout(self) -> BoardLayout: ...

    @property
    def cols(self) -> int: ...

    @property
    def rows(self) -> int: ...

    def place(self, piece: Piece, position: Position) -> None: ...
    def remove(self, position: Position) -> Piece | None: ...
    def piece_at(self, position: Position) -> Piece | None: ...
    def is_within_bounds(self, position: Position) -> bool: ...
    def _draw(self) -> None: ...
```

`Board` uses 1-indexed `col`/`row` coordinates, consistent with the engine's `coord` and `area` conventions. Layout-specific behaviour (coordinate mapping, neighbour logic, rendering) is handled internally based on the `BoardLayout` value.

#### `TurnManager`

Manages whose turn it is and the turn lifecycle.

```python
class Player(Enum):
    HUMAN = "human"
    AI = "ai"

class TurnManager:
    """Orchestrates sequential turn-based play."""

    @property
    def current_player(self) -> Player: ...

    @property
    def turn_number(self) -> int: ...

    @property
    def move_history(self) -> list[Move]: ...       # all moves in order, oldest first

    @property
    def last_move(self) -> Move | None: ...         # most recent move, or None on first turn

    def submit_move(self, move: Move) -> None: ...  # records move in history, ends current turn
    def is_game_over(self) -> bool: ...
    def winner(self) -> Player | None: ...           # winning player, or None for draw
```

**Sequential turn flow (v1):**

```
TURN.STARTED (Player.HUMAN)
  → Human clicks / selects piece / confirms move
  → submit_move(move)
TURN.ENDED (Player.HUMAN)
TURN.STARTED (Player.AI)
  → AI.choose_move() called
  → submit_move(move)
TURN.ENDED (Player.AI)
... repeat ...
```

#### `AI`

Concrete class with a default implementation that picks a random legal move. Games that need smarter AI subclass it and override `choose_move()`.

```python
class AI:
    """AI opponent. Default implementation selects a random valid move."""

    def choose_move(self, game: BoardGame) -> Move:
        """Select a move. Default: random choice from game.enumerate_moves().
        Override in a subclass for smarter strategies (minimax, neural nets, etc.)."""
        moves = game.enumerate_moves(Player.AI, game.board, game.turn_manager)
        return random.choice(moves)
```

The AI receives the `BoardGame` instance, giving it access to the board, turn state, and `enumerate_moves()`. The opponent's previous move is available via `game.turn_manager.last_move`, and the full game history via `game.turn_manager.move_history`. Games replace the default AI via the `BoardGame.ai` setter property — anything from weighted random to minimax to neural nets.

### 2.4 Board Sprites

`MovableSprite` is specific to RPGGame (directional animations, continuous movement). Board games have different needs — pieces slide discretely from one cell to another, and don't have directional facing. `BoardGame` will have its own sprite subclass(es) in `pyke_pyxel/board/`.

#### `BoardPieceSprite(Sprite)`

A sprite subclass tailored for board game pieces.

```python
class BoardPieceSprite(Sprite):
    """A sprite representing a board game piece with slide-to-position animation."""

    def __init__(self, name: str, default_frame: coord,
                 slide_speed_px_per_second: float = 60.0,
                 cols: int = 1, rows: int = 1,
                 resource_image_index: int = 0): ...

    @property
    def is_sliding(self) -> bool: ...

    def slide_to(self, target: coord) -> None: ...
```

**How sliding works:**

Modelled after `MovableActor`'s pixel accumulator pattern but simplified for board games:

1. `slide_to(target)` sets a target position and begins interpolation
2. Each frame, a pixel accumulator advances the piece toward the target at the configured speed
3. When the piece arrives, `is_sliding` becomes `False` and `BOARD.PIECE_MOVE_ENDED` is signalled
4. No directional animations — the piece sprite frame stays constant during the slide

**Default behaviour:** `BoardGame` auto-animates piece movement when a `Move` is submitted. The turn does not advance to the next player until the slide completes. This creates a natural pacing between turns.

Games that don't want animation can set `slide_speed_px_per_second` high enough that movement appears instant, or override this at the `BoardGame` level.

### 2.5 Data Types

```python
@dataclass
class Piece:
    """A game piece on the board."""
    player: Player          # Player.HUMAN or Player.AI
    kind: str               # game-specific, e.g. "king", "pawn"
    sprite: BoardPieceSprite      # visual representation

@dataclass
class Move:
    """A single move action."""
    piece: Piece
    from_position: Position
    to_position: Position

Position = coord   # reuse engine's coord type (1-indexed col/row)
```

**Move validation is two-layered:**
1. **Board bounds** (engine) — `Board.is_within_bounds()` rejects moves to positions outside the board. Always runs.
2. **Game rules** (`BoardGame.is_valid()`) — validates game-specific legality. Runs after bounds check. The default implementation accepts any in-bounds move; subclasses override for game-specific rules.

**Legal move enumeration:** `BoardGame.enumerate_moves()` returns all legal moves for a given player. This serves three purposes:
1. **AI** — `AI.choose_move()` can call it to get the full set of candidate moves
2. **UI** — the game can highlight valid targets when a piece is selected
3. **Validation** — can be used as an alternative to `is_valid()` (check membership) if the move space is small enough

---

## 3. Signals

New signals scoped under `BOARD`:

| Signal                 | Sender | Value                                                | When                            |
| ---------------------- | ------ | ---------------------------------------------------- | ------------------------------- |
| `BOARD.TURN_STARTED`   | game   | `{player: Player}`                                   | A player's turn begins          |
| `BOARD.TURN_ENDED`     | game   | `{player: Player}`                                   | A player's turn ends            |
| `BOARD.PIECE_MOVE_STARTED` | game   | `{player: Player, move: Move}`                   | A move is applied to the board  |
| `BOARD.GAME_OVER`      | game   | `{winner: Player \| None}`                           | Win/draw detected               |
| `BOARD.PIECE_PLACED`   | game   | `{player: Player, piece: Piece, position: Position}` | Piece placed on board           |
| `BOARD.PIECE_REMOVED`  | game   | `{player: Player, piece: Piece, position: Position}` | Piece removed from board        |
| `BOARD.PIECE_MOVE_ENDED`   | game   | `{player: Player, piece: Piece, position: Position}` | Piece slide animation completed |

Every signal value includes `player` so handlers always know which player the event relates to. Positional signals (`PIECE_PLACED`, `PIECE_REMOVED`) include the board `position`; `PIECE_MOVE_STARTED` includes the full `Move` (which carries both `from_position` and `to_position`).

Games connect to these signals to drive UI updates, sound effects, and game-specific logic (e.g. checking for checkmate after each move).

---

## 4. Turn Flow Detail — Sequential (v1)

```
                    ┌──────────────┐
                    │  Game Start  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
              ┌─────│ TURN_STARTED │
              │     └──────┬───────┘
              │            │
              │   ┌────────▼────────┐
              │   │  current_player   │
              │   │  == Player.HUMAN? │
              │   └──┬──────────┬───┘
              │      │ yes      │ no
              │      ▼          ▼
              │   Wait for    AI.choose_move()
              │   mouse/key     │
              │   input         │
              │      │          │
              │      ▼          ▼
              │   ┌──────────────┐
              │   │ submit_move()│
              │   └──────┬───────┘
              │          │
              │   ┌──────▼───────┐
              │   │  TURN_ENDED  │
              │   └──────┬───────┘
              │          │
              │   ┌──────▼───────┐
              │   │  Game over?  │
              │   └──┬───────┬───┘
              │      │ no    │ yes
              └──────┘       ▼
                        GAME_OVER
```

The human player's turn is **input-driven**: the game stays on their turn across frames until they submit a move. The AI's turn is **immediate**: `choose_move()` is called and the move applied within a single update cycle (or optionally spread across frames with a thinking delay for UX).

---

## 5. Integration with Existing Engine

| Engine concept | BoardGame usage |
|---|---|
| `coord` / `area` | Board positions are `coord` values (1-indexed col/row) |
| `Map` | Optional — could be used for board collision but `GridBoard` manages its own spatial state |
| `Sprite` | Each `Piece` has a sprite for rendering; placed/moved via `game.add_sprite()` |
| `Signals` | Turn lifecycle and piece events use standard signal system |
| `HUD` | Turn indicator, score, captured pieces |
| `Keyboard` | Piece selection hotkeys, undo |
| `Mouse` | Primary input — click to select piece, click to place |
| `Animation` | Piece movement animations between cells |
| `FX` | Capture effects, check/checkmate highlights |

---

## 6. Research

- [boardgame.io comparison](RESEARCH-BOARDGAMEIO.md) — high-level comparison of boardgame.io's architecture vs this plan. Key takeaway: adopted `enumerate_moves()` for legal move generation (benefits AI, UI, and validation) — now a method on `BoardGame`.
- [Board drawing](BOARD-DRAW.md) — design plan for board cell rendering. Evaluates three approaches; selects `BoardCellFactory` pattern with a separate highlight layer.

---

## 7. Implementation Phases

### Phase 1 — Scaffold & Draw Board

Set up the module structure and get a visible board rendering on screen.

- [ ] Create `pyke_pyxel/board/` package with module files per [Section 2.2](#22-module-layout)
- [ ] Implement `BoardLayout` enum with `GRID` value per [Section 2.3](#23-key-classes)
- [ ] Implement `Board` class: `__init__`, `cols`, `rows`, `layout`, `is_within_bounds()` per [Section 2.3](#23-key-classes)
- [ ] Implement `Board._draw()` for grid layout (grid lines, cell colouring) per [Board drawing plan](BOARD-DRAW.md)
- [ ] Implement `BoardGame(Game)` skeleton: `__init__`, `board` property, `_draw()` override that inserts board rendering between background and sprites per [Section 2.3](#23-key-classes)
- [ ] Wire `BoardGame` exports in `__init__.py` per [Section 2.2](#22-module-layout)
- [ ] Verify board renders correctly in a minimal test game

### Phase 2 — Draw Pieces

Place pieces on the board and render them as sprites.

- [ ] Implement `Piece` and `Position` data types per [Section 2.5](#25-data-types)
- [ ] Implement `BoardPieceSprite(Sprite)` (without slide animation) per [Section 2.4](#24-board-sprites)
- [ ] Implement `Board.place()`, `Board.remove()`, `Board.piece_at()` per [Section 2.3](#23-key-classes)
- [ ] Add `BOARD.PIECE_PLACED` and `BOARD.PIECE_REMOVED` signals per [Section 3](#3-signals)
- [ ] Wire piece sprites into `BoardGame._draw()` sprite layer per [Section 2.3](#23-key-classes)
- [ ] Verify pieces render at correct board positions in a test game

### Phase 3 — Player Turns & Default AI

Add turn management, move validation, and a default random AI.

- [ ] Implement `Player` enum per [Section 2.3](#23-key-classes)
- [ ] Implement `Move` data type per [Section 2.5](#25-data-types)
- [ ] Implement `TurnManager`: `current_player`, `turn_number`, `move_history`, `last_move`, `submit_move()`, `is_game_over()`, `winner()` per [Section 2.3](#23-key-classes)
- [ ] Implement `BoardGame.is_valid()` and `BoardGame.enumerate_moves()` with default implementations per [Section 2.3](#23-key-classes) and [Section 2.5](#25-data-types)
- [ ] Implement `AI` class with default random `choose_move()` per [Section 2.3](#23-key-classes)
- [ ] Wire `BoardGame.ai` property and setter per [Section 2.3](#23-key-classes)
- [ ] Implement `BoardGame._update()` turn-aware logic: human input → submit → AI turn per [Section 2.3](#23-key-classes) and [Section 4](#4-turn-flow-detail--sequential-v1)
- [ ] Add `BOARD.TURN_STARTED`, `BOARD.TURN_ENDED`, `BOARD.PIECE_MOVE_STARTED`, `BOARD.GAME_OVER` signals per [Section 3](#3-signals)
- [ ] Verify full human → AI turn cycle works in a test game

### Phase 4 — Animate Pieces & Turns

Add slide animation to piece movement and polish turn pacing.

- [ ] Implement `BoardPieceSprite.slide_to()` and `is_sliding` using pixel accumulator pattern per [Section 2.4](#24-board-sprites)
- [ ] Add `BOARD.PIECE_MOVE_ENDED` signal fired on slide completion per [Section 3](#3-signals)
- [ ] Wire auto-animation into `BoardGame`: animate piece on `submit_move()`, delay turn advance until slide completes per [Section 2.4](#24-board-sprites)
- [ ] Add AI thinking delay (0.8–1.8s random `Timer`) before AI move is applied per [Section 4](#4-turn-flow-detail--sequential-v1)
- [ ] Verify animated turn flow: human move → slide → AI delay → AI move → slide → next turn
- [ ] Update `pyke_pyxel/board/__init__.py` public exports per [Section 2.2](#22-module-layout)

---

## 8. Future Additions

### 8.1 Multi-grid col/row board positions

In v1, each board position maps 1:1 to a single grid col/row. This means a board cell is exactly one engine grid cell, and a piece sprite occupies exactly one frame.

In v2, a board position could span multiple grid cells (e.g. a 2×2 or 3×3 block), allowing larger piece sprites and richer visual layouts. Below is a tracker of what would need to change, to be updated as v1 is implemented and new dependencies are discovered.

#### 8.1.1 Board

- **`Board.__init__`** — add a `cell_scale: int` parameter (default `1`). A board position at `(col, row)` would occupy grid cells `(col * scale, row * scale)` through `((col + 1) * scale - 1, (row + 1) * scale - 1)`.
- **`Board.place()` / `Board.remove()` / `Board.piece_at()`** — internal storage stays keyed by board position (unchanged). No impact on the logical board state.
- **`Board.is_within_bounds()`** — unchanged; operates on board positions, not grid cells.
- **`Board._draw()`** — grid line rendering must account for `cell_scale`. Lines are drawn every `cell_scale` grid cells rather than every cell. Cell highlight areas grow proportionally.

#### 8.1.2 Coordinate conversion

- **v1:** board position *is* the grid position — `coord.with_xy` is sufficient for mouse-to-board conversion.
- **v2:** needs `board_to_grid(board_pos) -> coord` and `grid_to_board(grid_pos) -> coord` translation methods on `Board`. Mouse input would convert pixel → grid (via `coord.with_xy`) → board position (via `grid_to_board`). These methods do not exist in v1 — during implementation, ensure no code assumes board position == grid position in a way that would be hard to intercept later.

#### 8.1.3 BoardPieceSprite / Sprites

- **`BoardPieceSprite`** — currently assumes `cols=1, rows=1` sprite frame size. In v2, pieces would use multi-cell sprites (e.g. `cols=2, rows=2` for a 2×2 board cell). The `slide_to()` target would be a grid-level coordinate (top-left of the target board cell's grid region), not a board position directly.
- **`Sprite` base class** — already supports multi-cell sprites via `cols`/`rows` parameters, so no engine changes expected.

#### 8.1.4 BoardGame

- **`BoardGame.__init__`** — pass `cell_scale` through to `Board`.
- **`_draw()` ordering** — unchanged; board still draws before sprites.
- **Mouse input handling** — any click-to-board-position logic must route through `Board.grid_to_board()` instead of using grid coordinates directly.

#### 8.1.5 Move / Position

- **`Position` type alias** — stays as `coord` representing board positions (not grid positions). No change to `Move` or `enumerate_moves()`. The translation between board and grid coordinates is `Board`'s responsibility and stays internal to the rendering/input layer.

#### 8.1.6 AI

- No impact. AI receives the `BoardGame` instance and operates on board positions and `Move` objects, which are unaffected by grid scaling.

#### 8.1.7 v1 implementation notes

When implementing v1, keep an eye on these patterns that would complicate the v2 transition:

- **Direct use of board position as pixel/grid coordinate** — any place that passes a board `Position` directly to a rendering or sprite-placement call should go through a method that can later be swapped to include scaling. Even in v1 (where the method is identity), this creates the seam.
- **Hardcoded `cols=1, rows=1`** — avoid assuming piece sprites are always 1×1 in engine-level code. Game code can assume it; engine code should not.

### 8.2 Generic storage for custom data elements

v1 data types (`Move`, `Piece`) carry only the fields the engine needs. Games with richer semantics — captures, promotions, castling flags, scoring metadata — will need a way to attach arbitrary game-specific data without modifying the engine's core types.

**Possible approach: `metadata` dict**

Add an optional `metadata: dict | None = None` field to `Move` (and potentially `Piece`). This gives games a flexible escape hatch for passing extra context through the engine's turn pipeline without requiring new fields or subclasses.

```python
@dataclass
class Move:
    piece: Piece
    from_position: Position
    to_position: Position
    metadata: dict | None = None   # game-specific data (captures, promotions, etc.)
```

The engine would never read or write `metadata` — it is purely for game-level code and AI. For example, a chess game might store `{"captured": rook_piece, "promotion": "queen"}`, while a Scrabble-like game might store `{"word": "HELLO", "score": 12}`.

**Open questions:**
- Is an untyped `dict` sufficient, or should games be encouraged to subclass `Move` with typed fields instead?
- Should `Piece` also carry `metadata`, or is `kind: str` enough for game-specific piece identity?

### 8.3 Simultaneous turns

When we add Poker-style turns, should `TurnManager` be subclassed (`SequentialTurnManager` / `SimultaneousTurnManager`), or use a strategy/mode pattern?
