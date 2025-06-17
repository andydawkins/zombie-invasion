"""Game exceptions."""


class InvalidCoordinateException(Exception):
    """
    Raised when a characters coordinates are invalid.

    This can be because it's not on the board or because there are other reasons why the character cannot
    be placed there, such as being occupied by another character that doesn't allow it or an object."""
    pass

class CharacterNotFoundException(Exception):
    """Exception raised when a character is not found on the board."""
    pass 