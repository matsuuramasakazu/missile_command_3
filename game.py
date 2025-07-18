"""
Game class for Missile Command.
"""

import pygame
import math
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    SCORE_PER_METEOR,
    BONUS_PER_CITY,
    BONUS_PER_AMMO,
)
from sprites import City, MissileBase, EnemyMeteor, Explosion
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
        self.enemy_meteors = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.score = 0
        self.game_over = False
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        self.level = 0
        self.meteors_to_spawn_this_level = 0
        self.meteors_spawned_this_level = 0
        self._setup_initial_sprites()
        self.meteor_spawn_timer = 0
        self.meteor_spawn_interval = 60
        self._start_new_level()

    def _start_new_level(self):
        """Initializes parameters for a new game level."""
        self.level += 1
        self.meteors_to_spawn_this_level = 5 + (self.level * 2)
        self.meteors_spawned_this_level = 0
        self.meteor_spawn_interval = max(20, 60 - (self.level * 5))
        print(
            f"Starting Level {self.level} with {self.meteors_to_spawn_this_level} meteors."
        )

    def _spawn_meteor(self):
        """Spawns a single enemy meteor."""
        if self.meteors_spawned_this_level < self.meteors_to_spawn_this_level:
            start_x = random.randint(0, SCREEN_WIDTH)
            start_pos = (start_x, 0)

            all_targets = list(self.cities) + [
                b for b in self.bases if not b.is_destroyed()
            ]
            if not all_targets:
                return

            target = random.choice(all_targets)
            target_pos = target.rect.center

            speed = random.uniform(1 + (self.level * 0.2), 3 + (self.level * 0.2))

            EnemyMeteor(
                start_pos, target_pos, speed, self.all_sprites, self.enemy_meteors
            )
            self.meteors_spawned_this_level += 1

    def _setup_initial_sprites(self):
        """Create initial cities and missile bases."""
        ground_level = SCREEN_HEIGHT - 50

        # Setup missile bases
        base_positions = [100, SCREEN_WIDTH // 2, SCREEN_WIDTH - 100]
        for pos in base_positions:
            MissileBase(pos - 20, ground_level, 40, 20, 10, self.all_sprites, self.bases)

        # Setup cities
        city_positions = []
        # Cities to the right of the left base
        for i in range(3):
            city_positions.append(base_positions[0] + 50 + i * 60)
        # Cities to the left of the right base
        for i in range(3):
            city_positions.append(base_positions[2] - 90 - i * 60)

        for pos in city_positions:
            City(pos, ground_level + 5, 50, 30, self.all_sprites, self.cities)

    def handle_events(self, events):
        """Handle all game events."""
        if self.game_over:
            return

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                target_pos = event.pos
                closest_base = self._find_closest_base(target_pos)
                if closest_base:
                    closest_base.fire_missile(
                        target_pos, self.all_sprites, self.player_missiles
                    )

    def _find_closest_base(self, target_pos):
        """Finds the closest active missile base to the target position."""
        closest_base = None
        min_distance = float("inf")

        for base in self.bases:
            if not base.is_destroyed() and base.ammo > 0:
                distance = math.hypot(
                    base.rect.centerx - target_pos[0], base.rect.centery - target_pos[1]
                )
                if distance < min_distance:
                    min_distance = distance
                    closest_base = base
        return closest_base

    def update(self):
        """Update all game sprites."""
        if self.game_over:
            return

        self.meteor_spawn_timer += 1
        if self.meteor_spawn_timer >= self.meteor_spawn_interval:
            self._spawn_meteor()
            self.meteor_spawn_timer = 0

        self.all_sprites.update()

        for missile in self.player_missiles:
            if missile.is_at_target():
                Explosion(
                    missile.target_pos, 50, 2, 30, self.all_sprites, self.explosions
                )
                missile.kill()

        for meteor in self.enemy_meteors:
            if meteor.has_reached_target():
                Explosion(
                    meteor.rect.center, 30, 2, 30, self.all_sprites, self.explosions
                )
                meteor.kill()

        for explosion in self.explosions:
            destroyed_meteors = pygame.sprite.spritecollide(
                explosion, self.enemy_meteors, True, pygame.sprite.collide_circle
            )
            if destroyed_meteors:
                self.score += SCORE_PER_METEOR * len(destroyed_meteors)

        pygame.sprite.groupcollide(
            self.explosions, self.cities, False, True, pygame.sprite.collide_circle
        )
        collided_bases = pygame.sprite.groupcollide(
            self.explosions, self.bases, False, False, pygame.sprite.collide_circle
        )
        for _, bases in collided_bases.items():
            for base in bases:
                base.destroy()

        if (
            self.meteors_spawned_this_level == self.meteors_to_spawn_this_level
            and not self.enemy_meteors
        ):
            for city in self.cities:
                self.score += BONUS_PER_CITY
            for base in self.bases:
                if not base.is_destroyed():
                    self.score += BONUS_PER_AMMO * base.ammo

            self._start_new_level()

        if not self.cities:
            self.game_over = True

    def _draw_ui(self):
        """Draws the user interface (score, ammo, etc.)."""
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        cities_text = self.font.render(f"Cities: {len(self.cities)}", True, WHITE)
        self.screen.blit(cities_text, (SCREEN_WIDTH - cities_text.get_width() - 10, 10))

        for base in self.bases:
            if not base.is_destroyed():
                ammo_text = self.font.render(f"{base.ammo}", True, WHITE)
                ammo_pos = (
                    base.rect.centerx - ammo_text.get_width() // 2,
                    base.rect.bottom + 5,
                )
                self.screen.blit(ammo_text, ammo_pos)

    def _draw_game_over_screen(self):
        """Draws the game over screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("GAME OVER", True, WHITE)
        text_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40)
        )
        self.screen.blit(game_over_text, text_rect)

        final_score_text = self.font.render(
            f"Final Score: {self.score}", True, WHITE
        )
        score_rect = final_score_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)
        )
        self.screen.blit(final_score_text, score_rect)

    def draw(self):
        """Draw all sprites to the screen."""
        self.all_sprites.draw(self.screen)
        self._draw_ui()

        if self.game_over:
            self._draw_game_over_screen()