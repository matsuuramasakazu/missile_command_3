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
        """Move the missile."""
        self.current_pos += self.velocity
        self.rect.center = self.current_pos

    def is_at_target(self):
        """Check if the missile has reached its target."""
        return self.current_pos.distance_to(self.target_pos) < self.speed

class EnemyMeteor(pygame.sprite.Sprite):
    """Represents an enemy meteor falling from the sky."""
    def __init__(self, start_pos, target_pos, speed=2):
        """
        Initializes an EnemyMeteor sprite.

        Args:
            start_pos (tuple[int, int]): The starting (x, y) coordinates.
            target_pos (tuple[int, int]): The target (x, y) coordinates on the ground.
            speed (int): The speed of the meteor.
        """
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=start_pos)

        self.start_pos = start_pos
        self.target_pos = target_pos
        self.speed = speed

        self.current_pos = pygame.Vector2(start_pos)

        angle = math.atan2(target_pos[1] - start_pos[1], target_pos[0] - start_pos[0])
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * self.speed

    def update(self):
        """Move the meteor."""
        self.current_pos += self.velocity
        self.rect.center = self.current_pos

        # Kill if it goes off-screen
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()

    def has_reached_target(self):
        """Check if the meteor has reached or passed its target y-coordinate."""
        return self.current_pos.y >= self.target_pos[1]

class Explosion(pygame.sprite.Sprite):
    """Represents an explosion."""
    def __init__(self, pos, max_radius=50, expand_speed=2, lifespan=30):
        """
        Initializes an Explosion sprite.

        Args:
            pos (tuple[int, int]): The center of the explosion.
            max_radius (int): The maximum radius of the explosion.
            expand_speed (int): The speed at which the explosion expands.
            lifespan (int): The duration of the explosion in frames.
        """
        super().__init__()
        self.pos = pos
        self.max_radius = max_radius
        self.current_radius = 0
        self.expand_speed = expand_speed
        self.lifespan = lifespan
        self.radius = 0  # Add radius attribute for collision detection

        self.image = pygame.Surface([self.max_radius * 2, self.max_radius * 2], pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        """Expand the explosion and decrease its lifespan."""
        self.current_radius += self.expand_speed
        self.radius = self.current_radius  # Update radius for collision
        self.lifespan -= 1

        if self.lifespan <= 0 or self.current_radius > self.max_radius:
            self.kill()
            return

        self.image.fill((0, 0, 0, 0))  # Clear the surface
        pygame.draw.circle(self.image, WHITE, (self.max_radius, self.max_radius), self.current_radius)
        self.rect = self.image.get_rect(center=self.pos)
        self.rect = self.image.get_rect(center=self.pos)
