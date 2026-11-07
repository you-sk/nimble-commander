# 日本語版Forkの既定ブランチへの統合

実施日: 2026-11-07。

## 統合内容

GitHub CLIでFork `you-sk/nimble-commander` の既定ブランチが `main`、親が `mikekazakov/nimble-commander` であることを確認した。取得時のForkのmainは上流基準の `ee4abffb1`。

mainを基点に統合用ブランチを作成し、作業先端 `21d8aa56b` をマージコミット `7472c2618` で統合した。競合なし。統合直後のファイル内容は作業先端と完全一致し、追加の機能変更はない。

以下の各作業ブランチがすべて統合先の祖先であることを検証した。

- `docs/initial-ja-audit`: 環境・ビルド調査、開発計画。
- `feat/japanese-menu-file-dialogs`: 用語集、メインメニュー・主要操作画面。
- `feat/japanese-preferences`: 設定画面。
- `feat/japanese-search-connections-viewer`: 検索・接続・ビューア。
- `feat/japanese-localization-completion`: 残りのカタログ、翻訳監査ツール。
- `fix/japanese-ui-proofreading`: 長い名前の説明ラベル・入力欄の幅調整。
- `codex/disable-startup-prompts`: 上流更新機構と移動案内の停止、翻訳監査CI。

上流履歴と既存コミットを保持し、LICENSE.mdは変更なし。公開対象に生成物を追加していない。上流リポジトリにはpushせず、リリース・バイナリ公開も行わない。

## 検証方法

公式手順に沿い、Xcode 27.2で次のターゲットを順番にビルドした。ビルド出力はリポジトリ外へ配置。

```sh
xcodebuild -project Source/NimbleCommander/NimbleCommander.xcodeproj \
  -scheme NimbleCommander-Unsigned -configuration Debug \
  -destination 'platform=macOS,arch=arm64' \
  -derivedDataPath /tmp/nc-ja-localized-derived build
xcodebuild -project Source/NimbleCommander/NimbleCommander.xcodeproj \
  -scheme UnitTests -configuration Debug \
  -destination 'platform=macOS,arch=arm64' \
  -derivedDataPath /tmp/nc-ja-localized-derived build
python3 Scripts/audit_japanese_localization.py --check
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s Scripts/tests -v
```

Unsigned Debug・UnitTestsともBUILD SUCCEEDED、終了コード0。既存のシンボルなしobject、Swift埋込設定、出力指定なしスクリプト、テストInfo.plistのCopy Files登録等の警告は残る。

翻訳監査は55カタログ・1,415項目で未登録・未確認・引数エラー0。監査ツールの6テストも成功。単体テストは一時領域を作業場所にして実行し、ViewerUTはアプリ内部の実行ファイルを含める。

## 単体テスト結果

| テスト | ケース | アサーション | 結果 |
|---|---:|---:|---|
| BaseUT | 75 | 70,559 | 成功 |
| ConfigUT | 38 | 76 | 成功 |
| NimbleCommanderUT | 45 | 363 | 成功 |
| OperationsUT | 24 | 280 | 成功 |
| PanelUT | 50 | 1,292 | 想定内失敗 1件、終了コード0 |
| TermUT | 109 | 7,821 | 成功 |
| UtilityUT | 122 | 2,219 | 想定内失敗 3件、終了コード0 |
| VFSIconUT | 21 | 29 | 成功 |
| VFSUT | 62 | 42,625 | 成功 |
| ViewerUT | 43 | 1,207 | 成功 |

合計589ケース、126,471アサーション。全10本が終了コード0。

PanelUTの `ExternalTools execute a ui app` がPID取得で失敗。UtilityUTのタグ検索・変更に関する3ケース（RemoveTagFromAllItems / GatherAllItemsWithTag / ChangeLabelOfAllItemsWithTag）はインデックス待機の上限に到達した。いずれも上流で `[!mayfail]` が指定されたケースで、テストランナーは想定内失敗として扱った。想定外失敗は0、全ケース成功とは扱わない。

## 制約

この統合では同一ソースのビルド・テストを再実行し、日英の画面確認は既存の各検証記録を保持する。実IMEの追加経路、ログ画面・全エラー分岐の校正、署名が必要な特権ヘルパー、外部サービスが必要なIntegrationTestsは今回の確認範囲に含まない。

操作性改善の追加仕様は未実装。詳細は[表示校正記録](JAPANESE_UI_PROOFREADING_JA.md)と[起動・更新方針](FORK_STARTUP_POLICY_JA.md)を参照。
