import pyxel
from dataclasses import dataclass

from pyke_pyxel import DIRECTION
from pyke_pyxel.rpg import RPGGame, Player, Enemy


# State

@dataclass
class GameState:
    """Mutable game state."""
    pass


STATE = GameState()


# Handlers

def start(game: RPGGame):
    """Called on GAME.WILL_START."""
    pass


def update(game: RPGGame):
    """Called on GAME.UPDATE."""
    keyboard = game.keyboard
    player = game.player

    # Arrow-key movement
    if keyboard.was_pressed(pyxel.KEY_UP):
        player.start_moving(DIRECTION.UP)
    elif keyboard.was_released(pyxel.KEY_UP):
        player.stop_moving()
    elif keyboard.was_pressed(pyxel.KEY_DOWN):
        player.start_moving(DIRECTION.DOWN)
    elif keyboard.was_released(pyxel.KEY_DOWN):
        player.stop_moving()
    elif keyboard.was_pressed(pyxel.KEY_LEFT):
        player.start_moving(DIRECTION.LEFT)
    elif keyboard.was_released(pyxel.KEY_LEFT):
        player.stop_moving()
    elif keyboard.was_pressed(pyxel.KEY_RIGHT):
        player.start_moving(DIRECTION.RIGHT)
    elif keyboard.was_released(pyxel.KEY_RIGHT):
        player.stop_moving()


def player_blocked(player: Player, value):
    """Called on PLAYER.BLOCKED. value is the blocking Sprite, or None at map edge."""
    pass


def enemy_blocked(enemy: Enemy, value):
    """Called on ENEMY.BLOCKED. value is the blocking Sprite."""
    pass
