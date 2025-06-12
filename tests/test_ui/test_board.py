"""Tests for the Game Board."""
from unittest import result
from unittest.mock import Mock, patch

import pytest

from characters.human import Human
from ui.board import GameBoard, InvalidCoordinateException


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
