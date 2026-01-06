import random
from pyke_pyxel import coord
from pyke_pyxel.sprite import Sprite
from pyke_pyxel.rpg import RPGGame, Player

import sprites

def add_house(game: RPGGame) -> Sprite:
    house = sprites.house()
    
    game.room.add_wall(house, 20, 20)
    game.map.mark_open(coord(20,20))
    game.map.mark_open(coord(21,20))
    game.map.mark_open(coord(22,20))
    game.map.mark_open(coord(23,20))

    return house

def add_trees(game: RPGGame):
    # Top-left
    _trees_top(game,    at=coord(2, 2),     cols=8, rows=1)
    _trees(game,        at=coord(5, 4),     cols=6, rows=2)
    _trees_right(game,  at=coord(17,4),     cols=1, rows=2)
    _trees(game,        at=coord(6, 7),     cols=6, rows=1)
    _trees_right(game,  at=coord(18,7),     cols=1, rows=1)
    _trees(game,        at=coord(8, 9),     cols=4, rows=1)
    _trees(game,        at=coord(10, 11),   cols=2, rows=1)

    # Top-right
    _trees_top(game,    at=coord(24, 2),    cols=8, rows=1)
    _trees_top(game,    at=coord(26, 5),    cols=6, rows=2)
    _trees_left(game,   at=coord(28, 8),    cols=4, rows=6)
    _trees_right(game,  at=coord(31, 15),   cols=2, rows=4)

    # Mid-left
    _trees_top(game,    at=coord(2, 18),    cols=3, rows=1)
    _trees_right(game,  at=coord(2, 20),    cols=4, rows=1)
    _trees_right(game,  at=coord(2, 22),    cols=3, rows=1)
    _trees_right(game,  at=coord(2, 24),    cols=1, rows=1)

    # Bottom-left
    _trees_top(game,    at=coord(2, 32),    cols=7, rows=2)
    _trees_right(game,  at=coord(4, 35),    cols=8, rows=1)
    _trees(game,        at=coord(5, 37),    cols=7, rows=1)
    _trees_right(game,  at=coord(19, 37),   cols=1, rows=1)

    # Bottom-right
    _trees_top(game,    at=coord(28, 32),   cols=4, rows=2)
    _trees_right(game,  at=coord(29, 35),   cols=4, rows=1)
    _trees_right(game,  at=coord(32, 37),   cols=4, rows=1)


def _trees(game: RPGGame, at: coord, cols: int, rows: int):
    for c in range(cols):
        for r in range(rows):
            tree = sprites.tree()
            game.room.add_wall(tree, at.col + c*2, at.row + r)
            tree.position.move_by(random.randint(-2, 2), random.randint(0, 2))

def _trees_top(game: RPGGame, at: coord, cols: int, rows: int):
    _trees(game, at, cols, rows)

    row = at.row
    for c in range(cols):
        col = at.col + c*2
        game.map.mark_open(coord(col, row))
        game.map.mark_open(coord(col+1, row))

def _trees_right(game: RPGGame, at: coord, cols: int, rows: int):
    _trees(game, at, cols, rows)

    col = at.col + cols*2 - 1
    for r in range(rows):
        row = at.row + r*2
        game.map.mark_open(coord(col, row))
        game.map.mark_open(coord(col, row+1))

def _trees_left(game: RPGGame, at: coord, cols: int, rows: int):
    _trees(game, at, cols, rows)

    col = at.col
    for r in range(rows):
        row = at.row + r*2
        game.map.mark_open(coord(col, row))
        game.map.mark_open(coord(col, row+1))