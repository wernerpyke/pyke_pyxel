import pytest
import math
from unittest.mock import MagicMock, patch

from pyke_pyxel.sprite._sprite import Sprite
from pyke_pyxel.sprite._anim import Animation
from pyke_pyxel._types import coord, GameSettings


class TestSpriteCreation:
    """Tests for Sprite creation and initialization."""

    def test_basic_creation(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        assert sprite is not None
        assert sprite.name == "player"
        assert sprite.default_frame == default_frame

    def test_creation_with_cols_rows(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame, cols=2, rows=2)

        assert sprite.cols == 2
        assert sprite.rows == 2

    def test_creation_with_resource_image_index(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame, resource_image_index=1)

        assert sprite._resource_image_index == 1

    def test_width_height_calculated_from_tile_size(self, reset_game_settings):
        reset_game_settings.size.tile = 8
        default_frame = coord(1, 1)

        sprite = Sprite("player", default_frame, cols=2, rows=3)

        assert sprite.width == 16  # 2 * 8
        assert sprite.height == 24  # 3 * 8

    def test_active_frame_starts_as_default(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        assert sprite.active_frame == default_frame

    def test_animations_dict_starts_empty(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        assert sprite.animations == {}


class TestSpritePosition:
    """Tests for position management."""

    def test_set_position(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        position = coord(5, 5)

        sprite.set_position(position)

        assert sprite.position == position

    def test_position_property(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        position = coord(5, 5)
        sprite._position = position

        assert sprite.position == position

    def test_set_position_updates_linked_sprites(self, reset_game_settings):
        default_frame = coord(1, 1)
        parent = Sprite("parent", default_frame)
        child = Sprite("child", default_frame)

        parent.set_position(coord.with_xy(10, 10))
        child.set_position(coord.with_xy(15, 10))

        parent.link_sprite(child)

        # Move parent by 5 pixels right
        parent.set_position(coord.with_xy(15, 10))

        # Child should have moved by the same diff
        assert child.position.x == 20


class TestSpriteRotation:
    """Tests for rotation management."""

    def test_set_rotation(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite.set_rotation(45.0)

        assert sprite._rotation == 45.0

    def test_set_rotation_normalizes_over_360(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite.set_rotation(450.0)

        assert sprite._rotation == 90.0  # 450 % 360

    def test_set_rotation_none_clears(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite.set_rotation(45.0)
        sprite.set_rotation(None)

        assert sprite._rotation is None

    def test_set_rotation_zero_clears(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite.set_rotation(45.0)
        sprite.set_rotation(0.0)

        assert sprite._rotation is None

    def test_rotation_property_returns_sprite_rotation(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite.set_rotation(90.0)

        assert sprite.rotation == 90.0

    def test_rotation_property_returns_animation_rotation(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._id = 1

        animation = Animation(coord(1, 2), frames=4, rotation=45.0)
        sprite.add_animation("rotate", animation)
        sprite.activate_animation("rotate")

        assert sprite.rotation == 45.0

    def test_rotation_animation_takes_precedence(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._id = 1

        sprite.set_rotation(90.0)
        animation = Animation(coord(1, 2), frames=4, rotation=45.0)
        sprite.add_animation("rotate", animation)
        sprite.activate_animation("rotate")

        # Animation rotation should take precedence
        assert sprite.rotation == 45.0


class TestSpriteScale:
    """Tests for scale management."""

    def test_set_scale(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite.set_scale(2.0)

        assert sprite._scale == 2.0

    def test_set_scale_one_clears(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite.set_scale(2.0)
        sprite.set_scale(1.0)

        assert sprite._scale is None

    def test_scale_property(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite.set_scale(1.5)

        assert sprite.scale == 1.5


class TestSpriteAnimations:
    """Tests for animation management."""

    def test_add_animation(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        animation = Animation(coord(1, 2), frames=4)

        sprite.add_animation("walk", animation)

        assert "walk" in sprite.animations
        assert sprite.animations["walk"] == animation

    def test_add_animation_sets_name(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        animation = Animation(coord(1, 2), frames=4)

        sprite.add_animation("walk", animation)

        assert animation._name == "walk"

    def test_add_animation_sets_cols(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame, cols=2)
        animation = Animation(coord(1, 2), frames=4)

        sprite.add_animation("walk", animation)

        assert animation._cols == 2

    def test_activate_animation(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._id = 1
        animation = Animation(coord(1, 2), frames=4)
        sprite.add_animation("walk", animation)

        sprite.activate_animation("walk")

        assert sprite._animation == animation
        assert sprite.is_animating is True

    def test_activate_animation_with_callback(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._id = 1
        animation = Animation(coord(1, 2), frames=4)
        sprite.add_animation("walk", animation)
        callback = MagicMock()

        sprite.activate_animation("walk", on_animation_end=callback)

        assert animation._on_animation_end == callback

    def test_activate_animation_same_animation_is_noop(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._id = 1
        animation = Animation(coord(1, 2), frames=4)
        sprite.add_animation("walk", animation)

        sprite.activate_animation("walk")
        animation._current_frame_index = 2

        sprite.activate_animation("walk")  # Should not reset

        assert animation._current_frame_index == 2  # Not reset

    def test_deactivate_animations(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._id = 1
        animation = Animation(coord(1, 2), frames=4)
        sprite.add_animation("walk", animation)

        sprite.activate_animation("walk")
        sprite.deactivate_animations()

        assert sprite._animation is None
        assert sprite.is_animating is False

    def test_active_animation_is(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._id = 1
        animation = Animation(coord(1, 2), frames=4)
        sprite.add_animation("walk", animation)

        sprite.activate_animation("walk")

        assert sprite.active_animation_is("walk") is True
        assert sprite.active_animation_is("run") is False

    def test_is_animating_false_when_no_animation(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        assert sprite.is_animating is False


class TestSpriteLinkedSprites:
    """Tests for linked sprite management."""

    def test_link_sprite(self, reset_game_settings):
        default_frame = coord(1, 1)
        parent = Sprite("parent", default_frame)
        child = Sprite("child", default_frame)

        parent.link_sprite(child)

        assert child in parent._linked_sprites

    def test_link_multiple_sprites(self, reset_game_settings):
        default_frame = coord(1, 1)
        parent = Sprite("parent", default_frame)
        child1 = Sprite("child1", default_frame)
        child2 = Sprite("child2", default_frame)

        parent.link_sprite(child1)
        parent.link_sprite(child2)

        assert len(parent._linked_sprites) == 2
        assert child1 in parent._linked_sprites
        assert child2 in parent._linked_sprites

    def test_unlink_sprite(self, reset_game_settings):
        default_frame = coord(1, 1)
        parent = Sprite("parent", default_frame)
        child = Sprite("child", default_frame)

        parent.link_sprite(child)
        parent.unlink_sprite(child)

        assert child not in parent._linked_sprites

    def test_unlink_sprite_not_linked_does_nothing(self, reset_game_settings):
        default_frame = coord(1, 1)
        parent = Sprite("parent", default_frame)
        parent._id = 1
        child = Sprite("child", default_frame)
        child._id = 2  # Unique ID needed since __eq__ compares by ID

        parent.link_sprite(child)
        other = Sprite("other", default_frame)
        other._id = 3  # Different ID

        parent.unlink_sprite(other)  # Should not raise

        assert child in parent._linked_sprites

    def test_unlink_sprite_no_linked_sprites_does_nothing(self, reset_game_settings):
        default_frame = coord(1, 1)
        parent = Sprite("parent", default_frame)
        child = Sprite("child", default_frame)

        parent.unlink_sprite(child)  # Should not raise


class TestSpriteColourReplacement:
    """Tests for colour replacement."""

    def test_replace_colour(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite.replace_colour(7, 8)

        assert sprite._replace_colour == (7, 8)

    def test_reset_colour_replacements(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite.replace_colour(7, 8)
        sprite.reset_colour_replacements()

        assert sprite._replace_colour is None


class TestSpriteEquality:
    """Tests for sprite equality comparison."""

    def test_sprites_equal_by_id(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite1 = Sprite("player", default_frame)
        sprite1._id = 1
        sprite2 = Sprite("player", default_frame)
        sprite2._id = 1

        assert sprite1 == sprite2

    def test_sprites_not_equal_different_ids(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite1 = Sprite("player", default_frame)
        sprite1._id = 1
        sprite2 = Sprite("player", default_frame)
        sprite2._id = 2

        assert sprite1 != sprite2

    def test_sprite_not_equal_to_non_sprite(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._id = 1

        assert sprite != "not a sprite"
        assert sprite != 1
        assert sprite != None


class TestSpriteRotatedPosition:
    """Tests for rotated_position method."""

    def test_rotated_position_no_rotation(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        position = coord.with_xy(10, 10)
        sprite._position = position

        result = sprite.rotated_position()

        assert result.x == 10
        assert result.y == 10

    def test_rotated_position_90_degrees(self, reset_game_settings):
        reset_game_settings.size.tile = 8
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame, cols=1, rows=1)
        position = coord.with_xy(0, 0)
        sprite._position = position
        sprite.set_rotation(90.0)

        result = sprite.rotated_position()

        # For a 8x8 sprite at (0,0), center is (4,4)
        # Original top-left (0,0) rotated 90 degrees around (4,4)
        # x_new = 4 + (0-4)*cos(90) - (0-4)*sin(90) = 4 + 0 - (-4) = 8
        # y_new = 4 + (0-4)*sin(90) + (0-4)*cos(90) = 4 + (-4) + 0 = 0
        assert result.x == 8
        assert result.y == 0

    def test_rotated_position_180_degrees(self, reset_game_settings):
        reset_game_settings.size.tile = 8
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame, cols=1, rows=1)
        position = coord.with_xy(0, 0)
        sprite._position = position
        sprite.set_rotation(180.0)

        result = sprite.rotated_position()

        # For a 8x8 sprite at (0,0), center is (4,4)
        # Original top-left (0,0) rotated 180 degrees around (4,4)
        # x_new = 4 + (0-4)*cos(180) - (0-4)*sin(180) = 4 + 4 - 0 = 8
        # y_new = 4 + (0-4)*sin(180) + (0-4)*cos(180) = 4 + 0 + 4 = 8
        assert result.x == 8
        assert result.y == 8

    def test_rotated_position_uses_animation_rotation(self, reset_game_settings):
        reset_game_settings.size.tile = 8
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame, cols=1, rows=1)
        sprite._id = 1
        position = coord.with_xy(0, 0)
        sprite._position = position

        animation = Animation(coord(1, 2), frames=4, rotation=180.0)
        sprite.add_animation("spin", animation)
        sprite.activate_animation("spin")

        result = sprite.rotated_position()

        assert result.x == 8
        assert result.y == 8


class TestSpriteUpdateFrame:
    """Tests for _update_frame method."""

    def test_update_frame_no_animation(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)

        sprite._update_frame()

        assert sprite.active_frame == default_frame

    def test_update_frame_with_animation(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._id = 1
        animation = Animation(coord(5, 1), frames=4)
        sprite.add_animation("walk", animation)
        sprite.activate_animation("walk")

        sprite._update_frame()

        # Frame should be updated from animation
        assert sprite.active_frame._row == 1  # Same row

    def test_update_frame_animation_ends(self, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._id = 1
        animation = Animation(coord(5, 1), frames=2, loop=False)
        sprite.add_animation("once", animation)
        sprite.activate_animation("once")

        # Advance through all frames
        sprite._update_frame()  # frame 0 -> 1
        sprite._update_frame()  # frame 1 -> end trigger

        # On next update after trigger, callback would fire
        # But animation should still provide frame until callback fires


class TestSpriteDraw:
    """Tests for _draw method (with mocked pyxel)."""

    @patch('pyke_pyxel.sprite._sprite.pyxel')
    def test_draw_calls_blt(self, mock_pyxel, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._position = coord.with_xy(10, 20)

        sprite._draw(reset_game_settings)

        mock_pyxel.blt.assert_called_once()

    @patch('pyke_pyxel.sprite._sprite.pyxel')
    def test_draw_with_colour_replacement(self, mock_pyxel, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame)
        sprite._position = coord.with_xy(10, 20)
        sprite.replace_colour(7, 8)

        sprite._draw(reset_game_settings)

        # Should call pal before and after blt
        assert mock_pyxel.pal.call_count == 2

    @patch('pyke_pyxel.sprite._sprite.pyxel')
    def test_draw_with_flip_animation(self, mock_pyxel, reset_game_settings):
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame, cols=2)
        sprite._id = 1
        sprite._position = coord.with_xy(10, 20)
        animation = Animation(coord(5, 1), frames=4, flip=True)
        sprite.add_animation("walk", animation)
        sprite.activate_animation("walk")

        sprite._draw(reset_game_settings)

        # Width should be negative when flipped
        call_kwargs = mock_pyxel.blt.call_args.kwargs
        assert call_kwargs['w'] < 0


class TestSpriteProperties:
    """Tests for sprite properties."""

    def test_width_property(self, reset_game_settings):
        reset_game_settings.size.tile = 8
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame, cols=3)

        assert sprite.width == 24

    def test_height_property(self, reset_game_settings):
        reset_game_settings.size.tile = 8
        default_frame = coord(1, 1)
        sprite = Sprite("player", default_frame, rows=2)

        assert sprite.height == 16
