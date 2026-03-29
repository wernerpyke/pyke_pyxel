# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Sprite- and Map-based Python game engine built on top of [Pyxel](https://github.com/kitao/pyxel), a retro game engine for Python. The project contains:

- **pyke_pyxel/**: The reusable game engine library
- **games/**: Example games using the engine (td, rpg, jet, simple)

**Status:** v0.1.0, active development, no CI/CD.

## Dependencies

Install with: `uv sync --extra dev`

Key dependencies: pyxel, blinker (signals), pathfinding, pytest

## Architecture

The engine is signal-driven: games wire logic through `Signals` (pub/sub) rather than inheritance. The core primitives are `Game`, `coord`, `area`, `Map`, `Sprite`, and `Signals`.

- See `docs/README.md` for usage guide, lifecycle, and code examples (load with `@docs/README.md` when building or enhancing games).
- See `docs/pyke_pyxel_API.md` for auto-generated API reference.
- See `docs/TESTING.md` for test coverage status and priorities.
- See `plans/ROADMAP.md` for roadmap items and status

## Code Conventions

### Python

-   **PEP 8**: Follow the PEP 8 style guide for all Python code.
-   **Naming Conventions**:
    -   `PascalCase` for class names (e.g., `Player`, `SpriteManager`).
    -   `snake_case` for functions, methods, variables, and file names (e.g., `update_player`, `game_loop.py`).
    -   Internal method names are prefixed with `_` (e.g., `_update()`, `_draw()`)
-   **Typing**: Use Python type hints for all new function and method signatures. Analyze existing code for the proper types to use.
-   **Docstrings**: Add Google-style docstrings to all new public modules, classes, and functions to explain their purpose, arguments, and return values. This is critical as documentation is generated from them.

### Imports

- Organize imports in the standard order:
    1.  Standard library imports (e.g., `os`, `sys`).
    2.  Third-party library imports (e.g., `pyxel`).
    3.  Local application/library imports (e.g., `from pyke_pyxel import draw`).

### Refactoring

**Refactoring:** When asked to refactor code, prioritize **readability** over extreme micro-optimizations.

### Common Tasks

When asked to perform a task, use the following commands and workflows.

#### Running Games

- `./scripts/run-rpg.sh` — RPG game
- `./scripts/run-td.sh` — Tower Defense game ("Maw: Gate of Hell")

#### Testing

The tests in the `tests/` folder are implemented using `pytest`.

Run tests with `./scripts/run-tests.sh`. To run a specific file: `./scripts/run-tests.sh tests/test_coord.py`.

Test coverage is ~24% by class. Core primitives (`coord`, `area`, `Map`, `Sprite`, `Animation`, `Timer`) have good coverage; UI, drawing, and effects modules do not. See `docs/TESTING.md` for details.

#### Adding and Updating Documentation

The `docs/` directory is organised as follows:

- **`docs/README.md`** — Human-first how-to guide for building games with the engine. Keep it readable and example-driven; it should be useful to Claude but written for humans first.
- **`docs/pyke_pyxel_API.md`** — Auto-generated API reference from source code docstrings. Regenerate with `./scripts/update-docs.sh`.
- **Stand-alone topic docs** — Additional architectural areas (e.g. drawable, cell_auto) should be documented in their own markdown files in `docs/` and linked from `docs/README.md`.

The `plans/` directory holds roadmap and planning documents:

- **`plans/ROADMAP.md`** — Roadmap items and status tracking.

Keep `docs/` for technical documentation (guides, API reference, architecture) and `plans/` for project planning (roadmaps, milestones, design proposals).

#### Profiling

Run `tools/profiler.py` to benchmark performance.

### Game Engine Rules
- Columns and rows are 1-indexed in `coord` and `area` — never use 0-indexed grid coordinates
- Pixel coordinates use `x`/`y`; grid positions use `col`/`row`
- Sprites are added to Game via `game.add_sprite()` or `Signals.send_add_sprite()`
- Do not instantiate Pyxel directly — always go through `Game`
- Do not import from internal `_`-prefixed modules directly — use the public API from package `__init__.py` exports