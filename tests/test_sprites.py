
import pygame
import pytest
from sprites import MissileBase, PlayerMissile

def test_missile_base_ammo_consumption():
    """Test that MissileBase consumes ammo correctly."""
    # Initialize pygame to use its functionalities like Rect
    pygame.init()

    # Create a base with 10 ammo
    base = MissileBase(x=100, y=100, ammo=10)
    assert base.ammo == 10

    # Fire a missile
    missile = base.fire_missile(target_pos=(200, 200))

    # Check that ammo is reduced and a missile was returned
    assert base.ammo == 9
    assert isinstance(missile, PlayerMissile)

    # Fire all remaining missiles
    for _ in range(9):
        base.fire_missile(target_pos=(200, 200))
    
    assert base.ammo == 0

    # Try to fire one more time
    last_missile = base.fire_missile(target_pos=(200, 200))

    # Check that ammo is still 0 and no missile was returned
    assert base.ammo == 0
    assert last_missile is None

    pygame.quit()

def test_player_missile_movement():
    """Test that PlayerMissile moves towards its target."""
    pygame.init()

    start_pos = (100, 500)
    target_pos = (200, 300)
    missile = PlayerMissile(start_pos, target_pos, speed=10)

    # Check initial position
    assert missile.rect.center == start_pos

    # Update the missile's position a few times
    for _ in range(5):
        missile.update()

    # Check that the missile has moved from the start position
    assert missile.rect.center != start_pos

    # Continue updating until the missile should be destroyed
    # The distance is approx 223, so it should take about 23 updates
    for _ in range(25):
        missile.update()

    # The missile should be killed (removed from groups) when it reaches the target
    # We can check this by calling `alive()` on the sprite
    assert not missile.alive()

    pygame.quit()
