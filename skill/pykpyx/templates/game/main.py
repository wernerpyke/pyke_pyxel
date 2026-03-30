from pathlib import Path

from pyke_pyxel import GameSettings, COLOURS
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals

import game_loop

# Settings

settings = GameSettings()
settings.size.window = 160
settings.colours.background = COLOURS.GREEN
settings.colours.sprite_transparency = COLOURS.BEIGE

# Game

game = Game(
    settings=settings,
    title="Game Title",
    resources=f"{Path(__file__).parent.resolve()}/assets/resources.pyxres",
)

# Signals

Signals.connect(Signals.GAME.WILL_START, game_loop.start)
Signals.connect(Signals.GAME.UPDATE, game_loop.update)

# Start

game.start()
