# Game Types

The engine provides three game types, each a subclass of the one before it. All share the same constructor signature:

```python
def __init__(self, settings: GameSettings, title: str, resources: str)
```

See [README.md](README.md) for `GameSettings`, signals, and the shared APIs (sprites, HUD, FX, keyboard, timer, map).

---

## Game (`pyke_pyxel.Game`)

The base class for all games. Manages the core game loop, sprites, input, and rendering.

### Lifecycle

#### Update Order

1. Keyboard input polling (fires any signals registered via `keyboard.signal_for_key()`)
2. Mouse events — `Signals.MOUSE.MOVE`, `Signals.MOUSE.DOWN`, `Signals.MOUSE.UP` (if `mouse_enabled`)
3. *--- paused games stop here ---*
4. Timer updates (fires any signals scheduled via `timer.after()` / `timer.every()`)
5. `Signals.GAME.UPDATE` — your per-frame game logic hook
6. FX updates
7. Animation frame advancement

#### Draw Order

1. Background colour
2. TileMap (if set)
3. Debug map overlay (if `settings.debug`)
4. Sprites
5. HUD
6. FX

### Key API

| Method | Description |
| --- | --- |
| `start()` | Begin the game loop. Emits `GAME.WILL_START` then enters pyxel.run(). |
| `add_sprite(sprite)` | Add a `Sprite` or `CompoundSprite` to the game. |
| `remove_sprite(sprite)` | Remove by instance or ID. |
| `set_tilemap(position, tiles_wide, tiles_high)` | Set a repeating background tilemap layer. |
| `pause()` / `unpause()` | Pause/resume game logic and animations. Input still fires. |
| `start_music(number)` / `stop_music()` | Play or stop looping music. |
| `clear_all()` | Reset sprites, HUD, FX, and timers. |

**Properties:** `map`, `keyboard`, `hud`, `fx`, `timer`, `is_paused` (all lazy-initialized except `map` and `keyboard`).

### Example

See [`games/simple/`](../games/simple/) for a minimal Game that moves a sprite toward mouse clicks.

---

## RPGGame (`pyke_pyxel.rpg.RPGGame`)

Extends `Game` with room management, an actor system, and player/enemy lifecycle.

### What It Adds

| Feature | Description |
| --- | --- |
| Room | Convenience layer for placing walls, doors, enemies, and actors on the map. |
| Actor system | Managed collection of `Actor` / `MovableActor` instances, updated each frame. |
| Player | First-class player entity with movement, blocking detection, and door interaction. |
| Enemy tracking | Query enemies by position; automatic dead-actor cleanup. |

### Lifecycle

#### Update Order

1. Keyboard input polling (fires any signals registered via `keyboard.signal_for_key()`)
2. *--- paused games stop here ---*
3. Timer updates (fires any signals scheduled via `timer.after()` / `timer.every()`)
4. `Signals.GAME.UPDATE` — your per-frame game logic hook
5. **Actor updates** — each living actor's movement and pathfinding is advanced; dead actors are removed. During this step:
   - `Signals.PLAYER.MOVED` — when the player crosses a grid-cell boundary
   - `Signals.PLAYER.BLOCKED` — when player movement is blocked (value: the blocking `Sprite`)
   - `Signals.ENEMY.STOPPED` — when an enemy finishes its movement path
   - `Signals.ENEMY.BLOCKED` — when enemy movement is blocked (value: the blocking `Sprite`)
6. FX updates
7. Animation frame advancement

#### Draw Order

Identical to the base `Game`.

### Key API

**RPGGame methods:**

| Method | Description |
| --- | --- |
| `set_player(sprite, speed_px_per_second)` | Assign the player. Accepts a `MovableSprite` or a callable that returns one. Returns `Player`. |
| `add_actor(actor)` / `remove_actor(actor)` | Register or remove an `Actor` from the managed collection. |
| `enemies_at(position, tolerance)` | Return enemies at a `coord` or within an `area`. |

**Properties:** `player`, `room` (in addition to all base `Game` properties).

**Room methods** (`game.room`):

| Method | Description |
| --- | --- |
| `add_wall(sprite, col, row)` | Place a blocking obstacle. |
| `add_door(sprite, col, row, closed)` | Place an openable door (`OpenableSprite`). |
| `add_enemy(sprite, speed_px_per_second)` | Add an enemy. Returns `Enemy`. |
| `add_movable_actor(sprite, speed_px_per_second)` | Add a generic movable actor. Returns `MovableActor`. |
| `add_actor(sprite)` | Add a static (non-moving) actor. Returns `Actor`. |

### Example

See [`games/rpg/`](../games/rpg/) for a room-based RPG with player movement, enemies, doors, and projectiles.

---

## CellAutoGame (`pyke_pyxel.cell_auto.CellAutoGame`)

Extends `Game` with a 2D cellular automaton matrix for simulating spreading effects (fungus, fire, etc.).

### What It Adds

| Feature | Description |
| --- | --- |
| Matrix | A pixel-resolution 2D grid of `Cell` objects, rendered between the background and sprites. |

### Lifecycle

#### Update Order

Identical to the base `Game`. No additional signals.

#### Draw Order

1. Background colour
2. **Matrix**
3. Sprites
4. HUD
5. FX

### Key API

**CellAutoGame methods:**

| Method | Description |
| --- | --- |
| `clear_all()` | Inherited clear plus matrix re-initialization. |

**Properties:** `matrix` (in addition to all base `Game` properties).

**Matrix methods** (`game.matrix`):

| Method | Description |
| --- | --- |
| `cell_at(x, y)` | Return the `Cell` at grid coordinates, or `None` if out of bounds. |
| `neighbours(cell, filter_for_type)` | Return 8-connected neighbours, optionally filtered by cell type. |
| `neighbour_N/S/E/W/NE/NW/SE/SW(cell)` | Return a single directional neighbour or `None`. |
| `cells_at(position, include_empty)` | Return cells within a rectangular region. |
| `cells_in_line(from, to, extend_to_matrix_end)` | Bresenham line trace between two coordinates. |
| `clear()` | Reset all cells to empty. |

**Cell properties:**

| Property | Type | Description |
| --- | --- | --- |
| `x`, `y` | `int` | Grid coordinates. |
| `type` | `str` | Cell state (default `"empty"`, set to any string). |
| `colour` | `int` | Pyxel palette index. Setting this updates the backing image. |
| `can_propogate` | `bool` | Whether this cell can spread to neighbours. |
| `power` | `float` | Intensity value for effect logic. |
| `tag` | `Any` | Arbitrary user data. |
| `is_empty` | `bool` | `True` when `type == "empty"`. |

### Example

See [`games/td/`](../games/td/) for a tower defence game that uses the matrix for weapon effects (fungus spreading, fire lines).
