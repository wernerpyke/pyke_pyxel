# New Game Types

- [ ] `BoardGame` — turn-based player-vs-AI board games. **PAUSED.** See [board_game/BOARD-GAME-TYPE.md](board_game/BOARD-GAME-TYPE.md) for design plan.

# Documentation

## Pending

- [x] Document `cell_auto/` subsystem (`pyke_pyxel/cell_auto/game.py`, `matrix.py`) in `docs/GAME-TYPES.md` and link to from `docs/README.md`
- [x] Document `drawable/` subsystem (`pyke_pyxel/drawable/`) in `docs/DRAWABLES.md` and link to `docs/README.md` — clarify where `Image`, `Button`, `Rect`, and `Tilemap` live and how they relate to HUD

# Testing

Phases 1-2 are complete — see `docs/TESTING.md` for current coverage.

## Next Up

### Phase 3 — Movement & RPG

- [ ] `Actor` / `MovableActor` (`rpg/actor.py`) — movement system, path following, blocking detection. Requires Map mocking.
- [ ] `CompoundSprite` (`sprite/_compound_sprite.py`) — multi-tile grid, fill operations, off-by-one risk. Requires Pyxel mocking.

### Phase 4 — UI & Input

- [ ] `HUD` (`hud.py`) — collection add/remove, ID assignment. Pure logic.
- [ ] `Button` (`drawable/_button.py`) — click/hover state machine, hit testing. Requires Pyxel mocking.
- [ ] `Keyboard` (`_keyboard.py`) — key-signal registration, repeat-fire prevention. Requires Pyxel mocking.

### Phase 5 — Effects & Extensions

- [ ] `FX` (`fx.py`) — effect lifecycle, update/draw gating. Requires mocking.
- [ ] `Player`, `Enemy`, `Projectile` (`rpg/`) — thin extensions of MovableActor.
- [ ] `Room` (`rpg/room.py`) — signals and map integration.
- [ ] Effect classes (`effects/`) — visual effects, heavily Pyxel-dependent.

### Phase 6 — Integration (Optional)

- [ ] `Game` / `RPGGame` — requires full Pyxel mocking or acceptance-test approach.
- [ ] `Signals` (`signals.py`) — thin blinker wrapper, low priority.
- [ ] `Drawable`, `Image`, `ImageFactory`, `Rect` (`drawable/`) — rendering methods.
