from typing import Callable

from pyke_pyxel import GameSettings, DIRECTION, coord, log_debug, log_error
from pyke_pyxel.sprite import Sprite, MovableSprite
from pyke_pyxel.signals import Signals
from pyke_pyxel.map import Map

from ._projectile import Projectile

class Actor:
    """Represents an actor in the game world. 
    An actor can be a player, enemy, item, etc. which are present at a position on the game map.    
    """
    def __init__(self, sprite: Sprite):
        """
        Args:
            sprite (Sprite): the sprite that represents this actor
        """
        self._id: int = 0
        self._sprite = sprite

        self._projectiles: list[Projectile] = []

        self._is_alive = True

    def launch_projectile(self, sprite: Sprite|Callable[[], Sprite], speed_px_per_second: int, direction: DIRECTION):
        """
        Launch a projectile from this actor.

        Args:
            sprite_type (Sprite | Callable[[], Sprite]): The sprite of the projectile
            speed_px_per_second (int): The speed of the projectile expressed as pixels per second
            direction (DIRECTION): The direction the projectile is travelling
        """
        if isinstance(sprite, Callable):
            sprite = sprite()
        
        d_x = 0
        d_y = 0
        tile_size = round(GameSettings.get().size.tile * 0.5)
        match direction:
            case DIRECTION.UP:
                d_y = tile_size * -1
            case DIRECTION.DOWN:
                d_y = tile_size
            case DIRECTION.LEFT:
                d_x = tile_size * -1
            case DIRECTION.RIGHT:
                d_x = tile_size

        pos = self._sprite.position
        sprite.set_position(coord.with_xy(pos.x + d_x, pos.y + d_y))
        
        projectile = Projectile(sprite, speed_px_per_second, direction)
        self._projectiles.append(projectile)
        
        Signals.send_add_sprite(sprite)

    def remove(self):
        """Remove this actor from the game"""
        self._is_alive = False
        Signals.send_remove_sprite(self._sprite)

    def _update(self, map: Map):
        for projectile in self._projectiles:
            if projectile._update(map) == False:
                log_debug("Actor.update() removing projectile")
                self._projectiles.remove(projectile)

    def __hash__(self) -> int:
        return self._id

    def __eq__(self, other):
        return isinstance(other, Actor) and self._id == other._id

    @property 
    def name(self):
        """Returns the name of this actor"""
        return self._sprite.name
    
    @property
    def position(self):
        """Returns the position of this actor"""
        return self._sprite.position
    
    @property
    def sprite(self) -> Sprite:
        """Returns the sprite of this actor"""
        return self._sprite

    @property
    def sprite_id(self) -> int:
        """Returns the ID of the sprite of this actor"""
        return self._sprite._id

class MovableActor(Actor):

    def __init__(self, sprite: MovableSprite, speed_px_per_second: int):
        """
        Args:
            sprite (MovableSprite): the sprite that represents this actor
            speed_px_per_second (int): The speed of the actor's movements expressed as pixels per second
        """
        super().__init__(sprite)

        self._px_per_frame: float = speed_px_per_second / GameSettings.get().fps.game
        self._px_counter = 0
        self._move_to: coord|None = None
        self._move_path: list[coord]|None = None
        self._blocked_by: coord|None = None

        self.active_dir: DIRECTION|None = None
        self.facing_dir: DIRECTION = DIRECTION.DOWN

    def set_position(self, position: coord):
        """Set the position of the actor"""
        self._sprite.set_position(position)

    def start_moving(self, direction: DIRECTION):
        """Start moving in the provided direction"""
        if (self.active_dir == direction) and self._sprite.is_animating:
            return

        self._sprite.activate_animation(direction.value)
        self.active_dir = direction
        self.facing_dir = direction

        self._px_counter = 0

    def stop_moving(self):
        """Stop moving"""
        self._sprite.deactivate_animations()
        self.active_dir = None
        self._move_to = None
        self._move_path = None
        self._blocked_by = None
        self._px_counter = 0

    def move_to(self, position: coord, pathfinder: Map|None = None, allow_diagonal: bool|None = None):
        """
        Move to the provided coordinate.

        Args:
            position (coord): The coordinate to move to
            pathfinder (Map|None): the Map to use for pathfinding
            allow_diagonal (bool, optional): Whether to allow diagonal movement.
        """
        if pathfinder:
            self._move_path = pathfinder.find_path(self.position, position, allow_diagonal)
            if self._move_path:
                self._move_to = self._move_path.pop(0)
            else:
                log_error(f"MovableActor.move_to() cannot find path from {self.position} to {position}")
                self._move_to = position
        else:
            self._move_path = None
            self._move_to = position
        
        self.active_dir = None
        self._px_counter = 0

    def move_along_path(self, path: list[coord]):
        """
        Move along the provided path.

        Args:
            path (list[coord]): The path to follow
        """
        self._move_path = path
        self._move_to = self._move_path.pop(0)
        self.active_dir = None
        self._px_counter = 0

    @property
    def is_moving(self) -> bool:
        """Return True if the actor is moving"""
        return self.active_dir is not None or self._move_to is not None or self._move_path is not None

    def _update(self, map: Map):
        if self.active_dir or self._move_to or self._move_path:
            if self._move(map):
                pass
                # TODO - if, in future we want to send this signal
                # Then Player._move and Enemy._move should return False
                # and generate its own signals
                # Signals.send(Signals.ACTOR.MOVED, self)
        super()._update(map)

    def _move(self, map: Map) -> bool:
        # IMPORTANT: _move() is called once per frame
        self._px_counter += self._px_per_frame
        if self._px_counter < 1:
            return True
        self._px_counter = 0

        distance = round(self._px_per_frame) if self._px_per_frame > 1 else 1

        next_pos = self._next_direction_pos(distance)
        if not next_pos:
            next_pos = self._next_destination_pos(distance)
        
        if not next_pos:
            return False
        
        # Special condition - if we are moving along a path then we don't check for collissions
        # The problem with checking collissions on a path is it breaks sprite.position.clone_towards() 
        # since the path allows corner-hopping
        # TODO - is this ok?
        skip_collission_check = self._move_path is not None
        
        if skip_collission_check or map.sprite_can_move_to(next_pos):
            self._sprite.set_position(next_pos)
            return True
        else:
            # print(f"BLOCKED {next_pos}")
            self._blocked_by = next_pos
            return False

    def _next_destination_pos(self, distance: int) -> coord|None:
        move_to = self._move_to

        if not move_to:
            return None
        
        next_pos = self._sprite.position.clone_towards(move_to, distance)
        if next_pos.is_same_grid_location(move_to):
            if self._move_path: # Next position on the path
                self._move_to = self._move_path.pop(0)
                if len(self._move_path) == 0:
                    self._move_path = None
            else: # Done
                self._move_to = None

        return next_pos


    def _next_direction_pos(self, distance: int) -> coord|None:
        if not self.active_dir:
            return None
        
        by_x = 0
        by_y = 0
        match self.active_dir:
            case DIRECTION.UP:
                by_y = distance * -1
            case DIRECTION.DOWN:
                by_y = distance
            case DIRECTION.LEFT:
                by_x = distance * -1
            case DIRECTION.RIGHT:
                by_x = distance
        
        return self._sprite.position.clone_by(by_x, by_y, self.active_dir)