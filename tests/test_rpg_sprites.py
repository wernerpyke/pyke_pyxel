import pytest
from unittest.mock import patch, MagicMock

from pyke_pyxel._types import coord
from pyke_pyxel.sprite._rpg_sprites import (
    OpenableSprite, MovableSprite,
    OPEN, CLOSED, CLOSING, OPENING
)
from pyke_pyxel.sprite._anim import Animation


class TestStatusConstants:
    """Tests for status constants."""

    def test_status_values_are_distinct(self):
        statuses = [OPEN, CLOSED, CLOSING, OPENING]
        assert len(statuses) == len(set(statuses))

    def test_status_values(self):
        assert OPEN == 0
        assert CLOSED == 1
        assert CLOSING == 2
        assert OPENING == 3


class TestOpenableSpriteCreation:
    """Tests for OpenableSprite creation and initialization."""

    def test_basic_creation(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)
        assert sprite is not None
        assert sprite.name == "door"

    def test_starts_in_open_state(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)
        assert sprite.is_open
        assert not sprite.is_closed

    def test_initial_frame_is_open_frame(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)
        assert sprite.active_frame == open_frame


class TestOpenableSpriteClose:
    """Tests for OpenableSprite.close() method."""

    def test_close_changes_state(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)

        sprite.close()

        assert sprite.is_closed
        assert not sprite.is_open

    def test_close_updates_frame(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)

        sprite.close()

        assert sprite.active_frame == closed_frame

    def test_close_when_already_closed_is_idempotent(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)

        sprite.close()
        sprite.close()  # Close again

        assert sprite.is_closed
        assert sprite.active_frame == closed_frame


class TestOpenableSpriteOpen:
    """Tests for OpenableSprite.open() method."""

    def test_open_changes_state(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)

        sprite.close()
        sprite.open()

        assert sprite.is_open
        assert not sprite.is_closed

    def test_open_updates_frame(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)

        sprite.close()
        sprite.open()

        assert sprite.active_frame == open_frame

    def test_open_when_already_open_is_idempotent(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)

        sprite.open()  # Already open

        assert sprite.is_open
        assert sprite.active_frame == open_frame


class TestOpenableSpriteStateTransitions:
    """Tests for state transitions."""

    def test_toggle_open_close(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)

        # Start open
        assert sprite.is_open

        # Close
        sprite.close()
        assert sprite.is_closed

        # Open again
        sprite.open()
        assert sprite.is_open

        # Close again
        sprite.close()
        assert sprite.is_closed

    def test_frames_update_with_state(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("chest", open_frame, closed_frame)

        assert sprite.active_frame == open_frame

        sprite.close()
        assert sprite.active_frame == closed_frame

        sprite.open()
        assert sprite.active_frame == open_frame


class TestOpenableSpriteInheritance:
    """Tests for OpenableSprite inheriting from Sprite."""

    def test_inherits_sprite_properties(self):
        open_frame = coord(1, 1)
        closed_frame = coord(2, 1)
        sprite = OpenableSprite("door", open_frame, closed_frame)

        # Should have Sprite properties
        assert hasattr(sprite, 'name')
        assert hasattr(sprite, 'default_frame')
        assert hasattr(sprite, 'animations')
        assert hasattr(sprite, 'add_animation')


class TestMovableSpriteCreation:
    """Tests for MovableSprite creation and initialization."""

    def test_basic_creation(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame)
        assert sprite is not None
        assert sprite.name == "player"

    def test_creation_with_cols_rows(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame, cols=2, rows=2)
        assert sprite.cols == 2
        assert sprite.rows == 2

    def test_creation_with_resource_image_index(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame, resource_image_index=1)
        assert sprite._resource_image_index == 1


class TestMovableSpriteAnimationSetters:
    """Tests for MovableSprite animation setter methods."""

    def test_set_up_animation(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame)
        animation = Animation(coord(1, 2), frames=4)

        sprite.set_up_animation(animation)

        assert "up" in sprite.animations
        assert sprite.animations["up"] == animation

    def test_set_down_animation(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame)
        animation = Animation(coord(1, 3), frames=4)

        sprite.set_down_animation(animation)

        assert "down" in sprite.animations
        assert sprite.animations["down"] == animation

    def test_set_left_animation(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame)
        animation = Animation(coord(1, 4), frames=4)

        sprite.set_left_animation(animation)

        assert "left" in sprite.animations
        assert sprite.animations["left"] == animation

    def test_set_right_animation(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame)
        animation = Animation(coord(1, 5), frames=4)

        sprite.set_right_animation(animation)

        assert "right" in sprite.animations
        assert sprite.animations["right"] == animation

    def test_set_all_directional_animations(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame)

        sprite.set_up_animation(Animation(coord(1, 2), frames=4))
        sprite.set_down_animation(Animation(coord(1, 3), frames=4))
        sprite.set_left_animation(Animation(coord(1, 4), frames=4))
        sprite.set_right_animation(Animation(coord(1, 5), frames=4))

        assert len(sprite.animations) == 4
        assert "up" in sprite.animations
        assert "down" in sprite.animations
        assert "left" in sprite.animations
        assert "right" in sprite.animations


class TestMovableSpriteAnimationReplacement:
    """Tests for replacing animations."""

    def test_setting_animation_twice_replaces(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame)

        animation1 = Animation(coord(1, 2), frames=2)
        animation2 = Animation(coord(5, 2), frames=6)

        sprite.set_up_animation(animation1)
        sprite.set_up_animation(animation2)

        assert sprite.animations["up"] == animation2
        assert sprite.animations["up"]._frames == 6


class TestMovableSpriteInheritance:
    """Tests for MovableSprite inheriting from Sprite."""

    def test_inherits_sprite_properties(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame)

        # Should have Sprite properties
        assert hasattr(sprite, 'name')
        assert hasattr(sprite, 'default_frame')
        assert hasattr(sprite, 'animations')
        assert hasattr(sprite, 'active_frame')

    def test_can_use_base_add_animation(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame)
        animation = Animation(coord(1, 6), frames=8)

        # Use base class method directly
        sprite.add_animation("custom", animation)

        assert "custom" in sprite.animations

    def test_can_activate_directional_animation(self):
        default_frame = coord(1, 1)
        sprite = MovableSprite("player", default_frame)
        sprite._id = 1  # Set an ID for activation

        animation = Animation(coord(1, 2), frames=4)
        sprite.set_up_animation(animation)

        sprite.activate_animation("up")

        assert sprite.is_animating
        assert sprite.active_animation_is("up")
