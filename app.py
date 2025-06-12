# game loop
from random import randint

import pygame

from characters.human import Human
from constants import HUMAN_COUNT, GRID_WIDTH, GRID_HEIGHT, BACKGROUND_COLOR
from ui.board import GameBoard

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
board = GameBoard(screen)

def populate_initial_humans():
    """Places a number of humans on the grid at the beginning of the game."""
    for _ in range(HUMAN_COUNT):
        board.add_character(Human(location=[randint(0, GRID_WIDTH-1), randint(0, GRID_HEIGHT-1)]))

populate_initial_humans()

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

    dt = clock.tick(60) / 1000  # limits FPS to 60

pygame.quit()