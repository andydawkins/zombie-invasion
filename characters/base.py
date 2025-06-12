"""The Base Character class."""
from abc import ABC, abstractmethod

from pygame import image, transform
from pygame.sprite import Sprite


class BaseCharacter(ABC):
    """Abstract base class for characters."""
    @abstractmethod
    def __init__(self, location=(0,0)):
        self.location = location
        self.previous_location = location
        self.sprite = Sprite()
        self._load_image()

    def _load_image(self):
        """
        Load the image used for the Sprite for this character
        """
        self.image = image.load("assets/character-base.jpg")

    @abstractmethod
    def move(self):
        """
        Abstract method which defines the behaviour of the Character when it moves
        """
        pass

    def draw(self, screen, location, size):
        """
        Draw the character on the screen in a specific location.

        Args:
            screen (pygame.Surface): The screen to draw the character on
            location (tuple[int]): The location of the character on the screen.
                                   This is a pixel coordinate to the center of the grid location
            size (tuple[int]): The size of the grid box the character will occupy
        """

        # TODO: I don't like calculating and rescaling the image each time it's drawn.  It feels like a waste of CPU time.
        # We want to preserve the aspect ratio of the original image
        largest_demension = max(self.image.get_width(), self.image.get_height())
        # Fortunately our location is a Square so we are saved the trouble of worrying about the width and height being
        # different
        new_width = size * (self.image.get_width() / largest_demension)
        new_height = size * (self.image.get_height() / largest_demension)
        self.sprite.image = transform.scale(self.image, (new_width, new_height))

        # The sprite will be drawn with the location as it's top-left
        # We want to modify this based on the height and width of the sprite so that the location given sits
        # at it's center
        x_coord = location[0] - (self.sprite.image.get_width()/2)
        y_coord = location[1] - (self.sprite.image.get_height()/2)

        screen.blit(self.sprite.image, (x_coord, y_coord))

    @abstractmethod
    def commence_turn(self, board):
        """
        This is the main game loop where each turn all characters on the board get to have a 'turn'.
        """
        pass