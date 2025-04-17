# drawBotGrid

**drawBotGrid** is a small library that make grid based layout easy in the always amazing [DrawBot](https://www.drawbot.com).



## install

In DrawBot, open the package manager with the menu Python -> Install Python Packages...

Enter the following url `git+https://github.com/mathieureguer/drawbotgrid` and press `go`.

For drawBot as a command line module, just enter the following terminal command: 
`pip install git+https://github.com/mathieureguer/drawbotgrid`



## ColumnGrid

![ColumnGrid intro](drawBotGrid/docs/snippet_00_ColumnGrid_intro.png)

`ColumnGrid((x, y, h, w), subdivisions=8, gutter=10)` divides the page in a given number of columns, separated by a gutter, making it easy to retrieve absolute x coordinates within the page.

`ColumnGrid` is callable by index, just like a list.  `ColumnGrid[2]` will return the x coordinate of the *left* of the third column.
Negative indexes works, `ColumnGrid[-1]` will return the x coordinate of *right* of the last column.

```python
<insert-file: snippet_10_ColumnGrid_basics.py>
```

![ColumnGrid basic](drawBotGrid/docs/snippet_10_ColumnGrid_basics.png)


`ColumnGrid` is also multipliable. `ColumnGrid * 3` will return the width of 3 columns, including the 2 separating gutters. `ColumnGrid * 1` will return the width of a single column, with no gutter. Negative mutlipliers work as well. 

```python
<insert-file: snippet_20_ColumnGrid_multiply.py>
```

![ColumnGrid multiply](drawBotGrid/docs/snippet_20_ColumnGrid_multiply.png)


Conviniently, instead of creating a `ColumnGrid` from its `(x, y, w, h)` coordinates, you can initiate it from its margin values relative to the document with `ColumnGrid.from_margint((left_margin, bottom_margin, right_margin, top_margin), subdivisions, gutter)`. Margins are expressed with negative values (following [Vanilla conventions](https://github.com/robotools/vanilla)).

Handy coordinates can be easyly accessed with `ColumnGrid.bottom`, `ColumnGrid.top`, `ColumnGrid.left`, `ColumnGrid.right`, `ColumnGrid.width`, `ColumnGrid.height`.


```python
<insert-file: snippet_30_ColumnGrid_margins.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_30_ColumnGrid_margins.png)




## RowGrid

`RowGrid((x, y, h, w), subdivisions=8, gutter=10)` divides the page in a given number of rows, separated by a gutter, making it easy to retrieve absolute y coordinates within the page. It works like `ColumnGrid` but for horizontal rows.


```python
<insert-file: snippet_40_RowGrid_basics.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_40_RowGrid_basics.png)




## Grid

`Grid((x, y, h, w),, column_subdivisions=8, row_subdivisions=8, column_gutter=10, row_gutter=10)` combines the powers of `ColumnGrid` and `RowGrid` in a single object, for all your grid needs.

The underlying `ColumnGrid` and `RowGrid` can be accesed through `Grid.columns` and `Grid.rows`, repectiveley. 

```python
<insert-file: snippet_50_Grid_basics.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_50_Grid_basics.png)


If you're feeling adventurous, `Grid.column` and `Grid.row` can be called directly by a tuple of indexes. `Grid[(1, 5)]` will return the coordinate of the column at index 1 and the row at index 5.

`Grid` can also be multiplied by a tupple. `Grid*(2, 4)` will return the width value of 2 column and the height value of 4 rows (including the required gutters).

```python
<insert-file: snippet_60_Grid_advanced.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_60_Grid_advanced.png)

If you made it this far, you likely like grids, so we placed some grids inside your grid.

```python
<insert-file: snippet_70_Grid_inception.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_70_Grid_inception.png)




## BaselineGrid

`BaselineGrid((x, y, h, w), possize, line_height)` is a grid helper dedicated to text (it is limited to writing systems organised arround horizontal baselines).

Unlike `RowGrid`, `BaselineGrid` has no gutter and a fixed subdivison width.

Another notable difference is that folowing the top down direction of Latin text paragraphs, the first line,`BaselineGrid[0]` is a the top of the grid, rather than its bottom. 

```python
<insert-file: snippet_80_BaselineGrid_basics.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_80_BaselineGrid_basics.png)




## baselineGridTextBox

`BaselineGrid`only becomes usefull if you can snap text to it. `baselineGridTextBox(text, (x, y, w, h), baselineGrid, align_first_line_only=False, align="left")` is a `textBox` that takes a `BaselineGrid` object as an additonal argument. It will adjust the text `lineHeight` in order ot make it snap to the baseline grid.

```python
<insert-file: snippet_100_BaselineGridTextBox_basics.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_100_BaselineGridTextBox_basics.png)

`BaselineGridTextBox` will try to snap your defined `lineHeight` to the next multiple of its `BaselineGrid.line_height`. That mean you can use the same `BaselineGrid` for multiple size of text if you want to.

```python
<insert-file: snippet_110_BaselineGridTextBox_lineHeight.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_110_BaselineGridTextBox_lineHeight.png)



# columnTextBox

`columnTextBox(text, (x, y, w, h), subdivisions=2, gutter=10, align="left")` is a `textBox` powered by an internal `ColumnGrid`. It flows the given text into multiple columns automatically. Like a normal `textBox`, it returns the overflow text is there is any.


Setting the optional argument `draw_grid=True` will draw the underlying grid.

```python
<insert-file: snippet_120_ColumnTextBox_basics.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_120_ColumnTextBox_basics.png)



#  columnBaselineGridTextBox

`columnBaselineGridTextBox(text, (x, y, w, h), baselineGrid, subdivisions=2, gutter=10, align="left")` is a `columnTextBox` that takes a `BaselineGrid` object as an additonal argument. It will adjust the text `lineHeight` in order ot make it snap to the baseline grid.


```python
<insert-file: snippet_130_ColumnBaselineGridTextBox_basics.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_130_ColumnBaselineGridTextBox_basics.png)


# verticalAlignTextBox
`verticalAlignTextBox(text, (x, y, w, h), vertical_align="top", align="left")` is a `textBox` that takes `vertical_align` as an additonal argument. Possible values are `"top"`, `"center"` and `"bottom"`.

```python
<insert-file: snippet_140_verticalAlignTextBox_basics.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_140_verticalAlignTextBox_basics.png)

# textOverflowTestMode

Sometimes, you need to know if a textBox like object is overflowing before drawing it (you may want to adjust line spacing, or the number columns accordingly).
`textOverflowTestMode(True)` will trigger a special mode where all drawBotGrid textBox related object will return overflow but not be drawn on the page. `textOverflowTestMode(False)` will reverse back to default, where textBox related objects are drawn as usual.

```python
<insert-file: snippet_148_textOverflowTestMode.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_148_textOverflowTestMode.png)

*Note: This departs quite a bit from the DrawBot way handling text overflow testing and is subject to change :)*

# imageBox

`imageBox(image_path, (x, y, w, h), fitting="fit", anchor=("left", "top"), draw_box_frame=False)` behaves like `textBox` but for images.
By default, it takes an image or imageObject and scale it so that it fits within a given box. The `fitting` argument can be `fit`, `fill` or `crop`.

- `fitting="fit"` will scale the image so that it fits within the box.
- `fitting="fill"` will scale the image so that it fill the entire box and that at least the image width or height is displayed entirely.
- `fitting="crop"` will show the image at full size, and crop it so that it tays within the box.

```python
<insert-file: snippet_150_imageBox_fitting.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_150_imageBox_fitting.png)

### fitting=fit

```python
<insert-file: snippet_160_imageBox_fit.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_160_imageBox_fit.png)

### fitting=fill

```python
<insert-file: snippet_170_imageBox_fill.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_170_imageBox_fill.png)

### fitting=crop

```python
<insert-file: snippet_180_imageBox_crop.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_180_imageBox_crop.png)

### anchors

By default, when cropped or smaller than the box, the image is anchored to the top left of a the imageBox. An `anchor=("left", "top")` argument can be provided to adjust the origin of the image within the box. `anchor` must be a tupple describing the horizontal and vertical positioning. Possible values for horizontal positioning are `"left"`, `"center"` or `"right"`, possible values for vertical positioning are `"top"`, `"center"` or `"bottom"`.

```python
<insert-file: snippet_190_imageBox_anchors.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_190_imageBox_anchors.png)

Additionally, when using `fitting="crop"`, a `scale` argument can be provided to control the size at which the image will be displayed inside the `ìmageBox`.

When using `fitting="fill"` or `fitting="fit"`, the scale argument will be ignored, as the scale is automatically calculated against the box size.

```python
<insert-file: snippet_200_imageBox_scale.py>
```

![ColumnGrid margins](drawBotGrid/docs/snippet_200_imageBox_scale.png)


# Development

- There is a pre-commit hook we suggest to use, in order to do that, you have to set the hook folder with `git config core.hooksPath .githooks` and then flag the `pre-commit` script as executable with `chmod 755 .githooks/pre-commit`. To check that everything is in order you can run `git hook run pre-commit`. The hook takes care of formatting the codebase and re-run all the documentation snippets.