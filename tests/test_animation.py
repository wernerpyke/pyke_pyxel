import pytest
from unittest.mock import MagicMock

from pyke_pyxel.sprite._anim import Animation, AnimationFactory
from pyke_pyxel._types import coord, GameSettings


class TestAnimationCreation:
    """Tests for Animation creation and initialization."""

    def test_basic_creation(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)

        assert animation is not None
        assert animation._frames == 4
        assert animation._loop is True

    def test_creation_with_loop_false(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4, loop=False)

        assert animation._loop is False

    def test_creation_with_flip(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4, flip=True)

        assert animation.flip is True

    def test_creation_with_rotation(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4, rotation=90.0)

        assert animation.rotation == 90.0

    def test_creation_with_fps(self, reset_game_settings):
        reset_game_settings.fps.animation = 30
        start_frame = coord(1, 1)

        animation = Animation(start_frame, frames=4, fps=15)

        # 30 / 15 = 2, so skip every 2nd frame update
        assert animation._skip_animation_frame_update == 2

    def test_creation_with_fps_equal_to_animation_fps(self, reset_game_settings):
        reset_game_settings.fps.animation = 30
        start_frame = coord(1, 1)

        animation = Animation(start_frame, frames=4, fps=30)

        # 30 / 30 = 1
        assert animation._skip_animation_frame_update == 1

    def test_creation_with_fps_too_high_raises(self, reset_game_settings):
        reset_game_settings.fps.animation = 30
        start_frame = coord(1, 1)

        with pytest.raises(ValueError) as exc_info:
            Animation(start_frame, frames=4, fps=60)

        assert "fps cannot be > 30" in str(exc_info.value)

    def test_initial_frame_index_is_zero(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)

        assert animation._current_frame_index == 0


class TestAnimationSetCurrentFrame:
    """Tests for set_current_frame method."""

    def test_set_current_frame_valid(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)

        animation.set_current_frame(2)

        assert animation._current_frame_index == 2

    def test_set_current_frame_to_last_frame(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)

        animation.set_current_frame(3)  # 0-indexed, so 3 is last for 4 frames

        assert animation._current_frame_index == 3

    def test_set_current_frame_to_zero(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)

        animation.set_current_frame(2)
        animation.set_current_frame(0)

        assert animation._current_frame_index == 0

    def test_set_current_frame_out_of_range_raises(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)

        with pytest.raises(ValueError) as exc_info:
            animation.set_current_frame(4)  # Max is 3

        assert "frame_index cannot be > 3" in str(exc_info.value)


class TestAnimationActivate:
    """Tests for _activate method."""

    def test_activate_sets_sprite_id(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)

        animation._activate(sprite_id=42)

        assert animation._sprite_id == 42

    def test_activate_sets_callback(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)
        callback = MagicMock()

        animation._activate(sprite_id=1, on_animation_end=callback)

        assert animation._on_animation_end == callback

    def test_activate_resets_frame_index(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)

        animation._current_frame_index = 3
        animation._activate(sprite_id=1)

        assert animation._current_frame_index == 0

    def test_activate_resets_trigger_flag(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)

        animation._trigger_on_animation_end = True
        animation._activate(sprite_id=1)

        assert animation._trigger_on_animation_end is False

    def test_activate_calculates_current_col(self):
        start_frame = coord(5, 3)
        animation = Animation(start_frame, frames=4)
        animation._cols = 2  # 2 tiles wide

        animation._activate(sprite_id=1)

        # current_col = start_col + (current_frame_index * cols)
        # = 5 + (0 * 2) = 5
        assert animation._current_col == 5


class TestAnimationUpdateFrame:
    """Tests for _update_frame method."""

    def test_update_frame_advances_frame(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)
        animation._cols = 1
        animation._activate(sprite_id=1)

        frame1 = animation._update_frame()
        assert animation._current_frame_index == 1

        frame2 = animation._update_frame()
        assert animation._current_frame_index == 2

    def test_update_frame_returns_coord(self):
        start_frame = coord(5, 3)
        animation = Animation(start_frame, frames=4)
        animation._cols = 1
        animation._activate(sprite_id=1)

        frame = animation._update_frame()

        assert isinstance(frame, coord)
        assert frame._row == 3  # Row stays same

    def test_update_frame_looping_wraps_around(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=3, loop=True)
        animation._cols = 1
        animation._activate(sprite_id=1)

        animation._update_frame()  # frame 0 -> 1
        animation._update_frame()  # frame 1 -> 2
        animation._update_frame()  # frame 2 -> 0 (wrap)

        assert animation._current_frame_index == 0

    def test_update_frame_non_looping_stays_at_end(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=3, loop=False)
        animation._cols = 1
        animation._activate(sprite_id=1)

        animation._update_frame()  # frame 0 -> 1
        animation._update_frame()  # frame 1 -> 2
        animation._update_frame()  # frame 2 stays, trigger set

        assert animation._current_frame_index == 2
        assert animation._trigger_on_animation_end is True

    def test_update_frame_calls_callback_on_end(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=2, loop=False)
        animation._cols = 1
        callback = MagicMock()
        animation._activate(sprite_id=42, on_animation_end=callback)

        animation._update_frame()  # frame 0 -> 1
        animation._update_frame()  # frame 1 stays, trigger set

        # Callback is called on the NEXT update after trigger is set
        animation._update_frame()

        callback.assert_called_once_with(42)

    def test_update_frame_callback_only_called_once(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=2, loop=False)
        animation._cols = 1
        callback = MagicMock()
        animation._activate(sprite_id=42, on_animation_end=callback)

        animation._update_frame()
        animation._update_frame()
        animation._update_frame()  # Callback called
        animation._update_frame()  # Should not be called again

        callback.assert_called_once()

    def test_update_frame_with_multi_col_sprite(self):
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4)
        animation._cols = 2  # 2 tiles wide
        animation._activate(sprite_id=1)

        frame0 = animation._update_frame()
        # col = 1 + (0 * 2) = 1
        assert animation._current_col == 1

        frame1 = animation._update_frame()
        # col = 1 + (1 * 2) = 3
        assert animation._current_col == 3

        frame2 = animation._update_frame()
        # col = 1 + (2 * 2) = 5
        assert animation._current_col == 5


class TestAnimationFPSSkipping:
    """Tests for FPS-based frame skipping."""

    def test_fps_skipping_skips_updates(self, reset_game_settings):
        reset_game_settings.fps.animation = 30
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=4, fps=15)  # Skip every 2nd
        animation._cols = 1
        animation._activate(sprite_id=1)

        # FPS skipping logic: counter < skip_value means skip
        # When fps=15 and animation fps=30, skip=2
        # Update 1: counter=0 < 2, increment to 1, skip (no advance)
        # Update 2: counter=1 < 2, increment to 2, skip (no advance)
        # Update 3: counter=2 >= 2, reset to 0, advance frame

        animation._update_frame()  # counter -> 1, skip
        assert animation._current_frame_index == 0

        animation._update_frame()  # counter -> 2, skip
        assert animation._current_frame_index == 0

        animation._update_frame()  # counter reset, advance
        assert animation._current_frame_index == 1

    def test_fps_skipping_counter_resets(self, reset_game_settings):
        reset_game_settings.fps.animation = 30
        start_frame = coord(1, 1)
        animation = Animation(start_frame, frames=10, fps=10)  # Skip every 3rd
        animation._cols = 1
        animation._activate(sprite_id=1)

        # When fps=10 and animation fps=30, skip=3
        # Takes 4 updates to advance one frame (3 skips + 1 advance)
        animation._update_frame()  # counter = 1, skip
        animation._update_frame()  # counter = 2, skip
        animation._update_frame()  # counter = 3, skip
        animation._update_frame()  # counter reset to 0, advance
        assert animation._current_frame_index == 1

        animation._update_frame()  # counter = 1, skip
        animation._update_frame()  # counter = 2, skip
        animation._update_frame()  # counter = 3, skip
        animation._update_frame()  # advance
        assert animation._current_frame_index == 2


class TestAnimationFactoryCreation:
    """Tests for AnimationFactory creation."""

    def test_basic_creation(self):
        factory = AnimationFactory(frames=4)

        assert factory is not None
        assert factory._frames == 4

    def test_creation_with_fps(self):
        factory = AnimationFactory(frames=4, fps=15)

        assert factory._fps == 15

    def test_creation_with_loop(self):
        factory = AnimationFactory(frames=4, loop=False)

        assert factory._loop is False


class TestAnimationFactoryAt:
    """Tests for AnimationFactory.at() method."""

    def test_at_creates_animation(self):
        factory = AnimationFactory(frames=4)
        position = coord(1, 1)

        animation = factory.at(position)

        assert isinstance(animation, Animation)
        assert animation._frames == 4
        assert animation._start_frame == position

    def test_at_passes_fps(self, reset_game_settings):
        reset_game_settings.fps.animation = 30
        factory = AnimationFactory(frames=4, fps=15)
        position = coord(1, 1)

        animation = factory.at(position)

        assert animation._skip_animation_frame_update == 2

    def test_at_with_flip(self):
        factory = AnimationFactory(frames=4)
        position = coord(1, 1)

        animation = factory.at(position, flip=True)

        assert animation.flip is True

    def test_at_with_rotation(self):
        factory = AnimationFactory(frames=4)
        position = coord(1, 1)

        animation = factory.at(position, rotation=45.0)

        assert animation.rotation == 45.0

    def test_at_uses_factory_loop_by_default(self):
        factory = AnimationFactory(frames=4, loop=False)
        position = coord(1, 1)

        animation = factory.at(position)

        assert animation._loop is False

    def test_at_overrides_factory_loop(self):
        factory = AnimationFactory(frames=4, loop=False)
        position = coord(1, 1)

        animation = factory.at(position, loop=True)

        assert animation._loop is True

    def test_at_with_loop_none_uses_factory(self):
        factory = AnimationFactory(frames=4, loop=True)
        position = coord(1, 1)

        animation = factory.at(position, loop=None)

        assert animation._loop is True


class TestAnimationFactoryMultipleAnimations:
    """Tests for creating multiple animations with factory."""

    def test_factory_creates_independent_animations(self):
        factory = AnimationFactory(frames=4)

        anim1 = factory.at(coord(1, 1))
        anim2 = factory.at(coord(5, 5))

        # Modify one, shouldn't affect the other
        anim1._current_frame_index = 3

        assert anim1._current_frame_index == 3
        assert anim2._current_frame_index == 0

    def test_factory_creates_animations_with_different_positions(self):
        factory = AnimationFactory(frames=4)

        anim1 = factory.at(coord(1, 1))
        anim2 = factory.at(coord(5, 5))

        assert anim1._start_frame._col == 1
        assert anim2._start_frame._col == 5

    def test_factory_creates_animations_with_different_flips(self):
        factory = AnimationFactory(frames=4)

        anim_normal = factory.at(coord(1, 1), flip=False)
        anim_flipped = factory.at(coord(1, 1), flip=True)

        assert anim_normal.flip is False
        assert anim_flipped.flip is True
