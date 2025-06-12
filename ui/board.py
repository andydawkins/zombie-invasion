import pygame.draw
from pygame.examples.music_drop_fade import starting_pos

from constants import GRID_WIDTH, GRID_HEIGHT, GRID_COLOR


class InvalidCoordinateException(Exception):
    """
    Raised when a characters coordinates are invalid.

    This can be because it's not on the board or because there are other reasons why the character cannot
    be placed there, such as being occupied by another character that doesn't allow it or an object."""
    pass


class GameBoard:
    def __init__(self, screen):
        """
        Initialisation of the Game Board object.

        Args:
            screen: The screen to draw the game board.
        """
        self.screen = screen

        # TODO: I'm thinking that the Grid and the Board are different objects and should be separated
        grid_width = (self.screen.get_width()-20)/GRID_WIDTH
        grid_height = (self.screen.get_height()-20)/GRID_HEIGHT
        self.square_width = min(grid_width, grid_height)
        self.character_grid = [ [ [] for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
        self.character_list = []
        self.center_point = None

    def draw(self):
        """Draws the game board onto the screen."""

        top_left = self.grid_top_left()

        for n in range(0, GRID_WIDTH+1):
            x = top_left[0] + (n * self.square_width)
            pygame.draw.line(
                surface=self.screen,
                color=GRID_COLOR,
                start_pos=(x, top_left[1]),
                end_pos=(x, top_left[1]+(GRID_HEIGHT*self.square_width)),
                width=1
            )

        for n in range(0, GRID_HEIGHT+1):
            y = top_left[1] + (n * self.square_width)
            pygame.draw.line(
                surface=self.screen,
                color=GRID_COLOR,
                start_pos=(top_left[0], y),
                end_pos=(top_left[0]+(GRID_WIDTH*self.square_width), y),
                width=1
            )

        for character in self.character_list:
            self.draw_character(character)

    def grid_top_left(self):
        """
        Calculates the pixel coordinates of the top left corner of the grid.

        Returns:
            A tuple of the coordinates of the top left corner of the grid on the screen.
        """
        # Calculate the exact center of the screen
        self.center_point = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        # Find the top left by shifting LEFT half of the width of the grid
        # and UP half the height of the grid
        top_left = (
            self.center_point[0] - (GRID_WIDTH * self.square_width) / 2,
            self.center_point[1] - (GRID_HEIGHT * self.square_width) / 2
        )
        return top_left


    def location_to_screen_coordinates(self, location):
        """
        Coverts a given grid location into X and Y pixel coordinates on the screen at the given resolution and grid size.

        Args:
             location: A tuple containing the Grid location (x,y).

        Return:
            A tuple containing the X and Y pixel coordinates on the screen of the center of the grid square.
        """
        x, y = location
        # Top left of the Grid
        # Plus the width of each square multiplied by the X Grid coordinate
        # Plus Half the square with, in order to put the coordinate in the middle of the square
        x_coord = self.grid_top_left()[0]+(x*self.square_width)+(self.square_width/2)

        # Top left of the Grid
        # Plus the width of each square multiplied by the Y Grid coordinate
        # Plus Half the square with, in order to put the coordinate in the middle of the square
        y_coord = self.grid_top_left()[1]+(y*self.square_width)+(self.square_width/2)

        return (x_coord, y_coord)


    def draw_character(self, character):
        """Draws a single character at its location on the grid."""
        character.draw(self.screen, self.location_to_screen_coordinates(character.location), self.square_width-4)


    def add_character(self, character):
        """
        Adds a character to the game board.

        When placing a character on the game board the add_character method will echo back
        the co-ordinates that the character has been placed, this might be different to the requested
        co-ordinates.
        There may be reasons why the character has to be placed somewhere else.

        If the character was unable to be placed at those co-ordinates then the add_character method will
        raise an InvalidCoordinateException."""
        # TODO: Currently this doesn't check if the character is already on the board..... do we need to?
        coordinates = character.location
        try:
            self.character_grid[coordinates[0]][coordinates[1]].append(character)
            self.character_list.append(character)
        except IndexError:
            raise InvalidCoordinateException

        return coordinates

    def commence_turn(self):
        """
        This is the main game loop where each turn all characters on the board get to have a 'turn'.
        """
        for character in self.character_list:
            character.commence_turn(self)

