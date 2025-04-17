from drawBotGrid.text import correct_box_direction


def test_correct_box_direction() -> None:
    assert (0, -100, 100, 100) == correct_box_direction((0, 0, 100, -100))
