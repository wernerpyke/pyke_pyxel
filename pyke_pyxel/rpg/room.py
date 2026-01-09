from typing import Callable
from pyke_pyxel import coord
from pyke_pyxel.map import Map
from pyke_pyxel.sprite import Sprite, OpenableSprite, MovableSprite
from pyke_pyxel.signals import Signals
from .actor import Actor, MovableActor
from .enemy import Enemy

from . import _signals

class Room:

    def __init__(self, map: Map) -> None:
        self._map = map

    def add_wall(self, sprite: Sprite|Callable[[], Sprite], col: int, row: int):
        """
        Add a wall to the map. The related map position will be marked as blocked.


        Args:
            sprite (Sprite | Callable[[], Sprite]): The sprite (or a callable that returns a sprite) representing the wall.
            col (int): The column position of the wall
            row (int): The row position of the wall
        """
        if isinstance(sprite, Callable):
            sprite = sprite()
        sprite.set_position(coord(col, row))
        
        Signals.send_add_sprite(sprite)

        # TODO - should we check if there's an existing sprite at this col/row 
        # and then warn/replace the existing sprite?

        for c in range(0, sprite.cols):
            for r in range(0, sprite.rows):
                p = coord(col + c, row + r)
                self._map.mark_blocked(p, sprite)

    def add_door(self, sprite: OpenableSprite|Callable[[], OpenableSprite], col: int, row: int, closed: bool = True):
        """
        Add an openable door to the map. The related map position will be marked as either open or closed.

        Args:
            sprite (OpenableSprite | Callable[[], OpenableSprite]): The sprite (or a callable that returns a sprite) representing the door.
            col (int): The column position of the door
            row (int): The row position of the door
            closed (bool): whether the door should be closed or open by default
        """
        if isinstance(sprite, Callable):
            sprite = sprite()
        position = coord(col, row)
        sprite.set_position(position)
        
        if closed:
            sprite.close()
        else:
            sprite.open()

        Signals.send_add_sprite(sprite)
        self._map.mark_openable(position, sprite, closed)

    def add_enemy(self, sprite: Enemy|MovableSprite|Callable[[], MovableSprite], speed_px_per_second: int = 8) -> Enemy:
        """
        Add an enemy to the map.

        Args:
            sprite (Enemy | MovableSprite | Callable[[], MovableSprite]): The sprite (or a callable that returns a sprite) representing the enemy.
            speed_px_per_second (int): The speed of the enemy's movements expressed as pixels per second, defaults to 8

        Returns:
            Enemy: The initialized `Enemy` instance.
        """
        if isinstance(sprite, Enemy):
            enemy = sprite
            Signals.send_add_sprite(enemy._sprite)
        else:
            if isinstance(sprite, Callable):
                sprite = sprite()
            enemy = Enemy(sprite, speed_px_per_second)
            Signals.send_add_sprite(sprite)

        _signals._enemy_added(enemy)

        return enemy
    
    def add_movable_actor(self, sprite:MovableSprite|Callable[[], MovableSprite], speed_px_per_second: int = 8) -> MovableActor:
        """
        Add a movable actor to the map.

        Args:
            sprite (MovableSprite | Callable[[], MovableSprite]): The sprite (or a callable that returns a sprite) representing the actor.
            speed_px_per_second (int): The speed of the actor's movements expressed as pixels per second, defaults to 8.

        Returns:
            MovableActor: The initialized `MovableActor` instance.
        """
        if isinstance(sprite, Callable):
            sprite = sprite()
        actor = MovableActor(sprite, speed_px_per_second)
        Signals.send_add_sprite(sprite)

        _signals._actor_added(actor)

        return actor
    
    def add_actor(self, sprite:Sprite|Callable[[], Sprite]) -> Actor:
        """
        Add an actor to the map.

        Args:
            sprite (Sprite | Callable[[], Sprite]): The sprite (or a callable that returns a sprite) representing the actor.

        Returns:
            Actor: The initialized `Actor` instance.
        """
        
        if isinstance(sprite, Callable):
            sprite = sprite()
        actor = Actor(sprite)
        Signals.send_add_sprite(sprite)

        _signals._actor_added(actor)

        return actor
