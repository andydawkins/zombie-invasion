"""The Base Character class."""
from abc import ABC, abstractmethod


class BaseCharacter(ABC):
    """Abstract base class for characters."""
    @abstractmethod
    def __init__(self, location=(0,0)):
        self.location = location

    @abstractmethod
    def move(self):
        """
        Abstract method which defines the behaviour of the Character when it moves
        """
        pass