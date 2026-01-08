import pytest
from pyke_pyxel._types import coord, DIRECTION


class TestCoordCreation:
    """Tests for coord instantiation and factory methods."""

    def test_basic_creation(self):
        c = coord(1, 1)
        assert c.col == 1
        assert c.row == 1
        assert c.x == 0
        assert c.y == 0

    def test_col_row_to_pixel_conversion(self):
        # With default tile size of 8
        c = coord(2, 3)
        assert c.x == 8   # (2-1) * 8
        assert c.y == 16  # (3-1) * 8

    def test_custom_tile_size(self):
        c = coord(2, 2, size=16)
        assert c.x == 16  # (2-1) * 16
        assert c.y == 16
        assert c.size == 16

    def test_invalid_col_raises_error(self):
        with pytest.raises(ValueError, match="col values must be >= 1"):
            coord(0, 1)

    def test_invalid_row_raises_error(self):
        with pytest.raises(ValueError, match="row values must be >= 1"):
            coord(1, 0)

    def test_with_xy_factory(self):
        c = coord.with_xy(16, 24)
        assert c.x == 16
        assert c.y == 24
        assert c.col == 3  # round(16/8) + 1
        assert c.row == 4  # round(24/8) + 1

    def test_with_center_factory(self):
        # Center at (20, 20) with tile size 8 means top-left at (16, 16)
        c = coord.with_center(20, 20)
        assert c.x == 16  # 20 - 4 (half of 8)
        assert c.y == 16

    def test_with_map_bounds_clamps_values(self, reset_game_settings):
        # Window 160, tile 8 = max 21 tiles
        c = coord.with_map_bounds(100, 100)
        assert c.col <= 21
        assert c.row <= 21


class TestCoordProperties:
    """Tests for coord property accessors."""

    def test_mid_x_mid_y(self):
        c = coord(1, 1)  # x=0, y=0, size=8
        assert c.mid_x == 4  # 0 + 8/2
        assert c.mid_y == 4

    def test_min_max_properties(self):
        c = coord(2, 2)  # x=8, y=8
        assert c.min_x == 8
        assert c.min_y == 8
        assert c.max_x == 16  # 8 + 8
        assert c.max_y == 16


class TestCoordComparisons:
    """Tests for coord comparison and collision methods."""

    def test_is_same_grid_location(self):
        c1 = coord(5, 5)
        c2 = coord(5, 5)
        assert c1.is_same_grid_location(c2)

    def test_is_different_grid_location(self):
        c1 = coord(5, 5)
        c2 = coord(5, 6)
        assert c1.is_different_grid_location(c2)

    def test_is_at_exact_position(self):
        c1 = coord.with_xy(10, 20)
        c2 = coord.with_xy(10, 20)
        assert c1.is_at(c2)

    def test_is_not_at_different_position(self):
        c1 = coord.with_xy(10, 20)
        c2 = coord.with_xy(10, 21)
        assert not c1.is_at(c2)

    def test_is_above(self):
        c1 = coord(1, 1)  # y=0
        c2 = coord(1, 2)  # y=8
        assert c1.is_above(c2)
        assert not c2.is_above(c1)

    def test_is_below(self):
        c1 = coord(1, 2)  # y=8
        c2 = coord(1, 1)  # y=0
        assert c1.is_below(c2)

    def test_is_left_of(self):
        c1 = coord(1, 1)  # x=0
        c2 = coord(2, 1)  # x=8
        assert c1.is_left_of(c2)

    def test_is_right_of(self):
        c1 = coord(2, 1)  # x=8
        c2 = coord(1, 1)  # x=0
        assert c1.is_right_of(c2)

    def test_contains_point_inside(self):
        c = coord(2, 2)  # x=8, y=8, size=8
        assert c.contains(10, 10)  # Inside the tile
        assert c.contains(8, 8)    # Top-left corner
        assert c.contains(16, 16)  # Bottom-right corner

    def test_contains_point_outside(self):
        c = coord(2, 2)  # x=8, y=8
        assert not c.contains(0, 0)
        assert not c.contains(20, 20)

    def test_collides_with_overlapping(self):
        c1 = coord(1, 1)
        c2 = coord.with_xy(4, 4)  # Overlaps with c1
        assert c1.collides_with(c2)

    def test_collides_with_no_overlap(self):
        c1 = coord(1, 1)
        c2 = coord(5, 5)  # Far away
        assert not c1.collides_with(c2)

    def test_collides_with_tolerance(self):
        c1 = coord(1, 1)  # 0,0 to 8,8
        c2 = coord.with_xy(7, 0)  # Just barely overlapping
        # With default tolerance=1, edge cases are excluded
        assert not c1.collides_with(c2, tolerance=2)
        assert c1.collides_with(c2, tolerance=0)


class TestCoordMovement:
    """Tests for coord movement and cloning methods."""

    def test_move_by(self):
        c = coord(1, 1)
        c.move_by(x=10, y=5)
        assert c.x == 10
        assert c.y == 5

    def test_move_by_updates_grid_location(self):
        c = coord(1, 1)
        c.move_by(x=16, y=16)  # Move 2 tiles right and down
        assert c.col == 3
        assert c.row == 3

    def test_clone(self):
        c = coord.with_xy(10, 20)
        cloned = c.clone()
        assert cloned.x == c.x
        assert cloned.y == c.y
        # Ensure it's a different object
        cloned.move_by(x=5)
        assert c.x == 10

    def test_clone_by(self):
        c = coord(1, 1)
        cloned = c.clone_by(x=8, y=8)
        assert cloned.x == 8
        assert cloned.y == 8
        # Original unchanged
        assert c.x == 0

    def test_clone_by_with_direction_up(self):
        c = coord(5, 5)
        cloned = c.clone_by(x=0, y=-8, direction=DIRECTION.UP)
        assert cloned.row < c.row

    def test_clone_by_with_direction_down(self):
        c = coord(5, 5)
        cloned = c.clone_by(x=0, y=8, direction=DIRECTION.DOWN)
        assert cloned.row > c.row

    def test_clone_towards(self):
        c1 = coord(1, 1)  # x=0, y=0
        c2 = coord(5, 5)  # x=32, y=32
        cloned = c1.clone_towards(c2, distance=4)
        assert cloned.x == 4  # Moved towards c2
        assert cloned.y == 4

    def test_diff(self):
        c1 = coord.with_xy(20, 30)
        c2 = coord.with_xy(10, 10)
        diff = c1.diff(c2)
        assert diff == (10, 20)

    def test_distance_to(self):
        c1 = coord(1, 1)  # x=0, y=0
        c2 = coord.with_xy(3, 4)
        distance = c1.distance_to(c2)
        assert distance == 5.0  # 3-4-5 triangle


class TestCoordStringRepresentation:
    """Tests for coord string output."""

    def test_str(self):
        c = coord(3, 5)
        assert str(c) == "3/5"
