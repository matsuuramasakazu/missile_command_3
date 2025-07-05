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
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        game.handle_events(events)

        screen.fill(BLACK)

        game.update()
        game.draw()

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
