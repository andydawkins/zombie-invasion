import pygame.draw
from pygame.examples.music_drop_fade import starting_pos

from constants import GRID_WIDTH, GRID_HEIGHT, GRID_COLOR


class GameBoard:
    def __init__(self, screen):
        """
        Initialisation of the Game Board object.

        Args:
            screen: The screen to draw the game board.
        """
        self.screen = screen

        grid_width = (self.screen.get_width()-20)/GRID_WIDTH
        grid_height = (self.screen.get_height()-20)/GRID_HEIGHT
        self.square_width = min(grid_width, grid_height)

    def draw(self):
        """Draws the game board onto the screen."""

        center_point = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        top_left = (
            center_point[0] - (GRID_WIDTH * self.square_width) / 2 ,
            center_point[1] - (GRID_HEIGHT * self.square_width) / 2
        )

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


