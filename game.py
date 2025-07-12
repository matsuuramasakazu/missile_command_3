"""
Game class for Missile Command.
"""
import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from sprites import City, MissileBase, PlayerMissile, EnemyMeteor, Explosion
import random

class Game:
    """Manages game state, sprites, and game loop."""
    def __init__(self, screen):
        """Initialize the game."""
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.cities = pygame.sprite.Group()
        self.bases = pygame.sprite.Group()
        self.player_missiles = pygame.sprite.Group()
        self.enemy_meteors = pygame.sprite.Group() # New sprite group for meteors
        self.explosions = pygame.sprite.Group()
        self.level = 0 # Current game level
        self.meteors_to_spawn_this_level = 0
        self.meteors_spawned_this_level = 0
        self._setup_initial_sprites()
        self.meteor_spawn_timer = 0
        self.meteor_spawn_interval = 60
        self._start_new_level() # Start the first level

    def _start_new_level(self):
        """Initializes parameters for a new game level."""
        self.level += 1
        # Determine number of meteors to spawn based on level
        self.meteors_to_spawn_this_level = 5 + (self.level * 2) # Example: more meteors per level
        self.meteors_spawned_this_level = 0
        # Adjust spawn interval based on level (faster for higher levels)
        self.meteor_spawn_interval = max(20, 60 - (self.level * 5)) # Example: faster spawn
        print(f"Starting Level {self.level} with {self.meteors_to_spawn_this_level} meteors.")

    def _spawn_meteor(self):
        """Spawns a single enemy meteor."""
        if self.meteors_spawned_this_level < self.meteors_to_spawn_this_level:
            start_x = random.randint(0, SCREEN_WIDTH)
            start_pos = (start_x, 0) # Meteors start at the top of the screen

            # Choose a random target (city or base)
            all_targets = list(self.cities) + [b for b in self.bases if not b.is_destroyed()]
            if not all_targets:
                return # No targets left

            target = random.choice(all_targets)
            target_pos = target.rect.center

            speed = random.uniform(1 + (self.level * 0.2), 3 + (self.level * 0.2)) # Speed increases with level

            new_meteor = EnemyMeteor(start_pos, target_pos, speed)
            self.all_sprites.add(new_meteor)
            self.enemy_meteors.add(new_meteor)
            self.meteors_spawned_this_level += 1

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
        self.meteor_spawn_timer += 1
        if self.meteor_spawn_timer >= self.meteor_spawn_interval:
            self._spawn_meteor()
            self.meteor_spawn_timer = 0

        self.all_sprites.update()

        for missile in self.player_missiles:
            if missile.is_at_target():
                explosion = Explosion(missile.target_pos)
                self.all_sprites.add(explosion)
                self.explosions.add(explosion)
                missile.kill()

        for meteor in self.enemy_meteors:
            if meteor.has_reached_target():
                explosion = Explosion(meteor.rect.center, max_radius=30) # Smaller explosion for meteor impact
                self.all_sprites.add(explosion)
                self.explosions.add(explosion)
                meteor.kill()

        # Check for collisions between explosions and meteors
        for explosion in self.explosions:
            pygame.sprite.spritecollide(explosion, self.enemy_meteors, True, pygame.sprite.collide_circle)

        # Check for collisions with cities and bases
        pygame.sprite.groupcollide(self.explosions, self.cities, False, True, pygame.sprite.collide_circle)
        collided_bases = pygame.sprite.groupcollide(self.explosions, self.bases, False, False, pygame.sprite.collide_circle)
        for explosion, bases in collided_bases.items():
            for base in bases:
                if base.alive:
                    base.alive = False
                    base.image.fill((80, 80, 80)) # Change color to show destruction

    def draw(self):
        """Draw all sprites to the screen."""
        self.all_sprites.draw(self.screen)
