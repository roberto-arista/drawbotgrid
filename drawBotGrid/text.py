import math
from typing import Callable

import drawBot as db
from drawBot.aliases import RGBAColorTuple

from .aliases import Box, HorizontalAlign, Point, VerticalAlign
from .grid import BaselineGrid, ColumnGrid

_textbox_funct: Callable = db.textBox


def set_text_overflow_test_mode(value: bool) -> None:
    global _textbox_funct
    if value is False:
        _textbox_funct = db.textBox
    else:
        _textbox_funct = db.textOverflow


textOverflowTestMode = set_text_overflow_test_mode


def baseline_grid_textBox(
    txt: str,
    box: Box,
    baseline_grid: BaselineGrid,
    align_first_line_only: bool = False,
    align: HorizontalAlign = "left",
    vertical_align: VerticalAlign = "top",
) -> str:
    assert vertical_align in ("top", "bottom", "center")

    with db.savedState():
        box = correct_box_direction(box)
        x, y, w, h = box

        if not align_first_line_only:
            actual_line_height = db.fontLineHeight()
            target_line_height = math.ceil(actual_line_height / baseline_grid.line_height) * baseline_grid.line_height
            set_metric_baseline_height(target_line_height)

        absolute_cap_height = db.fontCapHeight()

        if vertical_align == "top":
            first_line_y = db.textBoxBaselines(txt, box)[0][1]
            current_cap_y = first_line_y + absolute_cap_height
            cap_distance_from_top = y + h - current_cap_y

            highest_possible_first_line = first_line_y + cap_distance_from_top
            target_line = baseline_grid.closest_line_below_coordinate(highest_possible_first_line)

            shift = target_line - first_line_y if target_line is not None else 0

        elif vertical_align == "bottom":
            last_line_y = db.textBoxBaselines(txt, box)[-1][1]
            target_line = baseline_grid.closest_line_above_coordinate(y)
            shift = target_line - last_line_y if target_line is not None else 0

        elif vertical_align == "center":
            lines = db.textBoxBaselines(txt, box)
            mid_line_index = int(len(lines) / 2)
            mid_line_y = lines[mid_line_index][1]
            target_line = baseline_grid.closest_line_below_coordinate(y + h / 2 - absolute_cap_height / 2)
            shift = target_line - mid_line_y if target_line is not None else 0

        overflow = _textbox_funct(txt, (x, y + shift, w, h), align=align)
        return overflow


baselineGridTextBox = baseline_grid_textBox


def column_textBox(
    txt: str,
    box: Box,
    subdivisions: int = 2,
    gutter: float = 10,
    align: HorizontalAlign = "left",
    draw_grid: bool = False,
) -> str:
    return _column_textBox_base(
        txt,
        box,
        baseline_grid=None,
        align_first_line_only=False,
        subdivisions=subdivisions,
        gutter=gutter,
        align=align,
        draw_grid=draw_grid,
    )


columnTextBox = column_textBox


def column_baseline_grid_textBox(
    txt: str,
    box: Box,
    baseline_grid: BaselineGrid,
    align_first_line_only: bool = False,
    subdivisions: int = 2,
    gutter: float = 10,
    align: HorizontalAlign = "left",
    draw_grid: bool = False,
) -> str:
    return _column_textBox_base(
        txt,
        box,
        baseline_grid,
        align_first_line_only=align_first_line_only,
        subdivisions=subdivisions,
        gutter=gutter,
        align=align,
        draw_grid=draw_grid,
    )


columnBaselineGridTextBox = column_baseline_grid_textBox


def _column_textBox_base(
    txt: str,
    box: Box,
    baseline_grid: BaselineGrid | None = None,
    align_first_line_only: bool = False,
    subdivisions: int = 2,
    gutter: float = 10,
    align: HorizontalAlign = "left",
    draw_grid: bool = False,
) -> str:
    columns = ColumnGrid(box, subdivisions=subdivisions, gutter=gutter)
    overflow = txt
    for col in columns:
        if len(overflow) > 0:
            sub_box = (col, columns.bottom, columns * 1, columns.height)
            if baseline_grid:
                overflow = baseline_grid_textBox(overflow, sub_box, baseline_grid, align=align)
            else:
                overflow = _textbox_funct(overflow, sub_box, align=align)

    if draw_grid:
        grid_color: RGBAColorTuple = (0.5, 0, 0.8, 1)
        with db.savedState():
            db.strokeWidth(0.5)

            db.fill(None)
            db.stroke(*grid_color)
            db.rect(*box)

            for col in columns[1:]:
                db.fill(None)
                db.stroke(*grid_color)
                db.line((col - columns.gutter, columns.bottom), (col - columns.gutter, columns.top))
                db.line((col, columns.bottom), (col, columns.top))

            for col in columns[1:]:
                db.fill(None)
                db.stroke(*grid_color)
                start_pt = (col - columns.gutter, columns.bottom)
                end_pt = (col, columns.top)
                text_flow_path = _get_text_flow_path(start_pt, end_pt)
                db.drawPath(text_flow_path)

                db.stroke(None)
                db.fill(*grid_color)
                _draw_point(start_pt, radius=4)
                _draw_point(end_pt, radius=4)

    return overflow


def _get_text_flow_path(xy1: Point, xy2: Point) -> db.BezierPath:
    x_1, y_1 = xy1
    x_2, y_2 = xy2
    off_curve_length = 100
    text_flow_path = db.BezierPath()
    text_flow_path.moveTo((x_1, y_1))
    text_flow_path.curveTo((x_1 + off_curve_length, y_1), (x_2 - off_curve_length, y_2), (x_2, y_2))
    return text_flow_path


def _draw_point(xy: Point, radius: float = 2) -> None:
    x, y = xy
    db.oval(x - radius, y - radius, radius * 2, radius * 2)


def vertical_align_textBox(
    txt: str, box: Box, align: HorizontalAlign | None = None, vertical_align: VerticalAlign = "top"
) -> str:
    assert vertical_align in ("top", "bottom", "center")

    x, y, w, h = correct_box_direction(box)

    absolute_cap_height = db.fontCapHeight()

    if vertical_align == "top":
        first_line_y = db.textBoxBaselines(txt, box)[0][1]
        target_line = y + h - absolute_cap_height
        shift = target_line - first_line_y

    elif vertical_align == "bottom":
        last_line_y = db.textBoxBaselines(txt, box)[-1][1]
        target_line = y
        shift = target_line - last_line_y

    elif vertical_align == "center":
        # maybe there is more refined solution here
        lines = db.textBoxBaselines(txt, box)

        top = lines[0][1] + absolute_cap_height
        bottom = lines[-1][1]
        text_h = top - bottom
        margin = (h - text_h) / 2
        shift = y + margin - bottom

    box = (x, y + shift, w, h)
    overflow = _textbox_funct(txt, box, align=align)
    return overflow


verticalAlignTextBox = vertical_align_textBox


def set_metric_baseline_height(baseline_height: float) -> float:
    # this seems to be necessary only for fonts with unusual vertical metrics
    line_height = _get_line_height_from_desired_baseline_height(baseline_height)
    db.lineHeight(line_height)
    return line_height


baselineHeight = set_metric_baseline_height


def _get_line_height_from_desired_baseline_height(baseline_height: float) -> float:
    with db.savedState():
        txt = "H\nH"
        db.lineHeight(baseline_height)
        # should calculate appropriate size here
        lines = db.textBoxBaselines(txt, (0, 0, 10000, 10000))
        line_dist = lines[0][1] - lines[1][1]
        target_line_dist = baseline_height
        required_line_dist = target_line_dist - line_dist + target_line_dist
    return required_line_dist


def correct_box_direction(box: Box) -> Box:
    x, y, w, h = box
    if h < 0:
        y = y + h
        h = h * -1
    return (x, y, w, h)
