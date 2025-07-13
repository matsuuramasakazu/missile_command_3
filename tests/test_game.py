import pygame
import pytest
from game import Game
from sprites import PlayerMissile, EnemyMeteor, Explosion
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Pygameの初期化をモックまたはスキップ
pygame.init = lambda: None
pygame.display.set_mode = lambda size: pygame.Surface(size)
pygame.display.get_surface = lambda: pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.sprite.Group = pygame.sprite.Group  # 実際のGroupを使用


@pytest.fixture
def game_instance():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game(screen)
    return game


def test_find_closest_base(game_instance):
    # 基地の初期位置を確認 (settings.pyに依存)
    # game_instance._setup_initial_sprites() で設定される
    base1 = list(game_instance.bases)[0]  # 左端の基地
    base2 = list(game_instance.bases)[1]  # 中央の基地
    base3 = list(game_instance.bases)[2]  # 右端の基地

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
    mouse_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": target_pos}
    )
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
    assert closest_base.ammo == 9  # 弾薬が1減っていることを確認

    # 弾薬がない基地からは発射されないことを確認
    # 全ての弾薬を消費させる
    for base in game_instance.bases:
        base.ammo = 0

    # 再度クリックしてもミサイルが発射されないことを確認
    game_instance.handle_events([mouse_event])
    assert len(game_instance.player_missiles) == 1  # ミサイルの数は増えていない

    # 破壊された基地からは発射されないことを確認
    # 全ての基地を破壊する
    for base in game_instance.bases:
        base.alive = False

    # 再度クリックしてもミサイルが発射されないことを確認
    game_instance.handle_events([mouse_event])
    assert len(game_instance.player_missiles) == 1  # ミサイルの数は増えていない


def test_explosion_destroys_meteor(game_instance):
    """
    爆発が隕石を正しく破壊することを確認するテスト。
    """
    # 隕石を作成
    meteor = EnemyMeteor(start_pos=(300, 0), target_pos=(300, SCREEN_HEIGHT), speed=1)
    game_instance.enemy_meteors.add(meteor)
    game_instance.all_sprites.add(meteor)

    # 隕石を迎撃するためのミサイルを発射
    missile = PlayerMissile(
        start_pos=(0, 0), target_pos=(300, 50)
    )  # 隕石の進路上に爆発を生成
    game_instance.player_missiles.add(missile)
    game_instance.all_sprites.add(missile)

    # ミサイルがターゲットに到達するまでゲームを更新
    while not missile.is_at_target():
        missile.update()

    # 最初の状態を確認
    assert meteor in game_instance.enemy_meteors
    assert missile in game_instance.player_missiles

    # 衝突判定と爆発の生成を実行
    game_instance.update()

    # ミサイルが消え、爆発が生成されたことを確認
    assert missile not in game_instance.player_missiles
    assert len(game_instance.explosions) == 1

    # 爆発が隕石を破壊するまでゲームを更新
    # 爆発は拡大するので、数フレーム更新して衝突を確実にする
    for _ in range(25):
        game_instance.update()

    # 隕石が破壊されたことを確認
    assert meteor not in game_instance.enemy_meteors
    assert not meteor.alive()


@pytest.fixture
def game_with_city(game_instance):
    city = list(game_instance.cities)[0]
    return game_instance, city


@pytest.fixture
def game_with_base(game_instance):
    base = list(game_instance.bases)[0]
    return game_instance, base


def test_explosion_destroys_city(game_with_city):
    """
    爆発が都市を正しく破壊することを確認するテスト。
    """
    game_instance, city = game_with_city

    # 最初の状態を確認
    assert city in game_instance.cities

    # 都市の位置に爆発を生成
    explosion = Explosion(pos=city.rect.center, max_radius=50)
    game_instance.explosions.add(explosion)
    game_instance.all_sprites.add(explosion)

    # 衝突判定を実行
    game_instance.update()

    # 都市が破壊されたことを確認
    assert city not in game_instance.cities
    assert not city.alive()


def test_explosion_destroys_base(game_with_base):
    """
    爆発が基地を正しく破壊することを確認するテスト。
    """
    game_instance, base = game_with_base

    # 最初の状態を確認
    assert base in game_instance.bases
    assert base.is_alive

    # 基地の位置に爆発を生成
    explosion = Explosion(pos=base.rect.center, max_radius=50)
    game_instance.explosions.add(explosion)
    game_instance.all_sprites.add(explosion)

    # 衝突判定を実行
    game_instance.update()

    # 基地が破壊されたことを確認
    assert not base.is_alive
    # 基地は破壊されてもリストに残るが、aliveフラグがFalseになる
    assert base in game_instance.bases
    assert not list(game_instance.bases)[0].is_alive
