import pygame
import pytest
from game import Game
from sprites import MissileBase, PlayerMissile
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Pygameの初期化をモックまたはスキップ
pygame.init = lambda: None
pygame.display.set_mode = lambda size: pygame.Surface(size)
pygame.sprite.Group = pygame.sprite.Group # 実際のGroupを使用

@pytest.fixture
def game_instance():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game(screen)
    return game

def test_find_closest_base(game_instance):
    # 基地の初期位置を確認 (settings.pyに依存)
    # game_instance._setup_initial_sprites() で設定される
    base1 = list(game_instance.bases)[0] # 左端の基地
    base2 = list(game_instance.bases)[1] # 中央の基地
    base3 = list(game_instance.bases)[2] # 右端の基地

    # クリック位置が中央の基地に近い場合
    target_pos_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    closest = game_instance._find_closest_base(target_pos_center)
    assert closest == base2

    # クリック位置が左端の基地に近い場合
    target_pos_left = (100, SCREEN_HEIGHT // 2)
    closest = game_instance._find_closest_base(target_pos_left)
    assert closest == base1

    # クリック位置が右端の基地に近い場合
    target_pos_right = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)
    closest = game_instance._find_closest_base(target_pos_right)
    assert closest == base3

def test_fire_missile_from_closest_base(game_instance):
    # 初期状態ではミサイルがないことを確認
    assert len(game_instance.player_missiles) == 0

    # 中央の基地に近い位置をクリック
    target_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Pygameイベントをシミュレート
    mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': target_pos})
    game_instance.handle_events([mouse_event])

    # ミサイルが1つ発射されたことを確認
    assert len(game_instance.player_missiles) == 1
    
    # 発射されたミサイルがPlayerMissileのインスタンスであることを確認
    missile = list(game_instance.player_missiles)[0]
    assert isinstance(missile, PlayerMissile)

    # 最も近い基地から発射されたことを確認 (ここでは中央の基地)
    closest_base = game_instance._find_closest_base(target_pos)
    # 発射元の基地の座標とミサイルの開始座標が一致することを確認
    assert missile.start_pos == closest_base.rect.midtop
    assert closest_base.ammo == 9 # 弾薬が1減っていることを確認

    # 弾薬がない基地からは発射されないことを確認
    # 全ての弾薬を消費させる
    for base in game_instance.bases:
        base.ammo = 0
    
    # 再度クリックしてもミサイルが発射されないことを確認
    game_instance.handle_events([mouse_event])
    assert len(game_instance.player_missiles) == 1 # ミサイルの数は増えていない

    # 破壊された基地からは発射されないことを確認
    # 全ての基地を破壊する
    for base in game_instance.bases:
        base.alive = False
    
    # 再度クリックしてもミサイルが発射されないことを確認
    game_instance.handle_events([mouse_event])
    assert len(game_instance.player_missiles) == 1 # ミサイルの数は増えていない
