# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

Only when asked to build or enhance games then see @docs/README.md for a guide on how to use the game engine. When asked to work on the engine in `pyke_pyxel` or to add or update tests do not load this file.

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

## Code Conventions

### 1. Python

-   **PEP 8**: Follow the PEP 8 style guide for all Python code.
-   **Naming Conventions**:
    -   `PascalCase` for class names (e.g., `Player`, `SpriteManager`).
    -   `snake_case` for functions, methods, variables, and file names (e.g., `update_player`, `game_loop.py`).
    -   Internal method names are prefixed with `_` (e.g., `_update()`, `_draw()`)
-   **Typing**: Use Python type hints for all new function and method signatures. Analyze existing code for the proper types to use.
-   **Docstrings**: Add Google-style docstrings to all new public modules, classes, and functions to explain their purpose, arguments, and return values. This is critical as documentation is generated from them.

### 2. Imports

- Organize imports in the standard order:
    1.  Standard library imports (e.g., `os`, `sys`).
    2.  Third-party library imports (e.g., `pyxel`).
    3.  Local application/library imports (e.g., `from pyke_pyxel import draw`).

### 3. Specific Instructions for AI

**Refactoring:** When asked to refactor code, prioritize **readability** over extreme micro-optimizations.

### 4. Common Tasks

When asked to perform a task, use the following commands and workflows.

### Testing

The tests in the `tests/` folder are implemented using `pytest`.

Run tests with the `./scripts/run-tests.sh`.

### Adding and Updating Documentation

The documentation in `docs/` is generated from source code docstrings using `pydoc-markdown`.

Add Google-style docstrings to all new public modules, classes, and functions to explain their purpose, arguments, and return values. This is critical as API documentation is generated from them.

To generate updated API documentation run the script `./scripts/update-docs.sh`.

### 5. Game Engine
- Columns and rows are 1-indexed in `coord` and `area`
- Pixel coordinates use `x`/`y`; grid positions use `col`/`row`
- Sprites are added to Game via `game.add_sprite()` or `Signals.send_add_sprite()`