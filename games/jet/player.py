from pyke_pyxel import DIRECTION, area, COLOURS
from pyke_pyxel.rpg.enemy import Enemy
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import Sprite
from pyke_pyxel.rpg import RPGGame, Player

import sprites

class _Player:

    def __init__(self) -> None:
        self.player: Player
        self.game: RPGGame
        self.trail: Sprite|None = None
        self.shockwave: Sprite|None = None

        self.active_dir: DIRECTION|None = None
        self.second_dir: DIRECTION|None = None

        self.house_damage = 0
        self.can_heal = 0

    def start(self, house: Sprite, game: RPGGame):
        self.house = house
        self.game = game
        self.player = game.player

    # Enemies
    def check_enemies_to_attack(self):
        pos = self.player.position
        c = pos.col
        r = pos.row

        match self.player.active_dir:
            case DIRECTION.RIGHT:
                c += 1
                attack_area = area.with_map_bounds(c, c, r-1, r+1, pos.size)
            case DIRECTION.LEFT:
                c -= 1
                attack_area = area.with_map_bounds(c, c, r-1, r+1, pos.size)
            case DIRECTION.DOWN:
                r += 1
                attack_area = area.with_map_bounds(c-1, c+1, r, r, pos.size)
            case _: # Up
                r -= 1
                attack_area = area.with_map_bounds(c-1, c+1, r, r, pos.size)

        # print(f"PLAYER pos:{self.player.position} dir:{self.player.active_dir} attack:{attack_area}")

        to_remove: list[Enemy] = [] 

        def _remove_enemy(sprite_id: int):
            for e in to_remove:
                if e.sprite_id == sprite_id:
                    e.remove()

        enemies = self.game.enemies_at(attack_area)
        for e in enemies:
            to_remove.append(e)
            
            # e.stop_moving()
            # We specifically do not call e.stop_moving()
            # so that the splatter does not cover up the "die" animation
            # is there a better solution?
            e.sprite.activate_animation("die", on_animation_end=_remove_enemy)
            self.game.fx.splatter(COLOURS.PINK, e.position)

            self.can_heal = 60 * 2 # 2 seconds
            self.player.sprite.replace_colour(COLOURS.WHITE, COLOURS.GREEN)
            


    def damage_house(self):
        self.house_damage += 1
        match self.house_damage:
            case 1:
                self.house.replace_colour(COLOURS.WHITE, COLOURS.PINK)
            case 2:
                self.house.replace_colour(COLOURS.WHITE, COLOURS.RED)
            case 3:
                self.house.replace_colour(COLOURS.WHITE, COLOURS.PURPLE)
            case _:
                print("DEAD!!")
        self.game.fx.scale_in_out(self.house, to_scale=1.2, duration=0.1)

    def heal_house(self):
        if self.can_heal == 0:
            return

        match self.house_damage:
            case 0:
                return
            case 1:
                self.house_damage = 0
                self.house.reset_colour_replacements()
            case 2:
                self.house_damage = 1
                self.house.replace_colour(COLOURS.WHITE, COLOURS.PINK)
            case 3:
                self.house_damage = 2
                self.house.replace_colour(COLOURS.WHITE, COLOURS.RED)
            case _:
                self.house_damage = 3

        self.can_heal = 0
        self.game.fx.scale_in_out(self.house, to_scale=1.2, duration=0.1)
        
    def update(self):
        player = self.player
        sprite = player.sprite

        # Movement
        if self.active_dir:
            if not player.active_dir == self.active_dir:
                self._start_movement()
        else:
            self.stop_movement()

        # Heal counter
        if self.can_heal > 0:
            self.can_heal -= 1
        else:
            sprite.reset_colour_replacements()

    # Movement

    def check_input(self, key: int, direction: DIRECTION):
        keyboard = self.game.keyboard

        if self.active_dir: # Moving
            if self.active_dir == direction: # Check for release
                if not keyboard.is_down(key):
                    # print(f"RELEASED {direction}")
                    self.active_dir = self.second_dir
                    self.second_dir = None
            elif keyboard.was_pressed(key): # Check for press
                # print(f"SWITCHED to {direction} from {self.active_dir}")
                self.second_dir = self.active_dir
                self.active_dir = direction
        else: # Not moving
            if keyboard.was_pressed(key):
                # print(f"PRESSED {direction}")
                self.active_dir = direction

    def stop_movement(self):
        self.player.stop_moving()

        if trail := self.trail:
            self.player.sprite.unlink_sprite(trail)
            Signals.send_remove_sprite(trail)
            self.trail = None

        if shockwave := self.shockwave:
            self.player.sprite.unlink_sprite(shockwave)
            Signals.send_remove_sprite(shockwave)
            self.shockwave = None

        self.active_dir = None
        self.second_dir = None

    def _start_movement(self):
        player = self.player
        player.start_moving(self.active_dir) # type: ignore warning
        if trail:= self.trail:
            Signals.send_remove_sprite(trail)
        if shockwave:= self.shockwave:
            Signals.send_remove_sprite(shockwave)
        
        trail = sprites.trail(player)
        Signals.send_add_sprite(trail)
        player.sprite.link_sprite(trail)

        shockwave = sprites.shockwave(player)
        Signals.send_add_sprite(shockwave)
        player.sprite.link_sprite(shockwave)

        self.trail = trail
        self.shockwave = shockwave

    @property
    def is_moving(self) -> bool:
        return self.active_dir is not None

PLAYER = _Player()