"""Tests for the Zombie class."""
from unittest.mock import Mock, MagicMock

import pytest

from characters.zombie import Zombie
from characters.human import Human


def test_zombie_instantiation():
    """Check we can instantiate a new instance of a Zombie."""
    _ = Zombie()


def test_zombie_location():
    """Check we can set a location on instantiation of a new instance of a Zombie."""
    assert Zombie(location=(2,3)).location == (2,3)


@pytest.mark.parametrize(
    ("expected"),
    [
        ("assets/character-zombie.png"),
    ]
)
def test_image_assets(expected):
    """Tests function that returns on the potential 'zombie' image assets available."""
    assets = Zombie.image_assets()

    assert expected in assets


@pytest.mark.parametrize(
    ("not_expected"),
    [
        ("assets/character-base.jpg"),
        ("assets/character-human1.png"),
    ]
)
def test_image_assets_missing(not_expected):
    """Tests function does not return assets for other character types."""
    assets = Zombie.image_assets()

    assert not_expected not in assets


def test_zombie_will_share_space():
    """Test that zombies will not share space with any other characters."""
    zombie = Zombie()
    other_zombie = Zombie()
    human = Human()
    
    # Zombies should not share space with other zombies
    assert not zombie.will_share_space(other_zombie)
    assert not other_zombie.will_share_space(zombie)
    
    # Zombies will share space with humans
    assert zombie.will_share_space(human)
    assert human.will_share_space(zombie)


def test_zombie_will_not_share_space_with_zombie():
    """Test that zombies cannot share space with other zombies."""
    zombie1 = Zombie(location=(0, 0))
    zombie2 = Zombie(location=(1, 1))
    
    # Zombies cannot share space with other zombies
    assert zombie1.will_share_space(zombie2) is False
    assert zombie2.will_share_space(zombie1) is False


def test_find_nearest_human():
    """Test finding the nearest human on the board."""
    zombie = Zombie(location=[10, 10])
    board = MagicMock()
    
    # Create some humans at different distances
    human1 = Human(location=[12, 10])  # 2 units away
    human2 = Human(location=[10, 15])  # 5 units away
    human3 = Human(location=[8, 8])    # ~2.8 units away
    
    board.character_list = [human1, human2, human3]
    
    nearest = zombie._find_nearest_human(board)
    assert nearest == [12, 10]  # human1 should be nearest


def test_movement_direction_towards_human():
    """Test that zombie moves towards nearest human."""
    zombie = Zombie(location=[10, 10])
    board = MagicMock()
    
    # Place a human to the northeast
    human = Human(location=[12, 8])
    board.character_list = [human]
    
    # Zombie should move east (horizontal distance is greater)
    assert zombie.movement_direction(board) == "E"
    
    # Place a human to the northwest
    human.location = [8, 8]
    
    # Zombie should move west
    assert zombie.movement_direction(board) == "W"
    
    # Place a human directly above
    human.location = [10, 8]
    
    # Zombie should move north
    assert zombie.movement_direction(board) == "N"
    
    # Place a human directly below
    human.location = [10, 12]
    
    # Zombie should move south
    assert zombie.movement_direction(board) == "S"


def test_movement_direction_no_humans():
    """Test that zombie moves randomly when no humans exist."""
    zombie = Zombie(location=[10, 10])
    board = MagicMock()
    board.characters = []
    
    # Should return one of the valid directions
    direction = zombie.movement_direction(board)
    assert direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


@pytest.mark.parametrize(
    ("human_location", "expected_direction", "expected_destination"),
    [
        [[13, 10], "E", [11, 10]],  # Move east towards human
        [[7, 10], "W", [9, 10]],    # Move west towards human
        [[10, 7], "N", [10, 9]],    # Move north towards human
        [[10, 13], "S", [10, 11]],  # Move south towards human
    ]
)
def test_zombie_movement_towards_human(human_location, expected_direction, expected_destination):
    """Check the zombie moves towards the human."""
    zombie = Zombie(location=[10, 10])
    board = MagicMock()
    
    # Place a human at the specified location
    human = Human(location=human_location)
    board.character_list = [human]
    
    # Move the zombie
    zombie.move(board)
    
    # Check final position
    assert zombie.location == expected_destination 