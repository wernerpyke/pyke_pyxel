import pytest
from pyke_pyxel._types import area, coord


class TestAreaCreation:
    """Tests for area instantiation and factory methods."""

    def test_basic_creation(self):
        a = area(1, 1, 3, 3)
        assert a._from_col == 1
        assert a._from_row == 1
        assert a._to_col == 3
        assert a._to_row == 3

    def test_pixel_position(self):
        a = area(2, 2, 4, 4)  # tile size 8
        assert a.x == 8   # (2-1) * 8
        assert a.y == 8   # (2-1) * 8

    def test_dimensions(self):
        a = area(1, 1, 3, 4)
        assert a.columns == 3  # 3 - 1 + 1
        assert a.rows == 4     # 4 - 1 + 1

    def test_custom_tile_size(self):
        a = area(1, 1, 2, 2, tile_size=16)
        assert a.tile_size == 16
        assert a.max_x == 32  # 2 columns * 16

    def test_invalid_col_raises_error(self):
        with pytest.raises(ValueError, match="col values must be >= 1"):
            area(0, 1, 2, 2)

    def test_invalid_row_raises_error(self):
        with pytest.raises(ValueError, match="row values must be >= 1"):
            area(1, 0, 2, 2)

    def test_to_col_less_than_from_col_raises_error(self):
        with pytest.raises(ValueError, match="to_col .* must be >= from_col"):
            area(5, 1, 3, 3)

    def test_to_row_less_than_from_row_raises_error(self):
        with pytest.raises(ValueError, match="to_row .* must be >= from_row"):
            area(1, 5, 3, 3)

    def test_with_map_bounds_clamps_values(self, reset_game_settings):
        # Window 160, tile 8 = 20 tiles max
        a = area.with_map_bounds(1, 100, 1, 100)
        assert a._to_col <= 20
        assert a._to_row <= 20

    def test_with_center_factory(self):
        a = area.with_center(40, 40, cols=3, rows=3)
        # Center at (40,40) with 3x3 tiles (24x24 pixels)
        # from_x = 40 - 12 = 28, from_y = 40 - 12 = 28
        assert a.mid_x == pytest.approx(40, abs=8)
        assert a.mid_y == pytest.approx(40, abs=8)


class TestAreaProperties:
    """Tests for area property accessors."""

    def test_mid_x_mid_y(self):
        a = area(1, 1, 3, 3)  # 3x3 tiles, 24x24 pixels
        # x=0, width=24, mid = 0 + 12 = 12
        assert a.mid_x == 12
        assert a.mid_y == 12

    def test_min_max_properties(self):
        a = area(2, 2, 4, 4)  # x=8, y=8, 3 cols/rows
        assert a.min_x == 8
        assert a.min_y == 8
        assert a.max_x == 32  # 8 + (3 * 8)
        assert a.max_y == 32


class TestAreaTiles:
    """Tests for area tile enumeration methods."""

    def test_tiles_returns_all_tiles(self):
        a = area(1, 1, 2, 2)  # 2x2 area
        tiles = a.tiles()
        assert len(tiles) == 4

        # Check all expected coords are present
        coords = [(t.col, t.row) for t in tiles]
        assert (1, 1) in coords
        assert (1, 2) in coords
        assert (2, 1) in coords
        assert (2, 2) in coords

    def test_tiles_single_tile(self):
        a = area(5, 5, 5, 5)
        tiles = a.tiles()
        assert len(tiles) == 1
        assert tiles[0].col == 5
        assert tiles[0].row == 5

    def test_boundary_tiles_2x2(self):
        a = area(1, 1, 2, 2)
        boundary = a.boundary_tiles()
        # For 2x2, all tiles are boundary tiles
        assert len(boundary) == 4

    def test_boundary_tiles_3x3(self):
        a = area(1, 1, 3, 3)
        boundary = a.boundary_tiles()
        # For 3x3, boundary is 8 tiles (excludes center)
        assert len(boundary) == 8

        coords = [(t.col, t.row) for t in boundary]
        # Center tile (2,2) should NOT be in boundary
        assert (2, 2) not in coords

    def test_boundary_tiles_single_column(self):
        a = area(1, 1, 1, 3)  # 1 column, 3 rows
        boundary = a.boundary_tiles()
        assert len(boundary) == 3


class TestAreaContains:
    """Tests for area containment checking."""

    def test_contains_coord_inside(self):
        a = area(2, 2, 5, 5)
        c = coord(3, 3)
        assert a.contains(c)

    def test_contains_coord_on_boundary(self):
        a = area(2, 2, 5, 5)
        c = coord(2, 2)  # Top-left corner
        assert a.contains(c)

        c2 = coord(5, 5)  # Bottom-right corner
        assert a.contains(c2)

    def test_contains_coord_outside(self):
        a = area(2, 2, 5, 5)
        c = coord(1, 1)
        assert not a.contains(c)

        c2 = coord(6, 6)
        assert not a.contains(c2)


class TestAreaStringRepresentation:
    """Tests for area string output."""

    def test_str(self):
        a = area(1, 2, 3, 4)
        assert str(a) == "1/2->3/4"
