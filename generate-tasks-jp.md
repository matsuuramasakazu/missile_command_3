---
description:
globs:
alwaysApply: false
---
# ルール: PRDからのタスクリスト生成

## 目標

既存のプロダクト要求仕様書 (PRD) に基づいて、詳細なステップバイステップのタスクリストをMarkdown形式で作成するAIアシスタントをガイドする。タスクリストは開発者が実装を進めるための指針となるべきである。

## 出力

- **フォーマット:** Markdown (`.md`)
- **場所:** `/tasks/`
- **ファイル名:** `tasks-[prd-file-name].md` (例: `tasks-prd-user-profile-editing.md`)

## プロセス

1.  **PRD参照を受け取る:** ユーザーはAIに特定のPRDファイルを指定する。
2.  **PRDを分析する:** AIは指定されたPRDの機能要件、ユーザーストーリー、その他のセクションを読み込み、分析する。
3.  **フェーズ1: 親タスクを生成する:** PRDの分析に基づいて、ファイルを生成し、機能の実装に必要な主要な高レベルタスクを生成する。高レベルタスクの数はあなたの判断に委ねる。おそらく5つ程度になるだろう。これらのタスクを指定されたフォーマットでユーザーに提示する（まだサブタスクは含めない）。ユーザーに「PRDに基づいて高レベルタスクを生成しました。サブタスクを生成する準備はできましたか？続行するには「Go」と応答してください。」と通知する。
4.  **確認を待つ:** 一時停止し、ユーザーが「Go」と応答するのを待つ。
5.  **フェーズ2: サブタスクを生成する:** 
    - ユーザーが確認したら、各親タスクを、親タスクを完了するために必要なより小さく実行可能なサブタスクに分解する。
    - サブタスクが親タスクから論理的に派生し、PRDによって示唆される実装の詳細をカバーしていることを確認する。
    - 追加した機能の実装ごとに単体テストを実装するサブタスクを作成する。
    - プルリクエストのコメントに従って修正するサブタスクを作成する。
6.  **関連ファイルを特定する:** タスクとPRDに基づいて、作成または変更が必要になる可能性のあるファイルを特定する。該当する場合は対応するテストファイルを含め、`Relevant Files` セクションの下にこれらをリストする。
7.  **最終出力を生成する:** 親タスク、サブタスク、関連ファイル、およびメモを組み合わせて最終的なMarkdown構造にする。
8.  **タスクリストを保存する:** 生成されたドキュメントを`/tasks/`ディレクトリに、入力PRDファイルのベース名と一致するファイル名`tasks-[prd-file-name].md`で保存する（例: 入力が`prd-user-profile-editing.md`だった場合、出力は`tasks-prd-user-editing.md`となる）。

## 出力フォーマット

生成されるタスクリストは、この構造に_従う必要がある_:

```markdown
## Relevant Files

- `path/to/file1.py` - このファイルが関連する理由の簡単な説明（例: この機能の主要コンポーネントを含む）。
- `path/to/test_file1.py` - `file1.py`の単体テスト。
- `path/to/helpers.py` - 簡単な説明（例: 計算に必要なユーティリティ関数）。
- `path/to/test_helpers.py` - `helpers.py`の単体テスト。

### Notes

- 単体テストは通常、テスト対象のコードファイルと同じディレクトリに配置する必要がある（例: `my_component.py`と`test_mycomponent.py`を同じディレクトリに）。
- テストを実行するには`uv run --frozen pytest [optional/path/to/test/file]`を使用する。パスを指定せずに実行すると、pytest構成によって検出されたすべてのテストが実行される。

## Tasks

- [ ] 1.0 親タスクのタイトル
  - [ ] 1.1 [サブタスクの説明 1.1]
  - [ ] 1.2 [サブタスクの説明 1.2]
- [ ] 2.0 親タスクのタイトル
  - [ ] 2.1 [サブタスクの説明 2.1]
- [ ] 3.0 親タスクのタイトル (構造または構成のみの場合はサブタスクが不要な場合がある)
```

## インタラクションモデル

プロセスでは、詳細なサブタスクの生成に進む前に、親タスクを生成した後にユーザーの確認（「Go」）を得るために明示的に一時停止が必要である。これにより、高レベルの計画が詳細に入る前にユーザーの期待と一致していることを確認する。

## 対象読者

タスクリストの主な読者は、機能を実装する**ジュニア開発者**であると想定する。