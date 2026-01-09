from typing import Callable

from pyke_pyxel.rpg.actor import Actor
from pyke_pyxel.rpg.enemy import Enemy

from pyke_pyxel import log_debug, GameSettings, coord, area
from pyke_pyxel.game import Game
from .player import Player
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import MovableSprite
from .room import Room

class RPGGame(Game):

    def __init__(self, settings: GameSettings, title: str, resources: str):
        """
        Specialised sub-class of `pyke_pyxel.Game` which adds basic room- and actor-based RPG mechanics.
        
        Attributes:
            player (Player): The player character. Use set_player() to assign the player instance.
            room (Room): The current room/map the player is in. Automatically initialized with the game map.
        """
        super().__init__(settings, title, resources)
        """
        Args:
            settings (GameSettings): The game settings configuration.
            title (str): The title of the game window.
            resources (str): The path to the resources directory.
        """

        self._player: Player
        self._room = Room(self._map)

        self._actor_id = 0
        self._actors: list[Actor] = []
        Signals.connect("enemy_added", self.add_actor)
        Signals.connect("enemy_removed", self.remove_actor)
        Signals.connect("actor_added", self.add_actor)
        Signals.connect("actor_removed", self.remove_actor)


    def set_player(self, sprite: MovableSprite|Callable[[], MovableSprite], speed_px_per_second: int) -> Player:
        """
        Assigns a player sprite to the game, creating a `Player` instance.

        Args:
            sprite (MovableSprite | Callable[[], MovableSprite]): The sprite
                (or a callable that returns a sprite) representing the player.
            speed_px_per_second (int): The speed of the player's movements expressed as pixels per second

        Returns:
            Player: The initialized `Player` instance.

        """
        if isinstance(sprite, Callable):
            sprite = sprite()

        self._player = Player(sprite, speed_px_per_second)

        self._sprites.append(sprite)

        self.add_actor(self.player)

        return self._player

    def clear_all(self):
        """Clear all sprites, TileMap, HUD and FX"""
        super().clear_all()
        self._actors.clear()
        self.player = None # type: ignore

    def add_actor(self, actor: Actor):
        """
        Add an actor to the game's actor collection.

        Args:
            actor (Actor): The actor object to add to the game.
        """
        self._actor_id += 1
        actor._id = self._actor_id
        self._actors.append(actor)

    def remove_actor(self, actor: Actor):
        """
        Remove an actor from the game's active actor collection.

        Args:
            actor (Actor): The actor object to remove from the game.
        """
        if actor in self._actors:
            self._actors.remove(actor)

    def enemies_at(self, position: coord|area, tolerance: float = 0.0) -> list[Enemy]:
        """
        Return a list of enemies which are at the grid location of the provided position.

        Args:
            position (coord): the grid location to check

        Returns:
            list[Enemy]: the enemies that are at the provided position
        """
        enemies: list[Enemy] = []

        if isinstance(position, coord):
            for actor in self._actors:
                if isinstance(actor, Enemy) and actor.position.is_same_grid_location(position):
                    enemies.append(actor)
        else:
            for actor in self._actors:
                if isinstance(actor, Enemy) and position.contains(actor.position):
                    enemies.append(actor)

        return enemies

    @property
    def player(self) -> Player:
        """Returns the `Player` instance for this game"""
        return self._player

    @property
    def room(self) -> Room:
        """Returns the `Room` instance for this game"""
        return self._room

    def _update(self):

        # Keyboard
        self._keyboard._update(self)

        if self._paused:
            return

        self._update_timer()

        Signals.send(Signals.GAME.UPDATE, self)

        to_remove: list[Actor] = []
        for actor in self._actors:
            if actor._is_alive:
                actor._update(self._map)
            else:
                to_remove.append(actor)

        for a in to_remove:
            # if a in self._actors: - should not be necessary
            self._actors.remove(a)

        self._update_fx()

        self._update_animations()