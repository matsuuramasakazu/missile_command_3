import pygame
from sprites import MissileBase, PlayerMissile, Explosion


def test_missile_base_ammo_consumption():
    """Test that MissileBase consumes ammo correctly."""
    pygame.init()

    base = MissileBase(x=100, y=100, ammo=10)
    assert base.ammo == 10

    missile = base.fire_missile(target_pos=(200, 200))

    assert base.ammo == 9
    assert isinstance(missile, PlayerMissile)

    for _ in range(9):
        base.fire_missile(target_pos=(200, 200))

    assert base.ammo == 0

    last_missile = base.fire_missile(target_pos=(200, 200))

    assert base.ammo == 0
    assert last_missile is None

    pygame.quit()


def test_player_missile_movement():
    """Test that PlayerMissile moves towards its target."""
    pygame.init()

    start_pos = (100, 500)
    target_pos = (200, 300)
    missile = PlayerMissile(start_pos, target_pos, speed=10)

    assert missile.rect.center == start_pos

    for _ in range(5):
        missile.update()

    assert missile.rect.center != start_pos

    at_target = False
    for _ in range(25):
        missile.update()
        if missile.is_at_target():
            at_target = True
            break

    assert at_target

    pygame.quit()


def test_explosion_expansion_and_lifespan():
    """Test that Explosion expands and eventually dies."""
    pygame.init()

    sprites = pygame.sprite.Group()
    explosion = Explosion((300, 300), 50, 5, 10, sprites)

    assert explosion.current_radius == 0
    assert explosion.lifespan == 10
    assert explosion.alive()

    for _ in range(5):
        sprites.update()

    assert explosion.current_radius == 25
    assert explosion.lifespan == 5
    assert explosion.alive()

    for _ in range(5):
        sprites.update()

    assert explosion.lifespan == 0
    assert not explosion.alive()

    pygame.quit()
