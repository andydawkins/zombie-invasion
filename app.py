# game loop
from random import randint

import pygame

from characters.human import Human
from characters.zombie import Zombie
from constants import HUMAN_COUNT, ZOMBIE_COUNT, GRID_WIDTH, GRID_HEIGHT, BACKGROUND_COLOR
from ui.board import GameBoard

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
board = GameBoard(screen)

# TODO: This file is currently untested, this makes me uncomfortable but I don't want to be testing the internals of pygame
#       And I definitely don't want to be unittesting UI elements that could get very complicated very quickly

def populate_initial_humans():
    """Places a number of humans on the grid at the beginning of the game."""
    for _ in range(HUMAN_COUNT):
        board.add_character(Human(location=[randint(0, GRID_WIDTH-1), randint(0, GRID_HEIGHT-1)]))


def populate_initial_zombies():
    """Places a number of zombies on the grid at the beginning of the game."""
    for _ in range(ZOMBIE_COUNT):
        # Keep trying to place zombies until we find a valid space
        while True:
            try:
                board.add_character(Zombie(location=[randint(0, GRID_WIDTH-1), randint(0, GRID_HEIGHT-1)]))
                break
            except InvalidCoordinateException:
                # If we can't place the zombie (due to space sharing rules), try again
                continue


# Populate the board with initial characters
populate_initial_humans()
populate_initial_zombies()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)

    # Render the screen surface
    board.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    board.commence_turn()

    dt = clock.tick(1) / 1000  # limits FPS to 1

pygame.quit()