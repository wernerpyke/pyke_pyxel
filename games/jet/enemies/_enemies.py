from dataclasses import dataclass
import random

from pyke_pyxel import coord, area
from pyke_pyxel.rpg import RPGGame
from pyke_pyxel.signals import Signals

from .spinner import Spinner

launch_areas: list[area] = [
    area(1, 1, 1, 40), # left

    area(1, 1, 40, 1), # top

    area(40, 1, 40, 40), #right

    area(1, 40, 40, 40) # bottom
    ]

targets: list[coord] = [
    coord(19, 21),
    coord(24, 21),

    coord(20, 24),
    coord(24, 24)
]

def _random_launch_area() -> area:
    return random.choice(launch_areas)

def _random_target() -> coord:
    return random.choice(targets)

def _launch_spinner(game: RPGGame):
    spinner = Spinner()

    location = game.map.random_location(_random_launch_area())
    spinner.set_position(location.position) # type: ignore warning

    game.room.add_enemy(spinner)
    spinner.move_to(_random_target(), game.map)

class _enemies:

    def __init__(self) -> None:
        self.count: float = 1.0
        self.min_delay: float = 2.0
        self.max_delay: float = 4.0

    def start(self, game: RPGGame):
        Signals.connect("timer_update_level", self._update_level)
        Signals.connect("timer_launch_enemy", self._launch_enemy)
        
        game.timer.every(10.0, "timer_update_level", game)

        self._enemy_timer(game)

    def update(self, game: RPGGame):
        pass
    
    def _launch_enemy(self, game: RPGGame):
        print(f"LAUNCH ENEMY {self.count}")
        for _ in range(round(self.count)):
            _launch_spinner(game)

    def _update_level(self, game: RPGGame):
        self.count += 0.02

        if self.min_delay > 1:
            self.min_delay -= 0.2
        
        if self.max_delay > 1.5:
            self.max_delay -= 0.4

        print(f"UPDATE LEVEL {self.count} {self.min_delay} {self.max_delay}")

        self._enemy_timer(game)

    def _enemy_timer(self, game: RPGGame):
        delta = self.max_delay - self.min_delay
        delay = self.min_delay + (random.random() * delta)
        game.timer.every(delay , "timer_launch_enemy", game)

ENEMIES = _enemies()