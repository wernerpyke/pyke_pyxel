# Sprites

The `sprite/` package provides the primary building blocks for visible entities in the engine: animated characters, multi-tile objects, text labels, and RPG-specific sprite variants. These classes are used across multiple systems:

- **Game** — `Sprite` and `CompoundSprite` are added to the game world and drawn each frame
- **HUD** — `Sprite`, `CompoundSprite`, and `TextSprite` serve as UI overlays
- **Drawable** — `Image` and `CompoundSprite` are used as button visuals (see [DRAWABLES.md](DRAWABLES.md))
- **RPGGame** — `MovableSprite` and `OpenableSprite` model characters and interactive objects (see [GAME-TYPES.md](GAME-TYPES.md))

See [README.md](README.md) for the game lifecycle, signal wiring, and code examples.

---

## Class Hierarchy

```
General-purpose (all game types):
  Sprite (base)          — animated, positioned entity
  CompoundSprite         — multi-tile grid sprite with graphics overlay
  TextSprite             — text rendered via a Pyxel font
  Animation              — frame sequence played on a Sprite
  AnimationFactory       — convenience factory for creating Animation instances

RPG game type only (see RPG Sprites section):
  Sprite
  ├── MovableSprite      — directional movement animations (up/down/left/right)
  └── OpenableSprite     — two-state open/close objects (doors, chests)
```

**Public API** (`from pyke_pyxel.sprite import ...`): `Sprite`, `CompoundSprite`, `TextSprite`, `Animation`, `AnimationFactory`, `MovableSprite`, `OpenableSprite`.

---

## Sprite (`pyke_pyxel.sprite.Sprite`)

Base class for all animated, positioned entities. A Sprite holds a set of named `Animation` objects, a current frame to draw, and a position.

### Constructor

```python
Sprite(name: str, default_frame: coord, cols: int = 1, rows: int = 1, resource_image_index: int = 0)
```

| Param | Description |
| --- | --- |
| `name` | Logical name for the sprite. |
| `default_frame` | Frame shown when no animation is active (idle frame), as a `coord` into the resource sheet. |
| `cols` | Width in tiles (default 1). |
| `rows` | Height in tiles (default 1). |
| `resource_image_index` | Pyxel resource image bank index (default 0). |

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Logical name. |
| `default_frame` | `coord` | Idle frame on the resource sheet. |
| `cols` | `int` | Width in tiles. |
| `rows` | `int` | Height in tiles. |
| `active_frame` | `coord` | Currently displayed frame (updated by animations). |
| `animations` | `dict[str, Animation]` | Named animations registered on this sprite. |
| `position` | `coord` | Current position (top-left corner). Raises `AttributeError` if not yet set. |
| `width` | `int` | Width in pixels (read-only). |
| `height` | `int` | Height in pixels (read-only). |
| `rotation` | `float \| None` | Rotation in degrees; returns the active animation's rotation if animating, otherwise the sprite's own rotation. |
| `scale` | `float \| None` | Scale multiplier, or `None` for default (1.0). |
| `is_animating` | `bool` | `True` if an animation is currently active. |

### Methods

| Method | Description |
| --- | --- |
| `add_animation(name, animation)` | Register a named `Animation` on this sprite. |
| `activate_animation(name, on_animation_end=None)` | Start the named animation. No-op if already active. Optional callback `(sprite_id) -> None` fires when a non-looping animation finishes. |
| `deactivate_animations()` | Stop any active animation and reset to the default frame. |
| `active_animation_is(name) -> bool` | Check whether the named animation is currently active. |
| `link_sprite(sprite)` | Link another sprite so its position updates whenever this sprite moves. |
| `unlink_sprite(sprite)` | Remove a previously linked sprite. |
| `set_position(position)` | Set the top-left corner position. Also moves any linked sprites by the same delta. |
| `set_rotation(rotation)` | Set rotation in degrees (normalised to 0–360). `None` or `0.0` clears rotation. |
| `set_scale(scale)` | Set scale multiplier. `1.0` clears scale. |
| `replace_colour(old_colour, new_colour)` | Swap a palette colour when drawing this sprite. |
| `reset_colour_replacements()` | Clear any colour replacement. |
| `rotated_position() -> coord` | Return the top-left corner position after applying rotation around the sprite's centre. |

Equality is based on the `_id` field, which is assigned by `Game` when the sprite is added.

### Example

```python
from pyke_pyxel import coord
from pyke_pyxel.sprite import Sprite, Animation

player = Sprite("player", default_frame=coord(1, 1))

walk = Animation(coord(2, 1), frames=4)
player.add_animation("walk", walk)

def game_start(game):
    player.set_position(coord.with_xy(100, 40))
    game.add_sprite(player)
    player.activate_animation("walk")
```

---

## CompoundSprite (`pyke_pyxel.sprite.CompoundSprite`)

A multi-tile sprite composed of a grid of tile coordinates (cols x rows) with an optional overlay graphics buffer. Useful for larger objects built from multiple sprite sheet tiles. The rendered image is cached and only regenerated when tiles change.

**Not a `Sprite` subclass** — CompoundSprite has its own independent implementation.

### Constructor

```python
CompoundSprite(name: str, cols: int, rows: int, resource_image_index: int = 0)
```

| Param | Description |
| --- | --- |
| `name` | Logical name for the sprite. |
| `cols` | Number of tile columns in the grid. |
| `rows` | Number of tile rows in the grid. |
| `resource_image_index` | Pyxel resource image bank index (default 0). |

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Logical name. |
| `cols` | `list[list[coord \| None]]` | 2D grid of tile coordinates (or `None` for empty tiles). |
| `position` | `coord` | Current position (top-left corner). |
| `width` | `int` | Width in pixels (read-only). |
| `height` | `int` | Height in pixels (read-only). |

### Methods

| Method | Description |
| --- | --- |
| `fill(tile_cols, tile_rows)` | Fill the entire grid by cycling through the provided column and row lists. |
| `fill_col(col, tile_col, tile_rows, from_row=1, to_row=None)` | Fill one column with a repeating sequence of tile rows. Indices are 1-based. |
| `fill_row(row, tile_row, tile_cols, from_col=1, to_col=None)` | Fill one row with a repeating sequence of tile columns. Indices are 1-based. |
| `set_tile(col, row, tile)` | Set a single tile in the grid. Indices are 1-based. |
| `clear_graphics()` | Clear the graphics overlay buffer. |
| `graph_rect(x, y, width_px, height_px, colour)` | Draw a filled rectangle to the graphics overlay (pixel coordinates relative to sprite origin). |
| `graph_triangle(x1, y1, x2, y2, x3, y3, colour)` | Draw a filled triangle to the graphics overlay. |
| `replace_colour(old_colour, new_colour)` | Swap a palette colour when drawing this sprite. |
| `reset_colour_replacements()` | Clear any colour replacement. |
| `set_position(position)` | Set the top-left corner position. |

Equality is based on the `_id` field, which is assigned by `Game` or `HUD` when the sprite is added.

### Example

```python
from pyke_pyxel import coord
from pyke_pyxel.sprite import CompoundSprite

panel = CompoundSprite("wall", cols=3, rows=2)
panel.fill(tile_cols=[1, 2, 3], tile_rows=[1, 2])
panel.set_position(coord.with_xy(0, 0))
game.add_sprite(panel)

# Draw a health bar overlay
panel.clear_graphics()
panel.graph_rect(2, 2, width_px=20, height_px=4, colour=11)
```

---

## TextSprite (`pyke_pyxel.sprite.TextSprite`)

Renders text on screen using the default Pyxel font or a custom BDF font file. **Not a `Sprite` subclass** — added to the HUD text layer rather than the game sprite layer.

### Constructor

```python
TextSprite(text: str, colour: int, font_file: str | None = None)
```

| Param | Description |
| --- | --- |
| `text` | Text content to display. |
| `colour` | Pyxel palette colour index. |
| `font_file` | Path to a BDF font file (optional). If `None`, uses the default Pyxel font. |

### Methods

| Method | Description |
| --- | --- |
| `set_position(position)` | Set the top-left corner position. |
| `set_text(text)` | Update the displayed text content. |
| `set_colour(colour)` | Update the text colour. |

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `position` | `coord` | Current position (top-left corner). |

### Example

```python
from pyke_pyxel import coord
from pyke_pyxel.sprite import TextSprite

score_label = TextSprite("Score: 0", colour=7)
score_label.set_position(coord.with_xy(4, 4))
game.hud.add_text(score_label)

# Update each frame:
score_label.set_text(f"Score: {score}")
```

---

## Animation (`pyke_pyxel.sprite.Animation`)

Represents a single frame-sequence animation for a `Sprite`. Manages frame advancement, looping, optional horizontal flip, rotation, and per-animation FPS control.

### Constructor

```python
Animation(start_frame: coord, frames: int, loop: bool = True, flip: bool = False, fps: int | None = None, rotation: float | None = None)
```

| Param | Description |
| --- | --- |
| `start_frame` | Position of the first frame on the resource sheet. |
| `frames` | Number of frames in the animation. |
| `loop` | Whether the animation loops (`True`) or plays once (`False`). Default `True`. |
| `flip` | Horizontally flip the sprite image during this animation. Default `False`. |
| `fps` | Animation-specific FPS. Must be <= `GameSettings.fps.animation`. If `None`, runs at the global animation FPS. |
| `rotation` | Rotation in degrees applied while this animation is active. Default `None`. |

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `flip` | `bool` | Whether the animation image is horizontally flipped. |
| `rotation` | `float \| None` | Rotation in degrees, or `None` for no rotation. |

### Methods

| Method | Description |
| --- | --- |
| `set_current_frame(frame_index)` | Jump to a specific frame (0-indexed). Raises `ValueError` if index >= frame count. |

### Timing

The `fps` parameter allows individual animations to run slower than the global animation FPS set in `GameSettings.fps.animation`. If `fps` is provided, frames are skipped to achieve the target rate. Setting `fps` higher than the global animation FPS raises a `ValueError`.

### Example

```python
from pyke_pyxel import coord
from pyke_pyxel.sprite import Sprite, Animation

sprite = Sprite("enemy", default_frame=coord(1, 1))

# Looping idle animation at 8 FPS
idle = Animation(coord(2, 1), frames=4, fps=8)
sprite.add_animation("idle", idle)

# One-shot attack animation with completion callback
def on_attack_done(sprite_id):
    sprite.activate_animation("idle")

attack = Animation(coord(6, 1), frames=6, loop=False)
sprite.add_animation("attack", attack)
sprite.activate_animation("attack", on_animation_end=on_attack_done)
```

---

## AnimationFactory (`pyke_pyxel.sprite.AnimationFactory`)

Convenience factory for creating multiple `Animation` instances that share the same frame count, FPS, and loop setting. Reduces boilerplate when building several animations from one sprite sheet.

### Constructor

```python
AnimationFactory(frames: int, fps: int | None = None, loop: bool = True)
```

| Param | Description |
| --- | --- |
| `frames` | Number of frames all created animations will have. |
| `fps` | FPS for all created animations (optional). |
| `loop` | Default loop setting (default `True`). |

### Methods

| Method | Description |
| --- | --- |
| `at(position, flip=False, loop=None, rotation=None) -> Animation` | Create an `Animation` at the given resource sheet position. `loop` overrides the factory default when provided. |

### Example

```python
from pyke_pyxel import coord
from pyke_pyxel.sprite import Sprite, AnimationFactory

anims = AnimationFactory(frames=4, fps=8)

player = Sprite("player", default_frame=coord(1, 1))
player.add_animation("walk", anims.at(coord(2, 1)))
player.add_animation("run", anims.at(coord(2, 2)))
player.add_animation("dodge", anims.at(coord(2, 3), flip=True))
```

---

## RPG Sprites

The following `Sprite` subclasses are designed for use with the `RPGGame` game type. They provide higher-level abstractions for characters that move in four directions and objects that toggle between open and closed states. See [GAME-TYPES.md](GAME-TYPES.md) for the full RPGGame API.

### MovableSprite (`pyke_pyxel.sprite.MovableSprite`)

Sprite subclass with convenience methods for registering directional (up/down/left/right) animations. Used as the base sprite for RPG `Player` and `Enemy` actors. Constructor parameters are identical to `Sprite`.

#### Constructor

```python
MovableSprite(name: str, default_frame: coord, cols: int = 1, rows: int = 1, resource_image_index: int = 0)
```

#### Methods (in addition to Sprite)

| Method | Description |
| --- | --- |
| `set_up_animation(animation)` | Register animation for the UP direction. |
| `set_down_animation(animation)` | Register animation for the DOWN direction. |
| `set_left_animation(animation)` | Register animation for the LEFT direction. |
| `set_right_animation(animation)` | Register animation for the RIGHT direction. |
| `deactivate_movement_animation()` | Stop any active directional animation (up/down/left/right) and reset to default frame. |

#### Example

```python
from pyke_pyxel import coord
from pyke_pyxel.sprite import MovableSprite, AnimationFactory

hero = MovableSprite("hero", default_frame=coord(1, 1))

anims = AnimationFactory(frames=4, fps=8)
hero.set_down_animation(anims.at(coord(2, 1)))
hero.set_up_animation(anims.at(coord(2, 2)))
hero.set_left_animation(anims.at(coord(2, 3)))
hero.set_right_animation(anims.at(coord(2, 3), flip=True))

hero.activate_animation("down")
```

### OpenableSprite (`pyke_pyxel.sprite.OpenableSprite`)

Sprite subclass for objects with open/closed states such as doors and chests. Manages an internal status that determines which frame is displayed. Inherits all `Sprite` functionality.

#### Constructor

```python
OpenableSprite(name: str, open_frame: coord, closed_frame: coord)
```

| Param | Description |
| --- | --- |
| `name` | Logical name for the sprite. |
| `open_frame` | Frame shown when the sprite is open (also used as the default frame). |
| `closed_frame` | Frame shown when the sprite is closed. |

#### Properties (in addition to Sprite)

| Property | Type | Description |
| --- | --- | --- |
| `is_open` | `bool` | `True` if the sprite is in the open state. |
| `is_closed` | `bool` | `True` if the sprite is in the closed state. |

#### Methods (in addition to Sprite)

| Method | Description |
| --- | --- |
| `open()` | Set the sprite to the open state and display the open frame. |
| `close()` | Set the sprite to the closed state and display the closed frame. |

#### Example

```python
from pyke_pyxel import coord
from pyke_pyxel.sprite import OpenableSprite

door = OpenableSprite("door", open_frame=coord(1, 5), closed_frame=coord(2, 5))
door.set_position(coord(5, 3))
game.add_sprite(door)

# Later, in response to player interaction:
if door.is_closed:
    door.open()
```

---

## Integration with Game

The `Game` class manages sprite lifecycle and rendering. Sprites participate in the update/draw loop as follows:

### Sprite Lifecycle

1. **Add** — `game.add_sprite(sprite)` or `Signals.send_add_sprite(sprite)` registers the sprite and assigns a unique `_id`
2. **Update** — each frame, `Game` calls `sprite._update_frame()` at the animation FPS rate to advance active animations
3. **Draw** — each frame, `Game` calls `sprite._draw(settings)` to render the sprite at its current position and frame

### Draw Order

1. Background and TileMap
2. **Game sprites** — `Sprite` and `CompoundSprite` instances added via `game.add_sprite()`
3. **HUD** — backgrounds, HUD sprites, buttons, then text (see [DRAWABLES.md](DRAWABLES.md))
4. FX

### Removal

Sprites are removed via `game.remove_sprite(sprite)` or `Signals.send_remove_sprite(sprite)`.

### Linked Sprites

When a sprite has linked sprites (via `link_sprite()`), moving the parent with `set_position()` automatically shifts all linked sprites by the same pixel delta. This is useful for accessories or status indicators that follow a character.
