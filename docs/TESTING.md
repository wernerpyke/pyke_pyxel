# Testing pyke_pyxel Game Engine

## Coverage

| Metric                   | Count |
| ------------------------ | ----- |
| Classes with tests       | 11    |
| Test coverage (by class) | ~24%  |

### Currently Tested

- `coord` — 50+ test cases
- `area` — 22+ test cases
- `Timer` — 21 test cases
- `_PathGrid` — 22 test cases
- `WeightedChoice` / `RandomChoice` — 20 test cases
- `OpenableSprite` / `MovableSprite` — 25 test cases
- `Map` — 67 test cases
- `Animation` / `AnimationFactory` — 39 test cases
- `Sprite` — 50 test cases

### Not Yet Tested

- `HUD` collection methods
- UI, drawing, and effects modules

## Test Infrastructure

- pytest with fixtures in `conftest.py`
- `reset_game_settings` fixture for singleton cleanup
- Tests run without a Pyxel context (pure logic)

## Mocking Pyxel

Classes that call `pyxel.blt()`, `pyxel.rect()`, `pyxel.btnp()`, `pyxel.btn()`, or `pyxel.Image` need the module patched:

```python
from unittest.mock import patch

@patch('pyke_pyxel.sprite._sprite.pyxel')
def test_sprite_draw(mock_pyxel):
    mock_pyxel.IMAGE_SIZE = 256
    # call drawing methods — assertions against mock_pyxel.blt, etc.
```
