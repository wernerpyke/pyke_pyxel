import pytest
from unittest.mock import patch, MagicMock

from pyke_pyxel.map import Map, MapLocation, LOCATION_STATUS
from pyke_pyxel._types import coord, area, GameSettings
from pyke_pyxel.sprite import Sprite, OpenableSprite


class TestMapCreation:
    """Tests for Map creation and initialization."""

    def test_basic_creation(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        assert game_map is not None

    def test_grid_dimensions(self, reset_game_settings):
        reset_game_settings.size.window = 160
        reset_game_settings.size.tile = 8
        game_map = Map(reset_game_settings)

        # 160 / 8 = 20 cols and rows
        assert game_map._cols == 20
        assert game_map._rows == 20

    def test_all_locations_start_free(self, reset_game_settings):
        game_map = Map(reset_game_settings)

        for col in range(1, game_map._cols + 1):
            for row in range(1, game_map._rows + 1):
                location = game_map.location_at(coord(col, row))
                assert location.status == LOCATION_STATUS.FREE

    def test_width_and_height_properties(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.width == 160
        assert game_map.height == 160


class TestMapLocationAt:
    """Tests for location_at method."""

    def test_location_at_valid_coord(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        location = game_map.location_at(coord(5, 5))

        assert location is not None
        assert location.is_edge is False
        assert location.position is not None
        assert location.position._col == 5
        assert location.position._row == 5

    def test_location_at_first_coord(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        location = game_map.location_at(coord(1, 1))

        assert location is not None
        assert location.is_edge is False

    def test_location_at_last_coord(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        location = game_map.location_at(coord(game_map._cols, game_map._rows))

        assert location is not None
        assert location.is_edge is False

    def test_location_at_out_of_bounds_right_returns_edge(self, reset_game_settings):
        game_map = Map(reset_game_settings)

        # Too far right
        location = game_map.location_at(coord(game_map._cols + 1, 5))
        assert location.is_edge is True

    def test_location_at_out_of_bounds_down_returns_edge(self, reset_game_settings):
        game_map = Map(reset_game_settings)

        # Too far down
        location = game_map.location_at(coord(5, game_map._rows + 1))
        assert location.is_edge is True


class TestMapMarkBlocked:
    """Tests for mark_blocked method."""

    def test_mark_blocked_changes_status(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)
        sprite = MagicMock(spec=Sprite)

        game_map.mark_blocked(pos, sprite)

        location = game_map.location_at(pos)
        assert location.status == LOCATION_STATUS.BLOCKED

    def test_mark_blocked_assigns_sprite(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)
        sprite = MagicMock(spec=Sprite)

        game_map.mark_blocked(pos, sprite)

        location = game_map.location_at(pos)
        assert location.sprite == sprite

    def test_mark_blocked_updates_path_grid(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)
        sprite = MagicMock(spec=Sprite)

        game_map.mark_blocked(pos, sprite)

        # Path grid should be blocked
        from pyke_pyxel._path_grid import PATH_STATUS
        assert game_map._path_grid._grid[4][4] == PATH_STATUS.BLOCKED

    def test_mark_blocked_edge_location_does_nothing(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        # Use out-of-bounds position (beyond grid size)
        pos = coord(game_map._cols + 1, game_map._rows + 1)
        sprite = MagicMock(spec=Sprite)

        # Should not raise, just log error
        game_map.mark_blocked(pos, sprite)

        # Edge location should remain unchanged
        location = game_map.location_at(pos)
        assert location.is_edge is True


class TestMapMarkOpenable:
    """Tests for mark_openable method."""

    def test_mark_openable_closed(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)
        sprite = MagicMock(spec=OpenableSprite)

        game_map.mark_openable(pos, sprite, closed=True)

        location = game_map.location_at(pos)
        assert location.status == LOCATION_STATUS.CLOSED
        assert location.sprite == sprite

    def test_mark_openable_open(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)
        sprite = MagicMock(spec=OpenableSprite)

        game_map.mark_openable(pos, sprite, closed=False)

        location = game_map.location_at(pos)
        assert location.status == LOCATION_STATUS.OPEN
        assert location.sprite == sprite


class TestMapMarkClosedOpen:
    """Tests for mark_closed and mark_open methods."""

    def test_mark_closed(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        game_map.mark_closed(pos)

        location = game_map.location_at(pos)
        assert location.status == LOCATION_STATUS.CLOSED

    def test_mark_open(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        game_map.mark_closed(pos)
        game_map.mark_open(pos)

        location = game_map.location_at(pos)
        assert location.status == LOCATION_STATUS.OPEN

    def test_mark_closed_updates_path_grid(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        game_map.mark_closed(pos)

        from pyke_pyxel._path_grid import PATH_STATUS
        assert game_map._path_grid._grid[4][4] == PATH_STATUS.BLOCKED


class TestMapStatusQueries:
    """Tests for is_blocked, is_openable, sprite_can_move_to methods."""

    def test_is_blocked_returns_true(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)
        sprite = MagicMock(spec=Sprite)

        game_map.mark_blocked(pos, sprite)

        assert game_map.is_blocked(pos) is True

    def test_is_blocked_returns_false(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        assert game_map.is_blocked(pos) is False

    def test_is_openable_returns_true_for_closed(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        game_map.mark_closed(pos)

        assert game_map.is_openable(pos) is True

    def test_is_openable_returns_true_for_open(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        game_map.mark_open(pos)

        assert game_map.is_openable(pos) is True

    def test_is_openable_returns_false_for_free(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        assert game_map.is_openable(pos) is False

    def test_sprite_can_move_to_free(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        assert game_map.sprite_can_move_to(pos) is True

    def test_sprite_can_move_to_open(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        game_map.mark_open(pos)

        assert game_map.sprite_can_move_to(pos) is True

    def test_sprite_cannot_move_to_blocked(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)
        sprite = MagicMock(spec=Sprite)

        game_map.mark_blocked(pos, sprite)

        assert game_map.sprite_can_move_to(pos) is False

    def test_sprite_cannot_move_to_closed(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        game_map.mark_closed(pos)

        assert game_map.sprite_can_move_to(pos) is False


class TestMapSpriteAt:
    """Tests for sprite_at and openable_sprite_at methods."""

    def test_sprite_at_returns_sprite(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)
        sprite = MagicMock(spec=Sprite)

        game_map.mark_blocked(pos, sprite)

        assert game_map.sprite_at(pos) == sprite

    def test_sprite_at_returns_none(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        assert game_map.sprite_at(pos) is None

    def test_openable_sprite_at_returns_sprite(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)
        sprite = MagicMock(spec=OpenableSprite)

        game_map.mark_openable(pos, sprite, closed=True)

        assert game_map.openable_sprite_at(pos) == sprite

    def test_openable_sprite_at_returns_none_for_free(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        assert game_map.openable_sprite_at(pos) is None

    def test_openable_sprite_at_returns_none_for_blocked(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)
        sprite = MagicMock(spec=Sprite)

        game_map.mark_blocked(pos, sprite)

        assert game_map.openable_sprite_at(pos) is None


class TestMapAdjacentLocations:
    """Tests for location_left_of, location_right_of, location_above, location_below."""

    def test_location_left_of(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        location = game_map.location_left_of(pos)

        assert location is not None
        assert location.position._col == 4
        assert location.position._row == 5

    def test_location_left_of_edge_returns_none(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(1, 5)

        location = game_map.location_left_of(pos)

        assert location is None

    def test_location_right_of(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        location = game_map.location_right_of(pos)

        assert location is not None
        assert location.position._col == 6
        assert location.position._row == 5

    def test_location_right_of_edge_returns_none(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        # The boundary check uses _grid.__len__() - 1 which is 19 for a 20-col grid
        pos = coord(game_map._cols - 1, 5)

        location = game_map.location_right_of(pos)

        assert location is None

    def test_location_above(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        location = game_map.location_above(pos)

        assert location is not None
        assert location.position._col == 5
        assert location.position._row == 4

    def test_location_above_edge_returns_none(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 1)

        location = game_map.location_above(pos)

        assert location is None

    def test_location_below(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, 5)

        location = game_map.location_below(pos)

        assert location is not None
        assert location.position._col == 5
        assert location.position._row == 6

    def test_location_below_edge_returns_none(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        pos = coord(5, game_map._rows - 1)

        location = game_map.location_below(pos)

        assert location is None


class TestMapAdjacentOpenable:
    """Tests for adjacent_openable method."""

    def test_adjacent_openable_left(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        center = coord(5, 5)
        left = coord(4, 5)
        sprite = MagicMock(spec=OpenableSprite)

        game_map.mark_openable(left, sprite, closed=True)

        result = game_map.adjacent_openable(center)

        assert result == sprite

    def test_adjacent_openable_right(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        center = coord(5, 5)
        right = coord(6, 5)
        sprite = MagicMock(spec=OpenableSprite)

        game_map.mark_openable(right, sprite, closed=False)

        result = game_map.adjacent_openable(center)

        assert result == sprite

    def test_adjacent_openable_above(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        center = coord(5, 5)
        above = coord(5, 4)
        sprite = MagicMock(spec=OpenableSprite)

        game_map.mark_openable(above, sprite, closed=True)

        result = game_map.adjacent_openable(center)

        assert result == sprite

    def test_adjacent_openable_below(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        center = coord(5, 5)
        below = coord(5, 6)
        sprite = MagicMock(spec=OpenableSprite)

        game_map.mark_openable(below, sprite, closed=False)

        result = game_map.adjacent_openable(center)

        assert result == sprite

    def test_adjacent_openable_none_found(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        center = coord(5, 5)

        result = game_map.adjacent_openable(center)

        assert result is None


class TestMapBounds:
    """Tests for bound_to_width and bound_to_height methods."""

    def test_bound_to_width_within_bounds(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.bound_to_width(50) == 50
        assert game_map.bound_to_width(0) == 0
        assert game_map.bound_to_width(160) == 160

    def test_bound_to_width_below_zero(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.bound_to_width(-10) == 0

    def test_bound_to_width_above_max(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.bound_to_width(200) == 160

    def test_bound_to_height_within_bounds(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.bound_to_height(50) == 50
        assert game_map.bound_to_height(0) == 0
        assert game_map.bound_to_height(160) == 160

    def test_bound_to_height_below_zero(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.bound_to_height(-10) == 0

    def test_bound_to_height_above_max(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.bound_to_height(200) == 160


class TestMapCenterQueries:
    """Tests for center and side queries."""

    def test_center_x(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.center_x == 80

    def test_center_y(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.center_y == 80

    def test_right_x(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.right_x == 160

    def test_bottom_y(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.bottom_y == 160

    def test_x_is_left_of_center(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.x_is_left_of_center(40) is True
        assert game_map.x_is_left_of_center(80) is False
        assert game_map.x_is_left_of_center(120) is False

    def test_y_is_above_center(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        assert game_map.y_is_above_center(40) is True
        assert game_map.y_is_above_center(80) is False
        assert game_map.y_is_above_center(120) is False


class TestMapDistanceCalculations:
    """Tests for distance calculation methods."""

    def test_shortest_distance_to_sides_left(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        # Closer to left
        assert game_map.shortest_distance_to_sides(40) == 40

    def test_shortest_distance_to_sides_right(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        # Closer to right (160 - 120 = 40)
        assert game_map.shortest_distance_to_sides(120) == 40

    def test_shortest_distance_to_sides_center(self, reset_game_settings):
        reset_game_settings.size.window = 160
        game_map = Map(reset_game_settings)

        # At center, both distances are equal
        assert game_map.shortest_distance_to_sides(80) == 80


class TestMapFindPath:
    """Tests for pathfinding integration."""

    def test_find_path_basic(self, reset_game_settings):
        reset_game_settings.pathfinding.allow_diagonal = False
        game_map = Map(reset_game_settings)
        start = coord(1, 1)
        end = coord(3, 1)

        path = game_map.find_path(start, end)

        assert path is not None
        assert len(path) >= 2
        assert path[0].is_same_grid_location(start)
        assert path[-1].is_same_grid_location(end)

    def test_find_path_around_obstacle(self, reset_game_settings):
        reset_game_settings.pathfinding.allow_diagonal = False
        reset_game_settings.pathfinding.reduce_hugging = False
        game_map = Map(reset_game_settings)
        sprite = MagicMock(spec=Sprite)

        # Block position between start and end
        game_map.mark_blocked(coord(2, 1), sprite)

        start = coord(1, 1)
        end = coord(3, 1)
        path = game_map.find_path(start, end)

        assert path is not None
        # Path should not include blocked position
        blocked_in_path = any(p.is_same_grid_location(coord(2, 1)) for p in path)
        assert blocked_in_path is False

    def test_find_path_from_blocked_returns_none(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        sprite = MagicMock(spec=Sprite)
        start = coord(1, 1)
        end = coord(5, 5)

        game_map.mark_blocked(start, sprite)

        path = game_map.find_path(start, end)

        assert path is None

    def test_find_path_to_blocked_returns_none(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        sprite = MagicMock(spec=Sprite)
        start = coord(1, 1)
        end = coord(5, 5)

        game_map.mark_blocked(end, sprite)

        path = game_map.find_path(start, end)

        assert path is None

    def test_find_path_with_diagonal_override(self, reset_game_settings):
        reset_game_settings.pathfinding.allow_diagonal = False
        game_map = Map(reset_game_settings)
        start = coord(1, 1)
        end = coord(2, 2)

        # Override setting for this call
        path = game_map.find_path(start, end, allow_diagonal=True)

        assert path is not None
        # Diagonal path should be shorter
        assert len(path) == 2


class TestMapRandomLocation:
    """Tests for random_location method."""

    def test_random_location_returns_location_in_area(self, reset_game_settings):
        game_map = Map(reset_game_settings)
        # area takes: from_col, from_row, to_col, to_row
        test_area = area(2, 2, 5, 5)

        location = game_map.random_location(test_area)

        assert location is not None
        assert location.position is not None
        # Location should be within the area bounds
        assert 2 <= location.position._col <= 5
        assert 2 <= location.position._row <= 5


class TestLocationStatus:
    """Tests for LOCATION_STATUS enum."""

    def test_status_values(self):
        assert LOCATION_STATUS.FREE.value == 0
        assert LOCATION_STATUS.BLOCKED.value == 1
        assert LOCATION_STATUS.CLOSED.value == 2
        assert LOCATION_STATUS.OPEN.value == 3

    def test_status_values_are_distinct(self):
        statuses = [LOCATION_STATUS.FREE, LOCATION_STATUS.BLOCKED,
                    LOCATION_STATUS.CLOSED, LOCATION_STATUS.OPEN]
        values = [s.value for s in statuses]
        assert len(values) == len(set(values))


class TestMapLocation:
    """Tests for MapLocation dataclass."""

    def test_default_values(self):
        location = MapLocation()

        assert location.position is None
        assert location.status == LOCATION_STATUS.FREE
        assert location.sprite is None
        assert location.is_edge is False

    def test_creation_with_position(self):
        pos = coord(5, 5)
        location = MapLocation(position=pos)

        assert location.position == pos
        assert location.status == LOCATION_STATUS.FREE

    def test_edge_location(self):
        location = MapLocation(is_edge=True)

        assert location.is_edge is True
