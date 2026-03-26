# Documentation

## Pending

- [ ] Document `cell_auto/` subsystem (`pyke_pyxel/cell_auto/game.py`, `matrix.py`) in `docs/README.md` and `CLAUDE.md`
- [ ] Document `drawable/` subsystem (`pyke_pyxel/drawable/`) in `docs/README.md` — clarify where `Image`, `Button`, `Rect`, and `Tilemap` live and how they relate to HUD

# Testing
## Ranked Testing Priority List

### Priority 1 - Critical (Pure Logic, High Complexity)

#### 1.1 Map (`map.py`) ✓ COMPLETE
- [x] Test `Map` class (test_map.py)
- **Complexity**: High (35+ methods, ~350 LOC)
- **Criticality**: Core - manages all spatial game state
- **Usage**: Every game uses Map via `game.map`
- **Risk**: High - pathfinding, collision detection, location status
- **Testability**: Easy - pure logic, no Pyxel drawing needed

**Justification**: Map is the second most complex class after coord/area. It handles blocked/open/closed status, adjacency queries, sprite placement, bounds checking, and pathfinding integration. Bugs here cause movement and collision issues.

**Suggested Testing Approach**:
```python
# Test categories:
# 1. Location status management (mark_blocked, mark_open, mark_closed)
# 2. Query methods (is_blocked, is_openable, location_at, sprite_at)
# 3. Adjacency methods (location_left_of, location_right_of, etc.)
# 4. Bounds methods (bound_to_width, bound_to_height)
# 5. Edge case handling (out-of-bounds coords)
# 6. Integration with _PathGrid (find_path)
```

---

#### 1.2 _PathGrid (`_path_grid.py`) ✓ COMPLETE
- [x] Test `_PathGrid` class (test_path_grid.py)
- **Complexity**: Medium (6 methods, ~115 LOC)
- **Criticality**: Core - A* pathfinding algorithm
- **Usage**: Used by Map for all pathfinding
- **Risk**: High - incorrect paths break enemy/player movement
- **Testability**: Easy - pure logic, uses external `pathfinding` library

**Justification**: Pathfinding is notoriously bug-prone. The class handles blocking/opening nodes and coordinate transformations for the pathfinding library. The `reduce_hugging` logic adds complexity.

**Suggested Testing Approach**:
```python
# Test categories:
# 1. Block/open operations
# 2. Neighbour detection
# 3. Path finding (direct paths, around obstacles)
# 4. Diagonal vs non-diagonal movement
# 5. No path scenarios (blocked destination)
# 6. reduce_hugging behavior
```

---

#### 1.3 Animation (`sprite/_anim.py`) ✓ COMPLETE
- [x] Test `Animation` class (test_animation.py)
- [x] Test `AnimationFactory` class (test_animation.py)
- **Complexity**: Medium (10 methods, ~120 LOC)
- **Criticality**: Core - drives all sprite animations
- **Usage**: Every animated sprite uses Animation
- **Risk**: High - frame timing, callbacks, FPS calculations
- **Testability**: Easy - pure logic with time-based behavior

**Justification**: Animation handles frame advancement, looping, flip state, custom FPS, and completion callbacks. Bugs cause visual glitches and broken game logic when `on_animation_end` fails.

**Suggested Testing Approach**:
```python
# Test categories:
# 1. Frame advancement (_update_frame)
# 2. Looping vs non-looping animations
# 3. FPS-based frame skipping
# 4. Callback invocation on animation end
# 5. Activation/deactivation
# 6. AnimationFactory convenience methods
```

---

#### 1.4 Sprite (`sprite/_sprite.py`) ✓ COMPLETE
- [x] Test `Sprite` class (test_sprite.py)
- **Complexity**: High (25+ methods, ~260 LOC)
- **Criticality**: Core - base for all game entities
- **Usage**: Used by every game, HUD, effects
- **Risk**: High - position, rotation, scale, linked sprites
- **Testability**: Medium - has some Pyxel draw calls to mock

**Justification**: Sprite is the foundational entity class. It manages position, rotation, scale, color replacement, animation state, and linked sprites. The `rotated_position()` method involves trigonometry.

**Suggested Testing Approach**:
```python
# Test categories:
# 1. Position management (set_position, position property)
# 2. Rotation (set_rotation, rotated_position with trig)
# 3. Scale management
# 4. Animation lifecycle (add, activate, deactivate)
# 5. Linked sprites (link_sprite, position propagation)
# 6. Color replacement
# 7. Equality comparison
```

---

### Priority 2 - High (Important Business Logic)

#### 2.1 MovableActor (`rpg/actor.py`)
- [ ] Test `Actor` class
- [ ] Test `MovableActor` class
- **Complexity**: High (20+ methods, ~250 LOC)
- **Criticality**: Core for RPG - player/enemy movement
- **Usage**: Base for Player and Enemy classes
- **Risk**: High - pathfinding integration, movement speed, blocking
- **Testability**: Medium - requires Map mocking

**Justification**: MovableActor implements the core movement system including pixel-per-frame calculations, path following, direction-based animation activation, and blocking detection.

**Suggested Testing Approach**:
```python
# Test categories:
# 1. Movement initialization (speed calculations)
# 2. start_moving/stop_moving state changes
# 3. move_to with and without pathfinder
# 4. move_along_path behavior
# 5. Blocking detection and handling
# 6. Direction-based position updates
# 7. Projectile launching
```

---

#### 2.2 CompoundSprite (`sprite/_compound_sprite.py`)
- [ ] Test `CompoundSprite` class
- **Complexity**: High (15 methods, ~210 LOC)
- **Criticality**: Supporting - multi-tile sprites
- **Usage**: UI elements, large game objects
- **Risk**: Medium - tile indexing, graphics buffer
- **Testability**: Medium - rendering requires Pyxel mocking

**Justification**: CompoundSprite manages a grid of tiles with fill operations and an overlay graphics buffer. The `fill`, `fill_col`, `fill_row` methods have indexing logic that could have off-by-one errors.

**Suggested Testing Approach**:
```python
# Test categories:
# 1. Tile grid initialization
# 2. fill() with various patterns
# 3. fill_col/fill_row operations
# 4. set_tile individual placement
# 5. Graphics buffer operations
# 6. Color replacement
# 7. Position management
```

---

#### 2.3 WeightedChoice & RandomChoice (`math.py`) ✓ COMPLETE
- [x] Test `RandomChoice` class (test_math.py)
- [x] Test `WeightedChoice` class (test_math.py)
- **Complexity**: Low (6 methods, ~75 LOC)
- **Criticality**: Supporting - game randomness
- **Usage**: Spawning, loot, procedural content
- **Risk**: Medium - probability bugs affect game balance
- **Testability**: Easy - pure logic (mock random for determinism)

**Justification**: These classes wrap Python's random module with a clean API. WeightedChoice in particular has probability logic that should be verified. Easy wins for test coverage.

**Suggested Testing Approach**:
```python
# Test categories:
# 1. RandomChoice selection (mock random.choice)
# 2. WeightedChoice probability distribution
# 3. set/add/reset operations
# 4. Edge cases (empty lists, single item)
```

---

#### 2.4 OpenableSprite (`sprite/_rpg_sprites.py`) ✓ COMPLETE
- [x] Test `OpenableSprite` class (test_rpg_sprites.py)
- [x] Test `MovableSprite` class (test_rpg_sprites.py)
- **Complexity**: Low (10 methods, ~90 LOC)
- **Criticality**: Supporting - doors, chests
- **Usage**: RPG games for interactive objects
- **Risk**: Medium - state machine for open/closed
- **Testability**: Easy - simple state logic

**Justification**: OpenableSprite manages a simple state machine (OPEN, CLOSED, OPENING, CLOSING). MovableSprite adds directional animation helpers. Both are thin wrappers but state bugs could trap players.

**Suggested Testing Approach**:
```python
# Test categories:
# 1. Initial state
# 2. open()/close() transitions
# 3. is_open/is_closed properties
# 4. Frame updates based on state
# 5. MovableSprite animation setters
```

---

### Priority 3 - Medium (Supporting Functionality)

#### 3.1 HUD (`hud.py`)
- [ ] Test `HUD` class
- **Complexity**: Medium (10 methods, ~95 LOC)
- **Criticality**: Supporting - UI management
- **Usage**: Every game with on-screen UI
- **Risk**: Low - collection management
- **Testability**: Easy - collection operations

**Suggested Testing Approach**:
```python
# Test categories:
# 1. add_text/add_sprite/add_button/add_bg
# 2. remove_* operations
# 3. ID assignment
# 4. _clear_all
```

---

#### 3.2 FX (`fx.py`)
- [ ] Test `FX` class
- **Complexity**: Medium (8 methods, ~117 LOC)
- **Criticality**: Supporting - visual effects
- **Usage**: Transitions, feedback effects
- **Risk**: Low - effect lifecycle management
- **Testability**: Medium - effect execution requires mocking

**Suggested Testing Approach**:
```python
# Test categories:
# 1. Effect creation methods
# 2. _update/_draw lifecycle
# 3. requires_draw/requires_update properties
# 4. _clear_all
```

---

#### 3.3 Keyboard (`_keyboard.py`)
- [ ] Test `Keyboard` class
- **Complexity**: Low (6 methods, ~90 LOC)
- **Criticality**: Supporting - input handling
- **Usage**: All games with keyboard input
- **Risk**: Medium - signal timing
- **Testability**: Medium - requires Pyxel button mocking

**Suggested Testing Approach**:
```python
# Test categories:
# 1. signal_for_key registration
# 2. remove_signal_for_key
# 3. _update signal firing logic
# 4. Sent flag to prevent repeat firing
```

---

#### 3.4 Button (`drawable/_button.py`)
- [ ] Test `Button` class
- **Complexity**: Medium (12 methods, ~165 LOC)
- **Criticality**: Supporting - UI buttons
- **Usage**: Menu screens, HUD
- **Risk**: Medium - click/hover state machine
- **Testability**: Medium - rendering requires mocking

**Suggested Testing Approach**:
```python
# Test categories:
# 1. State transitions (highlight, push_down, pop_up)
# 2. check_mouse_move behavior
# 3. contains() hit testing
# 4. Icon/text configuration
```

---

### Priority 4 - Lower (Extensions or Require Heavy Mocking)

#### 4.1 Signals (`signals.py`)
- [ ] Test `Signals` class
- **Complexity**: Low (8 methods, ~106 LOC)
- **Criticality**: Core but simple - thin wrapper
- **Testability**: Easy

**Justification**: Thin wrapper around blinker. Low priority because blinker is already tested externally.

---

#### 4.2 Drawable, Image, Rect (`drawable/`)
- [ ] Test `Drawable` class
- [ ] Test `Image` class
- [ ] Test `ImageFactory` class
- [ ] Test `Rect` class
- **Complexity**: Low
- **Testability**: Medium - rendering methods

---

#### 4.3 Player, Enemy, Projectile (`rpg/`)
- [ ] Test `Player` class
- [ ] Test `Enemy` class
- [ ] Test `Projectile` class
- **Complexity**: Low (thin extensions)
- **Testability**: Medium - inherit from MovableActor

---

#### 4.4 Room (`rpg/room.py`)
- [ ] Test `Room` class
- **Complexity**: Low (~85 LOC)
- **Testability**: Medium - signals and map integration

---

#### 4.5 Effect Classes (`effects/`)
- [ ] Test `_Effect` base
- [ ] Test `_CircularWipeEffect`
- [ ] Test `_SplatterEffect`
- [ ] Test `_ScaleEffect`
- [ ] Test `_ScaleInOutEffect`
- [ ] Test `_CameraShakeEffect`
- **Complexity**: Low-Medium
- **Testability**: Hard - heavily visual, require Pyxel mocking

---

#### 4.6 Game & RPGGame (`game.py`, `rpg/game.py`)
- [ ] Test `Game` class
- [ ] Test `RPGGame` class
- **Complexity**: High
- **Testability**: Hard - Pyxel initialization required

**Note**: These are integration-level tests. Consider integration testing approach with Pyxel mock or acceptance testing.

---

## Recommended Testing Order

### Phase 1: Quick Wins (1-2 days) ✓ COMPLETE
1. [x] `_PathGrid` - Critical pathfinding logic (test_path_grid.py)
2. [x] `WeightedChoice` / `RandomChoice` - Simple, high value (test_math.py)
3. [x] `OpenableSprite` / `MovableSprite` - Simple state machines (test_rpg_sprites.py)

### Phase 2: Core Logic (3-5 days) ✓ COMPLETE
4. [x] `Map` - Comprehensive spatial testing (test_map.py)
5. [x] `Animation` - Frame and callback logic (test_animation.py)
6. [x] `Sprite` - Position, rotation, linking (test_sprite.py)

### Phase 3: Movement & RPG (2-3 days)
7. [ ] `Actor` / `MovableActor` - Movement system
8. [ ] `CompoundSprite` - Multi-tile logic

### Phase 4: UI & Input (2-3 days)
9. [ ] `HUD` - Collection management
10. [ ] `Button` - State machine
11. [ ] `Keyboard` - Signal firing

### Phase 5: Effects & Extensions (2-3 days)
12. [ ] `FX` and effect classes
13. [ ] `Player`, `Enemy`, `Projectile`
14. [ ] `Room`

### Phase 6: Integration (Optional)
15. [ ] `Game` / `RPGGame` - With Pyxel mocking
