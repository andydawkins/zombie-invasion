"""The Zombie character class."""
import glob
import random
from copy import copy
import math

from pygame import image

from characters.base import BaseCharacter
from constants import ZOMBIE_PACES
from exceptions import InvalidCoordinateException


class Zombie(BaseCharacter):
    """
    A zombie character has the following behaviour.

    Each turn each Zombie will walk ZOMBIE_PACES paces towards the nearest Human.
    If a pace places them beyond the grid or bumps into a wall then the pace is not taken and is forfeit.

    Zombies may occupy space with other Zombies.

    If a Zombie occupies the same space as a Human then the Human will turn into a Zombie.
    """
    def __init__(self, **kwargs):
        """Initialize a Zombie character."""
        super(Zombie, self).__init__(**kwargs)

    def will_share_space(self, other_character):
        """
        Check if this zombie will share space with another character.
        Zombies can only share space with humans (for conversion purposes).
        
        Args:
            other_character: The other character to check space sharing with
            
        Returns:
            bool: True if this zombie will share space with the other character
        """
        # Zombies can only share space with humans (for conversion)
        return other_character.__class__.__name__ == 'Human'

    @classmethod
    def image_assets(cls):
        """
        Returns a list of assets for zombie characters.
        """
        return glob.glob("assets/character-zombie*")

    def _load_image(self):
        """
        Load the image used for the Sprite for this character
        """
        self.image = image.load(random.choice(self.image_assets()))

    def _find_nearest_human(self, board):
        """
        Find the nearest human on the board.
        
        Args:
            board: The board containing all characters
            
        Returns:
            tuple: The location of the nearest human, or None if no humans exist
        """
        nearest_human = None
        min_distance = float('inf')
        
        for character in board.character_list:
            if character.__class__.__name__ == 'Human':
                distance = math.sqrt(
                    (character.location[0] - self.location[0])**2 +
                    (character.location[1] - self.location[1])**2
                )
                if distance < min_distance:
                    min_distance = distance
                    nearest_human = character.location
                    
        return nearest_human

    def movement_direction(self, board):
        """
        Determine the direction to move towards the nearest human.
        If no humans exist, move randomly.
        
        Args:
            board: The board containing all characters
            
        Returns:
            str: The direction to move in (N, NE, E, SE, S, SW, W, NW)
        """
        nearest_human = self._find_nearest_human(board)
        
        if nearest_human is None:
            return random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
            
        dx = nearest_human[0] - self.location[0]
        dy = nearest_human[1] - self.location[1]
        
        # Determine primary direction (horizontal or vertical)
        if abs(dx) >= abs(dy):
            # Move horizontally
            if dx > 0:
                return "E"
            else:
                return "W"
        else:
            # Move vertically
            if dy > 0:
                return "S"
            else:
                return "N"

    def move(self, board):
        """Move the zombie towards the nearest human."""
        self.previous_location = copy(self.location)
        direction = self.movement_direction(board)
        if direction == "N":
            self.location[1] += -ZOMBIE_PACES
        elif direction == "NE":
            self.location[0] += ZOMBIE_PACES
            self.location[1] += -ZOMBIE_PACES
        elif direction == "E":
            self.location[0] += ZOMBIE_PACES
        elif direction == "SE":
            self.location[0] += ZOMBIE_PACES
            self.location[1] += ZOMBIE_PACES
        elif direction == "S":
            self.location[1] += ZOMBIE_PACES
        elif direction == "SW":
            self.location[0] += -ZOMBIE_PACES
            self.location[1] += ZOMBIE_PACES
        elif direction == "W":
            self.location[0] += -ZOMBIE_PACES
        elif direction == "NW":
            self.location[0] += -ZOMBIE_PACES
            self.location[1] += -ZOMBIE_PACES

    def commence_turn(self, board):
        """
        This is the main game loop where each turn all characters on the board get to have a 'turn'.

        Each turn a Zombie character will attempt to walk a number of ZOMBIE_PACES paces towards the nearest human

        Args:
            board: The board that this character is contained within.
        """
        self.move(board)
        try:
            board.move_character(self)
        except InvalidCoordinateException:
            self.location = self.previous_location 