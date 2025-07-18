## Relevant Files

-   `main.py` - ゲームのメインエントリーポイント。Pygameの初期化とメインゲームループを管理します。
-   `game.py` - ゲームの主要なロジック、状態（ステージ、ゲームオーバー）、オブジェクトの管理を行うクラスを含みます。
-   `sprites.py` - ゲームに登場するすべてのオブジェクト（都市、基地、ミサイル、隕石、爆発）のクラスを定義します。
-   `settings.py` - 画面サイズ、色、フレームレート、ゲームの基本設定などの定数を一元管理します。
-   `tests/test_game.py` - `game.py`内のゲームロジック（スコア計算、レベルアップなど）の単体テスト。
-   `tests/test_sprites.py` - `sprites.py`内の各クラスの動作（移動、衝突など）に関する単体テスト。

### Notes

-   単体テストは通常、テスト対象のコードファイルと同じディレクトリに配置する必要がある（例: `my_component.py`と`test_mycomponent.py`を同じディレクトリに）。
-   テストを実行するには`uv run --frozen pytest [optional/path/to/test/file]`を使用する。パスを指定せずに実行すると、pytest構成によって検出されたすべてのテストが実行される。

## Tasks

-   [x] 1.0 プロジェクトのセットアップと基本コンポーネントの作成
    -   [x] 1.1 `pygame`をプロジェクト依存関係として追加する (`uv add pygame`)。
    -   [x] 1.2 `main.py`でPygameを初期化し、指定されたサイズのゲームウィンドウを作成する。
    -   [x] 1.3 `settings.py`を作成し、画面の幅・高さ、色（黒、白など）、フレームレートを定義する。
    -   [x] 1.4 `sprites.py`に、静的な`City`クラスと`MissileBase`クラスを作成する。
    -   [x] 1.5 `game.py`で、PRDに従って6つの都市と3つのミサイル基地を画面下部に描画する処理を実装する。

-   [x] 2.0 プレイヤーのミサイル発射機能の実装
    -   [x] 2.1 `game.py`でマウスのクリックイベントを検知し、クリック座標を取得する。
    -   [x] 2.2 クリック座標に最も近い、破壊されていないミサイル基地を特定するロジックを実装する。
    -   [x] 2.3 `sprites.py`に`PlayerMissile`クラスを作成する。このクラスは発射元と目標地点の座標を持つ。
    -   [x] 2.4 `PlayerMissile`が発射元から目標地点まで直線上を移動するロジックを実装する。
    -   [x] 2.5 各`MissileBase`に弾薬数の属性を追加し、発射するたびに減少させる。

-   [x] 2.5 単体テストの作成
    -   [x] 2.5.1 `tests/test_sprites.py`で、`MissileBase`が正しく弾薬を消費することを確認するテストを作成する。
    -   [x] 2.5.2 `tests/test_sprites.py`で、`PlayerMissile`が目標に向かって正しく移動することを確認するテストを作成する。
    -   [x] 2.5.3 `tests/test_game.py`で、クリック時に最も近い基地からミサイルが発射されることを確認するテストを作成する。

-   [x] 3.0 敵（隕石）の出現と落下システムの実装
    -   [x] 3.1 `sprites.py`に`EnemyMeteor`クラスを作成する。
    -   [x] 3.2 `EnemyMeteor`が画面上部のランダムな位置に出現し、地上のランダムな目標（都市または基地）に向かって落下するロジックを実装する。
    -   [x] 3.3 `game.py`で、現在のレベルに基づいて一定数の隕石を生成するステージ管理システムを構築する。
    -   [x] 3.4 隕石の落下速度にバリエーションを持たせる（例: `speed`属性をランダムな範囲で設定する）。

-   [x] 4.0 衝突判定と破壊ロジックの実装
    -   [x] 4.1 `sprites.py`に`Explosion`クラスを作成する。このクラスは一定時間で半径が拡大し、その後消滅する。
    -   [x] 4.2 プレイヤーのミサイルが目標地点に到達したら、その場に`Explosion`オブジェクトを生成する。
    -   [x] 4.3 `Explosion`と`EnemyMeteor`の衝突判定を実装し、衝突した隕石を破壊する。
    -   [x] 4.4 隕石が地表（都市、基地）に到達したら、その場に`Explosion`オブジェクトを生成する。
    -   [x] 4.5 `Explosion`と`City`または`MissileBase`の衝突判定を実装し、衝突した都市や基地を破壊する。
    -   [x] 4.6 単体テストの作成
        -   [x] 4.6.1 `tests/test_sprites.py`で、`Explosion`が正しく拡大・消滅することを確認するテストを作成する。
        -   [x] 4.6.2 `tests/test_game.py`で、爆発が隕石を正しく破壊することを確認するテストを作成する。
        -   [x] 4.6.3 `tests/test_game.py`で、爆発が都市や基地を正しく破壊することを確認するテストを作成する。

-   [x] 5.0 ゲーム進行とUI（スコア・レベル）の実装
    -   [x] 5.1 隕石を破壊した際にスコアを加算するロジックを実装する。
    -   [x] 5.2 `game.py`にステージクリア条件（例: 全ての隕石を破壊）を判定するロジックを追加する。
    -   [x] 5.3 ステージクリア時にボーナススコアを計算し、次のレベルに進む処理を実装する。
    -   [x] 5.4 すべての都市が破壊されたらゲームオーバー状態に移行させる。
    -   [x] 5.5 画面上にスコア、残存都市数、各基地の弾薬数を描画するUI表示機能を実装する。

-   [x] 6.0 サウンドエフェクトの追加と仕上げ
    -   [x] 6.1 ゲームオーバー画面（例: 「Game Over」テキストと最終スコア表示）を実装する。
    -   [x] 6.2 全体のコードをレビューし、不要なコードの削除やコメントの追加を行う。
