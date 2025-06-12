"""Tests for the Human class."""
from unittest.mock import Mock

import pytest

from characters.human import Human, image_assets


def test_human_instantiation():
    """Check we can instantiate a new instance of a Human."""
    _ = Human()

def test_human_location():
    """Check we can set a location on instantiation of a new instance of a Human."""
    assert Human(location=(2,3)).location == (2,3)

@pytest.mark.parametrize(
    ("expected"),
    [
        ("assets/character-human1.png"),
        ("assets/character-human2.png"),
    ]
)
def test_image_assets(expected):
    """Tests function that returns on the potential 'human' image assets available."""
    assets = image_assets()

    assert expected in assets


@pytest.mark.parametrize(
    ("not_expected"),
    [
        ("assets/character-base.jpg"),
        ("assets/character-zombie.png"),
    ]
)
def test_image_assets_missing(not_expected):
    """Tests function does not return assets for other character types."""
    assets = image_assets()

    assert not_expected not in assets


@pytest.mark.parametrize(
    ("direction","expected_destination"),
    [
        ["N", [10,7]],
        ["NE", [13,7]],
        ["E", [13,10]],
        ["SE", [13,13]],
        ["S", [10,13]],
        ["SW", [7,13]],
        ["W", [7,10]],
        ["NW", [7,7]],
    ]
)
def test_human_movement(direction, expected_destination):
    """Check the direction of movement for a Human."""
    human = Human(location=[10,10])
    human.movement_direction = Mock(return_value=direction)
    human.move()
    assert human.location == expected_destination