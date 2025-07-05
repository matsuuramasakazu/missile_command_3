"""
Game class for Missile Command.
"""
import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from sprites import City, MissileBase, PlayerMissile

class Game:
    """Manages game state, sprites, and game loop."""
    def __init__(self, screen):
        """Initialize the game."""
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.cities = pygame.sprite.Group()
        self.bases = pygame.sprite.Group()
        self.player_missiles = pygame.sprite.Group()
        self._setup_initial_sprites()

    def _setup_initial_sprites(self):
        """Create initial cities and missile bases."""
        ground_level = SCREEN_HEIGHT - 50

        # Base positions
        base_positions = [100, SCREEN_WIDTH // 2, SCREEN_WIDTH - 100]
        for i, pos in enumerate(base_positions):
            base = MissileBase(x=pos - 20, y=ground_level)
            self.all_sprites.add(base)
            self.bases.add(base)

        # City positions
        city_group_1 = [p + 50 for p in base_positions[:1]] + [p + 110 for p in base_positions[:1]] + [p + 170 for p in base_positions[:1]]
        city_group_2 = [p - 50 for p in base_positions[2:]] + [p - 110 for p in base_positions[2:]] + [p - 170 for p in base_positions[2:]]
        city_positions = city_group_1 + city_group_2

        for pos in city_positions:
            city = City(x=pos - 25, y=ground_level + 5)
            self.all_sprites.add(city)
            self.cities.add(city)

    def handle_events(self, events):
        """Handle all game events."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                target_pos = event.pos
                closest_base = self._find_closest_base(target_pos)
                if closest_base:
                    new_missile = closest_base.fire_missile(target_pos)
                    if new_missile:
                        self.all_sprites.add(new_missile)
                        self.player_missiles.add(new_missile)

    def _find_closest_base(self, target_pos):
        """Finds the closest active missile base to the target position."""
        closest_base = None
        min_distance = float('inf')

        for base in self.bases:
            if not base.is_destroyed() and base.ammo > 0:
                distance = math.hypot(base.rect.centerx - target_pos[0], base.rect.centery - target_pos[1])
                if distance < min_distance:
                    min_distance = distance
                    closest_base = base
        return closest_base

    def update(self):
        """Update all game sprites."""
        self.all_sprites.update()

    def draw(self):
        """Draw all sprites to the screen."""
        self.all_sprites.draw(self.screen)
