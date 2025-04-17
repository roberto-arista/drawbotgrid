import drawBot as db
import pytest

from drawBotGrid.aliases import Box
from drawBotGrid.image import imageAtSize, imageBox

boxes = [
    (100, 100, 300, 300),
    (100, 100, 300, 0),
    (100, 100, 0, 300),
]


@pytest.mark.parametrize("box", boxes)
def test_image_at_size(box: Box) -> None:
    with db.drawing():
        db.newPage(1000, 1000)
        imageAtSize("drawBotGrid/docs/drawMech-small.jpg", box)


test_imageBox_parameters = [
    {"fitting": "crop", "scale": 0.15, "anchor": ("left", "bottom"), "result": (0, 0, 95.4, 135.0)},
    {"fitting": "crop", "scale": 0.15, "anchor": ("left", "center"), "result": (0, 15.0, 95.4, 135.0)},
    {"fitting": "crop", "scale": 0.15, "anchor": ("left", "top"), "result": (0, 30.0, 95.4, 135.0)},
    {"fitting": "crop", "scale": 0.15, "anchor": ("center", "bottom"), "result": (5.8, 0, 95.4, 135.0)},
    {"fitting": "crop", "scale": 0.15, "anchor": ("center", "center"), "result": (5.8, 15.0, 95.4, 135.0)},
    {"fitting": "crop", "scale": 0.15, "anchor": ("center", "top"), "result": (5.8, 30.0, 95.4, 135.0)},
    {"fitting": "crop", "scale": 0.15, "anchor": ("right", "bottom"), "result": (11.6, 0, 95.4, 135.0)},
    {"fitting": "crop", "scale": 0.15, "anchor": ("right", "center"), "result": (11.6, 15.0, 95.4, 135.0)},
    {"fitting": "crop", "scale": 0.15, "anchor": ("right", "top"), "result": (11.6, 30.0, 95.4, 135.0)},
    #
    {"fitting": "crop", "scale": 1, "anchor": ("left", "bottom"), "result": (0, 0, 107.0, 165.0)},
    {"fitting": "crop", "scale": 1, "anchor": ("left", "center"), "result": (0, 0.5, 107.0, 165.0)},
    {"fitting": "crop", "scale": 1, "anchor": ("left", "top"), "result": (0, 0.0, 107.0, 165.0)},
    {"fitting": "crop", "scale": 1, "anchor": ("center", "bottom"), "result": (-0.5, 0, 107.0, 165.0)},
    {"fitting": "crop", "scale": 1, "anchor": ("center", "center"), "result": (-0.5, 0.5, 107.0, 165.0)},
    {"fitting": "crop", "scale": 1, "anchor": ("center", "top"), "result": (-0.5, 0.0, 107.0, 165.0)},
    {"fitting": "crop", "scale": 1, "anchor": ("right", "bottom"), "result": (0.0, 0, 107.0, 165.0)},
    {"fitting": "crop", "scale": 1, "anchor": ("right", "center"), "result": (0.0, 0.5, 107.0, 165.0)},
    {"fitting": "crop", "scale": 1, "anchor": ("right", "top"), "result": (0.0, 0.0, 107.0, 165.0)},
]


@pytest.mark.parametrize("parameters", test_imageBox_parameters)
def test_imageBox(parameters: dict) -> None:
    with db.drawing():
        db.newPage(1000, 1000)
        result = imageBox(
            "drawBotGrid/docs/drawMech-small.jpg",
            (0, 0, 107.0, 165.0),
            scale=parameters["scale"],
            fitting=parameters["fitting"],
            anchor=parameters["anchor"],
        )
        assert result[0] == pytest.approx(parameters["result"][0])
        assert result[1] == pytest.approx(parameters["result"][1])
        assert result[2] == pytest.approx(parameters["result"][2])
        assert result[3] == pytest.approx(parameters["result"][3])


@pytest.mark.parametrize("anchor", [("Right", "center"), ("left", "Center")])
def test_imageBox_exceptions(anchor) -> None:
    with db.drawing():
        db.newPage(1000, 1000)
        with pytest.raises(ValueError):
            imageBox(
                "drawBotGrid/docs/drawMech-small.jpg",
                (0, 0, 107.0, 165.0),
                scale=1,
                fitting="crop",
                anchor=anchor,
            )
