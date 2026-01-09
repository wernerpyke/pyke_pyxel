from pyke_pyxel import coord
from pyke_pyxel.map import Map
from pyke_pyxel.rpg.enemy import Enemy

import games.jet.sprites as sprites


class Spinner(Enemy):

    def __init__(self):
        sprite = sprites.spinner()

        super().__init__(sprite, speed_px_per_second=50)