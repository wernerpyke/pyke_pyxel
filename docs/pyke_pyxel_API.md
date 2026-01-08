# None

## API Reference

* [signals](#pyke_pyxel.signals)
  * [Signals](#pyke_pyxel.signals.Signals)
    * [connect](#pyke_pyxel.signals.Signals.connect)
    * [disconnect](#pyke_pyxel.signals.Signals.disconnect)
    * [send](#pyke_pyxel.signals.Signals.send)
    * [send\_with](#pyke_pyxel.signals.Signals.send_with)
    * [send\_add\_sprite](#pyke_pyxel.signals.Signals.send_add_sprite)
    * [send\_remove\_sprite](#pyke_pyxel.signals.Signals.send_remove_sprite)
* [\_types](#pyke_pyxel._types)
  * [GameSettings](#pyke_pyxel._types.GameSettings)
  * [DIRECTION](#pyke_pyxel._types.DIRECTION)
  * [COLOURS](#pyke_pyxel._types.COLOURS)
  * [coord](#pyke_pyxel._types.coord)
    * [\_\_init\_\_](#pyke_pyxel._types.coord.__init__)
    * [with\_map\_bounds](#pyke_pyxel._types.coord.with_map_bounds)
    * [with\_center](#pyke_pyxel._types.coord.with_center)
    * [with\_xy](#pyke_pyxel._types.coord.with_xy)
    * [is\_different\_grid\_location](#pyke_pyxel._types.coord.is_different_grid_location)
    * [is\_same\_grid\_location](#pyke_pyxel._types.coord.is_same_grid_location)
    * [is\_at](#pyke_pyxel._types.coord.is_at)
    * [is\_above](#pyke_pyxel._types.coord.is_above)
    * [is\_below](#pyke_pyxel._types.coord.is_below)
    * [is\_left\_of](#pyke_pyxel._types.coord.is_left_of)
    * [is\_right\_of](#pyke_pyxel._types.coord.is_right_of)
    * [contains](#pyke_pyxel._types.coord.contains)
    * [diff](#pyke_pyxel._types.coord.diff)
    * [move\_by](#pyke_pyxel._types.coord.move_by)
    * [clone](#pyke_pyxel._types.coord.clone)
    * [clone\_by](#pyke_pyxel._types.coord.clone_by)
    * [collides\_with](#pyke_pyxel._types.coord.collides_with)
    * [distance\_to](#pyke_pyxel._types.coord.distance_to)
    * [x](#pyke_pyxel._types.coord.x)
    * [y](#pyke_pyxel._types.coord.y)
    * [mid\_x](#pyke_pyxel._types.coord.mid_x)
    * [mid\_y](#pyke_pyxel._types.coord.mid_y)
    * [min\_x](#pyke_pyxel._types.coord.min_x)
    * [min\_y](#pyke_pyxel._types.coord.min_y)
    * [max\_x](#pyke_pyxel._types.coord.max_x)
    * [max\_y](#pyke_pyxel._types.coord.max_y)
    * [col](#pyke_pyxel._types.coord.col)
    * [row](#pyke_pyxel._types.coord.row)
  * [area](#pyke_pyxel._types.area)
    * [\_\_init\_\_](#pyke_pyxel._types.area.__init__)
    * [tiles](#pyke_pyxel._types.area.tiles)
    * [boundary\_tiles](#pyke_pyxel._types.area.boundary_tiles)
    * [contains](#pyke_pyxel._types.area.contains)
    * [with\_map\_bounds](#pyke_pyxel._types.area.with_map_bounds)
    * [with\_center](#pyke_pyxel._types.area.with_center)
    * [columns](#pyke_pyxel._types.area.columns)
    * [rows](#pyke_pyxel._types.area.rows)
    * [x](#pyke_pyxel._types.area.x)
    * [y](#pyke_pyxel._types.area.y)
    * [mid\_x](#pyke_pyxel._types.area.mid_x)
    * [mid\_y](#pyke_pyxel._types.area.mid_y)
    * [min\_x](#pyke_pyxel._types.area.min_x)
    * [min\_y](#pyke_pyxel._types.area.min_y)
    * [max\_x](#pyke_pyxel._types.area.max_x)
    * [max\_y](#pyke_pyxel._types.area.max_y)
* [\_button](#pyke_pyxel.drawable._button)
  * [Button](#pyke_pyxel.drawable._button.Button)
    * [\_\_init\_\_](#pyke_pyxel.drawable._button.Button.__init__)
    * [set\_icon](#pyke_pyxel.drawable._button.Button.set_icon)
    * [highlight](#pyke_pyxel.drawable._button.Button.highlight)
    * [push\_down](#pyke_pyxel.drawable._button.Button.push_down)
    * [pop\_up](#pyke_pyxel.drawable._button.Button.pop_up)
    * [check\_mouse\_move](#pyke_pyxel.drawable._button.Button.check_mouse_move)
* [\_drawable](#pyke_pyxel.drawable._drawable)
  * [Drawable](#pyke_pyxel.drawable._drawable.Drawable)
    * [contains](#pyke_pyxel.drawable._drawable.Drawable.contains)
    * [width](#pyke_pyxel.drawable._drawable.Drawable.width)
    * [height](#pyke_pyxel.drawable._drawable.Drawable.height)
    * [position](#pyke_pyxel.drawable._drawable.Drawable.position)
    * [set\_position](#pyke_pyxel.drawable._drawable.Drawable.set_position)
* [\_image](#pyke_pyxel.drawable._image)
  * [Image](#pyke_pyxel.drawable._image.Image)
  * [ImageFactory](#pyke_pyxel.drawable._image.ImageFactory)
    * [at](#pyke_pyxel.drawable._image.ImageFactory.at)
* [game](#pyke_pyxel.game)
  * [Game](#pyke_pyxel.game.Game)
    * [\_\_init\_\_](#pyke_pyxel.game.Game.__init__)
    * [start](#pyke_pyxel.game.Game.start)
    * [clear\_all](#pyke_pyxel.game.Game.clear_all)
    * [add\_sprite](#pyke_pyxel.game.Game.add_sprite)
    * [remove\_sprite](#pyke_pyxel.game.Game.remove_sprite)
    * [remove\_sprite\_by\_id](#pyke_pyxel.game.Game.remove_sprite_by_id)
    * [set\_tilemap](#pyke_pyxel.game.Game.set_tilemap)
    * [pause](#pyke_pyxel.game.Game.pause)
    * [unpause](#pyke_pyxel.game.Game.unpause)
    * [start\_music](#pyke_pyxel.game.Game.start_music)
    * [stop\_music](#pyke_pyxel.game.Game.stop_music)
    * [map](#pyke_pyxel.game.Game.map)
    * [hud](#pyke_pyxel.game.Game.hud)
    * [fx](#pyke_pyxel.game.Game.fx)
    * [keyboard](#pyke_pyxel.game.Game.keyboard)
    * [timer](#pyke_pyxel.game.Game.timer)
* [timer](#pyke_pyxel.timer)
  * [Timer](#pyke_pyxel.timer.Timer)
    * [after](#pyke_pyxel.timer.Timer.after)
    * [every](#pyke_pyxel.timer.Timer.every)
    * [cancel](#pyke_pyxel.timer.Timer.cancel)
    * [has\_timer](#pyke_pyxel.timer.Timer.has_timer)
* [game](#pyke_pyxel.rpg.game)
  * [RPGGame](#pyke_pyxel.rpg.game.RPGGame)
    * [\_\_init\_\_](#pyke_pyxel.rpg.game.RPGGame.__init__)
    * [set\_player](#pyke_pyxel.rpg.game.RPGGame.set_player)
    * [clear\_all](#pyke_pyxel.rpg.game.RPGGame.clear_all)
    * [add\_actor](#pyke_pyxel.rpg.game.RPGGame.add_actor)
    * [remove\_actor](#pyke_pyxel.rpg.game.RPGGame.remove_actor)
    * [enemies\_at](#pyke_pyxel.rpg.game.RPGGame.enemies_at)
    * [player](#pyke_pyxel.rpg.game.RPGGame.player)
    * [room](#pyke_pyxel.rpg.game.RPGGame.room)
* [player](#pyke_pyxel.rpg.player)
  * [Player](#pyke_pyxel.rpg.player.Player)
    * [\_\_init\_\_](#pyke_pyxel.rpg.player.Player.__init__)
    * [adjacent\_openable](#pyke_pyxel.rpg.player.Player.adjacent_openable)
* [actor](#pyke_pyxel.rpg.actor)
  * [Actor](#pyke_pyxel.rpg.actor.Actor)
    * [\_\_init\_\_](#pyke_pyxel.rpg.actor.Actor.__init__)
    * [launch\_projectile](#pyke_pyxel.rpg.actor.Actor.launch_projectile)
    * [remove](#pyke_pyxel.rpg.actor.Actor.remove)
    * [name](#pyke_pyxel.rpg.actor.Actor.name)
    * [position](#pyke_pyxel.rpg.actor.Actor.position)
    * [sprite](#pyke_pyxel.rpg.actor.Actor.sprite)
    * [sprite\_id](#pyke_pyxel.rpg.actor.Actor.sprite_id)
  * [MovableActor](#pyke_pyxel.rpg.actor.MovableActor)
    * [\_\_init\_\_](#pyke_pyxel.rpg.actor.MovableActor.__init__)
    * [set\_position](#pyke_pyxel.rpg.actor.MovableActor.set_position)
    * [start\_moving](#pyke_pyxel.rpg.actor.MovableActor.start_moving)
    * [stop\_moving](#pyke_pyxel.rpg.actor.MovableActor.stop_moving)
    * [move\_to](#pyke_pyxel.rpg.actor.MovableActor.move_to)
    * [move\_along\_path](#pyke_pyxel.rpg.actor.MovableActor.move_along_path)
    * [is\_moving](#pyke_pyxel.rpg.actor.MovableActor.is_moving)
* [room](#pyke_pyxel.rpg.room)
  * [Room](#pyke_pyxel.rpg.room.Room)
    * [add\_wall](#pyke_pyxel.rpg.room.Room.add_wall)
    * [add\_door](#pyke_pyxel.rpg.room.Room.add_door)
    * [add\_enemy](#pyke_pyxel.rpg.room.Room.add_enemy)
* [enemy](#pyke_pyxel.rpg.enemy)
  * [Enemy](#pyke_pyxel.rpg.enemy.Enemy)
    * [\_\_init\_\_](#pyke_pyxel.rpg.enemy.Enemy.__init__)
* [map](#pyke_pyxel.map)
  * [LOCATION\_STATUS](#pyke_pyxel.map.LOCATION_STATUS)
  * [MapLocation](#pyke_pyxel.map.MapLocation)
  * [Map](#pyke_pyxel.map.Map)
    * [sprite\_can\_move\_to](#pyke_pyxel.map.Map.sprite_can_move_to)
    * [mark\_blocked](#pyke_pyxel.map.Map.mark_blocked)
    * [mark\_openable](#pyke_pyxel.map.Map.mark_openable)
    * [mark\_closed](#pyke_pyxel.map.Map.mark_closed)
    * [mark\_open](#pyke_pyxel.map.Map.mark_open)
    * [is\_blocked](#pyke_pyxel.map.Map.is_blocked)
    * [is\_openable](#pyke_pyxel.map.Map.is_openable)
    * [adjacent\_openable](#pyke_pyxel.map.Map.adjacent_openable)
    * [openable\_sprite\_at](#pyke_pyxel.map.Map.openable_sprite_at)
    * [sprite\_at](#pyke_pyxel.map.Map.sprite_at)
    * [location\_at](#pyke_pyxel.map.Map.location_at)
    * [location\_left\_of](#pyke_pyxel.map.Map.location_left_of)
    * [location\_right\_of](#pyke_pyxel.map.Map.location_right_of)
    * [location\_above](#pyke_pyxel.map.Map.location_above)
    * [location\_below](#pyke_pyxel.map.Map.location_below)
    * [random\_location](#pyke_pyxel.map.Map.random_location)
    * [x\_is\_left\_of\_center](#pyke_pyxel.map.Map.x_is_left_of_center)
    * [y\_is\_above\_center](#pyke_pyxel.map.Map.y_is_above_center)
    * [bound\_to\_width](#pyke_pyxel.map.Map.bound_to_width)
    * [bound\_to\_height](#pyke_pyxel.map.Map.bound_to_height)
    * [shortest\_distance\_to\_sides](#pyke_pyxel.map.Map.shortest_distance_to_sides)
    * [random\_distance\_to\_right](#pyke_pyxel.map.Map.random_distance_to_right)
    * [random\_distance\_to\_left](#pyke_pyxel.map.Map.random_distance_to_left)
    * [random\_distance\_down](#pyke_pyxel.map.Map.random_distance_down)
    * [find\_path](#pyke_pyxel.map.Map.find_path)
    * [height](#pyke_pyxel.map.Map.height)
    * [width](#pyke_pyxel.map.Map.width)
    * [center\_x](#pyke_pyxel.map.Map.center_x)
    * [center\_y](#pyke_pyxel.map.Map.center_y)
    * [right\_x](#pyke_pyxel.map.Map.right_x)
    * [bottom\_y](#pyke_pyxel.map.Map.bottom_y)
* [matrix](#pyke_pyxel.cell_auto.matrix)
  * [Cell](#pyke_pyxel.cell_auto.matrix.Cell)
    * [reset](#pyke_pyxel.cell_auto.matrix.Cell.reset)
    * [store\_state](#pyke_pyxel.cell_auto.matrix.Cell.store_state)
    * [recall\_state](#pyke_pyxel.cell_auto.matrix.Cell.recall_state)
  * [Matrix](#pyke_pyxel.cell_auto.matrix.Matrix)
    * [clear](#pyke_pyxel.cell_auto.matrix.Matrix.clear)
    * [neighbour\_N](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_N)
    * [neighbour\_S](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_S)
    * [neighbour\_E](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_E)
    * [neighbour\_W](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_W)
    * [neighbour\_NE](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_NE)
    * [neighbour\_NW](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_NW)
    * [neighbour\_SE](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_SE)
    * [neighbour\_SW](#pyke_pyxel.cell_auto.matrix.Matrix.neighbour_SW)
    * [neighbours](#pyke_pyxel.cell_auto.matrix.Matrix.neighbours)
    * [cell\_at](#pyke_pyxel.cell_auto.matrix.Matrix.cell_at)
    * [cells\_at](#pyke_pyxel.cell_auto.matrix.Matrix.cells_at)
    * [cells\_in\_line](#pyke_pyxel.cell_auto.matrix.Matrix.cells_in_line)
* [game](#pyke_pyxel.cell_auto.game)
  * [CellAutoGame](#pyke_pyxel.cell_auto.game.CellAutoGame)
    * [\_\_init\_\_](#pyke_pyxel.cell_auto.game.CellAutoGame.__init__)
* [\_rpg\_sprites](#pyke_pyxel.sprite._rpg_sprites)
  * [OpenableSprite](#pyke_pyxel.sprite._rpg_sprites.OpenableSprite)
    * [\_\_init\_\_](#pyke_pyxel.sprite._rpg_sprites.OpenableSprite.__init__)
    * [close](#pyke_pyxel.sprite._rpg_sprites.OpenableSprite.close)
    * [open](#pyke_pyxel.sprite._rpg_sprites.OpenableSprite.open)
    * [is\_closed](#pyke_pyxel.sprite._rpg_sprites.OpenableSprite.is_closed)
    * [is\_open](#pyke_pyxel.sprite._rpg_sprites.OpenableSprite.is_open)
  * [MovableSprite](#pyke_pyxel.sprite._rpg_sprites.MovableSprite)
    * [\_\_init\_\_](#pyke_pyxel.sprite._rpg_sprites.MovableSprite.__init__)
    * [set\_up\_animation](#pyke_pyxel.sprite._rpg_sprites.MovableSprite.set_up_animation)
    * [set\_down\_animation](#pyke_pyxel.sprite._rpg_sprites.MovableSprite.set_down_animation)
    * [set\_left\_animation](#pyke_pyxel.sprite._rpg_sprites.MovableSprite.set_left_animation)
    * [set\_right\_animation](#pyke_pyxel.sprite._rpg_sprites.MovableSprite.set_right_animation)
* [\_sprite](#pyke_pyxel.sprite._sprite)
  * [Sprite](#pyke_pyxel.sprite._sprite.Sprite)
    * [\_\_init\_\_](#pyke_pyxel.sprite._sprite.Sprite.__init__)
    * [add\_animation](#pyke_pyxel.sprite._sprite.Sprite.add_animation)
    * [activate\_animation](#pyke_pyxel.sprite._sprite.Sprite.activate_animation)
    * [deactivate\_animations](#pyke_pyxel.sprite._sprite.Sprite.deactivate_animations)
    * [active\_animation\_is](#pyke_pyxel.sprite._sprite.Sprite.active_animation_is)
    * [link\_sprite](#pyke_pyxel.sprite._sprite.Sprite.link_sprite)
    * [unlink\_sprite](#pyke_pyxel.sprite._sprite.Sprite.unlink_sprite)
    * [set\_position](#pyke_pyxel.sprite._sprite.Sprite.set_position)
    * [set\_rotation](#pyke_pyxel.sprite._sprite.Sprite.set_rotation)
    * [set\_scale](#pyke_pyxel.sprite._sprite.Sprite.set_scale)
    * [replace\_colour](#pyke_pyxel.sprite._sprite.Sprite.replace_colour)
    * [reset\_colour\_replacements](#pyke_pyxel.sprite._sprite.Sprite.reset_colour_replacements)
    * [position](#pyke_pyxel.sprite._sprite.Sprite.position)
    * [width](#pyke_pyxel.sprite._sprite.Sprite.width)
    * [height](#pyke_pyxel.sprite._sprite.Sprite.height)
    * [rotation](#pyke_pyxel.sprite._sprite.Sprite.rotation)
    * [scale](#pyke_pyxel.sprite._sprite.Sprite.scale)
* [\_compound\_sprite](#pyke_pyxel.sprite._compound_sprite)
  * [CompoundSprite](#pyke_pyxel.sprite._compound_sprite.CompoundSprite)
    * [fill](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill)
    * [fill\_col](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill_col)
    * [fill\_row](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill_row)
    * [set\_tile](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.set_tile)
    * [clear\_graphics](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.clear_graphics)
    * [graph\_rect](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.graph_rect)
    * [graph\_triangle](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.graph_triangle)
    * [replace\_colour](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.replace_colour)
    * [reset\_colour\_replacements](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.reset_colour_replacements)
    * [set\_position](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.set_position)
    * [position](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.position)
    * [width](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.width)
    * [height](#pyke_pyxel.sprite._compound_sprite.CompoundSprite.height)
* [\_anim](#pyke_pyxel.sprite._anim)
  * [Animation](#pyke_pyxel.sprite._anim.Animation)
    * [\_\_init\_\_](#pyke_pyxel.sprite._anim.Animation.__init__)
    * [set\_current\_frame](#pyke_pyxel.sprite._anim.Animation.set_current_frame)
  * [AnimationFactory](#pyke_pyxel.sprite._anim.AnimationFactory)
    * [\_\_init\_\_](#pyke_pyxel.sprite._anim.AnimationFactory.__init__)
    * [at](#pyke_pyxel.sprite._anim.AnimationFactory.at)
* [\_text\_sprite](#pyke_pyxel.sprite._text_sprite)
  * [TextSprite](#pyke_pyxel.sprite._text_sprite.TextSprite)
    * [set\_position](#pyke_pyxel.sprite._text_sprite.TextSprite.set_position)
    * [position](#pyke_pyxel.sprite._text_sprite.TextSprite.position)
    * [set\_text](#pyke_pyxel.sprite._text_sprite.TextSprite.set_text)
* [hud](#pyke_pyxel.hud)
  * [HUD](#pyke_pyxel.hud.HUD)
    * [add\_text](#pyke_pyxel.hud.HUD.add_text)
    * [add\_sprite](#pyke_pyxel.hud.HUD.add_sprite)
    * [remove\_sprite](#pyke_pyxel.hud.HUD.remove_sprite)
    * [add\_button](#pyke_pyxel.hud.HUD.add_button)
    * [remove\_button](#pyke_pyxel.hud.HUD.remove_button)
    * [add\_bg](#pyke_pyxel.hud.HUD.add_bg)
    * [remove\_bg](#pyke_pyxel.hud.HUD.remove_bg)
* [\_keyboard](#pyke_pyxel._keyboard)
  * [Keyboard](#pyke_pyxel._keyboard.Keyboard)
    * [was\_pressed](#pyke_pyxel._keyboard.Keyboard.was_pressed)
    * [was\_released](#pyke_pyxel._keyboard.Keyboard.was_released)
    * [is\_down](#pyke_pyxel._keyboard.Keyboard.is_down)
    * [signal\_for\_key](#pyke_pyxel._keyboard.Keyboard.signal_for_key)
    * [remove\_signal\_for\_key](#pyke_pyxel._keyboard.Keyboard.remove_signal_for_key)
* [math](#pyke_pyxel.math)
  * [RandomChoice](#pyke_pyxel.math.RandomChoice)
    * [select\_one](#pyke_pyxel.math.RandomChoice.select_one)
  * [WeightedChoice](#pyke_pyxel.math.WeightedChoice)
    * [set](#pyke_pyxel.math.WeightedChoice.set)
    * [add](#pyke_pyxel.math.WeightedChoice.add)
    * [reset](#pyke_pyxel.math.WeightedChoice.reset)
    * [select\_one](#pyke_pyxel.math.WeightedChoice.select_one)
* [fx](#pyke_pyxel.fx)
  * [FX](#pyke_pyxel.fx.FX)
    * [circular\_wipe](#pyke_pyxel.fx.FX.circular_wipe)
    * [splatter](#pyke_pyxel.fx.FX.splatter)
    * [scale\_in](#pyke_pyxel.fx.FX.scale_in)
    * [scale\_in\_out](#pyke_pyxel.fx.FX.scale_in_out)
    * [camera\_shake](#pyke_pyxel.fx.FX.camera_shake)

<a id="pyke_pyxel.signals"></a>

# signals

<a id="pyke_pyxel.signals.Signals"></a>

## Signals Objects

```python
class Signals()
```

Signal management system for game events.
This class provides a centralized signal dispatching mechanism for various game events,
organizing signals into categories (GAME, MOUSE) and providing methods
to connect listeners and send signals with optional parameters.

**Attributes**:

- `GAME` - Dataclass containing game-level signal constants
  - WILL_START: Signal emitted before game initialization, Game instance is passed as the sender
  - UPDATE: Signal emitted on each game update cycle, Game instance is passed as the sender
- `MOUSE` - Dataclass containing mouse input signal constants
  - DOWN: Signal emitted on mouse button down, Game instance and a tuple (x, y) is passed
  - UP: Signal emitted on mouse button up
  - MOVE: Signal emitted on mouse movement, Game instance and a tuple (x, y) is passed
  
  RPG-Specific Attributes:
- `PLAYER` - Dataclass containing player-related signal constants
  - BLOCKED: Signal emitted when player movement is blocked
  - INTERACT_OPENABLE: Signal emitted when player can interact with openable objects
  - ATTACK: Signal emitted when player performs an attack action
- `ENEMY` - Dataclass containing enemy-related signal constants
  - BLOCKED: Signal emitted when enemy movement is blocked

<a id="pyke_pyxel.signals.Signals.connect"></a>

#### connect

```python
@staticmethod
def connect(name: str, listener: Callable)
```

Connect a listener callback to a named signal

<a id="pyke_pyxel.signals.Signals.disconnect"></a>

#### disconnect

```python
@staticmethod
def disconnect(name: str, listener: Callable)
```

Disconnect a listener callback from a named signal

<a id="pyke_pyxel.signals.Signals.send"></a>

#### send

```python
@staticmethod
def send(name: str, sender: Any|None = None)
```

Send a signal with an optional sender object

**Arguments**:

- `sender` _Any_ - The object sending the signal.

<a id="pyke_pyxel.signals.Signals.send_with"></a>

#### send\_with

```python
@staticmethod
def send_with(name: str, sender: Any, value: Any)
```

Send a signal with additional data/parameter value

**Arguments**:

- `sender` _Any_ - The object sending the signal.
- `value` _Any_ - The additional data/parameter value

<a id="pyke_pyxel.signals.Signals.send_add_sprite"></a>

#### send\_add\_sprite

```python
@staticmethod
def send_add_sprite(sprite)
```

Globally-available signal to notify the game that a Sprite should been added to the game.
This can be used as a loosely-coupled alternative to `Game.add_sprite`

**Arguments**:

- `sprite` _Sprite | CompoundSprite _ - The sprite to be added to the game.

<a id="pyke_pyxel.signals.Signals.send_remove_sprite"></a>

#### send\_remove\_sprite

```python
@staticmethod
def send_remove_sprite(sprite)
```

Globally-available signal to notify the game that a Sprite should been removed from the game.
This can be used as a loosely-coupled alternative to `Game.remove_sprite`

**Arguments**:

- `sprite` _Sprite | CompoundSprite | int _ - The sprite to be removed from the game. The sprite can be identifed by an int `sprite_id`

<a id="pyke_pyxel._types"></a>

# \_types

<a id="pyke_pyxel._types.GameSettings"></a>

## GameSettings Objects

```python
class GameSettings()
```

Global settings for the game.

Usage:
>>>settings = GameSettings()
>>>settings.size.window = 320
>>> etc.
>>>game = Game(settings=settings)

**Attributes**:

- `debug` _bool_ - defaults to False
- `size.window` _int_ - defaults to 160
- `size.tile` _int_ - defaults to 8
- `colours.sprite_transparency` _int_ - defaults to COLOURS.BLACK
- `colours.background` _int_ - defaults to COLOURS.BLACK
- `colours.debug` _int_ - defaults to COLOURS.BEIGE
- `fps.game` _int_ - frames per second, defaults to 30
- `fps.animation` _int_ - frames per second, defaults to 8
- `display.smoothing` _bool_ - defaults to False
- `display.full_screen` _bool_ - defaults to False
- `pathfinding.allow_diagonal` _bool_ - whether to allow diagonal movement; defaults to True
- `pathfinding.reduce_hugging` _bool_ - whether to reduce tight hugging to obstacle boundaries, defaults to True
- `mouse_enabled` _bool_ - defaults to False

<a id="pyke_pyxel._types.DIRECTION"></a>

## DIRECTION Objects

```python
class DIRECTION(enum.Enum)
```

Enumerated direction values `UP`, `DOWN`, `LEFT`, and `RIGHT`

<a id="pyke_pyxel._types.COLOURS"></a>

## COLOURS Objects

```python
@dataclass
class COLOURS()
```

The pre-defined values for pyxel's colour values

<a id="pyke_pyxel._types.coord"></a>

## coord Objects

```python
class coord()
```

A grid-aware coordinate representing a tile and its pixel position.

coord stores both a grid location (column and row, 1-indexed) and the
corresponding top-left pixel coordinates (x, y) for a square tile of
a given size. It provides helpers for creating coordinates from pixel
centers or raw x/y, testing containment/collision, cloning and moving
in pixel space, and deriving mid/min/max bounding values.

<a id="pyke_pyxel._types.coord.__init__"></a>

#### \_\_init\_\_

```python
def __init__(col: int, row: int, size: int|None = None)
```

Create a coord where col and row are 1-indexed

**Arguments**:

- `col` _int_ - column
- `row` _int_ - row
- `size` _int_ - optionally, the size in pixels of the tile. Defaults to GameSettings.size.tile.

<a id="pyke_pyxel._types.coord.with_map_bounds"></a>

#### with\_map\_bounds

```python
@staticmethod
def with_map_bounds(col: int, row: int, size: int|None = None) -> "coord"
```

Create a coord that is bounded to the min/max col/row values of 
the map as determined by based on `GameSettings.size.window` and `GameSettings.size.tile`

<a id="pyke_pyxel._types.coord.with_center"></a>

#### with\_center

```python
@staticmethod
def with_center(x: int, y: int, size: int|None = None) -> "coord"
```

Create a coord where (x, y) are treated as the visual center.

The returned coord will have its internal pixel `x, y` set so that
the tile's center is at the given coordinates. Grid column/row are
calculated from the center position.

<a id="pyke_pyxel._types.coord.with_xy"></a>

#### with\_xy

```python
@staticmethod
def with_xy(x: int, y: int, size: int|None = None) -> "coord"
```

Create a coord with the provided top-left pixel coordinates.

The provided x and y are used directly as the tile's top-left
pixel coordinates and the grid column/row are computed from them.

<a id="pyke_pyxel._types.coord.is_different_grid_location"></a>

#### is\_different\_grid\_location

```python
def is_different_grid_location(coord: "coord") -> bool
```

Return True when this coord is on a different grid tile than `coord`.

Comparison is based on grid column and row (1-indexed), not pixel
offsets.

<a id="pyke_pyxel._types.coord.is_same_grid_location"></a>

#### is\_same\_grid\_location

```python
def is_same_grid_location(coord: "coord") -> bool
```

Return True when this coord is on the same grid tile as `coord`.

<a id="pyke_pyxel._types.coord.is_at"></a>

#### is\_at

```python
def is_at(coord: "coord") -> bool
```

Return true if this coord is at exactly the same (x,y) location as `coord`

<a id="pyke_pyxel._types.coord.is_above"></a>

#### is\_above

```python
def is_above(coord: "coord") -> bool
```

Return true if this coord is above `coord`

<a id="pyke_pyxel._types.coord.is_below"></a>

#### is\_below

```python
def is_below(coord: "coord") -> bool
```

Return true if this coord is below `coord`

<a id="pyke_pyxel._types.coord.is_left_of"></a>

#### is\_left\_of

```python
def is_left_of(coord: "coord") -> bool
```

Return true if this coord is to the left of `coord`

<a id="pyke_pyxel._types.coord.is_right_of"></a>

#### is\_right\_of

```python
def is_right_of(coord: "coord") -> bool
```

Return true if this coord is to the right of `coord`

<a id="pyke_pyxel._types.coord.contains"></a>

#### contains

```python
def contains(x: int, y: int) -> bool
```

Return True if the pixel (x, y) is within this `coord`'s bounding box.

The bounding box is inclusive on both edges (min <= value <= max).

<a id="pyke_pyxel._types.coord.diff"></a>

#### diff

```python
def diff(other: "coord") -> tuple[int, int]
```

Calculate the difference between this `coord` and the provided `coord`

**Arguments**:

- `other` _coord_ - the `coord` for which to calculate the difference
  

**Returns**:

- `(tuple)` - the x- and y- difference values

<a id="pyke_pyxel._types.coord.move_by"></a>

#### move\_by

```python
def move_by(x: int = 0, y: int = 0)
```

Move this coord by (x, y) pixels and update the grid location.

This mutates the coord in-place. Grid column/row are recalculated
from the new pixel position.

<a id="pyke_pyxel._types.coord.clone"></a>

#### clone

```python
def clone()
```

Return a shallow copy of this coord (same grid location and size).

<a id="pyke_pyxel._types.coord.clone_by"></a>

#### clone\_by

```python
def clone_by(x: int, y: int, direction: DIRECTION|None = None)
```

Return a new coord offset by (x, y) pixels from this one.

When a `direction` is provided ("up", "down", "left", "right")
the resulting grid column/row are adjusted so the cloned tile maps
appropriately to the direction of movement. Without a direction the
grid location is computed from the cloned midpoint.

**Arguments**:

- `x` _int_ - the horizontal pixels by which to move the cloned `coord`
- `y` _int_ - the vertical pixels by which to move the cloned `coord`
- `direction` _DIRECTION, optional_ - the optional direction in which to clone the `coord`

<a id="pyke_pyxel._types.coord.collides_with"></a>

#### collides\_with

```python
def collides_with(coord: "coord", tolerance: int = 1)
```

Return True if this `coord` collides with another `coord` using AABB.
This uses an axis-aligned bounding box (AABB) test with a small tolerance to reduce false positives on exact-edge overlaps.

**Arguments**:

- `coord` _coord_ - the `coord` to check against this `coord`
- `tolerance` _int, optional_ - the pixel tolerance to allow, defaults to `1`

<a id="pyke_pyxel._types.coord.distance_to"></a>

#### distance\_to

```python
def distance_to(coord: "coord") -> float
```

Return the distance between this coord and the provided coord

<a id="pyke_pyxel._types.coord.x"></a>

#### x

```python
@property
def x() -> int
```

Top-left pixel x coordinate for this tile.

<a id="pyke_pyxel._types.coord.y"></a>

#### y

```python
@property
def y() -> int
```

Top-left pixel y coordinate for this tile.

<a id="pyke_pyxel._types.coord.mid_x"></a>

#### mid\_x

```python
@property
def mid_x() -> int
```

Integer x coordinate of the visual center (midpoint) of the tile.

<a id="pyke_pyxel._types.coord.mid_y"></a>

#### mid\_y

```python
@property
def mid_y() -> int
```

Integer y coordinate of the visual center (midpoint) of the tile.

<a id="pyke_pyxel._types.coord.min_x"></a>

#### min\_x

```python
@property
def min_x() -> int
```

Alias for the minimum x (top-left) of the tile bounding box.

<a id="pyke_pyxel._types.coord.min_y"></a>

#### min\_y

```python
@property
def min_y() -> int
```

Alias for the minimum y (top-left) of the tile bounding box.

<a id="pyke_pyxel._types.coord.max_x"></a>

#### max\_x

```python
@property
def max_x() -> int
```

Maximum x (bottom-right) of the tile bounding box.

<a id="pyke_pyxel._types.coord.max_y"></a>

#### max\_y

```python
@property
def max_y() -> int
```

Maximum y (bottom-right) of the tile bounding box.

<a id="pyke_pyxel._types.coord.col"></a>

#### col

```python
@property
def col() -> int
```

Column of this tile (1-indexed).

<a id="pyke_pyxel._types.coord.row"></a>

#### row

```python
@property
def row() -> int
```

Row of this tile (1-indexed).

<a id="pyke_pyxel._types.area"></a>

## area Objects

```python
class area()
```

A grid-aware area representing a from/to column/row combination

<a id="pyke_pyxel._types.area.__init__"></a>

#### \_\_init\_\_

```python
def __init__(from_col: int, from_row: int, to_col: int, to_row: int, tile_size: int|None = None)
```

**Arguments**:

- `from_col` _int_ - from column
- `from_row` _int_ - from row
- `to_col` _int_ - to column
- `to_row` _int_ - to row
- `tile_size` _int_ - optionally, the size in pixels of a tile within the area. Defaults to GameSettings.size.tile.

<a id="pyke_pyxel._types.area.tiles"></a>

#### tiles

```python
def tiles() -> list[coord]
```

**Returns**:

- `list[coord]` - A list of all the tiles that make up the area

<a id="pyke_pyxel._types.area.boundary_tiles"></a>

#### boundary\_tiles

```python
def boundary_tiles() -> list[coord]
```

**Returns**:

- `list[coord]` - A list of all the (outer) boundary tiles that make up the area

<a id="pyke_pyxel._types.area.contains"></a>

#### contains

```python
def contains(position: coord) -> bool
```

Return `True` if the given `coord` falls within this area, otherwise `False`

<a id="pyke_pyxel._types.area.with_map_bounds"></a>

#### with\_map\_bounds

```python
@staticmethod
def with_map_bounds(from_col: int, to_col: int, from_row: int, to_row: int, tile_size: int|None = None) -> "area"
```

Create an area that is bounded to the min/max col/row values of 
the map as determined by based on `GameSettings.size.window` and `GameSettings.size.tile`

<a id="pyke_pyxel._types.area.with_center"></a>

#### with\_center

```python
@staticmethod
def with_center(x: int, y: int, cols: int, rows: int) -> "area"
```

Create an area where (x, y) are treated as the visual center.
Grid column/row positions are calculated from the center position.

The from- and to- column/row values are bounded to remain within the allowable values of the 
map based on `GameSettings.size.window` and `GameSettings.size.tile`

TODO - ugly bug:
If I have the following:
|---|---|---|
|   |   |   |
|---|---|---|
|   | $ |   |
|---|---|---|
|   |   |   |
|---|---|---|

And I want to create area.with_center($x, $y, cols=2)
Then I get a result from col1 to col3 (half of col1 and half of col3)

<a id="pyke_pyxel._types.area.columns"></a>

#### columns

```python
@property
def columns() -> int
```

Number of columns in the area.

<a id="pyke_pyxel._types.area.rows"></a>

#### rows

```python
@property
def rows() -> int
```

Number of rows in the area.

<a id="pyke_pyxel._types.area.x"></a>

#### x

```python
@property
def x() -> int
```

Top-left pixel x coordinate for this area.

<a id="pyke_pyxel._types.area.y"></a>

#### y

```python
@property
def y() -> int
```

Top-left pixel y coordinate for this area.

<a id="pyke_pyxel._types.area.mid_x"></a>

#### mid\_x

```python
@property
def mid_x() -> int
```

Integer x coordinate of the visual center (midpoint) of the area.

<a id="pyke_pyxel._types.area.mid_y"></a>

#### mid\_y

```python
@property
def mid_y() -> int
```

Integer y coordinate of the visual center (midpoint) of the area.

<a id="pyke_pyxel._types.area.min_x"></a>

#### min\_x

```python
@property
def min_x() -> int
```

Minimum x (top-left) of the area bounding box.

<a id="pyke_pyxel._types.area.min_y"></a>

#### min\_y

```python
@property
def min_y() -> int
```

Minimum y (top-left) of the area bounding box.

<a id="pyke_pyxel._types.area.max_x"></a>

#### max\_x

```python
@property
def max_x() -> int
```

Maximum x (bottom-right) of the area bounding box.

<a id="pyke_pyxel._types.area.max_y"></a>

#### max\_y

```python
@property
def max_y() -> int
```

Maximum y (bottom-right) of the area bounding box.

<a id="pyke_pyxel.drawable._button"></a>

# \_button

<a id="pyke_pyxel.drawable._button.Button"></a>

## Button Objects

```python
class Button(Drawable)
```

This class represents a clickable button in the UI. It is constructed from either `Image` or `CompoundSprite`
objects for its 'up' and 'down' states. It can also have an optional icon, which can also be a
`CompoundSprite` or a simple `Image`.

The button's state changes in response to mouse interactions, such as
highlighting when hovered over and appearing pressed ('down') when clicked.

<a id="pyke_pyxel.drawable._button.Button.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str, up: CompoundSprite|Image, down: CompoundSprite|Image)
```

**Arguments**:

- `up` _CompoundSprite|Image_ - The image to display when the button is in its 'up' state.
- `down` _CompoundSprite|Image_ - The image to display when the button is in its 'down' or highlighted state.

<a id="pyke_pyxel.drawable._button.Button.set_icon"></a>

#### set\_icon

```python
def set_icon(up: CompoundSprite|Image, down: CompoundSprite|Image)
```

Sets the icon for the button.

**Arguments**:

- `up` _CompoundSprite|Image_ - The icon to display when the button is in its 'up' state.
- `down` _CompoundSprite|Image_ - The icon to display when the button is in its 'down' or highlighted state.

<a id="pyke_pyxel.drawable._button.Button.highlight"></a>

#### highlight

```python
def highlight(active: bool)
```

Highlight the button. This sets the icon of the button to its down/active state.
No effect if the button does not have an icon

**Arguments**:

- `active` _bool_ - Enable or disable highlighting

<a id="pyke_pyxel.drawable._button.Button.push_down"></a>

#### push\_down

```python
def push_down()
```

Sets the button's state to 'down', drawing the down frame.

<a id="pyke_pyxel.drawable._button.Button.pop_up"></a>

#### pop\_up

```python
def pop_up()
```

Sets the button's state to 'up', drawing the up frame.

<a id="pyke_pyxel.drawable._button.Button.check_mouse_move"></a>

#### check\_mouse\_move

```python
def check_mouse_move(x: int, y: int)
```

Ask the button to respond to mouse movement. The default reaction is:
- MOUSE_IN: highlight=True
- MOUSE_OUT: highlight=False, is_down=False

**Arguments**:

- `x` _int_ - The x-coordinate to check.
- `y` _int_ - The y-coordinate to check.

<a id="pyke_pyxel.drawable._drawable"></a>

# \_drawable

<a id="pyke_pyxel.drawable._drawable.Drawable"></a>

## Drawable Objects

```python
class Drawable()
```

<a id="pyke_pyxel.drawable._drawable.Drawable.contains"></a>

#### contains

```python
def contains(x: int, y: int) -> bool
```

Checks if the given coordinates are within the bounds of the drawable.

**Arguments**:

- `x` _int_ - The x-coordinate to check.
- `y` _int_ - The y-coordinate to check.
  

**Returns**:

- `bool` - True if the coordinates are within the drawable's bounds, False otherwise.

<a id="pyke_pyxel.drawable._drawable.Drawable.width"></a>

#### width

```python
@property
def width() -> int
```

Returns the width of the drawable in pixels.

<a id="pyke_pyxel.drawable._drawable.Drawable.height"></a>

#### height

```python
@property
def height() -> int
```

Returns the height of the drawable in pixels.

<a id="pyke_pyxel.drawable._drawable.Drawable.position"></a>

#### position

```python
@property
def position() -> coord
```

Returns the current position of the drawable.

**Returns**:

- `coord` - The coordinate of the drawable's top-left corner.

<a id="pyke_pyxel.drawable._drawable.Drawable.set_position"></a>

#### set\_position

```python
def set_position(position: coord)
```

Sets the position of the drawable.

**Arguments**:

- `position` _coord_ - The new coordinate for the drawable's top-left corner.

<a id="pyke_pyxel.drawable._image"></a>

# \_image

<a id="pyke_pyxel.drawable._image.Image"></a>

## Image Objects

```python
class Image(Drawable)
```

Represents an image in the Pyxel resources image bank that can be positioned and rendered on the screen.

Parameters
----------
frame : coord
    The `coord` of the top-left corner of the image's graphic in the resource image.
cols : int, optional
    The number of columns the image graphic occupies, by default 1.
rows : int, optional
    The number of rows the image graphic occupies, by default 1.
image_index : int, optional
    The index of the Pyxel resources image bank where the image graphics are located, by default 0.

<a id="pyke_pyxel.drawable._image.ImageFactory"></a>

## ImageFactory Objects

```python
class ImageFactory()
```

Convenience class to create multiple `Image` instances with the same width/height and using the same image index.

Parameters
----------
cols : int, optional
    The number of columns the created images will occupy, by default 1.
rows : int, optional
    The number of rows the the created images will occupy, by default 1.
image_index : int, optional
    The index of the Pyxel resources image bank where the image graphics are located, by default 0.

<a id="pyke_pyxel.drawable._image.ImageFactory.at"></a>

#### at

```python
def at(position: coord) -> Image
```

Create an `Image` instance at the given position.

Parameters
----------
position : coord
    The `coord` of the top-left corner of the image's graphic on the Pyxel resource sheet.

Returns
-------
Image
    The created `Image` instance.

<a id="pyke_pyxel.game"></a>

# game

<a id="pyke_pyxel.game.Game"></a>

## Game Objects

```python
class Game()
```

Game class that manages the core game loop, sprite management, and rendering.
This class serves as the main controller for a Pyxel-based game, handling initialization,
sprite lifecycle management, signal connections, and the update/draw loop. It manages
game settings, sprites, tile maps, HUD, and visual effects.

Update and Draw Order:
- 1 User input:
    - 1.1 Keyboard input
    - 1.2 Mouse Events
- 2 Lifecycle (if not paused)
    - 2.1 Timers
    - 2.2 `GAME.UPDATE` signal
    - 2.3 Internal sprite, HUD & FX status updates
    - 2.4 Internal drawing routines

Signals:
- `GAME.WILL_START`: Emitted before the game loop begins.
- `GAME.UPDATE`: Emitted on every update frame.
- `MOUSE.MOVE`: Sent when mouse position changes, enabled by `GameSettings.mouse_enabled`.
- `MOUSE.DOWN`: Sent on left mouse button press, enabled by `GameSettings.mouse_enabled`.
- `MOUSE.UP`: Sent on left mouse button release, enabled by `GameSettings.mouse_enabled`.

<a id="pyke_pyxel.game.Game.__init__"></a>

#### \_\_init\_\_

```python
def __init__(settings: GameSettings, title: str, resources: str)
```

**Arguments**:

- `settings` _GameSettings_ - Configuration object containing debug flag, window and tile sizes,
  and FPS settings (game and animation). Also used to determine whether mouse input is enabled.
- `title` _str_ - Window title passed to pyxel.init.
- `resources` _str_ - Path to a resources file that will be loaded with pyxel.load.

<a id="pyke_pyxel.game.Game.start"></a>

#### start

```python
def start()
```

Initializes and starts the game loop.

Sends a signal indicating the game is about to start, then begins the main
update and draw loop using Pyxel's run function.

Signals:
    Signals.GAME.WILL_START: Sent before the game loop starts.

<a id="pyke_pyxel.game.Game.clear_all"></a>

#### clear\_all

```python
def clear_all()
```

Clear all sprites, TileMap, HUD and FX

<a id="pyke_pyxel.game.Game.add_sprite"></a>

#### add\_sprite

```python
def add_sprite(sprite: Sprite|CompoundSprite)
```

Add a sprite to the game's sprite collection.

**Arguments**:

- `sprite` _Sprite | CompoundSprite_ - The sprite object to add to the game.
  Can be either a single Sprite or a CompoundSprite containing multiple sprites.

<a id="pyke_pyxel.game.Game.remove_sprite"></a>

#### remove\_sprite

```python
def remove_sprite(sprite: Sprite|CompoundSprite|int)
```

Remove a sprite from the game's active sprite collection.

**Arguments**:

  sprite : Sprite | CompoundSprite
  The sprite (or compound sprite) instance to remove from the game's internal
  sprite list.

<a id="pyke_pyxel.game.Game.remove_sprite_by_id"></a>

#### remove\_sprite\_by\_id

```python
def remove_sprite_by_id(sprite_id: int)
```

Remove the first sprite with the specified identifier from the game's sprite list.

**Arguments**:

  sprite_id : int
  The identifier of the sprite to remove.

<a id="pyke_pyxel.game.Game.set_tilemap"></a>

#### set\_tilemap

```python
def set_tilemap(resource_position: coord, tiles_wide: int, tiles_high: int, resource_tilemap_index: int = 0)
```

Set a simplified version of standard Pyxel tilemaps as a background layer.
The tilemap is horizontally and vertically repeated to fill up the screen width/height.

For example:
`game.set_tilemap(coord(10, 8), 4, 6)`
will fetch a tilemap starting at column 10 and row 8 of the resource sheet and
load 4 columns and 6 rows which will then be repeated to fill the screen.

**Arguments**:

  resource_position : coord
  The col/row position of the tilemap in the loaded resource sheet
  tiles_wide : int
  The width of the tilemap on the resource sheet
  tiles_high : int
  The height of the tilemap on the resource sheet
  resource_tilemap_index : int
  The index of the tilemap in the resource bundle

<a id="pyke_pyxel.game.Game.pause"></a>

#### pause

```python
def pause()
```

Pause the game loop.
This will pause:
- Game logic update signals
- Sprite animation

But will not halt:
- Keyboard and mouse input signals
- Screen draw
- Music

<a id="pyke_pyxel.game.Game.unpause"></a>

#### unpause

```python
def unpause()
```

Unpause the game loop.

<a id="pyke_pyxel.game.Game.start_music"></a>

#### start\_music

```python
def start_music(number: int)
```

Starts the music identified by the provided number. Music loops until `stop_music` is called.

<a id="pyke_pyxel.game.Game.stop_music"></a>

#### stop\_music

```python
def stop_music()
```

Stops the currently playing music

<a id="pyke_pyxel.game.Game.map"></a>

#### map

```python
@property
def map() -> Map
```

Returns the `Map` instance for this game

<a id="pyke_pyxel.game.Game.hud"></a>

#### hud

```python
@property
def hud() -> HUD
```

Returns the `HUD` instance for this game

<a id="pyke_pyxel.game.Game.fx"></a>

#### fx

```python
@property
def fx() -> FX
```

Returns the `FX` instance for this game

<a id="pyke_pyxel.game.Game.keyboard"></a>

#### keyboard

```python
@property
def keyboard() -> Keyboard
```

Returns the `Keyboard` instance for this game

<a id="pyke_pyxel.game.Game.timer"></a>

#### timer

```python
@property
def timer() -> Timer
```

Returns the `Timer` instance of this game

<a id="pyke_pyxel.timer"></a>

# timer

<a id="pyke_pyxel.timer.Timer"></a>

## Timer Objects

```python
class Timer()
```

A centralised timer single (`after`) and multiple (`every`) support.
Individual timers are uniquely identifed by the signals that they send

This class should be accessed through the `Game` instance via `game.timer`.

<a id="pyke_pyxel.timer.Timer.after"></a>

#### after

```python
def after(seconds: float, signal: str, sender: Any|None = None)
```

Set a timer to fire once after the specified time period has passed.
If a timer with the same signal already exists the existing timer will be replaced.

**Arguments**:

- `seconds` _float_ - the number of seconds to wait until firing the signal
- `signal` _str_ - the signal to send
- `sender` _Any optional_ - an optional sender value to send with the signal

<a id="pyke_pyxel.timer.Timer.every"></a>

#### every

```python
def every(seconds: float, signal: str, sender: Any|None = None)
```

Set a timer to fire repeatedly after the specified time period has passed.
If a timer with the same signal already exists the existing timer will be replaced.

**Arguments**:

- `seconds` _float_ - the number of seconds to wait between firing the signal
- `signal` _str_ - the signal to send
- `sender` _Any optional_ - an optional sender value to send with the signal

<a id="pyke_pyxel.timer.Timer.cancel"></a>

#### cancel

```python
def cancel(signal: str)
```

Cancel a previously set timer. No-op is the timer does not exist.

**Arguments**:

- `signal` _str_ - the signal that identifies the timer

<a id="pyke_pyxel.timer.Timer.has_timer"></a>

#### has\_timer

```python
def has_timer(signal: str) -> bool
```

Return `True` if a timer is registered for the provided signal

<a id="pyke_pyxel.rpg.game"></a>

# game

<a id="pyke_pyxel.rpg.game.RPGGame"></a>

## RPGGame Objects

```python
class RPGGame(Game)
```

<a id="pyke_pyxel.rpg.game.RPGGame.__init__"></a>

#### \_\_init\_\_

```python
def __init__(settings: GameSettings, title: str, resources: str)
```

Specialised sub-class of `pyke_pyxel.Game` which adds basic room- and actor-based RPG mechanics.

**Attributes**:

- `player` _Player_ - The player character. Use set_player() to assign the player instance.
- `room` _Room_ - The current room/map the player is in. Automatically initialized with the game map.

<a id="pyke_pyxel.rpg.game.RPGGame.set_player"></a>

#### set\_player

```python
def set_player(sprite: MovableSprite|Callable[[], MovableSprite], speed_px_per_second: int) -> Player
```

Assigns a player sprite to the game, creating a `Player` instance.

**Arguments**:

- `sprite` _MovableSprite | Callable[[], MovableSprite]_ - The sprite
  (or a callable that returns a sprite) representing the player.
- `speed_px_per_second` _int_ - The speed of the player's movements expressed as pixels per second
  

**Returns**:

- `Player` - The initialized `Player` instance.

<a id="pyke_pyxel.rpg.game.RPGGame.clear_all"></a>

#### clear\_all

```python
def clear_all()
```

Clear all sprites, TileMap, HUD and FX

<a id="pyke_pyxel.rpg.game.RPGGame.add_actor"></a>

#### add\_actor

```python
def add_actor(actor: Actor)
```

Add an actor to the game's actor collection.

**Arguments**:

- `actor` _Actor_ - The actor object to add to the game.

<a id="pyke_pyxel.rpg.game.RPGGame.remove_actor"></a>

#### remove\_actor

```python
def remove_actor(actor: Actor)
```

Remove an actor from the game's active actor collection.

**Arguments**:

- `actor` _Actor_ - The actor object to remove from the game.

<a id="pyke_pyxel.rpg.game.RPGGame.enemies_at"></a>

#### enemies\_at

```python
def enemies_at(position: coord|area, tolerance: float = 0.0) -> list[Enemy]
```

Return a list of enemies which are at the grid location of the provided position.

**Arguments**:

- `position` _coord_ - the grid location to check
  

**Returns**:

- `list[Enemy]` - the enemies that are at the provided position

<a id="pyke_pyxel.rpg.game.RPGGame.player"></a>

#### player

```python
@property
def player() -> Player
```

Returns the `Player` instance for this game

<a id="pyke_pyxel.rpg.game.RPGGame.room"></a>

#### room

```python
@property
def room() -> Room
```

Returns the `Room` instance for this game

<a id="pyke_pyxel.rpg.player"></a>

# player

<a id="pyke_pyxel.rpg.player.Player"></a>

## Player Objects

```python
class Player(MovableActor)
```

<a id="pyke_pyxel.rpg.player.Player.__init__"></a>

#### \_\_init\_\_

```python
def __init__(sprite: MovableSprite, speed_px_per_second: int)
```

**Arguments**:

- `sprite` _MovableSprite_ - the sprite that represents the player
- `speed_px_per_second` _int_ - The speed of the player's movements expressed as pixels per second

<a id="pyke_pyxel.rpg.player.Player.adjacent_openable"></a>

#### adjacent\_openable

```python
def adjacent_openable(map: Map) -> OpenableSprite|None
```

Find an `OpenableSprite` adjacent to the player's current position

<a id="pyke_pyxel.rpg.actor"></a>

# actor

<a id="pyke_pyxel.rpg.actor.Actor"></a>

## Actor Objects

```python
class Actor()
```

Represents an actor in the game world.
An actor can be a player, enemy, item, etc. which are present at a position on the game map.

<a id="pyke_pyxel.rpg.actor.Actor.__init__"></a>

#### \_\_init\_\_

```python
def __init__(sprite: Sprite)
```

**Arguments**:

- `sprite` _Sprite_ - the sprite that represents this actor

<a id="pyke_pyxel.rpg.actor.Actor.launch_projectile"></a>

#### launch\_projectile

```python
def launch_projectile(sprite: Sprite|Callable[[], Sprite], speed_px_per_second: int, direction: DIRECTION)
```

Launch a projectile from this actor.

**Arguments**:

- `sprite_type` _Sprite | Callable[[], Sprite]_ - The sprite of the projectile
- `speed_px_per_second` _int_ - The speed of the projectile expressed as pixels per second
- `direction` _DIRECTION_ - The direction the projectile is travelling

<a id="pyke_pyxel.rpg.actor.Actor.remove"></a>

#### remove

```python
def remove()
```

Remove this actor from the game

<a id="pyke_pyxel.rpg.actor.Actor.name"></a>

#### name

```python
@property
def name()
```

Returns the name of this actor

<a id="pyke_pyxel.rpg.actor.Actor.position"></a>

#### position

```python
@property
def position()
```

Returns the position of this actor

<a id="pyke_pyxel.rpg.actor.Actor.sprite"></a>

#### sprite

```python
@property
def sprite() -> Sprite
```

Returns the sprite of this actor

<a id="pyke_pyxel.rpg.actor.Actor.sprite_id"></a>

#### sprite\_id

```python
@property
def sprite_id() -> int
```

Returns the ID of the sprite of this actor

<a id="pyke_pyxel.rpg.actor.MovableActor"></a>

## MovableActor Objects

```python
class MovableActor(Actor)
```

<a id="pyke_pyxel.rpg.actor.MovableActor.__init__"></a>

#### \_\_init\_\_

```python
def __init__(sprite: MovableSprite, speed_px_per_second: int)
```

**Arguments**:

- `sprite` _MovableSprite_ - the sprite that represents this actor
- `speed_px_per_second` _int_ - The speed of the actor's movements expressed as pixels per second

<a id="pyke_pyxel.rpg.actor.MovableActor.set_position"></a>

#### set\_position

```python
def set_position(position: coord)
```

Set the position of the actor

<a id="pyke_pyxel.rpg.actor.MovableActor.start_moving"></a>

#### start\_moving

```python
def start_moving(direction: DIRECTION)
```

Start moving in the provided direction

<a id="pyke_pyxel.rpg.actor.MovableActor.stop_moving"></a>

#### stop\_moving

```python
def stop_moving()
```

Stop moving

<a id="pyke_pyxel.rpg.actor.MovableActor.move_to"></a>

#### move\_to

```python
def move_to(position: coord, pathfinder: Map|None = None, allow_diagonal: bool|None = None)
```

Move to the provided coordinate.

**Arguments**:

- `position` _coord_ - The coordinate to move to
- `pathfinder` _Map|None_ - the Map to use for pathfinding
- `allow_diagonal` _bool, optional_ - Whether to allow diagonal movement.

<a id="pyke_pyxel.rpg.actor.MovableActor.move_along_path"></a>

#### move\_along\_path

```python
def move_along_path(path: list[coord])
```

Move along the provided path.

**Arguments**:

- `path` _list[coord]_ - The path to follow

<a id="pyke_pyxel.rpg.actor.MovableActor.is_moving"></a>

#### is\_moving

```python
@property
def is_moving() -> bool
```

Return True if the actor is moving

<a id="pyke_pyxel.rpg.room"></a>

# room

<a id="pyke_pyxel.rpg.room.Room"></a>

## Room Objects

```python
class Room()
```

<a id="pyke_pyxel.rpg.room.Room.add_wall"></a>

#### add\_wall

```python
def add_wall(sprite: Sprite|Callable[[], Sprite], col: int, row: int)
```

Add a wall to the map. The related map position will be marked as blocked.


**Arguments**:

- `sprite` _Sprite | Callable[[], Sprite]_ - The sprite (or a callable that returns a sprite) representing the wall.
- `col` _int_ - The column position of the wall
- `row` _int_ - The row position of the wall

<a id="pyke_pyxel.rpg.room.Room.add_door"></a>

#### add\_door

```python
def add_door(sprite: OpenableSprite|Callable[[], OpenableSprite], col: int, row: int, closed: bool = True)
```

Add an openable door to the map. The related map position will be marked as either open or closed.

**Arguments**:

- `sprite` _OpenableSprite | Callable[[], OpenableSprite]_ - The sprite (or a callable that returns a sprite) representing the door.
- `col` _int_ - The column position of the door
- `row` _int_ - The row position of the door
- `closed` _bool_ - whether the door should be closed or open by default

<a id="pyke_pyxel.rpg.room.Room.add_enemy"></a>

#### add\_enemy

```python
def add_enemy(sprite: Enemy|MovableSprite|Callable[[], MovableSprite], speed_px_per_second: int = 0) -> Enemy
```

Add an enemy to the map.

**Arguments**:

- `sprite` _Enemy | MovableSprite | Callable[[], MovableSprite]_ - The sprite (or a callable that returns a sprite) representing the enemy.
- `speed_px_per_second` _int_ - The speed of the enemy's movements expressed as pixels per second
  

**Returns**:

- `Enemy` - The initialized `Enemy` instance.

<a id="pyke_pyxel.rpg.enemy"></a>

# enemy

<a id="pyke_pyxel.rpg.enemy.Enemy"></a>

## Enemy Objects

```python
class Enemy(MovableActor)
```

<a id="pyke_pyxel.rpg.enemy.Enemy.__init__"></a>

#### \_\_init\_\_

```python
def __init__(sprite: MovableSprite, speed_px_per_second: int)
```

**Arguments**:

- `sprite` _MovableSprite_ - the sprite that represents this enemy
- `speed_px_per_second` _int_ - The speed of the enemy's movements expressed as pixels per second

<a id="pyke_pyxel.map"></a>

# map

<a id="pyke_pyxel.map.LOCATION_STATUS"></a>

## LOCATION\_STATUS Objects

```python
class LOCATION_STATUS(enum.Enum)
```

Enumerated location statuses `FREE`, `BLOCKED`, `CLOSED`, and `OPEN`

<a id="pyke_pyxel.map.MapLocation"></a>

## MapLocation Objects

```python
@dataclass
class MapLocation()
```

A location on the `Map`

**Attributes**:

- `is_edge` _bool_ - `True` if this location is on the edge of the map
- `position` _coord|None_ - the coordinate position of this location, or `None` if `is_edge` is `True`
- `status` _int_ - one of `LOCATIONSTATUS.FREE`, `LOCATIONSTATUS.BLOCKED`, `LOCATIONSTATUS.CLOSED`, or `LOCATIONSTATUS.OPEN`
- `sprite` _Sprite|None_ - the sprite at this map location, or `None` if there is no sprite

<a id="pyke_pyxel.map.Map"></a>

## Map Objects

```python
class Map()
```

A grid-aware representation of the game map.

This class should be accessed through the `Game` instance via `game.map`.

<a id="pyke_pyxel.map.Map.sprite_can_move_to"></a>

#### sprite\_can\_move\_to

```python
def sprite_can_move_to(coord: coord) -> bool
```

Determine if a sprite can move to the specified coordinate.

Checks the status of the location at the given coordinate and returns True
if the sprite is able to move there (i.e., the location is either `FREE` or `OPEN`).

**Arguments**:

- `coord` _coord_ - The coordinate to check for sprite movement.
  

**Returns**:

- `bool` - True if the location is `FREE` or `OPEN`, False otherwise.

<a id="pyke_pyxel.map.Map.mark_blocked"></a>

#### mark\_blocked

```python
def mark_blocked(coord: coord, sprite: Sprite)
```

Mark the location at the given coordinate as blocked and attach a sprite.

This updates the Location object returned by self.location_at(coord) by:
- setting its status to `LOCATION_STATUS.BLOCKED`
- assigning the provided sprite to its sprite attribute

**Arguments**:

- `coord` _coord_ - The coordinate of the location to mark as blocked.
- `sprite` _Sprite_ - The sprite to place on the blocked location (e.g. an obstacle graphic).

<a id="pyke_pyxel.map.Map.mark_openable"></a>

#### mark\_openable

```python
def mark_openable(coord: coord, sprite: OpenableSprite, closed: bool)
```

Mark a location as an openable object with the specified status.

**Arguments**:

- `coord` _coord_ - The coordinate of the location to mark.
- `sprite` _OpenableSprite_ - The sprite to assign to the openable object.
- `closed` _bool_ - Whether the openable object is closed (True) or open (False).

<a id="pyke_pyxel.map.Map.mark_closed"></a>

#### mark\_closed

```python
def mark_closed(coord: coord)
```

Mark a location as closed.

<a id="pyke_pyxel.map.Map.mark_open"></a>

#### mark\_open

```python
def mark_open(coord: coord)
```

Mark a location as open.

<a id="pyke_pyxel.map.Map.is_blocked"></a>

#### is\_blocked

```python
def is_blocked(coord: coord) -> bool
```

Check if a location is blocked

<a id="pyke_pyxel.map.Map.is_openable"></a>

#### is\_openable

```python
def is_openable(coord: coord) -> bool
```

Check if a location is openable

<a id="pyke_pyxel.map.Map.adjacent_openable"></a>

#### adjacent\_openable

```python
def adjacent_openable(coord: coord) -> OpenableSprite|None
```

Check if a location adjacent(UP, DOWN, LEFT, RIGHT) to the provided coordinate is openable

<a id="pyke_pyxel.map.Map.openable_sprite_at"></a>

#### openable\_sprite\_at

```python
def openable_sprite_at(coord: coord) -> OpenableSprite|None
```

Return the `OpenableSprite` at a coordinate

<a id="pyke_pyxel.map.Map.sprite_at"></a>

#### sprite\_at

```python
def sprite_at(coord: coord) -> Sprite|None
```

Return the `Sprite` at a coordinate

<a id="pyke_pyxel.map.Map.location_at"></a>

#### location\_at

```python
def location_at(coord: coord) -> MapLocation
```

Return the `MapLocation` at a coordinate

<a id="pyke_pyxel.map.Map.location_left_of"></a>

#### location\_left\_of

```python
def location_left_of(coord: coord) -> MapLocation|None
```

Return the location LEFT of the coordinate

<a id="pyke_pyxel.map.Map.location_right_of"></a>

#### location\_right\_of

```python
def location_right_of(coord: coord) -> MapLocation|None
```

Return the location RIGHT of the coordinate

<a id="pyke_pyxel.map.Map.location_above"></a>

#### location\_above

```python
def location_above(coord: coord) -> MapLocation|None
```

Return the location UP from of the coordinate

<a id="pyke_pyxel.map.Map.location_below"></a>

#### location\_below

```python
def location_below(coord: coord) -> MapLocation|None
```

Return the location DOWN from of the coordinate

<a id="pyke_pyxel.map.Map.random_location"></a>

#### random\_location

```python
def random_location(area: area) -> MapLocation
```

Return a random location within the provided area

<a id="pyke_pyxel.map.Map.x_is_left_of_center"></a>

#### x\_is\_left\_of\_center

```python
def x_is_left_of_center(x: int) -> bool
```

Return true if `x` is to the left of the center of the map

<a id="pyke_pyxel.map.Map.y_is_above_center"></a>

#### y\_is\_above\_center

```python
def y_is_above_center(y: int) -> bool
```

Return true if `y` is above the center of the map

<a id="pyke_pyxel.map.Map.bound_to_width"></a>

#### bound\_to\_width

```python
def bound_to_width(x: int) -> int
```

Check that `x` falls into the bounds of the map and return a safe value (max x of the map) if it does not

<a id="pyke_pyxel.map.Map.bound_to_height"></a>

#### bound\_to\_height

```python
def bound_to_height(y: int) -> int
```

Check that `y` falls into the bounds of the map and return a safe value (max y of the map) if it does not

<a id="pyke_pyxel.map.Map.shortest_distance_to_sides"></a>

#### shortest\_distance\_to\_sides

```python
def shortest_distance_to_sides(from_x: int) -> int
```

Return the shortest distance to the sides of the map (either left or right)

<a id="pyke_pyxel.map.Map.random_distance_to_right"></a>

#### random\_distance\_to\_right

```python
def random_distance_to_right(from_x: int, min: int, max: int) -> int
```

Generate a random distance to the right of `from_x` where the random distance falls between `min` and `max` without exceeding the bounds of the map.

<a id="pyke_pyxel.map.Map.random_distance_to_left"></a>

#### random\_distance\_to\_left

```python
def random_distance_to_left(from_x: int, min: int, max: int) -> int
```

Generate a random distance to the left of `from_x` where the random distance falls between `min` and `max` without exceeding the bounds of the map.

<a id="pyke_pyxel.map.Map.random_distance_down"></a>

#### random\_distance\_down

```python
def random_distance_down(from_y: int, min: int, max: int) -> int
```

Generate a random distance down of `from_y` where the random distance falls between `min` and `max` without exceeding the bounds of the map.

<a id="pyke_pyxel.map.Map.find_path"></a>

#### find\_path

```python
def find_path(frm: coord, to: coord, allow_diagonal: bool|None = None) -> list[coord]|None
```

Find a path between two locations

**Arguments**:

- `frm` _coord_ - The starting location
- `to` _coord_ - The ending location
- `allow_diagonal` _bool, optional_ - Whether to allow diagonal movement.
  

**Returns**:

- `list[coord]` - A list of coordinates representing the path or `None` if no path exists.

<a id="pyke_pyxel.map.Map.height"></a>

#### height

```python
@property
def height() -> int
```

Height of the map

<a id="pyke_pyxel.map.Map.width"></a>

#### width

```python
@property
def width() -> int
```

Width of the map

<a id="pyke_pyxel.map.Map.center_x"></a>

#### center\_x

```python
@property
def center_x() -> int
```

Horizontal center point of the map

<a id="pyke_pyxel.map.Map.center_y"></a>

#### center\_y

```python
@property
def center_y() -> int
```

Vertical center point of the map

<a id="pyke_pyxel.map.Map.right_x"></a>

#### right\_x

```python
@property
def right_x() -> int
```

Right-most `x` point of the map

<a id="pyke_pyxel.map.Map.bottom_y"></a>

#### bottom\_y

```python
@property
def bottom_y() -> int
```

Bottom-most `y` point of the map

<a id="pyke_pyxel.cell_auto.matrix"></a>

# matrix

<a id="pyke_pyxel.cell_auto.matrix.Cell"></a>

## Cell Objects

```python
class Cell()
```

A Cell represents a single unit in a cellular automaton grid.
Each cell has a position (x, y) in a 2D grid and maintains both current and stored state.
The cell can be rendered to a pyxel Image and tracks properties like type, color, propagation,
and power for use in cellular automaton simulations.

**Attributes**:

- `x` _int_ - The x-coordinate of the cell in the grid.
- `y` _int_ - The y-coordinate of the cell in the grid.
- `type` _str_ - The current type/state of the cell (default: "empty").
- `colour` _int_ - The current color value of the cell (default: 0).
- `can_propogate` _bool_ - Whether this cell can propagate its state (default: False).
- `power` _float_ - A power or intensity value for the cell (default: 0).
- `tag` _Any_ - An optional tag for custom data association (default: None).

<a id="pyke_pyxel.cell_auto.matrix.Cell.reset"></a>

#### reset

```python
def reset()
```

Reset this Cell to the default empty state and store it.

This clears type, colour, propagation flag, power and tag, and
then calls :meth:`store_state` to snapshot the cleared state.

<a id="pyke_pyxel.cell_auto.matrix.Cell.store_state"></a>

#### store\_state

```python
def store_state()
```

Save the current live state into the cell's stored-state slots.

Stored values are used by :meth:`recall_state` to restore a
previously saved state.

<a id="pyke_pyxel.cell_auto.matrix.Cell.recall_state"></a>

#### recall\_state

```python
def recall_state()
```

Restore the cell's live state from previously stored values.

After restoring, the stored slots are cleared to their default
'empty' values.

<a id="pyke_pyxel.cell_auto.matrix.Matrix"></a>

## Matrix Objects

```python
class Matrix()
```

Matrix(width: int = 0, height: int = 0)
A rectangular grid container that manages Cell objects and provides
utility methods for neighbour lookup, region queries and line tracing.

Parameters
----------
width : int, optional
    Number of columns in the matrix (x dimension). Defaults to 0.
height : int, optional
    Number of rows in the matrix (y dimension). Defaults to 0.

Threading / concurrency
-----------------------
- Not thread-safe: mutating methods (clear / direct Cell mutation) can
  invalidate caches and should be synchronised in multithreaded
  contexts.

Examples
--------
- Typical usage:
    m = Matrix(80, 60)
    c = m.cell_at(10, 5)
    neighs = m.neighbours(c)
    line = m.cells_in_line(coord(0, 0), coord(10, 5))

<a id="pyke_pyxel.cell_auto.matrix.Matrix.clear"></a>

#### clear

```python
def clear()
```

Re-initialise internal cell grid to a fresh width-by-height matrix.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_N"></a>

#### neighbour\_N

```python
def neighbour_N(cell: Cell) -> Cell|None
```

Return the northern neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_S"></a>

#### neighbour\_S

```python
def neighbour_S(cell: Cell) -> Cell|None
```

Return the southern neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_E"></a>

#### neighbour\_E

```python
def neighbour_E(cell: Cell) -> Cell|None
```

Return the eastern neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_W"></a>

#### neighbour\_W

```python
def neighbour_W(cell: Cell) -> Cell|None
```

Return the western neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_NE"></a>

#### neighbour\_NE

```python
def neighbour_NE(cell: Cell) -> Cell|None
```

Return the north-east neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_NW"></a>

#### neighbour\_NW

```python
def neighbour_NW(cell: Cell) -> Cell|None
```

Return the north-west neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_SE"></a>

#### neighbour\_SE

```python
def neighbour_SE(cell: Cell) -> Cell|None
```

Return the south-east neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbour_SW"></a>

#### neighbour\_SW

```python
def neighbour_SW(cell: Cell) -> Cell|None
```

Return the south-west neighbour of ``cell`` or ``None`` if out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.neighbours"></a>

#### neighbours

```python
def neighbours(cell: Cell, filter_for_type: Optional[str] = None) -> list[Cell]
```

Return the 8-connected neighbours of ``cell``.

The neighbour list is cached on the :class:`Cell` object as
``cell._neighbours`` and is only populated once; subsequent calls
return a copy of that list so callers may mutate the result without
affecting the cache. If ``filter_for_type`` is provided the result
is filtered by each neighbour's ``type`` attribute.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.cell_at"></a>

#### cell\_at

```python
def cell_at(x: int, y: int) -> Cell|None
```

Safe indexed access to the cell at grid coordinates (x, y).

Returns ``None`` if the coordinates are out of bounds.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.cells_at"></a>

#### cells\_at

```python
def cells_at(position: coord, include_empty: bool = False) -> list[Cell]
```

Return cells within the rectangular region described by ``position``.

``position`` is expected to expose ``min_x``, ``min_y``, ``max_x``
and ``max_y`` attributes. The method performs bounds-clipping so
the returned list contains only in-bounds cells. By default empty
cells (where ``c.is_empty`` is True) are excluded unless
``include_empty`` is True.

<a id="pyke_pyxel.cell_auto.matrix.Matrix.cells_in_line"></a>

#### cells\_in\_line

```python
def cells_in_line(from_position: coord, to_position: coord, extend_to_matrix_end: bool = False) -> list[Cell]
```

Return the sequence of cells forming a discrete line between two coords.

The result includes both endpoints.

<a id="pyke_pyxel.cell_auto.game"></a>

# game

<a id="pyke_pyxel.cell_auto.game.CellAutoGame"></a>

## CellAutoGame Objects

```python
class CellAutoGame(Game)
```

Specialised sub-class of `pyke_pyxel.Game` which adds a cellular automaton matrix.

**Attributes**:

- `matrix(Matrix)` - read-only access to the cellular automaton matrix

<a id="pyke_pyxel.cell_auto.game.CellAutoGame.__init__"></a>

#### \_\_init\_\_

```python
def __init__(settings: GameSettings, title: str, resources: str)
```

**Arguments**:

- `settings` _GameSettings_ - The game settings configuration.
- `title` _str_ - The title of the game window.
- `resources` _str_ - The path to the resources directory.

<a id="pyke_pyxel.sprite._rpg_sprites"></a>

# \_rpg\_sprites

<a id="pyke_pyxel.sprite._rpg_sprites.OpenableSprite"></a>

## OpenableSprite Objects

```python
class OpenableSprite(Sprite)
```

A Sprite that supports open/close states (e.g., doors, chests).

The OpenableSprite exposes simple open/close methods and manages an
internal status value that determines which frame is shown.

<a id="pyke_pyxel.sprite._rpg_sprites.OpenableSprite.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str, open_frame: coord, closed_frame: coord)
```

**Arguments**:

- `name` _str_ - the logical name of the sprite
- `open_frame` _coord_ - The frame to use when the sprite is in its open state.
- `closed_frame` _coord_ - The frame to use when the sprite is in its closed state.

<a id="pyke_pyxel.sprite._rpg_sprites.OpenableSprite.close"></a>

#### close

```python
def close()
```

Close the sprite

<a id="pyke_pyxel.sprite._rpg_sprites.OpenableSprite.open"></a>

#### open

```python
def open()
```

Open the sprite

<a id="pyke_pyxel.sprite._rpg_sprites.OpenableSprite.is_closed"></a>

#### is\_closed

```python
@property
def is_closed() -> bool
```

Return True if the sprite is closed

<a id="pyke_pyxel.sprite._rpg_sprites.OpenableSprite.is_open"></a>

#### is\_open

```python
@property
def is_open() -> bool
```

Return True if the sprite is open

<a id="pyke_pyxel.sprite._rpg_sprites.MovableSprite"></a>

## MovableSprite Objects

```python
class MovableSprite(Sprite)
```

Sprite with movement-related configuration and convenience setters.

MovableSprite stores a movement speed and provides helper methods to
create simple directional animations (up/down/left/right).

<a id="pyke_pyxel.sprite._rpg_sprites.MovableSprite.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str, default_frame: coord, cols: int = 1, rows: int = 1, resource_image_index: int = 0)
```

**Arguments**:

- `name` _str_ - Logical name for the sprite.
- `default_frame` _coord_ - The frame to use when no animation is active (idle frame).
- `cols` _int_ - Width in tiles for framed sprites (used when advancing frames).
- `rows` _int_ - Height in tiles for framed sprites (used when advancing frames).
- `resource_image_index` _int_ - Index of the image resource (if multiple images are used).

<a id="pyke_pyxel.sprite._rpg_sprites.MovableSprite.set_up_animation"></a>

#### set\_up\_animation

```python
def set_up_animation(animation: Animation)
```

Set the animation to be used when the sprite moves UP

<a id="pyke_pyxel.sprite._rpg_sprites.MovableSprite.set_down_animation"></a>

#### set\_down\_animation

```python
def set_down_animation(animation: Animation)
```

Set the animation to be used when the sprite moves DOWN

<a id="pyke_pyxel.sprite._rpg_sprites.MovableSprite.set_left_animation"></a>

#### set\_left\_animation

```python
def set_left_animation(animation: Animation)
```

Set the animation to be used when the sprite moves LEFT

<a id="pyke_pyxel.sprite._rpg_sprites.MovableSprite.set_right_animation"></a>

#### set\_right\_animation

```python
def set_right_animation(animation: Animation)
```

Set the animation to be used when the sprite moves RIGHT

<a id="pyke_pyxel.sprite._sprite"></a>

# \_sprite

<a id="pyke_pyxel.sprite._sprite.Sprite"></a>

## Sprite Objects

```python
class Sprite()
```

A drawable sprite with optional animations.

A Sprite contains a set of named Animation objects, a current active_frame
to draw, and a position. Animations may be started, paused, resumed and
looped. Sprites are lightweight containers for animation state and drawing
metadata.

<a id="pyke_pyxel.sprite._sprite.Sprite.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: str, default_frame: coord, cols: int = 1, rows: int = 1, resource_image_index: int = 0)
```

**Arguments**:

- `name` _str_ - Logical name for the sprite.
- `default_frame` _coord_ - The frame to use when no animation is active (idle frame).
- `cols` _int_ - Width in tiles for framed sprites (used when advancing frames).
- `rows` _int_ - Height in tiles for framed sprites (used when advancing frames).
- `resource_image_index` _int_ - Index of the image resource (if multiple images are used).

<a id="pyke_pyxel.sprite._sprite.Sprite.add_animation"></a>

#### add\_animation

```python
def add_animation(name: str, animation: Animation)
```

Add an animation to the sprite.

**Arguments**:

- `name` _str_ - The name to associate with the animation.
- `animation` _Animation_ - The Animation object to add.

<a id="pyke_pyxel.sprite._sprite.Sprite.activate_animation"></a>

#### activate\_animation

```python
def activate_animation(name: str, on_animation_end: Optional[Callable[[int], None]] = None)
```

Start the named animation.

If the named animation is already active this is a no-op. When
started the animation is unpaused, flip state is applied and the
optional `on_animation_end` callback will be invoked when a
non-looping animation finishes.

<a id="pyke_pyxel.sprite._sprite.Sprite.deactivate_animations"></a>

#### deactivate\_animations

```python
def deactivate_animations()
```

Stop any active animation and reset flip state.

<a id="pyke_pyxel.sprite._sprite.Sprite.active_animation_is"></a>

#### active\_animation\_is

```python
def active_animation_is(name: str) -> bool
```

Returns True if the named animation is active.

<a id="pyke_pyxel.sprite._sprite.Sprite.link_sprite"></a>

#### link\_sprite

```python
def link_sprite(sprite: "Sprite")
```

Link another sprite to this sprite.
The linked sprite's position will be updated whenever this sprite's position is updated.

**Arguments**:

- `sprite` _Sprite_ - The sprite to link.

<a id="pyke_pyxel.sprite._sprite.Sprite.unlink_sprite"></a>

#### unlink\_sprite

```python
def unlink_sprite(sprite: "Sprite")
```

Unlink a previously linked sprite.

**Arguments**:

- `sprite` _Sprite_ - The sprite to unlink.

<a id="pyke_pyxel.sprite._sprite.Sprite.set_position"></a>

#### set\_position

```python
def set_position(position: coord)
```

Sets the position of the sprite.

**Arguments**:

- `position` _coord_ - The new coordinate for the sprite's top-left corner.

<a id="pyke_pyxel.sprite._sprite.Sprite.set_rotation"></a>

#### set\_rotation

```python
def set_rotation(rotation: float|None)
```

Sets the rotation (in degrees) of the sprite.

<a id="pyke_pyxel.sprite._sprite.Sprite.set_scale"></a>

#### set\_scale

```python
def set_scale(scale: float)
```

Sets the scale of the sprite.

<a id="pyke_pyxel.sprite._sprite.Sprite.replace_colour"></a>

#### replace\_colour

```python
def replace_colour(old_colour: int, new_colour: int)
```

Replace the specified colour with a new colour when drawing this sprite.

**Arguments**:

- `old_colour` _int_ - The colour to replace.
- `new_colour` _int_ - The new colour.

<a id="pyke_pyxel.sprite._sprite.Sprite.reset_colour_replacements"></a>

#### reset\_colour\_replacements

```python
def reset_colour_replacements()
```

Reset the colour replacement specified in `replace_colour`.

<a id="pyke_pyxel.sprite._sprite.Sprite.position"></a>

#### position

```python
@property
def position() -> coord
```

Returns the current position of the sprite.

<a id="pyke_pyxel.sprite._sprite.Sprite.width"></a>

#### width

```python
@property
def width() -> int
```

Returns the width of the sprite in pixels.

<a id="pyke_pyxel.sprite._sprite.Sprite.height"></a>

#### height

```python
@property
def height() -> int
```

Returns the height of the sprite in pixels.

<a id="pyke_pyxel.sprite._sprite.Sprite.rotation"></a>

#### rotation

```python
@property
def rotation() -> float|None
```

Returns the rotation of the sprite in degrees.

<a id="pyke_pyxel.sprite._sprite.Sprite.scale"></a>

#### scale

```python
@property
def scale() -> float|None
```

Returns the scale of the sprite.

<a id="pyke_pyxel.sprite._compound_sprite"></a>

# \_compound\_sprite

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite"></a>

## CompoundSprite Objects

```python
class CompoundSprite()
```

A multi-tile sprite composed of a grid of `coord` tiles with optional overlay graphics.

CompoundSprite manages a matrix of tile coordinates (cols x rows)
and provides helpers to fill tiles or set individual tiles. Useful for
larger objects built from multiple sprite tiles.

The class also provides a graphics buffer allowing geometric shapes to be drawn over the sprite tiles

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill"></a>

#### fill

```python
def fill(tile_cols: list[int], tile_rows: list[int])
```

Fill the sprite with a grid of tiles, iterating over the provided columns and rows

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill_col"></a>

#### fill\_col

```python
def fill_col(col: int, tile_col: int, tile_rows: list[int], from_row: int = 1, to_row: int|None = None)
```

Fill one column (all rows) of a sprite with a sequence of tiles

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.fill_row"></a>

#### fill\_row

```python
def fill_row(row: int, tile_row: int, tile_cols: list[int], from_col: int = 1, to_col: int|None = None)
```

Fill one row (all columns) of a sprite with a sequence of tiles

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.set_tile"></a>

#### set\_tile

```python
def set_tile(col: int, row: int, tile: coord)
```

Set one tile in the sprite

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.clear_graphics"></a>

#### clear\_graphics

```python
def clear_graphics()
```

Clear the graphics buffer

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.graph_rect"></a>

#### graph\_rect

```python
def graph_rect(x: int, y: int, width_px: int, height_px: int, colour: int)
```

Draw a rectangle to the graphics buffer

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.graph_triangle"></a>

#### graph\_triangle

```python
def graph_triangle(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, colour: int)
```

Draw a triangle to the graphics buffer

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.replace_colour"></a>

#### replace\_colour

```python
def replace_colour(old_colour: int, new_colour: int)
```

Replace the specified colour with a new colour when drawing this sprite.

**Arguments**:

- `old_colour` _int_ - The colour to replace.
- `new_colour` _int_ - The new colour.

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.reset_colour_replacements"></a>

#### reset\_colour\_replacements

```python
def reset_colour_replacements()
```

Reset the colour replacement specified in `replace_colour`.

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.set_position"></a>

#### set\_position

```python
def set_position(position: coord)
```

Sets the position of the sprite.

**Arguments**:

- `position` _coord_ - The new coordinate for the sprite's top-left corner.

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.position"></a>

#### position

```python
@property
def position() -> coord
```

Returns the current position of the sprite.

**Returns**:

- `coord` - The coordinate of the sprite's top-left corner.

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.width"></a>

#### width

```python
@property
def width() -> int
```

Returns the width of the sprite in pixels.

<a id="pyke_pyxel.sprite._compound_sprite.CompoundSprite.height"></a>

#### height

```python
@property
def height() -> int
```

Returns the height of the sprite in pixels.

<a id="pyke_pyxel.sprite._anim"></a>

# \_anim

<a id="pyke_pyxel.sprite._anim.Animation"></a>

## Animation Objects

```python
class Animation()
```

An animation for a Sprite.

<a id="pyke_pyxel.sprite._anim.Animation.__init__"></a>

#### \_\_init\_\_

```python
def __init__(start_frame: coord, frames: int, loop: bool = True, flip: bool = False, fps: int|None = None, rotation: float|None = None)
```

**Arguments**:

- `start_frame` _coord_ - The position of the initial frame of the animation
- `frames` _int_ - The number of frames in the animation
- `loop` _bool_ - Whether the animation should loop or not
- `flip` _bool_ - Whether the animation image should be horizontally flipped
- `fps` _int_ - The FPS that the animation should run at. This value cannot be larger than the global animation FPS set in `GameSettings.fps.animation`
- `rotation` _float, optional_ - The rotation in degrees of this animation

<a id="pyke_pyxel.sprite._anim.Animation.set_current_frame"></a>

#### set\_current\_frame

```python
def set_current_frame(frame_index: int)
```

Set the current frame of the animation.

**Arguments**:

- `frame_index` _int_ - The index of the frame

<a id="pyke_pyxel.sprite._anim.AnimationFactory"></a>

## AnimationFactory Objects

```python
class AnimationFactory()
```

Convenience class to create multiple `Animation` instances with the same number of frames and FPS.

<a id="pyke_pyxel.sprite._anim.AnimationFactory.__init__"></a>

#### \_\_init\_\_

```python
def __init__(frames: int, fps: int|None = None, loop: bool = True)
```

**Arguments**:

- `frames` _int_ - The number of frames the created animations will have
- `fps` _int_ - The FPS of the created animations

<a id="pyke_pyxel.sprite._anim.AnimationFactory.at"></a>

#### at

```python
def at(position: coord, flip: bool = False, loop: bool|None = None, rotation: float|None = None) -> Animation
```

Create an `Animation` instance at the given position.

**Arguments**:

- `position` _coord_ - The `coord` of the top-left corner of the animation's graphic on the Pyxel resource sheet.
- `loop` _bool_ - Whether the animation should loop
- `flip` _bool_ - Whether the animation image should be horizontally flipped
- `rotation` _float, optional_ - The rotation in degrees of this animation

<a id="pyke_pyxel.sprite._text_sprite"></a>

# \_text\_sprite

<a id="pyke_pyxel.sprite._text_sprite.TextSprite"></a>

## TextSprite Objects

```python
class TextSprite()
```

A simple text sprite for rendering text using a pyxel font.

**Arguments**:

  text(str):
  colour(int):
- `font_file(str)` - The path to the BDF font file to load and use

<a id="pyke_pyxel.sprite._text_sprite.TextSprite.set_position"></a>

#### set\_position

```python
def set_position(position: coord)
```

Sets the position of the sprite.

**Arguments**:

- `position` _coord_ - The new coordinate for the sprite's top-left corner.

<a id="pyke_pyxel.sprite._text_sprite.TextSprite.position"></a>

#### position

```python
@property
def position() -> coord
```

Returns the current position of the sprite.

**Returns**:

- `coord` - The coordinate of the sprite's top-left corner.

<a id="pyke_pyxel.sprite._text_sprite.TextSprite.set_text"></a>

#### set\_text

```python
def set_text(text: str)
```

Sets the text content of the sprite.

**Arguments**:

- `text` _str_ - The new text content.

<a id="pyke_pyxel.hud"></a>

# hud

<a id="pyke_pyxel.hud.HUD"></a>

## HUD Objects

```python
class HUD()
```

HUD manages on-screen heads-up display elements for a game.

This class should be accessed through the `Game` instance via `game.hud`.

<a id="pyke_pyxel.hud.HUD.add_text"></a>

#### add\_text

```python
def add_text(text: TextSprite)
```

Add a TextSprite to the HUD.

<a id="pyke_pyxel.hud.HUD.add_sprite"></a>

#### add\_sprite

```python
def add_sprite(sprite: Sprite|CompoundSprite)
```

Add a Sprite or CompoundSprite to the HUD and assign a unique ID.

<a id="pyke_pyxel.hud.HUD.remove_sprite"></a>

#### remove\_sprite

```python
def remove_sprite(sprite: Sprite)
```

Remove a Sprite or CompoundSprite from the HUD.

Behavior:
- If the provided sprite is present in the _sprites list, it is removed.
- If the sprite is not present, the method does nothing (no exception raised).

<a id="pyke_pyxel.hud.HUD.add_button"></a>

#### add\_button

```python
def add_button(button: Button)
```

Add a Button to the HUD and assign a unique ID.

<a id="pyke_pyxel.hud.HUD.remove_button"></a>

#### remove\_button

```python
def remove_button(button: Button)
```

Remove a Button from the HUD.

Behavior:
- If the button is not present, the method does nothing (no exception raised).

<a id="pyke_pyxel.hud.HUD.add_bg"></a>

#### add\_bg

```python
def add_bg(item: Drawable|Image|Rect)
```

Add a background Drawable to the HUD and assign a unique ID.

<a id="pyke_pyxel.hud.HUD.remove_bg"></a>

#### remove\_bg

```python
def remove_bg(item: Drawable|Image|Rect)
```

Remove a background Drawable from the HUD.

Behavior:
- If the item is not present, the method does nothing (no exception raised).

<a id="pyke_pyxel._keyboard"></a>

# \_keyboard

<a id="pyke_pyxel._keyboard.Keyboard"></a>

## Keyboard Objects

```python
class Keyboard()
```

Access keyboard events and status.

This class should be accessed through the `Game` instance via `game.keyboard`.

In order to use the correct pyxel key mapping it is necessary to import pyxel.
For example:
>>> import pyxel
>>>
>>> if game.keyboard.was_pressed(pyxel.KEY_UP):
>>>     print("UP")

<a id="pyke_pyxel._keyboard.Keyboard.was_pressed"></a>

#### was\_pressed

```python
def was_pressed(key: int) -> bool
```

Return True if the provided key was pressed down this frame.

**Arguments**:

- `key(int)` - The `pyxel.KEY_*` value of the key to check

<a id="pyke_pyxel._keyboard.Keyboard.was_released"></a>

#### was\_released

```python
def was_released(key: int) -> bool
```

Return True if the provided key was pressed down this frame.

**Arguments**:

- `key(int)` - The `pyxel.KEY_*` value of the key to check

<a id="pyke_pyxel._keyboard.Keyboard.is_down"></a>

#### is\_down

```python
def is_down(key: int) -> bool
```

Return True if the provided key is pressed and held down this frame.

**Arguments**:

- `key(int)` - The `pyxel.KEY_*` value of the key to check

<a id="pyke_pyxel._keyboard.Keyboard.signal_for_key"></a>

#### signal\_for\_key

```python
def signal_for_key(key: int, signal: str)
```

Send a signal when a key is pressed. If the key is pressed down the signal will be emitted once
and then only emitted again if the key is pressed again.

**Arguments**:

- `key(int)` - The `pyxel.KEY_*` value of the key to connect the signal to
- `signal(str)` - The name of the signal to emit when the key is pressed down

<a id="pyke_pyxel._keyboard.Keyboard.remove_signal_for_key"></a>

#### remove\_signal\_for\_key

```python
def remove_signal_for_key(key: int)
```

Disconnect a signal from a key press.

**Arguments**:

- `key(int)` - The `pyxel.KEY_*` value of the key to disconnect the signal from

<a id="pyke_pyxel.math"></a>

# math

<a id="pyke_pyxel.math.RandomChoice"></a>

## RandomChoice Objects

```python
class RandomChoice()
```

Convenience class to select a random item from a list of choices.

<a id="pyke_pyxel.math.RandomChoice.select_one"></a>

#### select\_one

```python
def select_one() -> Any
```

Select one choice from the list of choices.

**Returns**:

- `Any` - The selected choice.

<a id="pyke_pyxel.math.WeightedChoice"></a>

## WeightedChoice Objects

```python
class WeightedChoice()
```

Convenience class to select a random choice based on a set of probabilities.
For example:
- choices = ["A", "B", "C"]
- probabilities = [0.3, 0.4, 0.3]

The sum of the probabilities should be 1.0.

<a id="pyke_pyxel.math.WeightedChoice.set"></a>

#### set

```python
def set(choices: list[Any], probabilities: list[float])
```

Set the list of choices and their matching probabilities.

**Arguments**:

- `choices` _list[Any]_ - A list of choices.
- `probabilities` _list[float]_ - A list of probabilities for each choice.

<a id="pyke_pyxel.math.WeightedChoice.add"></a>

#### add

```python
def add(choice: Any, probability: float)
```

Add a choice and its matching probability to the list of choices and probabilities.

**Arguments**:

- `choice` _Any_ - The choice to add.
- `probability` _float_ - The probability for the choice.

<a id="pyke_pyxel.math.WeightedChoice.reset"></a>

#### reset

```python
def reset()
```

Reset the list of choices and probabilities.

<a id="pyke_pyxel.math.WeightedChoice.select_one"></a>

#### select\_one

```python
def select_one() -> Any
```

Select one choice from the list of choices based on their matching probabilities.

**Returns**:

- `Any` - The selected choice.

<a id="pyke_pyxel.fx"></a>

# fx

<a id="pyke_pyxel.fx.FX"></a>

## FX Objects

```python
class FX()
```

FX class for managing visual effects in the game, specifically circular wipe transitions that can open or close,
transitioning between scenes or states.

This class should be accessed through the `Game` instance via `game.fx`.

<a id="pyke_pyxel.fx.FX.circular_wipe"></a>

#### circular\_wipe

```python
def circular_wipe(colour: int, wipe_closed: bool, completion_signal: str)
```

Create a full-screen circular wipe animation.

Parameters
----------
colour : int
    Colour index/value to use when rendering the wipe.
wipe_closed : bool
    If True, the wipe is configured to close (shrink) toward the centre.
    If False, the wipe is configured to open (expand) outward.
completion_signal : str
    Identifier of the signal/event to emit when the wipe animation finishes.

<a id="pyke_pyxel.fx.FX.splatter"></a>

#### splatter

```python
def splatter(colour: int, position: coord)
```

Create a splatter effect at the specified position.
The splatter effect animates within a single tile for 30 frames.

**Arguments**:

- `colour` _int_ - Colour index/value to use for the splatter.
- `position` _coord_ - The coordinate where the splatter effect should appear.

<a id="pyke_pyxel.fx.FX.scale_in"></a>

#### scale\_in

```python
def scale_in(image: Image, duration: float = 0.5, completion_signal: str|None = None)
```

Scale (zoom) an image in over a specified duration.
The image will be drawn as part of the FX.

**Arguments**:

- `image` _Image_ - the image to scale/zoom in
- `duration` _float_ - the duration in seconds over which to scale the image in
- `completion_signal` _str|None_ - an optional signal to send once the scale animation is complete

<a id="pyke_pyxel.fx.FX.scale_in_out"></a>

#### scale\_in\_out

```python
def scale_in_out(sprite: Sprite, to_scale: float, duration: float = 0.5, completion_signal: str|None = None)
```

Scale (zoom) a sprite in and back out over the specified duration.
The sprite will be scaled from its current scale to `to_scale` and back to its current scale.
The sprite has to already be added to the game, it will not be added as part of the FX, only its scale updated.

**Arguments**:

- `sprite` _Sprite_ - the sprite to scale/zoom in and out
- `duration` _float_ - the duration in seconds over which to scale the sprite in
- `completion_signal` _str|None_ - an optional signal to send once the scale animation is complete

<a id="pyke_pyxel.fx.FX.camera_shake"></a>

#### camera\_shake

```python
def camera_shake(duration: float, direction: DIRECTION, completion_signal: str|None = None)
```

Apply camera shake in the specified direction for the specified duration.

**Arguments**:

- `duration` _float_ - the duration in seconds over which to shake the camera
- `direction` _DIRECTION_ - the direction to shake the camera in
- `completion_signal` _str|None_ - an optional signal to send once the effect is complete

