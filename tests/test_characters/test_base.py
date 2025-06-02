"""Tests for the Character base class."""
import pytest

from characters.base import BaseCharacter

def test_base_instantiation():
    """
    Create a new instance of a base character.
    This should error since BaseCharacter is an abstract base class.
    """
    with pytest.raises(TypeError):
        BaseCharacter()