import pytest
from unittest.mock import patch, MagicMock

from pyke_pyxel.timer import Timer
from pyke_pyxel.signals import Signals


class TestTimerCreation:
    """Tests for timer creation methods."""

    def test_after_creates_timer(self):
        timer = Timer()
        timer.after(1.0, "test_signal")
        assert timer.has_timer("test_signal")

    def test_every_creates_timer(self):
        timer = Timer()
        timer.every(1.0, "test_signal")
        assert timer.has_timer("test_signal")

    def test_after_with_sender(self):
        timer = Timer()
        sender = {"key": "value"}
        timer.after(1.0, "test_signal", sender)
        assert timer.has_timer("test_signal")

    def test_has_timer_returns_false_for_nonexistent(self):
        timer = Timer()
        assert not timer.has_timer("nonexistent")

    def test_after_replaces_existing_timer(self):
        timer = Timer()
        timer.after(5.0, "test_signal")
        timer.after(1.0, "test_signal")  # Replace with shorter time
        # Timer should still exist (replaced, not duplicated)
        assert timer.has_timer("test_signal")
        assert len(timer._timers) == 1


class TestTimerCancel:
    """Tests for timer cancellation."""

    def test_cancel_marks_timer_for_removal(self):
        timer = Timer()
        timer.after(1.0, "test_signal")
        timer.cancel("test_signal")
        # Timer marked for removal but not yet removed
        assert "test_signal" in timer._to_remove

    def test_cancel_removes_on_update(self):
        timer = Timer()
        timer.after(10.0, "test_signal")  # Long delay so it won't fire
        timer.cancel("test_signal")
        timer._update()
        assert not timer.has_timer("test_signal")

    def test_cancel_nonexistent_is_noop(self):
        timer = Timer()
        timer.cancel("nonexistent")  # Should not raise
        assert len(timer._to_remove) == 0


class TestTimerClearAll:
    """Tests for clearing all timers."""

    def test_clear_all_removes_all_timers(self):
        timer = Timer()
        timer.after(1.0, "signal_1")
        timer.every(2.0, "signal_2")
        timer.after(3.0, "signal_3")

        timer._clear_all()

        assert not timer.has_timer("signal_1")
        assert not timer.has_timer("signal_2")
        assert not timer.has_timer("signal_3")
        assert len(timer._timers) == 0

    def test_clear_all_also_clears_pending_removals(self):
        timer = Timer()
        timer.after(1.0, "test_signal")
        timer.cancel("test_signal")

        timer._clear_all()

        assert len(timer._to_remove) == 0


class TestTimerUpdate:
    """Tests for timer update and signal firing."""

    def test_after_fires_signal_when_time_elapsed(self):
        timer = Timer()
        received = []

        def handler(sender):
            received.append(sender)

        Signals.connect("test_after_signal", handler)

        with patch('pyke_pyxel.timer.time') as mock_time:
            # Initial time
            mock_time.time.return_value = 1000.0
            timer.after(0.5, "test_after_signal", "test_sender")

            # Time hasn't elapsed yet
            mock_time.time.return_value = 1000.3
            timer._update()
            assert len(received) == 0

            # Time has elapsed
            mock_time.time.return_value = 1000.6
            timer._update()
            assert len(received) == 1
            assert received[0] == "test_sender"

        Signals.disconnect("test_after_signal", handler)

    def test_after_fires_only_once(self):
        timer = Timer()
        fire_count = []

        def handler(sender):
            fire_count.append(1)

        Signals.connect("test_once_signal", handler)

        with patch('pyke_pyxel.timer.time') as mock_time:
            mock_time.time.return_value = 1000.0
            timer.after(0.5, "test_once_signal")

            # Fire it
            mock_time.time.return_value = 1000.6
            timer._update()
            assert len(fire_count) == 1

            # Timer should be marked for removal, remove it
            timer._update()

            # Should not fire again
            mock_time.time.return_value = 1001.2
            timer._update()
            assert len(fire_count) == 1

        Signals.disconnect("test_once_signal", handler)

    def test_every_fires_repeatedly(self):
        timer = Timer()
        fire_count = []

        def handler(sender):
            fire_count.append(1)

        Signals.connect("test_repeat_signal", handler)

        with patch('pyke_pyxel.timer.time') as mock_time:
            mock_time.time.return_value = 1000.0
            timer.every(0.5, "test_repeat_signal")

            # First fire
            mock_time.time.return_value = 1000.6
            timer._update()
            assert len(fire_count) == 1

            # Second fire
            mock_time.time.return_value = 1001.2
            timer._update()
            assert len(fire_count) == 2

            # Third fire
            mock_time.time.return_value = 1001.8
            timer._update()
            assert len(fire_count) == 3

        Signals.disconnect("test_repeat_signal", handler)

    def test_after_removed_after_firing(self):
        timer = Timer()

        def handler(sender):
            pass

        Signals.connect("test_removal_signal", handler)

        with patch('pyke_pyxel.timer.time') as mock_time:
            mock_time.time.return_value = 1000.0
            timer.after(0.5, "test_removal_signal")
            assert timer.has_timer("test_removal_signal")

            # Fire it
            mock_time.time.return_value = 1000.6
            timer._update()

            # Process removal
            timer._update()
            assert not timer.has_timer("test_removal_signal")

        Signals.disconnect("test_removal_signal", handler)

    def test_every_not_removed_after_firing(self):
        timer = Timer()

        def handler(sender):
            pass

        Signals.connect("test_persist_signal", handler)

        with patch('pyke_pyxel.timer.time') as mock_time:
            mock_time.time.return_value = 1000.0
            timer.every(0.5, "test_persist_signal")

            # Fire it multiple times
            mock_time.time.return_value = 1000.6
            timer._update()
            timer._update()

            mock_time.time.return_value = 1001.2
            timer._update()
            timer._update()

            # Timer should still exist
            assert timer.has_timer("test_persist_signal")

        Signals.disconnect("test_persist_signal", handler)


class TestTimerUpsert:
    """Tests for timer update/replace behavior."""

    def test_upsert_updates_existing_timer_seconds(self):
        timer = Timer()

        with patch('pyke_pyxel.timer.time') as mock_time:
            mock_time.time.return_value = 1000.0
            timer.after(5.0, "test_signal")

            # Update to shorter time
            mock_time.time.return_value = 1000.1
            timer.after(0.1, "test_signal")

            # Check internal timer was updated
            internal_timer = timer._timers["test_signal"]
            assert internal_timer.seconds == 0.1

    def test_upsert_resets_last_fire_time(self):
        timer = Timer()

        with patch('pyke_pyxel.timer.time') as mock_time:
            mock_time.time.return_value = 1000.0
            timer.after(1.0, "test_signal")

            mock_time.time.return_value = 1005.0
            timer.after(1.0, "test_signal")  # Reset timer

            internal_timer = timer._timers["test_signal"]
            assert internal_timer.last_fire_time == 1005.0

    def test_upsert_resets_has_fired_flag(self):
        timer = Timer()

        def handler(sender):
            # Re-register the same timer from within handler
            timer.after(1.0, "recursive_signal")

        Signals.connect("recursive_signal", handler)

        with patch('pyke_pyxel.timer.time') as mock_time:
            mock_time.time.return_value = 1000.0
            timer.after(0.5, "recursive_signal")

            # Fire it - handler will re-register
            mock_time.time.return_value = 1000.6
            timer._update()

            # Timer should still exist (re-registered)
            # Process any pending removals
            timer._update()

            # The timer should still exist because it was re-registered
            assert timer.has_timer("recursive_signal")

        Signals.disconnect("recursive_signal", handler)
