# aliases.py
from typing import Literal, TypeAlias

# Basic geometric types
Box = Margins = tuple[float, float, float, float]
Point: TypeAlias = tuple[float, float]  # x, y coordinates

# Text alignment types
HorizontalAlign = Literal["left", "right", "center"]
VerticalAlign = Literal["top", "bottom", "center"]

# Image types
ImageFitting = Literal["fit", "fill", "crop"]
ImageAnchor = tuple[str, str]  # (horizontal, vertical)

# Table types
ColumnDescription: TypeAlias = dict[str, str | float | None]
TableItem: TypeAlias = dict[str, str]
TableData: TypeAlias = list[TableItem]
TableRow: TypeAlias = list[str]
TableRows: TypeAlias = list[TableRow]
