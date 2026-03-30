# Research: boardgame.io vs BoardGame Plan

**Status:** Draft
**Source:** [boardgame.io](https://github.com/boardgameio/boardgame.io) (JS/TS, MIT)
**Our plan:** `plans/BOARD-GAME-TYPE.md`

---

## 1. High-Level Summary

| Aspect | boardgame.io | Our BoardGame plan |
|---|---|---|
| Language / Runtime | TypeScript (browser + Node) | Python (Pyxel retro engine) |
| Primary goal | Framework-agnostic game logic with automatic multiplayer | Game *type* within an existing sprite/map engine |
| Rendering | None — bring your own UI (React, plain HTML, etc.) | Built-in — Pyxel pixel rendering, sprites, HUD, FX |
| Multiplayer | Core feature (client ↔ server via WebSocket) | Out of scope (v1); human vs AI only |
| AI | Generic MCTS bot + random bot; game provides `enumerate()` | Abstract `AI` base; each game supplies its own implementation |
| State model | Freeform JSON object (`G`) + framework context (`ctx`) | Typed dataclasses (`Board`, `Piece`, `Move`) + signal-driven lifecycle |

---

## 2. Game Definition

### boardgame.io — Declarative config object

A game is a plain object with `setup`, `moves`, `phases`, `turn`, `endIf`, and `plugins`. No class inheritance; the framework drives all state transitions.

```js
const TicTacToe = {
  setup: () => ({ cells: Array(9).fill(null) }),
  moves: {
    clickCell: ({ G, playerID }, id) => {
      G.cells[id] = playerID;
    },
  },
  endIf: ({ G }) => { /* check winner */ },
};
```

### Our plan — Class inheritance + signals

`BoardGame` subclasses `Game`, overrides `_update()` and `_draw()`, and wires behaviour through signals (`BOARD.TURN_STARTED`, `BOARD.MOVE_SUBMITTED`, etc.). Game-specific rules live in subclasses and validator objects.

```python
class ChessGame(BoardGame):
    def __init__(self):
        super().__init__(..., ai=ChessAI(), move_validator=ChessValidator())
```

### Takeaways

| Point | boardgame.io | Ours | Notes |
|---|---|---|---|
| Defining a game | Config object (declarative) | Subclass + signals (imperative) | Our engine is already class-based; staying consistent is the right call |
| Move definitions | Named functions in `moves` dict | `Move` dataclass + `MoveValidator` ABC | boardgame.io's approach is more concise; our typed dataclasses give stronger IDE support |
| Game-end condition | `endIf()` hook on game config | `TurnManager.is_game_over()` + signal | Equivalent — different ergonomics |

---

## 3. Turn Management

### boardgame.io — Phases → Turns → Stages

Three-level hierarchy:

- **Phases** — named game modes with distinct move sets and rules (e.g. "draw", "play", "score"). One active at a time.
- **Turns** — within a phase, players act in configurable order (round-robin, custom, etc.).
- **Stages** — within a turn, multiple players can act simultaneously in named sub-states (e.g. "discard" while another player plays a card).

Turn order is selected from presets (`TurnOrder.DEFAULT`, `TurnOrder.ONCE`, `TurnOrder.CUSTOM`, etc.) or defined via custom `first()`/`next()` functions.

Events like `endTurn()`, `setPhase()`, and `setStage()` are called from within moves and queued for processing after the move completes.

### Our plan — TurnManager (sequential only, v1)

Single-level: `TurnManager` alternates between player 1 (human) and player 2 (AI). No phases or stages. Turn transitions are driven by `submit_move()` and signalled via `BOARD.TURN_STARTED` / `BOARD.TURN_ENDED`.

### Takeaways

- **Phases and stages are powerful but not needed for v1.** Our plan correctly defers simultaneous turns. If we add phases later, boardgame.io's pattern (named modes with per-phase move sets) is a solid reference.
- **Turn order presets.** boardgame.io offers pluggable turn orders. Worth noting for future work, but irrelevant for the always-two-player v1.
- **Event queuing.** boardgame.io queues events triggered during a move and processes them after. Our signal system fires synchronously. No change needed for v1, but worth considering if move chains become complex.

---

## 4. State & Board Representation

### boardgame.io — Freeform `G`

Game state is a plain JSON-serializable object. There is no `Board` class — the game defines whatever structure it needs (array, 2D grid, object map, etc.). The framework enforces immutability via Immer.

This gives maximum flexibility but means every game reinvents board utilities (bounds checking, neighbour lookup, coordinate mapping).

### Our plan — Typed `Board` class

`Board` is a first-class engine object with `cols`, `rows`, `place()`, `remove()`, `piece_at()`, `is_within_bounds()`, and `_draw()`. Layout-specific behaviour is selected via `BoardLayout` enum.

### Takeaways

- **Our typed Board is a strength.** boardgame.io's freeform state is flexible for a framework that serves many UI targets, but our engine owns rendering, so a concrete `Board` that knows how to draw itself and manage spatial state is the right abstraction.
- **Immutability is not needed.** boardgame.io needs it for Redux + network sync. Our single-process, no-network architecture can mutate state directly.
- **Serialization.** boardgame.io requires JSON-serializable state for networking and time-travel. We have no such constraint, so using dataclasses with sprite references (as in `Piece`) is fine.

---

## 5. Move Validation

### boardgame.io

Moves return `INVALID_MOVE` to reject. Validation runs on both client (optimistic) and server (authoritative). Long-form move definitions can restrict moves to server-only (`client: false`) for secret state.

### Our plan

Two-layered: `Board.is_within_bounds()` (engine) then `MoveValidator.is_valid()` (game-provided). No client/server split since there's no network.

### Takeaways

- Architecturally similar — both separate engine-level checks from game-level rules.
- Our two-layer approach is cleaner for single-process use. No need for `INVALID_MOVE` sentinel; the validator simply returns `bool`.

---

## 6. AI

### boardgame.io — Generic MCTS + enumerate

Games provide an `enumerate(G, ctx, playerID)` function that lists all legal actions. The framework ships two bots:

- **MCTSBot** — Monte Carlo Tree Search with configurable iterations, playout depth, and weighted objectives.
- **RandomBot** — Picks a random legal action.

The AI simulates full games internally (using the game's own reducer) to evaluate moves. This means any boardgame.io game gets a competent AI "for free" if it provides `enumerate()`.

### Our plan — Abstract `AI` base, game implements

Each game supplies its own `AI.choose_move()`. The engine provides only the interface.

### Takeaways

- **boardgame.io's generic MCTS is appealing** but relies on being able to simulate the full game state cheaply (pure JS state + reducer). Our engine ties state to Pyxel's rendering context and sprites, making lightweight simulation harder.
- **Our approach is pragmatic for v1.** Game-specific AI gives each game full control. A generic search-based bot could be added later if we introduce a "headless simulation" mode.
- **Consider borrowing the `enumerate` pattern.** Even without MCTS, having games provide a list of legal moves (via `MoveValidator` or a dedicated method) would benefit both AI and UI (highlighting legal moves for the human player).

---

## 7. Event / Signal System

### boardgame.io

Events (`endTurn`, `setPhase`, `endGame`, etc.) are framework-provided functions available in move context. They are **queued during move execution** and **processed after the move completes**. This prevents mid-move state inconsistencies.

There is no pub/sub signal system — the framework owns all state transitions. UI subscribes to state changes through the client's `subscribe()` callback.

### Our plan

Uses the engine's existing `Signals` (blinker-based pub/sub). New signals: `BOARD.TURN_STARTED`, `BOARD.TURN_ENDED`, `BOARD.MOVE_SUBMITTED`, `BOARD.GAME_OVER`, `BOARD.PIECE_PLACED`, `BOARD.PIECE_REMOVED`, `BOARD.PIECE_ARRIVED`.

### Takeaways

- **Different paradigms, both valid.** boardgame.io's event queuing prevents re-entrancy bugs. Our signal system is synchronous but well-understood in the engine.
- **Our signals are richer for rendering.** `PIECE_PLACED`, `PIECE_ARRIVED` etc. have no equivalent in boardgame.io because it doesn't own rendering. These are essential for animation and FX.

---

## 8. Features We Don't Need (v1)

These boardgame.io features are irrelevant or premature for our plan:

| Feature | Why skip |
|---|---|
| Client/server networking | Single-process, no multiplayer |
| Optimistic updates | No network latency to hide |
| Redux state management | No React, no browser |
| Plugin system | Our engine uses signals + class inheritance; plugins add complexity without clear benefit at this scale |
| Secret state / `playerView` | AI has full board access by design |
| Undo/redo with delta logs | Nice-to-have, not v1 |
| Time travel / replay | Not needed for retro pixel games |
| Immer immutability | No shared state or network sync |

---

## 9. Ideas Worth Borrowing

1. ~~**`enumerate()` for legal moves** — adopted.~~ Added as `MoveValidator.enumerate_moves()` in the plan. Returns all legal moves for a given player. Benefits AI (move selection), UI (highlighting valid targets), and validation.

2. **Turn order presets.** When we extend beyond two-player sequential, boardgame.io's `TurnOrder` presets (round-robin, custom, once-around) are a clean pattern to follow.

3. **Phase concept.** Some board games have distinct modes (setup → play → scoring). Our `TurnManager` could gain an optional `phase` field in the future, gated by a `PhaseConfig` similar to boardgame.io's phase definitions.

4. **Min/max moves per turn.** boardgame.io lets turns enforce move count constraints. Useful for games where a player must make exactly N actions per turn. Easy to add to `TurnManager` later.

5. **AI objectives weighting.** MCTS with named, weighted objectives is an elegant way to tune bot behaviour without rewriting search logic. If we add a generic bot, this pattern is worth adopting.

---

## 10. Conclusion

boardgame.io is a mature, network-first framework designed to decouple game logic from rendering. Our `BoardGame` plan is a rendering-first game *type* within a pixel engine. The two serve fundamentally different audiences:

- **boardgame.io** → web developers building multiplayer board games with any UI framework
- **Our BoardGame** → a pyke_pyxel user building a retro-styled, single-player board game with built-in rendering, sprites, and animation

Our current plan is well-suited to its context. The main refinement adopted from this research is **`MoveValidator.enumerate_moves()`** to formalise legal move generation — benefiting AI, UI, and validation. Other boardgame.io patterns (phases, turn order presets, move count constraints) are good candidates for future iterations but not blockers for v1.
