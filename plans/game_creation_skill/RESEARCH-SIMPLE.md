# Research: Simple Game Analysis

Analysis of `games/simple/main.py` against GAME-SPEC-TEMPLATE.md and the existing multi-file pattern (`main.py` + `game_loop.py` + `game_load.py`) used by the TD and RPG games.

---

## 1. Spec Template Fitness

### Sections that map well

| Template Section | Simple Game Coverage | Notes |
|---|---|---|
| **Game Type** | `Game` | Straightforward; simple game uses the base `Game` type |
| **Title and Assets** | title=`"Hello, World"`, resources=`assets/resources.pyxres`, transparency=`BEIGE` | All three fields present and needed |
| **Settings** | window=160, tile=8, mouse=yes, bg=BLUE | Maps cleanly to the Settings table |
| **Sprites** | `skeleton` sprite with 4 directional animations | Maps well to the Sprites section format |
| **Game Start** | Sprite positioned at map center, added to game; text sprite added to HUD | Maps to "Game Start" section |
| **Game Update** | Move sprite toward destination, cycle text colour | Maps to "Game Update" section |
| **Input > Mouse** | Mouse down sets destination | Maps well |
| **Input > Keyboard** | Q key resets sprite to center | Maps well |
| **HUD** | `TextSprite` showing instructions, colour-cycling | Partially maps -- the template says "score, turn indicator, health" but the simple game uses a `TextSprite` on the HUD for instructions |

### Sections not needed by this game

- **Board** (BoardGame only) -- not applicable
- **Pieces** (BoardGame only) -- not applicable
- **Turn Rules** (BoardGame only) -- not applicable
- **AI** (BoardGame only) -- not applicable
- **Win Condition** (BoardGame only) -- not applicable
- **Game Rules** -- there are no real "rules" (no collisions, scoring, boundaries); the game is purely a demo of movement. The section exists but would be nearly empty.
- **Sound and Music** -- none used

### What's missing from the template

1. **Game State definition** -- The simple game uses a `@dataclass class _state` with fields `text_colour: int` and `destination: coord`. The template has no section for declaring custom game state. This is critical because every game needs some state, and the skill needs to know what state variables to generate. Proposed section:

   ```
   ## Game State
   > Describe the mutable state the game tracks across frames.
   - `destination`: coord -- where the sprite is moving toward
   - `text_colour`: int -- current colour index for cycling HUD text
   ```

2. **TextSprite / HUD text** -- The HUD section in the template is vague ("Describe any on-screen status displays"). The simple game uses `TextSprite` (a specific engine class) positioned at `coord(2, 2)` with dynamic text and colour-cycling. The template should either:
   - Explicitly support "text elements" in the HUD section, or
   - Have a sub-section for HUD text items with position, initial text, and dynamic behaviour.

3. **Animation details** -- The template's Sprites section says `<n> frames` but doesn't capture the `AnimationFactory` pattern. The simple game uses `AnimationFactory(frames=2)` then `anims.at(coord(col, row))` and `anims.at(coord(col, row), flip=True)`. The template should note:
   - Whether animations share a common frame count (enabling `AnimationFactory`)
   - The `flip` flag for mirrored animations (used for `left` direction)

4. **Sprite movement logic** -- The template's "Game Update" is free-text. For simple movement-toward-destination patterns, it would help to have a structured way to describe sprite movement (e.g., "sprite moves 1px/frame toward destination, activating directional animation"). This is probably fine as free-text though.

5. **Sprite deactivation** -- The game calls `sprite.deactivate_animations()` when the sprite reaches its destination. The template doesn't capture animation lifecycle (activate/deactivate on conditions).

### Concrete spec values for this game

```yaml
game_type: Game
title: "Hello, World"
resources: assets/resources.pyxres
sprite_transparency: BEIGE

settings:
  window_size: 160
  tile_size: 8
  background: BLUE
  mouse_enabled: true

state:
  text_colour: int = 0
  destination: coord = coord(1, 1)

sprites:
  skeleton:
    default_frame: (1, 1)
    animation_factory: { frames: 2 }
    animations:
      down:  at (2, 1)
      up:    at (4, 1)
      right: at (6, 1)
      left:  at (6, 1), flipped

hud:
  text:
    initial: "Click anywhere and then press 'Q'"
    position: (2, 2)
    colour: cycles through 0-15 each frame

input:
  mouse_down: set destination to click position, update text
  keyboard:
    Q: reset destination to map center, update text

game_start:
  - position skeleton at map center
  - add skeleton to game
  - set destination to skeleton position
  - add text to HUD

game_update:
  - if skeleton not at destination, move 1px/frame toward it with directional animation
  - if at destination, deactivate animations
  - cycle text colour (increment mod 16)
```

---

## 2. Python Template Structure

### Current single-file structure (simple/main.py)

The simple game is 122 lines in a single `main.py`. It follows this structure:

```
1. Imports
2. Game State dataclass
3. GameSettings configuration
4. Game instantiation
5. Sprite creation + animation setup
6. TextSprite creation
7. Mouse handler function + signal connection
8. Keyboard handler function + signal connection + key registration
9. game_start() function
10. game_update() function
11. Signal connections for WILL_START and UPDATE
12. game.start()
```

### Proposed three-file split

Looking at the TD game's pattern:
- **`main.py`**: settings, Game creation, signal wiring, `game.start()`
- **`game_load.py`**: sprite creation, positioning, adding to game (called from game_start)
- **`game_loop.py`**: state, start(), update(), and signal handler functions

#### `main.py` (boilerplate + wiring)

```python
from pathlib import Path
import pyxel
from pyke_pyxel import COLOURS, GameSettings
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals

import game_loop

settings = GameSettings()
settings.size.window = 160
settings.size.tile = 8
settings.mouse_enabled = True
settings.colours.background = COLOURS.BLUE
settings.colours.sprite_transparency = COLOURS.BEIGE

game = Game(settings, title="Hello, World",
            resources=f"{Path(__file__).parent.resolve()}/assets/resources.pyxres")

# Signal wiring
Signals.connect(Signals.GAME.WILL_START, game_loop.start)
Signals.connect(Signals.GAME.UPDATE, game_loop.update)
Signals.connect(Signals.MOUSE.DOWN, game_loop.mouse_down)
Signals.connect("q_key_pressed", game_loop.q_key_pressed)

game.start()
```

**Key observation**: `game.keyboard.signal_for_key(pyxel.KEY_Q, "q_key_pressed")` can't be called here because it needs the `game` instance at module level (which it has), but the TD game pattern avoids calling `game.keyboard` in main.py. This could go in `game_loop.start()` instead, since the game instance is passed to it.

#### `game_load.py` (sprite creation + game population)

```python
from pyke_pyxel import coord
from pyke_pyxel.game import Game
from pyke_pyxel.sprite import Sprite, TextSprite, AnimationFactory

def load(game: Game, state):
    # Skeleton sprite
    sprite = Sprite("skeleton", default_frame=coord(1, 1))
    anims = AnimationFactory(frames=2)
    sprite.add_animation("down", anims.at(coord(2, 1)))
    sprite.add_animation("up", anims.at(coord(4, 1)))
    sprite.add_animation("right", anims.at(coord(6, 1)))
    sprite.add_animation("left", anims.at(coord(6, 1), flip=True))

    map = game.map
    position = coord.with_center(map.center_x, map.center_y)
    sprite.set_position(position)
    game.add_sprite(sprite)

    state.destination = position

    # HUD text
    text = TextSprite("Click anywhere and then press 'Q'", state.text_colour)
    text.set_position(coord(2, 2))
    game.hud.add_text(text)

    return sprite, text
```

**Consideration**: The sprites need to be accessible from `game_loop.py` for the update function. The simple game uses module-level variables (`sprite`, `text`). In a split, `game_load.py` would return them and `game_loop.py` would store them in its module scope or in the state object.

#### `game_loop.py` (state + logic + handlers)

```python
from dataclasses import dataclass
import pyxel
from pyke_pyxel import coord
from pyke_pyxel.game import Game
from game_load import load

@dataclass
class _state:
    text_colour: int = 0
    destination: coord = coord(1, 1)

STATE = _state()
sprite = None
text = None

def start(game: Game):
    global sprite, text
    sprite, text = load(game, STATE)
    game.keyboard.signal_for_key(pyxel.KEY_Q, "q_key_pressed")

def update(game: Game):
    pos = sprite.position
    dest = STATE.destination
    # ... movement logic ...
    # ... text colour cycling ...

def mouse_down(game: Game, value: tuple[int, int]):
    x, y = value[0], value[1]
    STATE.destination = coord.with_xy(x, y)
    text.set_text(f"Clicked {STATE.destination}")

def q_key_pressed(game: Game):
    map = game.map
    STATE.destination = coord.with_center(map.center_x, map.center_y)
    text.set_text("Click again")
```

### Boilerplate vs game-specific code

| Element | Boilerplate (templatable) | Game-specific |
|---|---|---|
| Imports in main.py | Yes -- always `Path`, `GameSettings`, `COLOURS`, `Signals`, `Game` | Game type import varies (`Game` vs `RPGGame` vs `CellAutoGame`) |
| `GameSettings` block | Structure is boilerplate; values are game-specific | Values from spec |
| `Game(...)` instantiation | Pattern is boilerplate | Title, resources path from spec |
| `Signals.connect` for WILL_START, UPDATE | Always present | Additional signals are game-specific |
| `game.start()` | Always the last line | Always the same |
| State dataclass | Pattern is boilerplate | Fields are game-specific |
| `game_load.py` structure | `load(game)` function pattern | Sprite definitions, positions, animations are game-specific |
| `game_loop.py` start/update | Function signatures are boilerplate | All logic inside is game-specific |

### Essential structural elements for `base_main.py`

1. **Imports**: `Path`, `GameSettings`, `COLOURS`, `Signals`, game type class, `import game_loop`
2. **Settings block**: All `GameSettings` assignments
3. **Game instantiation**: `game = GameType(settings, title=..., resources=...)`
4. **Core signal wiring**: `WILL_START -> game_loop.start`, `UPDATE -> game_loop.update`
5. **Input signal wiring**: Mouse signals (if enabled), keyboard signal names
6. **`game.start()`**: Always last

### Observations for template design

1. **The simple game is small enough that the three-file split adds overhead** -- the TD game benefits because `game_load.py` is complex (tilemaps, compound sprites, HUD loading). For a simple game, `game_load.py` might be only 15-20 lines. But consistency across all game types is valuable for the skill's code generation.

2. **Module-level sprite references are a pattern to handle carefully.** The simple game declares `sprite` and `text` at module level, then uses them in both `game_start` and `game_update`. In a split, `game_loop.py` needs references to sprites created in `game_load.py`. Options:
   - Return sprites from `load()` and store as module globals in `game_loop.py` (shown above)
   - Store sprites in the state dataclass
   - Access sprites from `game.sprites` by name (the engine may support this)

3. **Keyboard signal registration needs the game instance.** `game.keyboard.signal_for_key()` is called with the game object. In the current simple game this is at module level (line 63), but in the split it should move to `game_loop.start()` since that receives the game instance.

4. **The `_state` dataclass pattern is consistent** -- both simple game and TD game use it. This should be a standard part of the `game_loop.py` template.

5. **Signal handler signatures vary.** Some take `(game: Game)`, some take `(game: Game, value: ...)`. The template needs to generate correct signatures based on which signal is being handled:
   - `MOUSE.DOWN` and `MOUSE.MOVE`: `(game: Game, value: tuple[int, int])`
   - `MOUSE.UP`: `(game: Game)`
   - `GAME.WILL_START` and `GAME.UPDATE`: `(game: Game)`
   - Custom keyboard signals: `(game: Game)`
