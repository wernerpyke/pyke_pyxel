from typing import Optional
from pyke_pyxel import coord, DIRECTION
from ._sprite import Sprite
from ._anim import Animation

OPEN: int = 0
CLOSED: int = 1
CLOSING: int = 2
OPENING: int = 3

class OpenableSprite(Sprite):
    """A Sprite that supports open/close states (e.g., doors, chests).

    The OpenableSprite exposes simple open/close methods and manages an
    internal status value that determines which frame is shown.
    """
    def __init__(self, name: str, open_frame: coord, closed_frame: coord):
        """
        Args:
            name (str): the logical name of the sprite
            open_frame (coord): The frame to use when the sprite is in its open state.
            closed_frame (coord): The frame to use when the sprite is in its closed state.
        """
        super().__init__(name, open_frame)
        self._open_frame = open_frame
        self._closed_frame = closed_frame

        self._status = OPEN

    def close(self):
        """Close the sprite"""
        self._status = CLOSED
        self._update_frame()

    def open(self):
        """Open the sprite"""
        self._status = OPEN
        self._update_frame()

    @property
    def is_closed(self) -> bool:
        """Return True if the sprite is closed"""
        return self._status == CLOSED
    
    @property
    def is_open(self) -> bool:
        """Return True if the sprite is open"""
        return self._status == OPEN
    
    def _update_frame(self):
        match self._status:
            case 0: # Open
                self.active_frame = self._open_frame
                return
            
            case 1: # Closed
                self.active_frame = self._closed_frame

class MovableSprite(Sprite):
    """Sprite with movement-related configuration and convenience setters.

    MovableSprite stores a movement speed and provides helper methods to
    create simple directional animations (up/down/left/right).
    """
    def __init__(self, name: str, default_frame: coord, cols: int = 1, rows: int = 1, resource_image_index: int=0):
        """
        Args:
            name (str): Logical name for the sprite.
            default_frame (coord): The frame to use when no animation is active (idle frame).
            cols (int): Width in tiles for framed sprites (used when advancing frames).
            rows (int): Height in tiles for framed sprites (used when advancing frames).
            resource_image_index (int): Index of the image resource (if multiple images are used).
        """
        super().__init__(name, default_frame, cols=cols, rows=rows, resource_image_index=resource_image_index)

    def set_up_animation(self, animation: Animation):
        """Set the animation to be used when the sprite moves UP"""
        self.add_animation(DIRECTION.UP.value, animation)

    def set_down_animation(self, animation: Animation):
        """Set the animation to be used when the sprite moves DOWN"""
        self.add_animation(DIRECTION.DOWN.value, animation)

    def set_left_animation(self, animation: Animation):
        """Set the animation to be used when the sprite moves LEFT"""
        self.add_animation(DIRECTION.LEFT.value, animation)

    def set_right_animation(self, animation: Animation):
        """Set the animation to be used when the sprite moves RIGHT"""
        self.add_animation(DIRECTION.RIGHT.value, animation)

    def deactivate_movement_animation(self):
        if (
                self.active_animation_is(DIRECTION.UP.value) or 
                self.active_animation_is(DIRECTION.DOWN.value) or
                self.active_animation_is(DIRECTION.LEFT.value) or
                self.active_animation_is(DIRECTION.RIGHT.value) 
            ):
                self.deactivate_animations()