from dataclasses import dataclass

from pyke_pyxel.game import Game
from pyke_pyxel.sprite import Sprite

import game_load


# State

@dataclass
class GameState:
    """Mutable game state. Sprite references are populated by game_load."""
    player_sprite: Sprite | None = None


STATE = GameState()


# Handlers

def start(game: Game):
    """Called on GAME.WILL_START."""
    game_load.load(game, STATE)


def update(game: Game):
    """Called on GAME.UPDATE."""
    pass
