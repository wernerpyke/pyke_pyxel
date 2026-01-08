# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
See @README for project overview.

## Project Overview

This is a Sprite- and Map-based Python game engine built on top of [Pyxel](https://github.com/kitao/pyxel), a retro game engine for Python. The project contains:

- **pyke_pyxel/**: The reusable game engine library
- **games/**: Example games using the engine (td, rpg, jet, simple)

## Dependencies

Install with: `pip install -r requirements.txt`

Key dependencies: pyxel, blinker (signals), pathfinding, pytest

## Architecture

### Core Classes (pyke_pyxel/)

- **Game** (`game.py`): Main game loop controller. Manages sprites, tilemaps, HUD, FX, and the update/draw cycle. Configured via `GameSettings`.
- **RPGGame** (`rpg/game.py`): Extends Game with room-based RPG mechanics, player/enemy actors, and pathfinding.
- **Sprite** (`sprite/_sprite.py`): Drawable entity with animations. Supports rotation, scaling, colour replacement, and linked sprites.
- **coord** (`_types.py`): Grid-aware coordinate (1-indexed col/row) that also tracks pixel position. Core primitive for positioning.
- **area** (`_types.py`): Grid-aware rectangular region for spatial queries.
- **Signals** (`signals.py`): Pub/sub event system (wraps blinker). Used for decoupled communication between game components.
- **Map** (`map.py`): Spatial grid with blocked/free/open/closed status per tile. Supports A* pathfinding.

### Game Lifecycle

See @docs/README.md for a guide on how to build games with the game engine.

1. Create `GameSettings` and configure (window size, FPS, colours, mouse)
2. Instantiate `Game` or `RPGGame` with settings, title, and `.pyxres` resource path
3. Connect signal handlers (`Signals.connect()`)
4. Call `game.start()` to begin the loop

The update loop runs at `settings.fps.game` and processes:
- Keyboard/mouse input (always)
- `Signals.GAME.UPDATE` signal (unless paused)
- Sprite animation frames (unless paused)
- Draw: background/tilemap, sprites, HUD, FX

### Signal-Driven Design

Games wire logic through signals rather than inheritance:
- `Signals.GAME.WILL_START` - setup before loop starts
- `Signals.GAME.UPDATE` - per-frame game logic
- `Signals.MOUSE.DOWN/UP/MOVE` - mouse input
- Custom signals for game-specific events (enemy_killed, weapon_selected, etc.)

### Resource Files

Games use `.pyxres` files (Pyxel resource format) containing sprites, tilemaps, sounds. Created with Pyxel's editor or Aseprite exports.

### Key Subsystems

- **HUD** (`hud.py`): On-screen UI elements (buttons, images, text)
- **FX** (`fx.py`): Visual effects (circular wipes, splatters, camera shake, scaling)
- **Timer** (`timer.py`): Schedule signals after delays or at intervals
- **Animation** (`sprite/_anim.py`): Frame-based sprite animations with looping and callbacks

## Testing

Run tests with pytest:

```bash
pytest tests/           # Run all tests
pytest tests/ -v        # Verbose output
pytest tests/test_coord.py::TestCoordCreation::test_basic_creation  # Single test
```

Tests cover pure logic components (`coord`, `area`) that don't require Pyxel's graphics context.

## Code Conventions

- Columns and rows are 1-indexed in `coord` and `area`
- Pixel coordinates use `x`/`y`; grid positions use `col`/`row`
- Internal methods prefixed with `_` (e.g., `_update()`, `_draw()`)
- Sprites are added to Game via `game.add_sprite()` or `Signals.send_add_sprite()`
