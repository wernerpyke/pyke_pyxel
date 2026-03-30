from pyke_pyxel import coord
from pyke_pyxel.sprite import Sprite, Animation
from pyke_pyxel.rpg import Room, Player


def player_sprite():
    """Return the sprite (or callable) used to create the player."""
    pass


def build_room(room: Room):
    """Create walls, doors, and obstacles. Called before game.start()."""
    pass


def set_player_position(player: Player):
    """Set the player's starting position."""
    player.set_position(coord(1, 1))
