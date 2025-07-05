"""
Sprite classes for Missile Command.
"""
import pygame
from settings import WHITE

class City(pygame.sprite.Sprite):
    """Represents a city to be protected."""
    def __init__(self, x, y, width=50, height=30):
        """
        Initializes a City sprite.

        Args:
            x (int): The x-coordinate of the top-left corner.
            y (int): The y-coordinate of the top-left corner.
            width (int): The width of the city.
            height (int): The height of the city.
        """
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class MissileBase(pygame.sprite.Sprite):
    """Represents a missile base that fires missiles."""
    def __init__(self, x, y, width=40, height=20):
        """
        Initializes a MissileBase sprite.

        Args:
            x (int): The x-coordinate of the top-left corner.
            y (int): The y-coordinate of the top-left corner.
            width (int): The width of the base.
            height (int): The height of the base.
        """
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
