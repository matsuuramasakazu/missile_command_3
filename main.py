"""
Main file for Missile Command game.
"""
import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, FPS
from game import Game

def main():
    """Main game loop."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Missile Command")

    clock = pygame.time.Clock()
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        game.update()
        game.draw()

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
