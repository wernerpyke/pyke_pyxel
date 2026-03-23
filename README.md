# 🕹️ Pixel-art Games with Pyxel (and pixel art)

A simple Sprite- and Map-based Python game engine on top of [Pyxel](https://github.com/kitao/pyxel) with example games.

---

## 🎯 Project Structure
- [pyke_pyxel](pyke_pyxel/): a semi-reusable, Sprite- and Map-based game engine on top of Pyxel
    - with an [overview](docs/README.md) and basic [API Documentation](docs/pyke_pyxel_API.md)
- `games`
  - [simple](games/simple/): hello world
  - [td](games/td/): "Maw: Gate of Hell": a tower defence game
  - [rpg](games/rpg/): prototype for a room-based RPG

---

| Maw | Gate | of Hell |
| :--- | :--- | :--- |
| <img src="docs/screenshots/td1.png" width="240"> | <img src="docs/screenshots/td2.png" width="240"> |  <img src="docs/screenshots/td3.png" width="240"> |

---

## 🧩 TODO

- In `Game.remove_sprite`:
    - Consider moving to an approach in which a Sprite is flagged for deletion and then deleted in `update()` rather than removed from the array immediately. The current approach might be a cause for weird callback-type bugs.
- In `pyke_pyxel.sprite.CompoundSprite`:
    - Support animations, would mean caching multiple images (one per frame)
    - Support horizontal flipping
- In `pyke_pyxel.fx`
    - Should FX have its own separate `_update()` so that FX are not updated if `game.pause()`?

---

## 🔧 Setup

```
uv sync --extra dev
```

Scripts (`run-tests.sh`, `run-td.sh`, `run-rpg.sh`, `update-docs.sh`) use `uv run` — no manual venv activation needed.

---

## 🔧 Tools

- **Python 3.x** - not bad once you get used to it but singletons are messy
- **[Pyxel](https://github.com/kitao/pyxel)** — a retro game engine for Python
- **[Aseprite](https://www.aseprite.org/)** — a wonderful pixel art sprite editor
- **[Blinker](https://github.com/pallets-eco/blinker)** - a fast Python in-process signal/event dispatching system
- **[pydocs-markdown](https://niklasrosenstein.github.io/pydoc-markdown/)** - for docstrings documentation
- **[pytest](https://pytest.org/)** - automated testing
- VSCode for development
