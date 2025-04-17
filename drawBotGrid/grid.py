import math
from typing import Any, Iterator, Self, overload

import drawBot as db
from drawBot.aliases import RGBAColorTuple

from .aliases import Box, Margins


class AbstractArea:
    """
    This is mostly a PosSize, margin manager

    """

    def __init__(self, possize: Box) -> None:
        self._x, self._y, self._width, self._height = possize

    @classmethod
    def from_margins(cls, margins: Margins, *args: Any, **kwargs: Any) -> Self:
        left_margin, bottom_margin, right_margin, top_margin = margins
        possize = (
            -left_margin,
            -bottom_margin,
            db.width() + left_margin + right_margin,
            db.height() + bottom_margin + top_margin,
        )
        return cls(possize, *args, **kwargs)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @property
    def top(self) -> float:
        """
        the absolute y value of the top of the grid
        """
        return self._y + self._height

    @property
    def bottom(self) -> float:
        """
        the absolute y value of the bottom of the grid
        """
        return self.y

    @property
    def left(self) -> float:
        """
        the absolute x value of the left of the grid
        """
        return self.x

    @property
    def right(self) -> float:
        """
        the absolute x value of the right of the grid
        """
        return self.x + self.width

    @property
    def center(self) -> tuple[float, float]:
        return self.horizontal_center, self.vertical_center

    @property
    def horizontal_center(self) -> float:
        return self.x + self.width / 2

    @property
    def vertical_center(self) -> float:
        return self.y + self.height / 2

    draw_color: RGBAColorTuple = (1, 0, 1, 1)

    def draw(self, show_index: bool = False) -> None:
        with db.savedState():
            db.stroke(*self.draw_color)
            db.fill(None)
            db.strokeWidth(0.5)
            self.draw_frame()

        if show_index:
            with db.savedState():
                db.stroke(None)
                db.fill(*self.draw_color)
                db.fontSize(5)
                self.draw_indexes()

    def draw_frame(self) -> None:  # pragma: no cover
        raise NotImplementedError

    def draw_indexes(self) -> None:  # pragma: no cover
        raise NotImplementedError


class AbstractGutterGrid(AbstractArea):
    """
    this is meant to be subclassed by Columns and Grid

    """

    def __init__(self, possize: Box, subdivisions: int = 8, gutter: float = 10) -> None:
        super().__init__(possize)
        self.subdivisions = subdivisions
        self.gutter = gutter

    @property
    def _start_point(self) -> float:  # pragma: no cover
        raise NotImplementedError

    @property
    def _end_point(self) -> float:  # pragma: no cover
        raise NotImplementedError

    @property
    def _reference_dimension(self) -> float:
        return self._end_point - self._start_point

    @property
    def subdivision_dimension(self) -> float:
        """
        the absolute dimension of a single subdivision within the grid
        """
        return (self._reference_dimension - ((self.subdivisions - 1) * self.gutter)) / self.subdivisions

    def span(self, span: float) -> float:
        """
        the absolute dimension of a span of consecutive subdivisions within the grid,
        including their inbetween gutters
        """
        assert isinstance(span, (float, int))
        if span >= 0:
            return self.subdivision_dimension * span + self.gutter * (math.ceil(span) - 1)
        else:
            return self.subdivision_dimension * span + self.gutter * (math.ceil(span) + 1)

    @overload
    def __getitem__(self, key: int) -> float: ...

    @overload
    def __getitem__(self, key: slice) -> list[float]: ...

    def __getitem__(self, key):
        if isinstance(key, slice):
            values = []
            for i in range(*key.indices(len(self))):
                values.append(self[i])
            return values

        elif isinstance(key, int):
            index = key
            if index >= 0:
                return self._start_point + index * (self.gutter + self.subdivision_dimension)
            else:
                return self._end_point + (index + 1) * (self.gutter + self.subdivision_dimension)

        else:
            raise TypeError(f"Wrong value input: {key}.")

    def __len__(self) -> int:
        return self.subdivisions

    def __iter__(self) -> Iterator[float]:
        for i in range(self.subdivisions):
            value = self.__getitem__(i)
            assert isinstance(value, float | int)
            yield value

    def __mul__(self, factor: float) -> float:
        return self.span(factor)


class ColumnGrid(AbstractGutterGrid):
    """
    Will return coordinates according to a column based grid.

    Columns are refered to by index, accessing a column index will return its absolute x coordinate in the page.

    ```
    my_columns = Columns((50, 50, 900, 900), 8, 10)
    print(my_columns[3])
    > 505.0
    ```

    Negative indexes refer the right part of a column, starting from the right of the page.

    ```
    my_columns = Columns((50, 50, 900, 900), 8, 10)
    print(my_columns[-2])
    > 798.33
    ```

    The grid can return the total width of a span of consecutive columns, including the related inbween gutters

    ```
    my_columns = Columns((50, 50, 900, 900), 8, 10)
    print(my_columns.span(4))
    > 596.66
    ```

    The whole point is to use this as coordinate helpers to draw shapes of course

    ```
    my_columns = Columns((50, 50, 900, 900), 8, 10)
    fill(0, 1, 0, .5)
    rect(my_columns[1], my_columns.bottom, my_columns.span(3), my_columns.height)
    fill(1, 0, 0, .5)
    rect(my_columns[0], my_columns.top, my_columns.span(3), -200)
    rect(my_columns[2], my_columns.top-200, my_columns.span(1), -200)
    rect(my_columns[5], my_columns.top-400, my_columns.span(2), -200)
    ```

    The columns grid can also draw itself, if necessary
    ```
    my_columns = Columns((50, 50, 900, 900), 8, 10)
    fill(None)
    stroke(1, 0, 1)
    strokeWidth(1)
    my_columns.draw()
    ```

    """

    @property
    def columns(self) -> int:
        return self.subdivisions

    @property
    def column_width(self) -> float:
        return self.subdivision_dimension

    @property
    def _start_point(self) -> float:
        return self.left

    @property
    def _end_point(self) -> float:
        return self.right

    def draw_frame(self):
        for column in self:
            db.rect(column, self.bottom, self.column_width, self.height)

    def draw_indexes(self):
        for i, column in enumerate(self):
            db.text(str(i), (column + 2, self.bottom + 2))


class RowGrid(AbstractGutterGrid):
    """
    Row-based grid implementation

    """

    @property
    def rows(self) -> int:
        return self.subdivisions

    @property
    def row_height(self) -> float:
        return self.subdivision_dimension

    @property
    def _start_point(self) -> float:
        return self.bottom

    @property
    def _end_point(self) -> float:
        return self.top

    def draw_frame(self) -> None:
        for row in self:
            db.line((self.left, row), (self.right, row))

    def draw_indexes(self) -> None:
        for index, row in enumerate(self):
            db.text(str(index), (self.left + 2, row + 2))


class Grid(AbstractGutterGrid):
    """
    Combined column and row grid

    """

    def __init__(
        self,
        possize: Box,
        column_subdivisions: int = 8,
        row_subdivisions: int = 8,
        column_gutter: float = 10,
        row_gutter: float = 10,
    ) -> None:
        self.columns = ColumnGrid(possize, column_subdivisions, column_gutter)
        self.rows = RowGrid(possize, row_subdivisions, row_gutter)
        super().__init__(possize)

    @property
    def _reference_dimension(self) -> float:  # pragma: no cover
        return 0.0  # Not used in this implementation

    @property
    def _start_point(self) -> float:  # pragma: no cover
        return 0.0  # Not used in this implementation

    @property
    def _end_point(self) -> float:  # pragma: no cover
        return 0.0  # Not used in this implementation

    @property
    def column_width(self) -> float:
        return self.columns.column_width

    @property
    def row_height(self) -> float:
        return self.rows.row_height

    @property
    def subdivision_dimension(self) -> float:  # pragma: no cover
        return 0.0  # Not used in this implementation

    def column_span(self, span: float) -> float:
        return self.columns.span(span)

    def row_span(self, span: float) -> float:
        return self.rows.span(span)

    def span(self, column_span_row_span: tuple[float, float]) -> tuple[float, float]:
        column_span, row_span = column_span_row_span
        return self.column_span(column_span), self.row_span(row_span)

    def __getitem__(self, index: tuple[int, int]) -> tuple[float, float]:
        column_index, row_index = index
        assert isinstance(column_index, int) and isinstance(row_index, int)
        x = self.columns[column_index]
        y = self.rows[row_index]
        assert isinstance(x, float) and isinstance(y, float)
        return x, y

    def __len__(self) -> int:
        return len(self.columns) * len(self.rows)

    def __iter__(self) -> Iterator[tuple[float, float]]:
        for row in self.rows:
            for col in self.columns:
                yield (col, row)

    def draw_frame(self) -> None:
        self.columns.draw_frame()
        self.rows.draw_frame()

    def draw_indexes(self) -> None:
        for index_col, col in enumerate(self.columns):
            for index_row, row in enumerate(self.rows):
                db.text(f"({index_col}, {index_row})", (col + 2, row + 2))


class BaselineGrid(AbstractArea):
    """
    Baseline grid implementation

    """

    def __init__(self, possize: Box, line_height: float) -> None:
        self.input_possize = possize
        super().__init__(possize)
        self.line_height = line_height

    @property
    def _start_point(self) -> float:
        return self.top

    @property
    def _end_point(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        """the absolute y value of the bottom of the grid"""
        value = self[-1]
        assert isinstance(value, float | int)
        return value

    @property
    def height(self) -> float:
        """height is overwritten with the actual distance from last to first line"""
        return self.top - self.bottom

    @property
    def _reference_dimension(self) -> float:
        return self._end_point - self._start_point

    @property
    def subdivisions(self) -> int:
        return abs(int(self._reference_dimension // self.subdivision_dimension)) + 1

    @property
    def subdivision_dimension(self) -> float:
        """the absolute dimension of a single subdivision within the grid"""
        return -self.line_height

    def span(self, span: float) -> float:
        """
        the absolute dimension of a span of consecutive subdivisions within the grid,
        including their inbetween gutters
        """
        return span * self.subdivision_dimension

    def baseline_index_from_coordinate(self, y_coordinate: float) -> int | None:
        for i, line in sorted(enumerate(self)):
            if y_coordinate >= line:
                return i

    def closest_line_below_coordinate(self, y_coordinate: float) -> float | None:
        for i, line in sorted(enumerate(self)):
            if y_coordinate >= line:
                return line

    def closest_line_above_coordinate(self, y_coordinate: float) -> float | None:
        for i, line in sorted(enumerate(self)):
            if y_coordinate > line:
                return line + self.line_height

    @overload
    def __getitem__(self, key: int) -> float: ...

    @overload
    def __getitem__(self, key: slice) -> list[float]: ...

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(len(self)))]

        elif isinstance(key, int):
            index = key
            if index >= 0:
                return self._start_point + index * self.subdivision_dimension
            else:
                return self._start_point + len(self) * self.subdivision_dimension + index * self.subdivision_dimension

        else:
            raise TypeError(f"Wrong value input: {key}.")

    def __len__(self) -> int:
        return self.subdivisions

    def __iter__(self) -> Iterator[float]:
        for i in range(self.subdivisions):
            value = self.__getitem__(i)
            assert isinstance(value, float | int)
            yield value

    def __mul__(self, factor: float) -> float:
        return self.span(factor)

    draw_color: RGBAColorTuple = (0, 1, 1, 1)

    def draw_frame(self) -> None:
        for line in self:
            db.line((self.left, line), (self.right, line))

    def draw_indexes(self) -> None:
        for index, line in enumerate(self):
            db.text(str(index), (self.left + 2, line + 2))
