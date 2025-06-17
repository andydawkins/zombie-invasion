import pygame.draw
from pygame.examples.music_drop_fade import starting_pos
from copy import copy

from constants import GRID_WIDTH, GRID_HEIGHT, GRID_COLOR
from characters.zombie import Zombie
from exceptions import InvalidCoordinateException, CharacterNotFoundException


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

    def _check_space_sharing(self, character, location):
        """
        Check if a character can share space with existing characters at a location.
        
        Args:
            character: The character attempting to move to the location
            location: The location to check (x, y coordinates)
            
        Returns:
            bool: True if the character can share the space, False otherwise
            
        Raises:
            InvalidCoordinateException: If the location is invalid
        """
        try:
            existing_characters = self.character_grid[location[0]][location[1]]
        except IndexError:
            raise InvalidCoordinateException
            
        # Check if the new character can share space with all existing characters
        for existing_char in existing_characters:
            if not existing_char.will_share_space(character) or not character.will_share_space(existing_char):
                return False
                
        return True

    def _convert_human_to_zombie(self, human, location=None):
        """
        Convert a human character to a zombie character.
        
        Args:
            human: The human character to convert
            location: Optional location for the new zombie. If None, uses human's location.
            
        Returns:
            Zombie: The newly created zombie character
        """
        # Create a new zombie at the specified location or human's location
        zombie = Zombie(location=location if location is not None else human.location)
        
        # Remove the human from the board using its previous location
        # This is important because the human's location has already been updated
        # to where it's trying to move to
        human_location = self.find_character_location(human)
        self.character_grid[human_location[0]][human_location[1]].remove(human)
        self.character_list.remove(human)
        
        # Add the zombie to the board at the new location
        self.character_grid[zombie.location[0]][zombie.location[1]].append(zombie)
        self.character_list.append(zombie)
        
        return zombie

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


    def add_character(self, character, is_initial_placement=False):
        """
        Add a character to the board.

        Args:
            character: The character to add.
            is_initial_placement: Whether this is initial placement (True) or movement/conversion (False)
            
        Raises:
            InvalidCoordinateException: If the location is invalid or space sharing is not allowed
        """
        if character.location[0] < 0 or character.location[1] < 0:
            raise InvalidCoordinateException

        try:
            # For initial placement, only zombies cannot share spaces
            if is_initial_placement and isinstance(character, Zombie):
                if self.character_grid[character.location[0]][character.location[1]]:
                    raise InvalidCoordinateException
            else:
                # For movement/conversion or initial human placement, check space sharing rules
                if not self._check_space_sharing(character, character.location):
                    raise InvalidCoordinateException

            self.character_grid[character.location[0]][character.location[1]].append(character)
            self.character_list.append(character)
            
        except IndexError:
            raise InvalidCoordinateException
        
        return character.location

    def move_character(self, character):
        """
        Move the character to its location on the grid.

        Args:
            character: The character to move.
            
        Raises:
            InvalidCoordinateException: If the location is invalid or space sharing is not allowed
        """
        if character.location[0] < 0 or character.location[1] < 0:
            raise InvalidCoordinateException

        try:
            # Get characters at the destination location
            destination_characters = copy(self.character_grid[character.location[0]][character.location[1]])
            
            # First check if the character can share the space with existing characters
            # This needs to happen before any conversions
            if not self._check_space_sharing(character, character.location):
                raise InvalidCoordinateException
            
            # Then handle any human-to-zombie conversions
            if isinstance(character, Zombie):
                # If moving character is a zombie, check for humans at destination
                for existing_char in destination_characters:
                    if existing_char.__class__.__name__ == 'Human':
                        # Convert human to zombie at the destination location
                        self._convert_human_to_zombie(existing_char)
            elif character.__class__.__name__ == 'Human':
                # If moving character is a human, check for zombies at destination
                for existing_char in destination_characters:
                    if isinstance(existing_char, Zombie):
                        # Convert human to zombie
                        self._convert_human_to_zombie(character, existing_char.location)
                        return  # The original character is now a zombie, so we're done
            
            # Finally, move the character
            character_location = self.find_character_location(character)
            self.character_grid[character_location[0]][character_location[1]].remove(character)
            self.character_grid[character.location[0]][character.location[1]].append(character)
            
        except IndexError:
            raise InvalidCoordinateException

    def commence_turn(self):
        """
        This is the main game loop where each turn all characters on the board get to have a 'turn'.
        """
        for character in self.character_list:
            character.commence_turn(self)

    def find_character_location(self, character):
        """
        Find the location of a character in the character grid.
        
        Args:
            character: The character to find
            
        Returns:
            tuple: The (x, y) coordinates where the character is found
            
        Raises:
            CharacterNotFoundException: If the character is not found on the board
        """
        # Search through the character grid
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if character in self.character_grid[x][y]:
                    return (x, y)
                    
        # If we get here, the character wasn't found
        raise CharacterNotFoundException(f"Character {character} not found on the board")

    def count_humans(self):
        """
        Count the number of humans on the board.
        
        Returns:
            int: The number of humans currently on the board
        """
        return sum(1 for char in self.character_list if char.__class__.__name__ == 'Human')
        
    def count_zombies(self):
        """
        Count the number of zombies on the board.
        
        Returns:
            int: The number of zombies currently on the board
        """
        return sum(1 for char in self.character_list if isinstance(char, Zombie))

