import pathlib

from drawBot import fill, font, fontSize, height, lineHeight, newPage, rect, savedState, saveImage, stroke, width

# <include> ----------------------------------------
from drawBotGrid import BaselineGrid, ColumnGrid, baselineGridTextBox

newPage("A4Landscape")

# </include> ----------------------------------------
with savedState():
    fill(1, 1, 1, 0.5)
    rect(0, 0, width(), height())
# <include> ----------------------------------------

columns = ColumnGrid.from_margins((-50, -50, -50, -50), subdivisions=3, gutter=10)
baselines = BaselineGrid.from_margins((0, 0, 0, 0), line_height=40)
font("Georgia")
fontSize(34)
lineHeight(40)
baselineGridTextBox(
    "HELLO\nFROM UP\nTHERE\n(SORT OF)",
    (columns[0], columns.bottom, columns * 1, columns.height),
    baselines,
    vertical_align="top",
    align="center",
)

baselineGridTextBox(
    "HELLO\nFROM MID\nTHERE\n(SORT OF)",
    (columns[1], columns.bottom, columns * 1, columns.height),
    baselines,
    vertical_align="center",
    align="center",
)

baselineGridTextBox(
    "HELLO\nFROM DOWN\nTHERE\n(SORT OF)",
    (columns[2], columns.bottom, columns * 1, columns.height),
    baselines,
    vertical_align="bottom",
    align="center",
)

columns.draw(show_index=True)
baselines.draw()
# </include> ----------------------------------------

fill(None)
stroke(0.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, {"imageResolution": 144})
