from typing import Optional, Callable
import pyxel
import math

from pyke_pyxel import coord, area, GameSettings

from ._anim import Animation

class Sprite:
    """A drawable sprite with optional animations.

    A Sprite contains a set of named Animation objects, a current active_frame
    to draw, and a position. Animations may be started, paused, resumed and
    looped. Sprites are lightweight containers for animation state and drawing
    metadata.
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
        self._id: int = 0
        self.name = name
        self.default_frame = default_frame
        self.cols = cols
        self.rows = rows
        self._resource_image_index = resource_image_index

        tile_size = GameSettings.get().size.tile
        self._width = cols * tile_size
        self._height = rows * tile_size

        self._position: coord
        self._rotation: float|None = None
        self._scale: float|None = None

        self.active_frame = self.default_frame
        self.animations: dict[str, Animation] = { }
        self._animation: Animation|None = None

        self._linked_sprites: list[Sprite]|None = None

        self._replace_colour: tuple[int,int]|None = None

    def add_animation(self, name: str, animation: Animation):
        """Add an animation to the sprite.
        
        Args:
            name (str): The name to associate with the animation.
            animation (Animation): The Animation object to add.


        """
        animation._name = name
        self.animations[name] = animation

        # The animation needs to know how 'wide' the sprite is
        # to be able to update frames correctly
        animation._cols = self.cols

    def activate_animation(self, name: str, on_animation_end: Optional[Callable[[int], None]] = None):
        """Start the named animation.

        If the named animation is already active this is a no-op. When
        started the animation is unpaused, flip state is applied and the
        optional `on_animation_end` callback will be invoked when a
        non-looping animation finishes.
        """
        if self._animation and self._animation._name == name:
            return

        self._animation = self.animations[name]
        self._animation._activate(self._id, on_animation_end)

    def deactivate_animations(self):
        """Stop any active animation and reset flip state."""
        self._animation = None

    def active_animation_is(self, name: str) -> bool:
        """Returns True if the named animation is active."""
        return self._animation is not None and self._animation._name == name

    @property
    def is_animating(self) -> bool:
        return self._animation is not None

    def link_sprite(self, sprite: "Sprite"):
        """
        Link another sprite to this sprite. 
        The linked sprite's position will be updated whenever this sprite's position is updated.

        Args:
            sprite (Sprite): The sprite to link.
        """
        if not self._linked_sprites:
            self._linked_sprites = []
        self._linked_sprites.append(sprite)

    def unlink_sprite(self, sprite: "Sprite"):
        """
        Unlink a previously linked sprite.

        Args:
            sprite (Sprite): The sprite to unlink.
        """
        if not self._linked_sprites:
            return
        if sprite in self._linked_sprites:
            self._linked_sprites.remove(sprite)

    def set_position(self, position: coord):
        """
        Sets the position of the sprite.

        Args:
            position (coord): The new coordinate for the sprite's top-left corner.
        """
        if self._linked_sprites:
            diff = position.diff(self._position)
            for s in self._linked_sprites:
                s._position.move_by(diff[0], diff[1])

        self._position = position # .clone()

    def set_rotation(self, rotation: float|None):
        """Sets the rotation (in degrees) of the sprite."""
        # TODO, what about self._linked_sprite ?
        if (rotation is None) or (rotation == 0.0):
            self._rotation = None
        else:
            self._rotation = rotation % 360

    def set_scale(self, scale: float):
        """Sets the scale of the sprite."""
        # TODO, what about self._linked_sprite ?
        if scale == 1.0:
            self._scale = None
        else:
            self._scale = scale

    def replace_colour(self, old_colour: int, new_colour: int):
        """
        Replace the specified colour with a new colour when drawing this sprite.

        Args:
            old_colour (int): The colour to replace.
            new_colour (int): The new colour.
        """
        self._replace_colour = (old_colour, new_colour)

    def reset_colour_replacements(self):
        """Reset the colour replacement specified in `replace_colour`."""
        self._replace_colour = None

    @property
    def position(self) -> coord:
        """Returns the current position of the sprite."""
        return self._position
    
    @property
    def width(self) -> int:
        """Returns the width of the sprite in pixels."""
        return self._width
    
    @property
    def height(self) -> int:
        """Returns the height of the sprite in pixels."""
        return self._height
    
    @property
    def rotation(self) -> float|None:
        """Returns the rotation of the sprite in degrees."""
        if anim := self._animation:
            return anim.rotation
        else:
            return self._rotation
        
    @property
    def scale(self) -> float|None:
        """Returns the scale of the sprite."""
        return self._scale
        
    def rotated_position(self) -> coord:
        pos = self._position
        rotation = self.rotation
        if not rotation:
            return pos
        else:
            # 1. Convert degrees to radians, as math functions use radians
            angle_rad = math.radians(rotation)
            
            # 2. Define the Pivot Point (Center of the Cell)
            # The center is the top-left (x, y) plus half the size.
            pivot_x = pos.mid_x
            pivot_y = pos.mid_y
            
            # The point we are rotating is the original top-left corner (self.x, self.y)
            point_x = pos.x
            point_y = pos.y

            # 3. Apply the 2D Rotation Formula (around the pivot)
            # Formulas for rotating a point (px, py) around a pivot (cx, cy) by angle (a):
            # x_new = cx + (px - cx) * cos(a) - (py - cy) * sin(a)
            # y_new = cy + (px - cx) * sin(a) + (py - cy) * cos(a)

            # Pre-calculate the difference vectors (px - cx) and (py - cy)
            dx = point_x - pivot_x
            dy = point_y - pivot_y
            
            # Apply the rotation
            x_rotated = round(pivot_x + (dx * math.cos(angle_rad) - dy * math.sin(angle_rad)))
            y_rotated = round(pivot_y + (dx * math.sin(angle_rad) + dy * math.cos(angle_rad)))

            return coord.with_xy(x_rotated, y_rotated)
    
    def __eq__(self, other):
        return isinstance(other, Sprite) and self._id == other._id

    def _update_frame(self):
        if anim := self._animation:
            if frame := anim._update_frame():
                self.active_frame = frame
            else:
                self._animation = None
                self.active_frame = self.default_frame
                
        else:
            self.active_frame = self.default_frame

    def _draw(self, settings: GameSettings):
        frame = self.active_frame
        position = self._position

        width = self._width
        if anim := self._animation:
            if anim.flip:
                width *= -1

        if self._replace_colour:
            pyxel.pal(self._replace_colour[0], self._replace_colour[1])

        pyxel.blt(x=position.x,
                y=position.y,
                img=self._resource_image_index,
                u=frame.x,
                v=frame.y,
                w=width,
                h=self._height,
                rotate=self.rotation,
                scale=self.scale,
                colkey=settings.colours.sprite_transparency)
        
        if self._replace_colour:
            pyxel.pal()

        # rp = self.rotated_position()
        # pyxel.circ(rp.x, rp.y, 1, 8)
