from pathlib import Path

from pyke_pyxel import GameSettings
from pyke_pyxel.signals import Signals
from pyke_pyxel.rpg.game import RPGGame

import game_loop
import game_load

# Signals

Signals.connect(Signals.GAME.WILL_START, game_loop.start)
Signals.connect(Signals.GAME.UPDATE, game_loop.update)
Signals.connect(Signals.PLAYER.BLOCKED, game_loop.player_blocked)
Signals.connect(Signals.ENEMY.BLOCKED, game_loop.enemy_blocked)

# Settings

settings = GameSettings()
settings.fps.game = 30
settings.fps.animation = 8
settings.size.window = 160

# Game

game = RPGGame(
    settings=settings,
    title="Game Title",
    resources=f"{Path(__file__).parent.resolve()}/assets/resources.pyxres",
)

# Room and Player

game_load.build_room(game.room)
player = game.set_player(game_load.player_sprite(), 30)
game_load.set_player_position(player)

# Start

game.start()
