import pathlib

from drawBot import fill, height, newPage, rect, saveImage, stroke, width

# <include> ----------------------------------------
from drawBotGrid import Grid, imageAtSize

newPage("A4Landscape")

grid = Grid.from_margins((-60, -40, -60, -40), column_subdivisions=2, row_subdivisions=1)


img_path = "drawBotGrid/docs/drawMech-small.jpg"
imageAtSize(img_path, (grid.columns[0], grid.rows[0], grid.columns * 1, grid.rows * 1))
imageAtSize(img_path, (grid.columns[1], grid.rows[0], grid.columns * 1, grid.rows * 1), preserve_proportions=False)

# </include> ----------------------------------------

fill(None)
stroke(0.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
