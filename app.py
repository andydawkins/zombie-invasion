# game loop
from random import randint

import pygame
import random

from characters.human import Human
from characters.zombie import Zombie
from constants import HUMAN_COUNT, ZOMBIE_COUNT, GRID_WIDTH, GRID_HEIGHT, BACKGROUND_COLOR
from exceptions import InvalidCoordinateException
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


def populate_initial_zombies(board):
    """
    Place a number of zombies on the grid at the start of the game.
    
    Args:
        board: The game board to populate with zombies
    """
    for _ in range(ZOMBIE_COUNT):
        while True:
            try:
                # Generate random coordinates
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                
                # Create and add zombie at the random location
                zombie = Zombie(location=[x, y])
                board.add_character(zombie, is_initial_placement=True)
                break
            except InvalidCoordinateException:
                # If the space is occupied, try again
                continue


# Populate the board with initial characters
populate_initial_humans()
populate_initial_zombies(board)

# Initialize turn counter
turn_count = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)

    # Draw the board
    board.draw()

    # Update the display
    pygame.display.flip()

    # Check if all humans are gone
    if board.count_humans() == 0:
        print(f"Game Over - All humans have been converted to zombies in {turn_count} turns!")
        running = False
    else:
        # Only process the next turn if the game is still running
        board.commence_turn()
        turn_count += 1

    dt = clock.tick(2) / 1000  # limits FPS to 2

# Quit pygame
pygame.quit()