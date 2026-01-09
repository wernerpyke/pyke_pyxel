
from pyke_pyxel.signals import Signals

def _actor_added(sprite):
    Signals.send("actor_added", sprite)

def _actor_removed(sprite):
    Signals.send("actor_removed", sprite)

def _enemy_added(sprite):
    Signals.send("enemy_added", sprite)

def _enemy_removed(sprite):
    Signals.send("enemy_removed", sprite)