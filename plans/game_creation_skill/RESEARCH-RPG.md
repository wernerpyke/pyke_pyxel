# Research: RPG Game Analysis

Analysis of `games/rpg/` to inform spec template and Python template design.

---

## 1. Spec Template Fitness

### Sections That Map Well

**Game Type** — Maps directly. Value: `RPGGame`.

**Title and Assets** — Maps directly.
- Title: `"Pyke Dungeon RPG"`
- Resources: `assets/sample.pyxres`
- Sprite transparency colour: not explicitly set (uses engine default, BEIGE)

**Settings** — Maps well. The RPG sets:
- Window size: 160
- FPS game: 30
- FPS animation: 8
- Debug: True

**Sprites** — The template structure works but needs adaptation for RPG-specific sprite types. The RPG uses four distinct sprite categories, each needing different spec fields:

| Category | Engine class | Spec needs |
|---|---|---|
| Player | `MovableSprite` | Default frame, 4 directional animations (up/down/left/right), flip flags, speed |
| Enemy | `MovableSprite` | Same as player |
| Wall | `Sprite` | Default frame only (no animations) |
| Door | `OpenableSprite` | Closed frame + open frame (two coords) |
| Projectile | `Sprite` | Default frame + looping animation |

The current template has a single `Sprites` section with a flat structure. This works for simple sprites but doesn't capture the RPG distinction between walls, doors, projectiles, and movable characters. Specifically:

1. **MovableSprite directional animations** — The template lists animations as generic name/frame/count tuples, but RPG movable sprites use a standardised pattern: `set_up_animation`, `set_down_animation`, `set_left_animation`, `set_right_animation` with an `AnimationFactory`. The template should have a shorthand for "directional sprite with N frames per direction" rather than requiring 4 separate animation entries.

2. **OpenableSprite dual-frame** — Doors/chests need two frames (closed + open), not a default frame + animations. The template has no field for this.

3. **AnimationFactory frame count** — The RPG uses `AnimationFactory(2)` to create all directional animations with a shared frame count. This is a single value that applies across all directions.

4. **Flip flag** — Left animations reuse right animation frames with `flip=True`. The template does mention "flipped" but the RPG pattern is specifically: left reuses right's frames, flipped.

**Game Start** — Maps well. The RPG's game start logic (`game_started` in `game_loop.py`) creates and positions an enemy, then starts it moving. The template's "Game Start" section could capture this.

**Game Update** — Maps well for describing per-frame logic. The RPG update handles keyboard input for player movement and actions (X to interact, Z to fire projectile, arrows to move).

**Input > Keyboard** — Maps well. The RPG uses:
- Arrow keys: directional movement (press to start, release to stop)
- X key: interact with adjacent openable
- Z key: fire projectile in facing direction

**Input > Mouse** — Not used by RPG. Mouse is not enabled.

### Sections That Are Missing

**Room / Map Layout** — The RPG has a `game_load.py` that builds a room by placing walls and doors at specific grid coordinates. There is no spec section for describing a room/map layout. This is a major gap. The spec needs a way to describe:
- Wall placements (sprite type + position)
- Door placements (sprite type + position + initial open/closed state)
- Helper patterns like `build_horizontal_wall(type, fromCol, toCol, row)`
- Player starting position

**Sprite Config / Factory Pattern** — The RPG has a dedicated `config.py` that acts as a sprite catalogue/factory. Each entry is a static method that returns a configured sprite instance. The spec needs to capture this catalogue concept — the mapping from a logical name (e.g., `WALLS.BROWN`) to a sprite definition.

**Collision / Blocking Signals** — The RPG wires `Signals.PLAYER.BLOCKED` and `Signals.ENEMY.BLOCKED` handlers. The spec template has a "Game Rules" section but no specific field for collision/blocking behaviour. For RPG games, blocked-by handling is a core mechanic.

**Projectiles** — The RPG has a projectile system (`player.launch_projectile`). No spec field exists for projectile definitions (sprite, speed, direction).

**Enemy Behaviour** — The RPG has simple enemy AI (random direction change when blocked). The "AI" section exists but is marked "BoardGame only". RPG enemies also need behavioural descriptions.

**FPS Animation** — The settings table has no row for animation FPS (`settings.fps.animation`), only game FPS. The RPG sets this to 8.

**Debug Flag** — No field for `settings.debug`.

### Sections That Are Unnecessary for RPG

- **Board** (BoardGame only) — Not applicable
- **Pieces** (BoardGame only) — Not applicable
- **Turn Rules** (BoardGame only) — Not applicable
- **Win Condition** (BoardGame only) — Not applicable
- **AI** (BoardGame only) — Though a more generic "NPC/Enemy Behaviour" section would be useful

### Concrete Spec Values for This Game

If filling out the template for this RPG, here is what the non-obvious fields would need:

```
Game Type: RPGGame

Title: "Pyke Dungeon RPG"
Resources: assets/sample.pyxres

Settings:
  Window size: 160
  FPS game: 30
  FPS animation: 8
  Debug: True

Sprite Catalogue:
  Walls:
    BROWN: frame (2,14)
    GREY: frame (8,14)
    LAVA: frame (6,14), name "lava wall"
    BOULDER: frame (7,14)
  Doors:
    BROWN: closed (10,15), open (8,15)
  Projectiles:
    FIREBALL: frame (6,5), animation "go" at (6,5) 2 frames
  Player:
    name: "player", default (1,1), speed 30
    Animations (2 frames each via AnimationFactory):
      UP: (4,1)
      DOWN: (2,1)
      LEFT: (6,1) flipped
      RIGHT: (6,1)
  Enemies:
    DEMON:
      name: "demon", default (1,3), speed 20
      Animations (2 frames each via AnimationFactory):
        UP: (3,3)
        DOWN: (1,3)
        LEFT: (5,3) flipped
        RIGHT: (5,3)

Room Layout:
  Walls:
    BROWN at (5,10)
    LAVA at (5,11)
    BOULDER at (5,12)
    GREY at (6,13), (6,14)
    BROWN horizontal from (7,10) to (15,10)
    BROWN horizontal from (6,15) to (15,15)
    GREY at (15,11), (15,12), (15,13), (15,14)
  Doors:
    BROWN at (6,10), initially open
  Player start: (1,10)

Keyboard:
  Arrow keys: directional movement (press=start, release=stop)
  X: interact with adjacent openable (open/close door)
  Z: fire FIREBALL projectile at speed 60 in facing direction

Enemy Behaviour:
  DEMON: starts at (10,12), moves in random direction, changes to new random direction when blocked

Collision Rules:
  Player blocked: log which sprite blocked the player (or "edge")
  Enemy blocked: log and change to random direction
  Player interacts with openable: toggle open/close state, update map accordingly
```

---

## 2. Python Template Structure

### File: `main.py` — Entry Point and Wiring

**Structure:**
```
1. Imports (Path, GameSettings, Signals, RPGGame, game modules)
2. Signal wiring (connect signals to handlers)
3. Settings configuration
4. Game instantiation
5. Room building (via game_load)
6. Player creation and positioning
7. game.start()
```

**Boilerplate (same for every RPG game):**
- Import pattern: `Path`, `GameSettings`, `Signals`, `RPGGame`, then local `game_load`, `game_loop`, `config`
- Signal wiring structure: `Signals.connect(signal, handler)`
- Game instantiation: `RPGGame(settings=settings, title=..., resources=...)`
- Final call: `game.start()`

**Game-specific (varies per game):**
- Which signals are wired and to which handlers
- Settings values (window size, FPS, debug, etc.)
- `game_load.build_room(game.room)` — the load function name/args
- `game.set_player(config.PLAYER.SPRITE, speed)` — player sprite factory + speed
- `game_load.set_player_position(player)` — player start position

**Signal wiring in this game:**
| Signal | Handler |
|---|---|
| `Signals.GAME.WILL_START` | `game_loop.game_started` |
| `Signals.GAME.UPDATE` | `game_loop.game_update` |
| `Signals.PLAYER.BLOCKED` | `game_loop.player_blocked_by` |
| `Signals.ENEMY.BLOCKED` | `game_loop.enemy_blocked_by` |

**Key observation:** The player is created via `game.set_player(factory, speed)` where the factory is a callable (`config.PLAYER.SPRITE` — a static method reference, not a call). The speed is passed as a second argument (30 in this case). This is an RPGGame-specific API.

### File: `game_loop.py` — Runtime Logic

**Structure:**
```
1. Imports
2. Helper functions (game-specific utilities)
3. game_started(game) handler — one-time setup after game starts
4. game_update(game) handler — per-frame logic
5. Signal handler functions (player_blocked_by, enemy_blocked_by, etc.)
```

**Boilerplate (structural pattern for every RPG):**
- `game_started(game: RPGGame)` function signature — always receives the game instance
- `game_update(game: RPGGame)` function signature — always receives the game instance
- Arrow key movement pattern (lines 36-51) — press starts, release stops. This is a recurring pattern that could be extracted or templated. Uses `keyboard.was_pressed()` / `keyboard.was_released()` with `player.start_moving(DIRECTION.X)` / `player.stop_moving()`
- Blocked-by handler signatures: `player_blocked_by(player: Player, value)` and `enemy_blocked_by(enemy: Enemy, value: Sprite)`

**Game-specific:**
- `game_started`: what enemies to spawn, where, initial behaviour
- `game_update`: what keys do beyond movement (X for interact, Z for projectile)
- Interaction logic (`player_interacts_with` — toggling openables)
- Enemy blocked behaviour (random direction change)
- Helper functions (`choose_random_direction`)

**Key patterns in game_update:**
1. **Action keys** (lines 28-33): Check `keyboard.was_pressed(KEY)`, then perform action. Two actions here:
   - X: find adjacent openable via `player.adjacent_openable(game.map)`, then toggle it
   - Z: `player.launch_projectile(factory, speed, direction)`
2. **Movement keys** (lines 36-51): Arrow key press/release pattern. This is 16 lines of boilerplate that repeats for every RPG with arrow-key movement. Strong candidate for engine-level helper or template default.

**Signal handler patterns:**
- `player_blocked_by(player, value)` — `value` is the blocking Sprite or None (edge). The handler receives the player as first arg and the blocker as second.
- `enemy_blocked_by(enemy, value)` — `value` is the blocking Sprite. Handler receives the enemy as first arg and blocker as second.

### File: `game_load.py` — Room/Map Construction

**Structure:**
```
1. Imports (coord, RPG types, config factories)
2. Helper functions for room building (e.g., build_horizontal_wall)
3. build_room(room: Room) — main room construction function
4. set_player_position(player: Player) — player start position
```

**Boilerplate:**
- Function signatures: `build_room(room: Room)` and `set_player_position(player: Player)`
- Import of `coord` and `Room`/`Player` from `pyke_pyxel.rpg`
- Import of sprite factories from `config`

**Game-specific:**
- All wall/door placements and coordinates
- Helper functions like `build_horizontal_wall` (game-specific convenience)
- Player starting coordinate

**Key API calls:**
- `room.add_wall(factory, col, row)` — places a wall sprite. The factory is a static method reference (e.g., `WALLS.BROWN`), not an instance.
- `room.add_door(factory, col, row, initially_open)` — places a door. Fourth arg is boolean for initial state.
- `player.set_position(coord(col, row))` — sets player grid position

### File: `config.py` — Sprite Catalogue

**Structure:**
```
1. Imports (dataclass, coord, sprite classes, Animation, AnimationFactory)
2. OBJECTS dataclass — string constants for sprite names
3. WALLS class — static factory methods returning Sprite instances
4. DOOR class — static factory methods returning OpenableSprite instances
5. PROJECTILE class — static factory methods returning animated Sprite instances
6. PLAYER class — static factory method returning configured MovableSprite
7. ENEMY class — static factory methods returning configured MovableSprite
```

**Boilerplate (pattern for every RPG config):**
- Each sprite category is a class with `@staticmethod` factory methods
- `OBJECTS` dataclass holds name constants
- `MovableSprite` configuration pattern: create sprite with name + default frame, create `AnimationFactory(frame_count)`, call `set_up/down/left/right_animation(anim.at(coord, flip=...))`
- Factory methods return fully configured sprite instances (not classes, not partials)

**Game-specific:**
- Which sprite categories exist and how many variants
- All coord values (frame positions in the sprite sheet)
- Animation frame counts
- Whether left reuses right (flipped) or has its own frames
- Sprite names

**Key patterns:**
- `Sprite(name, default_frame_coord)` — simplest sprite, just a frame
- `OpenableSprite(name, closed_frame_coord, open_frame_coord)` — two states
- `MovableSprite(name, default_frame_coord)` + directional animation setup — the most complex pattern
- `AnimationFactory(n)` is used to create animations with a shared frame count, then `.at(coord, flip=bool)` produces individual `Animation` instances
- Projectile sprites get an animation added and immediately activated

### Cross-File Dependencies

```
main.py
  imports: config (sprite factories), game_load (room building), game_loop (handlers)
  passes: game.room -> game_load, config.PLAYER.SPRITE -> game.set_player

game_loop.py
  imports: config (PROJECTILE, ENEMY factories)
  receives: game instance via signal handlers

game_load.py
  imports: config (WALLS, DOOR factories)
  receives: room and player via function args

config.py
  imports: only engine types (coord, Sprite, etc.)
  no game-module dependencies (leaf node)
```

The dependency graph is clean: `config.py` is a leaf with no game imports. `game_load.py` and `game_loop.py` both import from `config` but not from each other. `main.py` imports all three and wires everything together.

### Template Generation Implications

1. **config.py** can be generated entirely from a sprite catalogue in the spec. Each entry maps to a factory method with predictable code structure.

2. **game_load.py** can be generated from a room layout description. Each wall/door placement is a single `room.add_wall()` or `room.add_door()` call. Helper functions (like `build_horizontal_wall`) are optimisations that could be generated when the spec describes ranges.

3. **game_loop.py** is the most game-specific file. The arrow-key movement block is boilerplate that should be included by default for any RPG. Action keys and their effects are game-specific but follow a consistent pattern (check key, perform action). Signal handlers for blocked-by events are structurally similar.

4. **main.py** is mostly boilerplate with game-specific values slotted in. The signal wiring, settings, and startup sequence follow a fixed pattern.
