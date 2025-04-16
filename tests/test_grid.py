import drawBot as db
import pytest

from drawBotGrid.grid import AbstractArea, ColumnGrid, Grid, RowGrid


class TestAbstractArea:
    def test_init(self):
        area = AbstractArea((10, 20, 100, 200))
        assert area.x == 10
        assert area.y == 20
        assert area.width == 100
        assert area.height == 200

    def test_from_margins(self):
        with db.drawing():
            db.newPage(1000, 1000)
            area = AbstractArea.from_margins((-50, -50, -50, -50))
            assert area.x == 50
            assert area.y == 50
            assert area.width == 900
            assert area.height == 900

    def test_properties(self):
        area = AbstractArea((10, 20, 100, 200))
        assert area.top == 220  # y + height
        assert area.bottom == 20  # y
        assert area.left == 10  # x
        assert area.right == 110  # x + width
        assert area.center == (60, 120)  # (x + width/2, y + height/2)
        assert area.horizontal_center == 60
        assert area.vertical_center == 120


class TestColumnGrid:
    def test_init(self):
        grid = ColumnGrid((10, 20, 100, 200), subdivisions=4, gutter=5)
        assert grid.columns == 4
        assert grid.column_width == pytest.approx(21.25)

    def test_start_end_points(self):
        grid = ColumnGrid((10, 20, 100, 200))
        assert grid._start_point == 10  # left
        assert grid._end_point == 110  # right

    def test_getitem(self):
        grid = ColumnGrid((0, 0, 100, 100), subdivisions=4, gutter=5)
        # First column starts at 0
        assert grid[0] == 0
        # Second column starts at first column width + gutter
        assert grid[1] == pytest.approx(26.25)  # 21.25 + 5
        # Test slice
        columns = grid[1:3]
        assert len(columns) == 2
        assert columns[0] == pytest.approx(26.25)
        assert columns[1] == pytest.approx(52.5)  # 26.25 + 21.25 + 5


class TestRowGrid:
    def test_init(self):
        grid = RowGrid((10, 20, 100, 200), subdivisions=4, gutter=5)
        assert grid.rows == 4
        assert grid.row_height == pytest.approx(46.25)  # (200 - 15) / 4

    def test_start_end_points(self):
        grid = RowGrid((10, 20, 100, 200))
        assert grid._start_point == 20  # bottom
        assert grid._end_point == 220  # top

    def test_getitem(self):
        grid = RowGrid((0, 0, 100, 100), subdivisions=4, gutter=5)
        # First row starts at bottom
        assert grid[0] == 0
        # Second row starts at first row height + gutter
        assert grid[1] == 26.25
        # Test negative indexing
        assert grid[-1] == 100


class TestGrid:
    def test_init(self):
        grid = Grid((10, 20, 100, 200), column_subdivisions=4, row_subdivisions=3, column_gutter=5, row_gutter=10)
        assert isinstance(grid.column_grid, ColumnGrid)
        assert isinstance(grid.row_grid, RowGrid)
        assert grid.column_grid.subdivisions == 4
        assert grid.row_grid.subdivisions == 3
        assert grid.column_grid.gutter == 5
        assert grid.row_grid.gutter == 10

    def test_getitem(self):
        grid = Grid((0, 0, 100, 100), column_subdivisions=4, row_subdivisions=4)
        # Test getting a specific point in the grid
        x, y = grid[(1, 2)]  # Second column, third row
        assert x == pytest.approx(27.5)
        assert y == pytest.approx(55)
