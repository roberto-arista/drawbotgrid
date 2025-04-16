import drawBot as db

from . import text
from .aliases import (
    Box,
    ColumnDescription,
    TableData,
    TableItem,
    TableRow,
    TableRows,
)


class Table:
    def __init__(
        self,
        possize: Box,
        items: TableData,
        column_descriptions: list[ColumnDescription],
        base_row_height: float = 12,
        margins: float = 6,
        header_gap: float = 0,
    ) -> None:
        self.x, self.y, self.width, self.input_height = possize
        self.margins = margins
        self.columns_manager = ColumnsManager(self, column_descriptions)
        self.rows_manager = RowsManager(self, items, base_row_height=base_row_height, header_gap=header_gap)
        self.actual_height = self.rows_manager.total_height
        self.vertical_align = False
        self._show_header: bool = True

    def draw_columns_lines(self) -> None:
        for x in self.columns_manager.separator_origins:
            db.line((x, self.y), (x, self.y + self.height))

    def draw_rows_lines(self) -> None:
        for y in self.rows_manager.separator_origins:
            db.line((self.x, y), (self.x + self.width, y))

    def draw_frame(self) -> None:
        db.rect(self.x, self.y, self.width, self.height)

    def draw_rows_frame(self) -> None:
        db.line((self.x, self.y), (self.x + self.width, self.y))
        db.line((self.x, self.y + self.height), (self.x + self.width, self.y + self.height))

    def draw_columns_frame(self) -> None:
        db.line((self.x, self.y), (self.x, self.y + self.height))
        db.line((self.x + self.width, self.y), (self.x + self.width, self.y + self.height))

    def draw_content(self) -> None:
        for contents, cells in zip(self.cell_values, self.cell_rects):
            for content, cell in zip(contents, cells):
                if self.vertical_align:
                    text.verticalAlignTextBox(content, cell.raw_textbox, vertical_align="center")
                else:
                    db.textBox(content, cell.textbox)

    def draw_header_background(self) -> None:
        db.rect(*self.header_rect)

    def draw_content_background(self) -> None:
        db.rect(*self.content_rect)

    @property
    def show_header(self) -> bool:
        return self._show_header

    @show_header.setter
    def show_header(self, value: bool) -> None:
        self._show_header = value
        self.rows_manager.show_header = value

    @property
    def height(self) -> float:
        return -self.rows_manager.total_height

    @property
    def cell_rects(self) -> list[list["CellBox"]]:
        out: list[list[CellBox]] = []
        for y, height in zip(self.rows_manager.origins, self.rows_manager.heights):
            row: list[CellBox] = []
            for x, width in zip(self.columns_manager.origins, self.columns_manager.widths):
                row.append(CellBox(self, (x, y, width, height)))
            out.append(row)
        return out

    @property
    def cell_values(self) -> TableRows:
        return self.rows_manager.cell_values

    @property
    def table_rect(self) -> Box:
        return self.rows_manager.table_rect

    @property
    def header_rect(self) -> Box:
        return self.rows_manager.header_rect

    @property
    def content_rect(self) -> Box:
        return self.rows_manager.content_rect

    @property
    def content_rects(self) -> list[Box]:
        return self.rows_manager.content_rects


class ColumnsManager:
    WIDTH_KEY = "width"
    TITLE_KEY = "title"
    LABEL_KEY = "label"

    def __init__(self, parent: Table, column_descriptions: list[ColumnDescription]) -> None:
        self.table = parent
        self.column_descriptions = column_descriptions
        self.widths = self._calculate_columns_widths()
        self.origins = self._calculate_columns_origins()
        self.titles = self._get_column_descriptions_filtered_key()

    @property
    def rects(self) -> list[Box]:
        return [(x, self.table.y, w, self.table.height) for x, w in zip(self.origins, self.widths)]

    @property
    def separator_origins(self) -> list[float]:
        return self.origins[1:]

    def _get_number_of_flex_columns_width(self) -> int:
        return len([col for col in self.column_descriptions if col.get(self.WIDTH_KEY) is None])

    def _get_sum_of_defined_columns_width(self) -> float:
        return sum(i.get(self.WIDTH_KEY, 0) for i in self.column_descriptions)

    def _calculate_flex_width(self) -> float:
        return (self.table.width - self._get_sum_of_defined_columns_width()) / max(
            1, self._get_number_of_flex_columns_width()
        )

    def _calculate_columns_widths(self) -> list[float]:
        widths: list[float] = []
        flex_width = self._calculate_flex_width()
        for col in self.column_descriptions:
            width = col.get(self.WIDTH_KEY, flex_width)
            widths.append(width)
        return widths

    def _calculate_columns_origins(self) -> list[float]:
        origins: list[float] = []
        current_x = self.table.x
        for width in self.widths:
            origins.append(current_x)
            current_x += width
        return origins

    def _get_column_descriptions_filtered_key(self) -> list[str]:
        return [i[self.TITLE_KEY] for i in self.column_descriptions]

    def get_column_labels(self) -> list[str]:
        return [i.get(self.LABEL_KEY, i[self.TITLE_KEY]) for i in self.column_descriptions]

    def filter_row_content(self, row: TableItem) -> TableRow:
        return [row.get(k, "") for k in self.titles]


class RowsManager:
    def __init__(self, parent: Table, rows: TableData, base_row_height: float = 12, header_gap: float = 0) -> None:
        self.table = parent
        self.rows = [self.table.columns_manager.get_column_labels()] + self.filter_rows_content(rows)
        self.base_row_height = base_row_height
        self.header_gap = header_gap
        self._show_header = True
        self.heights = self._calculate_rows_heights()
        self.origins = self._calculate_rows_origins()

    @property
    def show_header(self) -> bool:
        return self._show_header

    @show_header.setter
    def show_header(self, value: bool) -> None:
        self._show_header = value
        self.heights = self._calculate_rows_heights()
        self.origins = self._calculate_rows_origins()

    @property
    def rects(self) -> list[Box]:
        return [(self.table.x, y, self.table.width, h) for y, h in zip(self.origins, self.heights)]

    @property
    def separator_origins(self) -> list[float]:
        return self.origins[:-1]

    @property
    def total_height(self) -> float:
        return -self.origins[-1] + self.table.y

    @property
    def content_height(self) -> float:
        return sum(self.heights[1:])

    @property
    def header_rect(self) -> Box:
        return (self.table.x, self.origins[0], self.table.width, self.heights[0])

    @property
    def content_rect(self) -> Box:
        return (self.table.x, self.origins[-1], self.table.width, self.content_height)

    @property
    def content_rects(self) -> list[Box]:
        return [(self.table.x, y, self.table.width, h) for y, h in zip(self.origins[1:], self.heights[1:])]

    @property
    def table_rect(self) -> Box:
        return (self.table.x, self.origins[-1], self.table.width, self.total_height)

    @property
    def content_values(self) -> TableRows:
        return self.rows[1:]

    @property
    def header_values(self) -> TableRow:
        return self.rows[0]

    @property
    def cell_values(self) -> TableRows:
        if self.show_header:
            return self.rows
        else:
            return self.content_values

    def filter_rows_content(self, rows: TableData) -> TableRows:
        return [self.table.columns_manager.filter_row_content(row) for row in rows]

    def _calculate_rows_heights(self) -> list[float]:
        heights: list[float] = []
        if self.show_header:
            rows = self.rows
        else:
            rows = self.rows[1:]
        for row in rows:
            heights.append(self._calculate_row_height(row))
        return heights

    def _calculate_row_height(self, row: TableRow) -> float:
        heights: list[float] = []
        for content, width in zip(row, self.table.columns_manager.widths):
            heights.append(self._calculate_cell_height(content, width))
        return max(heights)

    def _calculate_cell_height(self, content: str, width: float) -> float:
        with db.savedState():
            return -db.textSize(content, width=width)[1] + self.table.margins * 2


class CellBox:
    def __init__(self, parent: Table, possize: Box) -> None:
        self.table = parent
        self.x, self.y, self.width, self.height = possize

    @property
    def rect(self) -> Box:
        return (self.x, self.y, self.width, self.height)

    @property
    def textbox(self) -> Box:
        return (
            self.x + self.table.margins,
            self.y + self.table.margins,
            self.width - self.table.margins * 2,
            self.height - self.table.margins * 2,
        )

    @property
    def raw_textbox(self) -> Box:
        return (
            self.x + self.table.margins,
            self.y,
            self.width - self.table.margins * 2,
            self.height,
        )
