import drawBot as db
import pytest

from drawBotGrid.grid import AbstractArea, BaselineGrid, ColumnGrid, Grid, RowGrid


def test_abstract_area_init() -> None:
    area = AbstractArea((10, 20, 100, 200))
    assert area.x == 10
    assert area.y == 20
    assert area.width == 100
    assert area.height == 200


def test_abstract_area_from_margins() -> None:
    with db.drawing():
        db.newPage(1000, 1000)
        area = AbstractArea.from_margins((-50, -50, -50, -50))
        assert area.x == 50
        assert area.y == 50
        assert area.width == 900
        assert area.height == 900


def test_abstract_area_properties() -> None:
    area = AbstractArea((10, 20, 100, 200))
    assert area.top == 220  # y + height
    assert area.bottom == 20  # y
    assert area.left == 10  # x
    assert area.right == 110  # x + width
    assert area.center == (60, 120)  # (x + width/2, y + height/2)
    assert area.horizontal_center == 60
    assert area.vertical_center == 120


def test_columngrid_init() -> None:
    grid = ColumnGrid((10, 20, 100, 200), subdivisions=4, gutter=5)
    assert grid.columns == 4
    assert grid.column_width == 21.25


def test_columngrid_start_end_points() -> None:
    grid = ColumnGrid((10, 20, 100, 200))
    assert grid._start_point == 10  # left
    assert grid._end_point == 110  # right


def test_columngrid_getitem() -> None:
    grid = ColumnGrid((0, 0, 100, 100), subdivisions=4, gutter=5)
    # First column starts at 0
    assert grid[0] == 0
    # Second column starts at first column width + gutter
    assert grid[1] == 26.25  # 21.25 + 5
    # Test slice
    columns = grid[1:3]
    assert len(columns) == 2
    assert columns[0] == 26.25
    assert columns[1] == 52.5  # 26.25 + 21.25 + 5


def test_rowgrid_init() -> None:
    grid = RowGrid((10, 20, 100, 200), subdivisions=4, gutter=5)
    assert grid.rows == 4
    assert grid.row_height == 46.25  # (200 - 15) / 4


def test_rowgrid_start_end_points() -> None:
    grid = RowGrid((10, 20, 100, 200))
    assert grid._start_point == 20  # bottom
    assert grid._end_point == 220  # top


def test_rowgrid_getitem() -> None:
    grid = RowGrid((0, 0, 100, 100), subdivisions=4, gutter=5)
    # First row starts at bottom
    assert grid[0] == 0
    # Second row starts at first row height + gutter
    assert grid[1] == 26.25
    # Test negative indexing
    assert grid[-1] == 100

    with pytest.raises(TypeError):
        grid["hello"]  # type: ignore


@pytest.fixture
def grid() -> Grid:
    return Grid((10, 20, 100, 200), column_subdivisions=4, row_subdivisions=4, column_gutter=10, row_gutter=10)


def test_grid_init(grid) -> None:
    assert isinstance(grid.columns, ColumnGrid)
    assert isinstance(grid.rows, RowGrid)
    assert grid.columns.subdivisions == 4
    assert grid.rows.subdivisions == 4
    assert grid.columns.gutter == 10
    assert grid.rows.gutter == 10


def test_grid_getitem(grid) -> None:
    # Test getting a specific point in the grid
    x, y = grid[(1, 2)]  # Second column, third row
    assert x == 37.5
    assert y == 125


def test_grid_len(grid) -> None:
    assert len(grid) == 16


def test_grid_properties(grid) -> None:
    assert grid.row_height == 42.5
    assert grid.column_width == 17.5


def test_grid_iter(grid) -> None:
    for i, _ in enumerate(grid):
        pass
    assert i == 15  # 16-1


@pytest.fixture
def baseline_grid() -> BaselineGrid:
    return BaselineGrid((0, 0, 100, 200), line_height=10)


def test_baseline_grid_init(baseline_grid: BaselineGrid) -> None:
    assert baseline_grid.x == 0
    assert baseline_grid.y == 0
    assert baseline_grid.height == 200
    assert baseline_grid.width == 100
    assert baseline_grid.top == 200
    assert baseline_grid.bottom == 0
    assert baseline_grid.center == (50, 100)
    assert baseline_grid.line_height == 10


def test_baseline_grid_getitem(baseline_grid: BaselineGrid) -> None:
    assert baseline_grid[2] == 180
    assert baseline_grid[::] == list(reversed(range(0, 201, 10)))
    assert baseline_grid[::-1] == list(range(0, 201, 10))
    assert baseline_grid[1::2] == [190, 170, 150, 130, 110, 90, 70, 50, 30, 10]
    with pytest.raises(TypeError):
        baseline_grid["hello"]  # type: ignore


def test_baseline_grid_len(baseline_grid: BaselineGrid) -> None:
    assert len(baseline_grid) == 21


def test_baseline_grid_properties(baseline_grid: BaselineGrid) -> None:
    assert baseline_grid.baseline_index_from_coordinate(105) == 10
    assert baseline_grid.closest_line_above_coordinate(105) == 110
    assert baseline_grid.closest_line_below_coordinate(105) == 100


def test_baseline_grid_iter(baseline_grid: BaselineGrid) -> None:
    for i, _ in enumerate(baseline_grid):
        pass
    assert i == 20  # 21-1
