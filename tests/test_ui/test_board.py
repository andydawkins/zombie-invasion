"""Tests for the Game Board."""
from unittest import result
from unittest.mock import Mock, patch, MagicMock

import pytest
import pygame

from characters.human import Human
from characters.zombie import Zombie
from ui.board import GameBoard
from exceptions import InvalidCoordinateException, CharacterNotFoundException


@pytest.fixture
def mock_screen():
    """A Screen-like object used in testing"""
    screen = Mock()
    screen.get_width = Mock(return_value=1280)
    screen.get_height = Mock(return_value=720)
    yield screen


@pytest.mark.parametrize(
    "X,Y",
    [
        [10,10],
        [1,10],
        [10,1]
    ]
)
def test_character_grid_setup(mock_screen, X, Y):
    """
    Test the data structure for the character grid is setup as expected.

    In a 10x10 grid the resulting character grid should look like this:
    [
      [],[],[],[],[],[],[],[],[],[],
      [],[],[],[],[],[],[],[],[],[],
      [],[],[],[],[],[],[],[],[],[],
      [],[],[],[],[],[],[],[],[],[],
      [],[],[],[],[],[],[],[],[],[],
      [],[],[],[],[],[],[],[],[],[],
      [],[],[],[],[],[],[],[],[],[],
      [],[],[],[],[],[],[],[],[],[],
      [],[],[],[],[],[],[],[],[],[],
      [],[],[],[],[],[],[],[],[],[],
      [],[],[],[],[],[],[],[],[],[],
    ]
    """
    with patch("ui.board.GRID_WIDTH", X):
        with patch("ui.board.GRID_HEIGHT", Y):
            board = GameBoard(screen=mock_screen)

            # there should be X 'columns' to the grid
            assert len(board.character_grid) == X
            # and each 'columns' should have Y rows
            for col in board.character_grid:
                assert len(col) == Y

def test_add_character(mock_screen):
    """
    Test adding a character to the game board.

    When placing a character on the game board the add_charcter method will echo back
    the co-ordinates that the character has been placed, this might be different to the requested
    co-ordinates.

    If the character was unable to be placed at those co-ordinates then the add_character method will
    raise an InvalidCoordinateException.
    """
    human = Human(location=[10,10])
    board = GameBoard(screen=mock_screen)

    result = board.add_character(human)

    assert result == [10,10]
    assert board.character_grid[10][10] == [human]
    assert board.character_list == [human]

def test_add_character_invalid_location(mock_screen):
    """
    Test adding a character to the game board in a location that isn't on the game board.

    This should raise an InvalidCoordinateException.
    """
    human = Human(location=[100,100])
    board = GameBoard(screen=mock_screen)

    with pytest.raises(InvalidCoordinateException):
        _ = board.add_character(human)

def test_location_to_screen_coordinates(mock_screen):
    """
    Test converting a grid position (x,y) to screen coordinates based on screen resolution.

    The Mock_screen object has a width of 1280 and height of 720 pixels.

    Args:
        mock_screen (Mock): A mocked screen object.
    """
    with patch("ui.board.GRID_WIDTH", 9):
        with patch("ui.board.GRID_HEIGHT", 9):
            board = GameBoard(screen=mock_screen)
            # Remember grid indexing starts at 0, so the middle grid square is at index 4, not 5
            result = board.location_to_screen_coordinates(location=(4,4))

            assert result == (640, 360)

def test_move_character(mock_screen):
    """
    Test for moving a character from one location to another on the board.

    The Character must be on the board already.
    The destination location should be valid

    Args:
        mock_screen (Mock): A mocked screen object.
    """
    board = GameBoard(screen=mock_screen)
    character = Human(location=[5,5])
    board.add_character(character)

    character.location = (7,7)
    board.move_character(character)

    # The character should be in the new location
    assert board.character_grid[character.location[0]][character.location[1]] == [character]
    # It should not be in the old location
    assert board.character_grid[5][5] == []
    # It should exist once in the character_list
    assert board.character_list == [character]


def test_move_character_out_of_bounds_positive(mock_screen):
    """
    Test for moving a character to a location that is out of range of the board.

    This will return False and NOT move the character.

    The destination location should be valid

    Args:
        mock_screen (Mock): A mocked screen object.
    """
    with patch("ui.board.GRID_WIDTH", 6):
        with patch("ui.board.GRID_HEIGHT", 6):
            board = GameBoard(screen=mock_screen)
            character = Human(location=[5,5])
            board.add_character(character)

            character.location = (7,7)

            with pytest.raises(InvalidCoordinateException):
                board.move_character(character)

    # It should still be in the old location
    assert board.character_grid[5][5] == [character]
    # It should exist once in the character_list
    assert board.character_list == [character]

def test_move_character_out_of_bounds_negative(mock_screen):
    """
    Test for moving a character to a location that is out of range of the board into negative indexes.

    This will return False and NOT move the character.

    The destination location should be valid

    Args:
        mock_screen (Mock): A mocked screen object.
    """
    with patch("ui.board.GRID_WIDTH", 6):
        with patch("ui.board.GRID_HEIGHT", 6):
            board = GameBoard(screen=mock_screen)
            character = Human(location=[5,5])
            board.add_character(character)

            character.location = (-1,-1)

            with pytest.raises(InvalidCoordinateException):
                board.move_character(character)

    # It should still be in the old location
    assert board.character_grid[5][5] == [character]
    # It should exist once in the character_list
    assert board.character_list == [character]

def test_board_initialization():
    """Test that the board initializes correctly."""
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    
    board = GameBoard(screen)
    
    assert len(board.character_grid) == 40  # GRID_WIDTH
    assert len(board.character_grid[0]) == 20  # GRID_HEIGHT
    assert len(board.character_list) == 0


def test_add_character():
    """Test adding a character to the board."""
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    
    board = GameBoard(screen)
    human = Human(location=(5, 5))
    
    coordinates = board.add_character(human)
    assert coordinates == (5, 5)
    assert human in board.character_list
    assert human in board.character_grid[5][5]


def test_add_character_invalid_location():
    """Test adding a character to an invalid location."""
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    
    board = GameBoard(screen)
    human = Human(location=(50, 50))  # Outside grid
    
    with pytest.raises(InvalidCoordinateException):
        board.add_character(human)


def test_space_sharing_humans():
    """Test that humans can share space with other humans."""
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    
    board = GameBoard(screen)
    
    # Add first human
    human1 = Human(location=(5, 5))
    board.add_character(human1)
    
    # Add second human to same location
    human2 = Human(location=(5, 5))
    board.add_character(human2)
    
    # Both humans should be in the same grid location
    assert human1 in board.character_grid[5][5]
    assert human2 in board.character_grid[5][5]


def test_move_character_space_sharing_allowed():
    """Test that character movement respects space sharing rules.
    
    Humans are allowed to share spaces with other humans"""
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    
    board = GameBoard(screen)
    
    # Add two humans
    human1 = Human(location=(5, 5))
    human2 = Human(location=(6, 6))
    board.add_character(human1)
    board.add_character(human2)
    
    # Move human2 to human1's location (should be allowed)
    human2.location = (5, 5)
    board.move_character(human2)
    assert human2 in board.character_grid[5][5]



def test_move_character_space_sharing_not_allowed():
    """Test that character movement respects space sharing rules.
    
    Zombies are not allowed to share spaces with other zombies"""
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    
    board = GameBoard(screen)
   
    # Add two zombies
    zombie1 = Zombie(location=(7, 7))
    zombie2 = Zombie(location=(8, 8))
    board.add_character(zombie1)
    board.add_character(zombie2)
    
    # Try to move zombie1 to zombie2's location (should fail)
    zombie1.location = (8, 8)
    with pytest.raises(InvalidCoordinateException):
        board.move_character(zombie1)

def test_convert_human_to_zombie():
    """Test the human to zombie conversion helper method."""
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    
    board = GameBoard(screen)
    
    # Add a human
    human = Human(location=(5, 5))
    board.add_character(human)
    
    # Convert the human to a zombie
    zombie = board._convert_human_to_zombie(human)
    
    # Check that the human is removed
    assert human not in board.character_list
    assert human not in board.character_grid[5][5]
    
    # Check that the zombie is added
    assert zombie in board.character_list
    assert zombie in board.character_grid[5][5]
    assert isinstance(zombie, Zombie)
    assert zombie.location == (5, 5)


def test_zombie_moves_to_human():
    """Test that a zombie moving to a human's space converts the human."""
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    
    board = GameBoard(screen)
    
    # Add a human and a zombie
    human = Human(location=(5, 5))
    zombie = Zombie(location=(6, 6))
    board.add_character(human)
    board.add_character(zombie)
    
    # Move zombie to human's location
    zombie.location = (5, 5)
    board.move_character(zombie)
    
    # Check that the human is converted to a zombie
    assert human not in board.character_list
    assert human not in board.character_grid[5][5]
    assert len(board.character_grid[5][5]) == 2  # Both zombies should be there
    assert all(isinstance(char, Zombie) for char in board.character_grid[5][5])


def test_human_moves_to_zombie():
    """Test that a human moving to a zombie's space gets converted."""
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    
    board = GameBoard(screen)
    
    # Add a human and a zombie
    human = Human(location=(5, 5))
    zombie = Zombie(location=(6, 6))
    board.add_character(human)
    board.add_character(zombie)
    
    # Move human to zombie's location
    human.location = (6, 6)
    board.move_character(human)
    
    # Check that the human is converted to a zombie
    assert human not in board.character_list
    assert human not in board.character_grid[6][6]
    assert len(board.character_grid[6][6]) == 2  # Both zombies should be there
    assert all(isinstance(char, Zombie) for char in board.character_grid[6][6])


def test_multiple_humans_convert_to_zombies():
    """Test that multiple humans can be converted to zombies in one move."""
    screen = MagicMock()
    screen.get_width.return_value = 800
    screen.get_height.return_value = 600
    
    board = GameBoard(screen)
    
    # Add multiple humans and a zombie
    human1 = Human(location=(5, 5))
    human2 = Human(location=(5, 5))
    zombie = Zombie(location=(6, 6))
    board.add_character(human1)
    board.add_character(human2)
    board.add_character(zombie)
    
    # Move zombie to humans' location
    zombie.location = (5, 5)
    board.move_character(zombie)
    
    # Check that both humans are converted to zombies
    assert human1 not in board.character_list
    assert human2 not in board.character_list
    assert len(board.character_grid[5][5]) == 3  # All three zombies should be there
    assert all(isinstance(char, Zombie) for char in board.character_grid[5][5])

def test_find_character_location():
    """Test finding a character's location on the board."""
    # Create a board and some characters
    screen = pygame.Surface((800, 600))
    board = GameBoard(screen)
    human = Human(location=(2, 3))
    zombie = Zombie(location=(4, 5))
    
    # Add characters to the board
    board.add_character(human)
    board.add_character(zombie)
    
    # Test finding existing characters
    assert board.find_character_location(human) == (2, 3)
    assert board.find_character_location(zombie) == (4, 5)
    
    # Test finding a character that's not on the board
    non_existent_human = Human(location=(0, 0))
    with pytest.raises(CharacterNotFoundException):
        board.find_character_location(non_existent_human)
