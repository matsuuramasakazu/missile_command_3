"""
Sprite classes for Missile Command.
"""
import math
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
    def __init__(self, x, y, width=40, height=20, ammo=10):
        """
        Initializes a MissileBase sprite.

        Args:
            x (int): The x-coordinate of the top-left corner.
            y (int): The y-coordinate of the top-left corner.
            width (int): The width of the base.
            height (int): The height of the base.
            ammo (int): The initial number of missiles.
        """
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ammo = ammo
        self.alive = True

    def is_destroyed(self):
        """Check if the base is destroyed."""
        return not self.alive

    def fire_missile(self, target_pos):
        """Fire a missile if ammo is available."""
        if self.ammo > 0 and self.alive:
            self.ammo -= 1
            return PlayerMissile(self.rect.midtop, target_pos)
        return None

class PlayerMissile(pygame.sprite.Sprite):
    """Represents a missile fired by the player."""
    def __init__(self, start_pos, target_pos, speed=10):
        """
        Initializes a PlayerMissile sprite.

        Args:
            start_pos (tuple[int, int]): The starting (x, y) coordinates.
            target_pos (tuple[int, int]): The target (x, y) coordinates.
            speed (int): The speed of the missile.
        """
        super().__init__()
        self.image = pygame.Surface([4, 4])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=start_pos)

        self.start_pos = start_pos
        self.target_pos = target_pos
        self.speed = speed

        self.current_pos = pygame.Vector2(start_pos)
        
        angle = math.atan2(target_pos[1] - start_pos[1], target_pos[0] - start_pos[0])
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * self.speed

    def update(self):
        """Move the missile and check for arrival."""
        self.current_pos += self.velocity
        self.rect.center = self.current_pos

        # Check if the missile has reached or passed the target
        if self.current_pos.distance_to(self.target_pos) < self.speed:
            self.kill()
