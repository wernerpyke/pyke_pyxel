import pyxel
from pyke_pyxel import coord
from ._effect import _Effect

class _SplatterEffect(_Effect):
    def __init__(self, position: coord, colour: int):
        super().__init__(None)
        self._colour = colour
        self._position = position
        self._frame = 0

        self._x = position.mid_x
        self._y = position.mid_y

    def _do(self):
        # TODO - the below assumes 60 FPS
        frame = self._frame

        if frame <= 10:
            # Centre
            pyxel.pset(self._x-1, self._y, self._colour)
            pyxel.pset(self._x-1, self._y+1, self._colour)
            pyxel.pset(self._x, self._y, self._colour)
            pyxel.pset(self._x, self._y+1, self._colour)
            
        if (frame > 5) and (frame <= 10):
            pyxel.pset(self._x-1, self._y-2, self._colour)  # Top
            pyxel.pset(self._x+1, self._y+3, self._colour)  # Bottom
            pyxel.pset(self._x+3, self._y, self._colour)    # Right
            pyxel.pset(self._x-2, self._y+1, self._colour)  # Left

        if (frame > 10) and (frame <= 20):
            pyxel.pset(self._x-1, self._y-4, self._colour)  # N
            pyxel.pset(self._x+4, self._y, self._colour)    # E
            pyxel.pset(self._x+1, self._y+4, self._colour)  # S
            pyxel.pset(self._x-4, self._y, self._colour)    # W

        if (frame > 10) and (frame <= 40):
            pyxel.pset(self._x+4, self._y-3, self._colour)  # NE
            pyxel.pset(self._x+3, self._y+2, self._colour)  # SE
            pyxel.pset(self._x, self._y+2, self._colour)    # SW
            pyxel.pset(self._x-2, self._y-2, self._colour)  # NW

        if frame > 40:
            self._complete()

        self._frame += 1