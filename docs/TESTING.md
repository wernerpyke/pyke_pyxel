# Testing pyke_pyxel Game Engine

## Summary Statistics

| Metric                   | Count                                                                                                                                                |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Total Python modules     | 40                                                                                                                                                   |
| Total classes            | ~45                                                                                                                                                  |
| Classes with tests       | 11                                                                                                                                                   |
| Test coverage (by class) | ~24%                                                                                                                                                 |
| Test files               | 9 (test_coord.py, test_area.py, test_timer.py, test_path_grid.py, test_math.py, test_rpg_sprites.py, test_map.py, test_animation.py, test_sprite.py) |

### Currently Tested
- `coord` - Comprehensive tests (50+ test cases)
- `area` - Comprehensive tests (22+ test cases)
- `Timer` - Good coverage (21 test cases)
- `_PathGrid` - Good coverage (22 test cases)
- `WeightedChoice` / `RandomChoice` - Good coverage (20 test cases)
- `OpenableSprite` / `MovableSprite` - Good coverage (25 test cases)
- `Map` - Comprehensive tests (67 test cases)
- `Animation` / `AnimationFactory` - Good coverage (39 test cases)
- `Sprite` - Comprehensive tests (50 test cases)

### Test Infrastructure
- pytest framework with fixtures in `conftest.py`
- `reset_game_settings` fixture for singleton cleanup
- Tests run without Pyxel context (pure logic tests)

---

## Priority Ranking Criteria

Classes are ranked based on:

1. **Complexity** (methods, logic branches, LOC)
   - High: 20+ methods or 150+ LOC
   - Medium: 10-20 methods or 75-150 LOC
   - Low: <10 methods or <75 LOC

2. **Business Criticality**
   - Core: Central to engine functionality
   - Supporting: Important but not critical path
   - Utility: Helper functions

3. **Usage Frequency**
   - High: Imported/used in 5+ modules
   - Medium: 2-4 modules
   - Low: 1 module

4. **Risk Level**
   - High: Handles spatial logic, pathfinding, state machines
   - Medium: Collection management, callbacks
   - Low: Simple getters/setters, rendering

5. **Testability**
   - Easy: Pure logic, no Pyxel dependencies
   - Medium: Requires mocking Pyxel
   - Hard: Deeply integrated with Pyxel rendering

---



---

## Testing Checklist

### Setup Tasks
- [ ] Create test file structure mirroring source
- [ ] Add common fixtures for Sprite/Map/Game mocking
- [ ] Add Pyxel mock utilities if needed

### Per-Class Template
```
- [ ] Create test file
- [ ] Test initialization/construction
- [ ] Test each public method
- [ ] Test property getters/setters
- [ ] Test edge cases (null, empty, bounds)
- [ ] Test error conditions (ValueError, etc.)
```

---

## Notes

### Classes Requiring Pyxel Mocking
The following require mocking `pyxel` module for:
- `pyxel.blt()`, `pyxel.rect()` - drawing
- `pyxel.btnp()`, `pyxel.btn()` - input
- `pyxel.Image` - image buffers

```python
from unittest.mock import MagicMock, patch

@patch('pyke_pyxel.sprite._sprite.pyxel')
def test_sprite_draw(mock_pyxel):
    # Test drawing without actual Pyxel context
    pass
```

### Pure Logic Classes (No Mocking Needed)
- `coord`, `area` - Already tested
- `Timer` - Already tested
- `_PathGrid` - Already tested
- `WeightedChoice`, `RandomChoice` - Already tested
- `OpenableSprite`, `MovableSprite` - Already tested
- `Map`, `Animation`, `AnimationFactory` - Already tested (Phase 2)
- `Sprite` - Already tested (Phase 2)
- `HUD` collection methods
