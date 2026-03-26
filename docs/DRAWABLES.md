# Drawables

The `drawable/` package provides the visual building blocks for the engine: static images, rectangles, interactive buttons, and tiled backgrounds. These classes are used across multiple systems:

- **Game** — `TileMap` renders a repeating tiled background behind everything else
- **HUD** — `Image` and `Rect` serve as UI backgrounds; `Button` handles interaction
- **Effects** — `Image` is consumed by the scale effect for visual transforms

See [README.md](README.md) for the game lifecycle and HUD usage context. See [GAME-TYPES.md](GAME-TYPES.md) for the draw order that determines when each layer renders.

---

## Class Hierarchy

```
Drawable (abstract base)
├── Image       — rectangular section of a Pyxel resource image
├── Button      — interactive two-state button with optional icon and text
└── Rect        — filled/bordered rectangle

Standalone (not Drawable subclasses):
├── TileMap      — repeating tiled background (set via Game)
└── ImageFactory — convenience factory for creating Image instances
```

**Public API** (`from pyke_pyxel.drawable import ...`): `Drawable`, `Image`, `ImageFactory`, `Button`, `Rect`.
`TileMap` is internal — set it via `game.set_tilemap()`.

---

## Drawable (`pyke_pyxel.drawable.Drawable`)

Abstract base class that defines the shared interface for all positioned, renderable UI elements.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `position` | `coord` | Top-left corner. Raises `ValueError` if not yet set. |
| `width` | `int` | Width in pixels (read-only). |
| `height` | `int` | Height in pixels (read-only). |

### Methods

| Method | Description |
| --- | --- |
| `set_position(position: coord)` | Set the top-left corner position. |
| `contains(x, y) -> bool` | Hit-test: returns `True` if the pixel coordinate falls within bounds. |
| `_render_image(settings) -> pyxel.Image` | Render to an off-screen image (used by Button for caching). |
| `_draw(settings)` | Draw to the screen at the current position. |

Equality is based on the `_id` field, which is assigned by `HUD` when the drawable is added.

---

## Image (`pyke_pyxel.drawable.Image`)

Renders a rectangular section from a Pyxel resource image bank. Dimensions are expressed in tile units and converted to pixels using `settings.size.tile`.

### Constructor

```python
Image(frame: coord, cols: int = 1, rows: int = 1, image_index: int = 0)
```

| Param | Description |
| --- | --- |
| `frame` | Top-left corner of the graphic on the resource sheet (pixel coordinates). |
| `cols` | Width in tiles (default 1). |
| `rows` | Height in tiles (default 1). |
| `image_index` | Pyxel resource image bank index (default 0). |

### Example

```python
from pyke_pyxel.drawable import Image

logo = Image(frame=coord(1, 1), cols=24, rows=10, image_index=1)
logo.set_position(coord(0, 0))
game.hud.add_bg(logo)
```

---

## ImageFactory (`pyke_pyxel.drawable.ImageFactory`)

Convenience factory for creating multiple `Image` instances that share the same dimensions and resource bank. Useful when building several buttons from one sprite sheet region.

### Constructor

```python
ImageFactory(cols: int = 1, rows: int = 1, image_index: int = 0)
```

### Methods

| Method | Description |
| --- | --- |
| `at(position: coord) -> Image` | Create an `Image` at the given frame coordinate on the resource sheet. |

### Example

```python
from pyke_pyxel.drawable import ImageFactory, Button

imgs = ImageFactory(cols=16, rows=4, image_index=1)
play_button = Button(
    name="play",
    up=imgs.at(coord(1, 11)),
    down=imgs.at(coord(17, 11)),
)
```

---

## Button (`pyke_pyxel.drawable.Button`)

Interactive clickable button built from two visuals — an "up" state and a "down" state. Each state can be an `Image` or a `CompoundSprite`. Buttons optionally support an icon overlay and a text label.

### Constructor

```python
Button(name: str, up: CompoundSprite | Image, down: CompoundSprite | Image)
```

### State Machine

```
Normal                     Highlighted                Pressed
(mouse outside)     →      (mouse inside)      →      (mouse click)
up image + up icon         up image + down icon       down image + down icon
text colour                highlight colour           highlight colour
```

State transitions are driven by `check_mouse_move(x, y)`, which is called automatically via HUD mouse signals.

### Methods

| Method | Description |
| --- | --- |
| `set_icon(up, down)` | Set optional icon overlays (`CompoundSprite` or `Image`). |
| `set_text(text, font, colour, alignment, highlight_colour)` | Add a text label. Alignment: `'left'`, `'center'`, `'right'`. |
| `highlight(active: bool)` | Manually enable/disable highlight state. |
| `push_down()` | Set button to pressed state. |
| `pop_up()` | Set button to released state. |
| `check_mouse_move(x, y)` | Update highlight/pressed state based on mouse position. |
| `contains(x, y) -> bool` | Hit-test (inherited from Drawable). |

### Example

```python
from pyke_pyxel.drawable import ImageFactory, Image, Button

imgs = ImageFactory(cols=4, rows=4)
btn = Button("attack", imgs.at(coord(1, 1)), imgs.at(coord(5, 1)))
btn.set_icon(
    up=Image(coord(1, 13), cols=4, rows=4),
    down=Image(coord(5, 13), cols=4, rows=4),
)
btn.set_position(coord(10, 10))
game.hud.add_button(btn)
```

See [`games/td/ui/`](../games/td/ui/) for full button usage including text labels, weapon selection, and pause buttons.

---

## Rect (`pyke_pyxel.drawable.Rect`)

Simple rectangle with optional background fill and border. Position is set in the constructor. Dimensions are in tile units.

### Constructor

```python
Rect(position: coord, col_count: int, row_count: int)
```

### Methods

| Method | Description |
| --- | --- |
| `set_background(colour: int)` | Set the fill colour (Pyxel palette index). |
| `set_border(colour: int, width: int)` | Set the border colour and width in pixels. |

### Example

```python
from pyke_pyxel.drawable import Rect

panel = Rect(position=coord(8, 6), col_count=24, row_count=30)
panel.set_background(0)       # black fill
panel.set_border(1, 2)        # dark-blue border, 2px wide
game.hud.add_bg(panel)
```

---

## TileMap (`pyke_pyxel.drawable.TileMap`)

Repeating tiled background rendered from a Pyxel resource tilemap. **Not a `Drawable` subclass** and not part of the public API — it is created internally by `Game.set_tilemap()`.

TileMap is distinct from `Map`: TileMap is a **visual** background layer; `Map` is the **spatial/collision** logic grid. They are independent systems.

### How It Works

1. `game.set_tilemap()` creates a `TileMap` from the specified resource region
2. The constructor pre-renders the repeating pattern into a cached `pyxel.Image` sized to fill the screen
3. Each frame, `Game._draw_background()` blits the cached image — no per-tile work at runtime

### Usage

```python
# Set a repeating 8x8 tile background from tilemap resource position (1, 1)
game.set_tilemap(coord(1, 1), tiles_wide=8, tiles_high=8)
```

See [`games/td/game_load.py`](../games/td/game_load.py) for a working example.

---

## Integration with HUD

The `HUD` class (`game.hud`) manages drawable elements in layered collections. Elements are added via typed methods and drawn in a fixed order:

### Draw Order

1. **Backgrounds** — `Image`, `Rect`, or any `Drawable` (via `add_bg()`)
2. **Sprites** — `Sprite` or `CompoundSprite` (via `add_sprite()`)
3. **Buttons** — `Button` instances (via `add_button()`)
4. **Text** — `TextSprite` instances (via `add_text()`)

### HUD API

| Method | Description |
| --- | --- |
| `add_bg(item)` | Add a `Drawable`, `Image`, or `Rect` to the background layer. |
| `remove_bg(item)` | Remove a background drawable. |
| `add_button(button)` | Add a `Button`. |
| `remove_button(button)` | Remove a button. |
| `add_sprite(sprite)` | Add a `Sprite` or `CompoundSprite`. |
| `remove_sprite(sprite)` | Remove a sprite. |
| `add_text(text)` | Add a `TextSprite`. |

Each `add_*` method assigns a unique `_id` used for equality and removal.
