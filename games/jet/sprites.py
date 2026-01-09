import random
from pyke_pyxel import coord, DIRECTION
from pyke_pyxel.sprite import Sprite, MovableSprite, AnimationFactory, Animation
from pyke_pyxel.rpg import Player
from pyke_pyxel.math import RandomChoice

tree_frames = RandomChoice([coord(1, 7), coord(3, 7), coord(5, 7), coord(7, 7), coord(9, 7), coord(9,7), coord(11,7), coord(13,7), coord(15,7)])

def player() -> MovableSprite:
    sprite = MovableSprite("player", coord(1,1), cols=1, rows=1)

    anim= AnimationFactory(4, loop=False)
    sprite.set_up_animation(anim.at(coord(2, 1)))
    sprite.set_right_animation(anim.at(coord(2, 1), rotation=90))
    sprite.set_down_animation(anim.at(coord(2, 1), rotation=180))
    sprite.set_left_animation(anim.at(coord(2, 1), rotation=270))
    return sprite

def trail(player: Player) -> Sprite:
    rotate: float|None = None
    pos: coord
    match player.active_dir:
        case DIRECTION.RIGHT:
            rotate = 90
            pos = player.position.clone_by(-8, 0, DIRECTION.LEFT)
        case DIRECTION.DOWN:
            rotate = 180
            pos = player.position.clone_by(0, -8, DIRECTION.UP)
        case DIRECTION.LEFT:
            rotate = 270
            pos = player.position.clone_by(8, 0, DIRECTION.RIGHT)
        case _:
            pos = player.position.clone_by(0, 8, DIRECTION.DOWN)

    sprite = Sprite("trail", coord(1,2))
    sprite.set_rotation(rotate)
    sprite.add_animation("loop", Animation(coord(1,2), 4, loop=True, rotation=rotate))
    sprite.activate_animation("loop")
    sprite.set_position(pos)
    return sprite

def shockwave(player: Player) -> Sprite:
    rotate: float|None = None
    pos: coord
    match player.active_dir:
        case DIRECTION.RIGHT:
            rotate = 90
            pos = player.position.clone_by(0, 0, DIRECTION.RIGHT)
        case DIRECTION.DOWN:
            rotate = 180
            pos = player.position.clone_by(-8, 8, DIRECTION.DOWN)
        case DIRECTION.LEFT:
            rotate = 270
            pos = player.position.clone_by(-16, 0, DIRECTION.LEFT)
        case _:
            pos = player.position.clone_by(-8, -8, DIRECTION.UP)

    sprite = Sprite("shockwave", coord(1,9), cols=3, rows=1)
    sprite.set_rotation(rotate)
    sprite.add_animation("loop", Animation(coord(1,9), 4, loop=True, rotation=rotate))
    sprite.activate_animation("loop")
    sprite.set_position(pos)
    return sprite


def house() -> Sprite:
    sprite = Sprite("house", coord(1,3), rows=4, cols=4)
    sprite.add_animation("loop", Animation(coord(1,3), 4, loop=True, fps=4))
    sprite.activate_animation("loop")
    return sprite

def spinner() -> MovableSprite:
    sprite = MovableSprite("spinner", coord(6,1))
    
    anim = AnimationFactory(frames=4)

    # anim = Animation(coord(6, 1), 4)
    sprite.set_up_animation(anim.at(coord(6,1)))
    sprite.set_down_animation(anim.at(coord(6,1)))
    sprite.set_left_animation(anim.at(coord(6,1)))
    sprite.set_right_animation(anim.at(coord(6,1)))

    # See nasty bug in Animation._update_frame()
    sprite.add_animation("die", Animation(coord(6,2), 2, loop=False))
    sprite.add_animation("kill", Animation(coord(8,2), 2, loop=False))

    return sprite

def tree() -> Sprite:
    return Sprite("tree", tree_frames.select_one(), rows=2, cols=2)