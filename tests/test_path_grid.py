import pytest
from unittest.mock import patch, MagicMock

from pyke_pyxel._path_grid import _PathGrid, PATH_STATUS
from pyke_pyxel._types import coord, GameSettings


class TestPathGridCreation:
    """Tests for _PathGrid creation and initialization."""

    def test_basic_creation(self):
        grid = _PathGrid(cols=10, rows=10)
        assert grid is not None

    def test_grid_initialized_with_available_status(self):
        grid = _PathGrid(cols=5, rows=5)
        # All cells should be AVAILABLE by default
        for row in grid._grid:
            for cell in row:
                assert cell == PATH_STATUS.AVAILABLE

    def test_grid_dimensions(self):
        grid = _PathGrid(cols=8, rows=12)
        # Note: The grid is constructed with rows as outer list
        assert len(grid._grid) == 8  # cols
        assert len(grid._grid[0]) == 12  # rows


class TestPathGridBlock:
    """Tests for blocking positions."""

    def test_block_position(self):
        grid = _PathGrid(cols=10, rows=10)
        pos = coord(5, 5)
        grid.block(pos)
        # coord is 1-indexed, grid is 0-indexed
        assert grid._grid[4][4] == PATH_STATUS.BLOCKED

    def test_block_corner_position(self):
        grid = _PathGrid(cols=10, rows=10)
        pos = coord(1, 1)
        grid.block(pos)
        assert grid._grid[0][0] == PATH_STATUS.BLOCKED

    def test_block_with_reduce_hugging_sets_neighbours_to_avoid(self, reset_game_settings):
        reset_game_settings.pathfinding.reduce_hugging = True
        grid = _PathGrid(cols=10, rows=10)
        pos = coord(5, 5)
        grid.block(pos)

        # Blocked position
        assert grid._grid[4][4] == PATH_STATUS.BLOCKED

        # Neighbours should be AVOID (left, right, up, down of index 4,4)
        assert grid._grid[4][3] == PATH_STATUS.AVOID  # left
        assert grid._grid[4][5] == PATH_STATUS.AVOID  # right
        assert grid._grid[3][4] == PATH_STATUS.AVOID  # up
        assert grid._grid[5][4] == PATH_STATUS.AVOID  # down

    def test_block_without_reduce_hugging_leaves_neighbours_available(self, reset_game_settings):
        reset_game_settings.pathfinding.reduce_hugging = False
        grid = _PathGrid(cols=10, rows=10)
        pos = coord(5, 5)
        grid.block(pos)

        # Blocked position
        assert grid._grid[4][4] == PATH_STATUS.BLOCKED

        # Neighbours should still be AVAILABLE
        assert grid._grid[4][3] == PATH_STATUS.AVAILABLE
        assert grid._grid[4][5] == PATH_STATUS.AVAILABLE
        assert grid._grid[3][4] == PATH_STATUS.AVAILABLE
        assert grid._grid[5][4] == PATH_STATUS.AVAILABLE

    def test_block_edge_position_no_out_of_bounds(self, reset_game_settings):
        reset_game_settings.pathfinding.reduce_hugging = True
        grid = _PathGrid(cols=5, rows=5)
        # Block corner - should not raise even with reduce_hugging
        pos = coord(1, 1)
        grid.block(pos)
        assert grid._grid[0][0] == PATH_STATUS.BLOCKED


class TestPathGridOpen:
    """Tests for opening positions."""

    def test_open_blocked_position(self, reset_game_settings):
        reset_game_settings.pathfinding.reduce_hugging = False
        grid = _PathGrid(cols=10, rows=10)
        pos = coord(5, 5)
        grid.block(pos)
        assert grid._grid[4][4] == PATH_STATUS.BLOCKED

        grid.open(pos)
        assert grid._grid[4][4] == PATH_STATUS.AVAILABLE

    def test_open_with_reduce_hugging_sets_to_avoid(self, reset_game_settings):
        reset_game_settings.pathfinding.reduce_hugging = True
        grid = _PathGrid(cols=10, rows=10)
        pos = coord(5, 5)
        grid.block(pos)
        grid.open(pos)
        # When reduce_hugging is enabled, opening a previously blocked cell
        # sets it to AVOID (not AVAILABLE)
        assert grid._grid[4][4] == PATH_STATUS.AVOID


class TestPathGridNeighbours:
    """Tests for the _neighbours method."""

    def test_neighbours_center(self):
        grid = _PathGrid(cols=10, rows=10)
        neighbours = grid._neighbours(5, 5)
        # Should have 4 neighbours: left, right, up, down
        assert len(neighbours) == 4
        assert (4, 5) in neighbours  # left
        assert (6, 5) in neighbours  # right
        assert (5, 4) in neighbours  # up
        assert (5, 6) in neighbours  # down

    def test_neighbours_top_left_corner(self):
        grid = _PathGrid(cols=10, rows=10)
        neighbours = grid._neighbours(0, 0)
        # Should have 2 neighbours: right, down
        assert len(neighbours) == 2
        assert (1, 0) in neighbours  # right
        assert (0, 1) in neighbours  # down

    def test_neighbours_bottom_right_corner(self):
        grid = _PathGrid(cols=10, rows=10)
        neighbours = grid._neighbours(9, 9)
        # Should have 2 neighbours: left, up
        assert len(neighbours) == 2
        assert (8, 9) in neighbours  # left
        assert (9, 8) in neighbours  # up

    def test_neighbours_left_edge(self):
        grid = _PathGrid(cols=10, rows=10)
        neighbours = grid._neighbours(0, 5)
        # Should have 3 neighbours: right, up, down
        assert len(neighbours) == 3
        assert (1, 5) in neighbours  # right
        assert (0, 4) in neighbours  # up
        assert (0, 6) in neighbours  # down


class TestPathGridFindPath:
    """Tests for A* pathfinding."""

    def test_find_path_direct(self, reset_game_settings):
        reset_game_settings.pathfinding.allow_diagonal = False
        grid = _PathGrid(cols=10, rows=10)
        start = coord(1, 1)
        end = coord(3, 1)
        path = grid.find_path(start, end)

        assert path is not None
        assert len(path) >= 2
        assert path[0].is_same_grid_location(start)
        assert path[-1].is_same_grid_location(end)

    def test_find_path_around_obstacle(self, reset_game_settings):
        reset_game_settings.pathfinding.allow_diagonal = False
        reset_game_settings.pathfinding.reduce_hugging = False
        grid = _PathGrid(cols=10, rows=10)

        # Block position between start and end
        grid.block(coord(2, 1))

        start = coord(1, 1)
        end = coord(3, 1)
        path = grid.find_path(start, end)

        assert path is not None
        # Path must go around the blocked position
        assert coord(2, 1) not in path
        assert path[0].is_same_grid_location(start)
        assert path[-1].is_same_grid_location(end)

    def test_find_path_no_path_exists(self, reset_game_settings):
        reset_game_settings.pathfinding.allow_diagonal = False
        grid = _PathGrid(cols=5, rows=5)

        # Block all paths to destination
        grid.block(coord(2, 1))
        grid.block(coord(2, 2))
        grid.block(coord(2, 3))
        grid.block(coord(2, 4))
        grid.block(coord(2, 5))

        start = coord(1, 1)
        end = coord(3, 1)
        path = grid.find_path(start, end)

        assert path is None

    def test_find_path_with_diagonal(self, reset_game_settings):
        reset_game_settings.pathfinding.allow_diagonal = True
        grid = _PathGrid(cols=10, rows=10)
        start = coord(1, 1)
        end = coord(3, 3)
        path = grid.find_path(start, end)

        assert path is not None
        assert path[0].is_same_grid_location(start)
        assert path[-1].is_same_grid_location(end)

    def test_find_path_without_diagonal(self, reset_game_settings):
        reset_game_settings.pathfinding.allow_diagonal = False
        grid = _PathGrid(cols=10, rows=10)
        start = coord(1, 1)
        end = coord(2, 2)
        path = grid.find_path(start, end)

        assert path is not None
        # Without diagonal movement, path length should be longer
        # Need at least 3 nodes: start, intermediate, end
        assert len(path) >= 3

    def test_find_path_override_diagonal_setting(self, reset_game_settings):
        reset_game_settings.pathfinding.allow_diagonal = False
        grid = _PathGrid(cols=10, rows=10)
        start = coord(1, 1)
        end = coord(2, 2)

        # Override the setting for this specific call
        path = grid.find_path(start, end, allow_diagonal=True)

        assert path is not None
        # With diagonal override, direct diagonal path is possible
        assert len(path) == 2

    def test_find_path_same_start_and_end(self):
        grid = _PathGrid(cols=10, rows=10)
        pos = coord(5, 5)
        path = grid.find_path(pos, pos)

        assert path is not None
        assert len(path) == 1
        assert path[0].is_same_grid_location(pos)


class TestPathStatus:
    """Tests for PATH_STATUS constants."""

    def test_status_values(self):
        assert PATH_STATUS.BLOCKED == 0
        assert PATH_STATUS.PREFERRED == 1
        assert PATH_STATUS.AVAILABLE == 2
        assert PATH_STATUS.AVOID == 3

    def test_blocked_is_lowest(self):
        # BLOCKED should be 0 so pathfinding library treats it as impassable
        assert PATH_STATUS.BLOCKED < PATH_STATUS.PREFERRED
        assert PATH_STATUS.BLOCKED < PATH_STATUS.AVAILABLE
        assert PATH_STATUS.BLOCKED < PATH_STATUS.AVOID
