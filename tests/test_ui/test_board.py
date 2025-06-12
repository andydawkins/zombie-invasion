"""Tests for the Game Board."""
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
            result = board.location_to_screen_coordinates(location=(5,5))

            assert result == (640, 360)
