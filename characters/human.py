"""The Human character class."""
import glob
import random
from copy import copy

from pygame import image

from characters.base import BaseCharacter
from constants import HUMAN_PACES
from ui.board import InvalidCoordinateException


class Human(BaseCharacter):
    """
    A human character has the following behaviour.

    Each turn each Human will walk HUMAN_PACES paces in a random direction (N,NE,E,SE,S,SW,W,NW)
    if a pace places them beyond the grid or bumps into a wall then the pace is not taken and is forfeit.

    Humans may occupy space with other Humans.

    If a Human occupies the same space as a Zombie then the Human will turn into a Zombie and contiune behaving
    as one.
    """
    def __init__(self, **kwargs):
        """Initialize a Human character."""
        super(Human, self).__init__(**kwargs)

    def will_share_space(self, other_character):
        """
        Check if this human will share space with another character.
        Humans can share space with other humans and zombies (for conversion purposes).
        
        Args:
            other_character: The other character to check space sharing with
            
        Returns:
            bool: True if this human will share space with the other character
        """
        # Humans can share space with other humans and zombies
        return other_character.__class__.__name__ in ['Human', 'Zombie']

    @classmethod
    def image_assets(cls):
        """
        Returns a list of assets for human characters.
        """
        return glob.glob("assets/character-human*")

    def _load_image(self):
        """
        Load the image used for the Sprite for this character
        """
        self.image = image.load(random.choice(self.image_assets()))

    @staticmethod
    def movement_direction():
        """Randomly choose a compass direction for the character to move in."""
        return random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])

    def move(self):
        """Move the human to a new space."""
        self.previous_location = copy(self.location)
        direction = self.movement_direction()
        if direction == "N":
            self.location[1] += -HUMAN_PACES
        elif direction == "NE":
            self.location[0] += HUMAN_PACES
            self.location[1] += -HUMAN_PACES
        elif direction == "E":
            self.location[0] += HUMAN_PACES
        elif direction == "SE":
            self.location[0] += HUMAN_PACES
            self.location[1] += HUMAN_PACES
        elif direction == "S":
            self.location[1] += HUMAN_PACES
        elif direction == "SW":
            self.location[0] += -HUMAN_PACES
            self.location[1] += HUMAN_PACES
        elif direction == "W":
            self.location[0] += -HUMAN_PACES
        elif direction == "NW":
            self.location[0] += -HUMAN_PACES
            self.location[1] += -HUMAN_PACES

    def commence_turn(self, board):
        """
        This is the main game loop where each turn all characters on the board get to have a 'turn'.

        Each turn a Human character will attempt to walk a number of HUMAN_PACES paces in a random direction

        Args:
            board: The board that this character is contained within.
        """
        self.move()
        try:
            board.move_character(self)
        except InvalidCoordinateException:
            self.location = self.previous_location



