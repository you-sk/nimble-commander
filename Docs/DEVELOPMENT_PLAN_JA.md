# 日本語版Fork 開発計画・初回調査

調査日: 2026-11-05。対象上流コミット: `ee4abffb165019106c7420db5ea8b51623e4baa4`。
上流: https://github.com/mikekazakov/nimble-commander

初回は調査と文書整備のみ。以下の「実装あり」はソース確認を示し、GUIでの動作検証とは区別する。

## 環境と再現方法

- macOS 27.0.1 (26A434)、arm64。
- Xcode 27.2 (27B52)、Xcode内Command Line Tools、Apple Swift 6.4.2。
- Git 2.54.0、GitHub CLI 2.103.3。既存キーチェーン認証を使用。
- 上流 `Docs/Building.md` もXcode 27.2を要求。追加インストールなしでベースラインを試行。
- `3rd_Party/README.md` によると依存ライブラリのヘッダとビルド済み成果物は上流に同梱。初回にbootstrapを実行する必要はない。
- `xcpretty` と `create-dmg` は未導入。前者は上流テスト補助スクリプトの整形用、後者は配布DMG作成用。今回はxcodebuildとテスト実行ファイルを直接利用し、配布物は作成しない。

リポジトリ直下から実行する（成果物はソース外に置く）:

```sh
xcodebuild -project Source/NimbleCommander/NimbleCommander.xcodeproj \
  -scheme NimbleCommander-Unsigned -configuration Debug \
  -derivedDataPath /tmp/nc-ja-baseline-derived build
xcodebuild -project Source/NimbleCommander/NimbleCommander.xcodeproj \
  -scheme UnitTests -configuration Debug -destination 'platform=macOS,arch=arm64' \
  -derivedDataPath /tmp/nc-ja-tests-derived build
```

`UnitTests` はXCTestテストケースではなく実行ファイル群をビルドする。`Scripts/run_all_unit_tests.sh` と同様に、生成された各 `*UT` を実行する必要がある。統合テストは別スキームであり、Docker等の前提があるため単体テストと区別する。
### 確定したビルド・テスト結果

- 無改造Unsigned Debug: `BUILD SUCCEEDED`、終了コード0。既定のarm64/x86_64をビルド。
- UnitTests Debug (arm64): `BUILD SUCCEEDED`、終了コード0。
- 生成された9本を実行し全て終了コード0。合計546ケース、124,952アサーション。

| 実行ファイル | ケース数 | アサーション数 |
|---|---:|---:|
| BaseUT | 75 | 70,559 |
| ConfigUT | 38 | 76 |
| NimbleCommanderUT | 45 | 363 |
| OperationsUT | 24 | 280 |
| PanelUT | 50 | 1,295 |
| TermUT | 109 | 7,821 |
| UtilityUT | 122 | 1,898 |
| VFSIconUT | 21 | 29 |
| VFSUT | 62 | 42,631 |

初期の制限付き実行ではFSEvents/UTI等の失敗と一部プロセス終了があった。ビルド完了後、制限外で全9本を再実行して上記成功を確認した。初期失敗の各原因を完全に特定したものではない。破壊操作を含むOperations単体テストはTempTestDirを用いる既存fixtureを確認した。統合テストは未実行。

Unsignedアプリを起動し、アクセシビリティツリーで左右2ペインと英語メニューを確認。日本語表示と全ファイル操作のGUI検証は今後の課題。ヘルパー導入・権限変更はしていない。

警告: XIBのTextured appearance非推奨、libtoolの一部objectにシンボルなし、静的ライブラリへのSwift標準ライブラリ埋込設定、出力指定のないRun Script。CoreSimulator/ログサービスへの接続メッセージも出たがビルドは成功。TermUTでuptimeの標準出力メッセージ、UtilityUTでhdiutil detach非推奨メッセージあり。いずれも最終テスト終了コードは0。

生ログはローカル一時領域に保持し、環境固有パスを含むためコミットしない。移動前のソースで実行したビルドであり、最終配置先での再ビルドは未実施。

## 日本語化対象一覧

`Source` 以下のString Catalogは55ファイル、1,412エントリ。ローカライズ登録数は zh-Hans 1,412、ru 1,304、en 1,049、ja 0（ソース言語によるフォールバックを含むため登録数と表示可能数は異なる）。

| 対象 | 実装場所（リポジトリ相対） | 作業 |
|---|---|---|
| メニュー | Source/NimbleCommander/NimbleCommander/Bootstrap/mul.lproj/MainMenu.xcstrings | ja追加、キー表記統一 |
| 一般UI・アプリ名 | 同 Resources/Localizable.xcstrings、InfoPlist.xcstrings | ja追加、製品名の方針決定 |
| 設定画面 | 同 Preferences/Preferences.xcstrings、mul.lproj/*.xcstrings | 全タブ、説明文、競合表示 |
| パネル・接続・検索 | 同 States/FilePanels 以下のxcstrings | 文脈別翻訳、件数・書式引数維持 |
| コピー・移動・削除等 | Source/Operations 以下のxcstrings | 破壊操作の意味を明確化 |
| ビューア・共通UI | Source/Viewer、Utility、CUI、RoutedIO のリソース | 依存バンドルもja対応 |
| 英語直書き | .mm/.cppの表示文字列、XIB | NSLocalizedString呼出しと未対応箇所を分類。ログや内部識別子は翻訳しない |

String CatalogとBase.lprojのXIBが中心で、従来形式のstringsはサードパーティにも存在する。既存のNSLocalizedString / NSLocalizedStringFromTableとバンドル構造を維持する。プロジェクトの言語登録と各リソースバンドルへのja出力を確認し、macOSのアプリ別言語設定で日本語・英語の両方を試す。

日本語フォント・文字幅は未検証。`States/FilePanels/List/PanelListViewGeometry.mm` 等の独自レイアウトとテーマのフォント指定が対象。漢字・かな・半角カナ・結合濁点・絵文字・長いパスの一時fixtureを使い、リスト/簡易/ギャラリー表示、検索、インライン改名、設定ダイアログの欠けを確認する。

## キーバインド対応表

根拠: `Source/NimbleCommander/NimbleCommander/Bootstrap/Actions.h`、`Core/ActionsShortcutsManager.cpp`、`States/FilePanels/PanelView.mm`。

| 要望 | 現在の既定値・実装 | 方針 |
|---|---|---|
| Enterで起動・移動 | Returnがmenu.file.enter→OnOpen。明示的なネイティブOpenはShift+Return。重ね合わせターミナルにもReturnの優先処理あり | 既存機能を維持。通常パネル・ターミナル・IME確定を区別して実機確認 |
| F2改名 | Ctrl+F6がrename_in_place、Shift+F6がmove_as | 既存アクションへF2を割当可能か検証 |
| Ctrl+X/C/V | ファイルコピーはCmd+C、貼付Cmd+V、移動Option+Cmd+V。専用cutは既定アクション表にない | Windowsプリセットは切取状態と取消仕様を先に定義 |
| F5コピー | copy_to実装済み | 維持 |
| F6移動 | move_to実装済み | 維持 |
| F7フォルダ作成 | create_directory実装済み | 維持 |
| F8削除 | delete実装済み。永久削除はShift+F8、ゴミ箱はCmd+Delete | 確認と意味を維持し日本語化 |
| Space選択 | Spaceはプレビュー。invert_item_selectionアクションは既定割当なし | プリセットで選択に割当、プレビューの代替を提示 |
| 複数選択 | Shift+移動、Shift+クリックの範囲選択、Cmd+クリックの個別選択 | Ctrl+クリックはmacOS文脈メニューとの競合を評価 |

設定のHotkeysタブと `hotkeyOverrides_v1` が既にあり、複数ショートカットの保存にも対応。新しい入力基盤は作らず、従来・Windows風プリセットの適用/復元をこの仕組みに載せる案とする。個別カスタマイズを保持する適用方式が必要。

OS競合の実機確認項目: Fキーのメディア機能/Fn設定、Mission Control等のユーザー割当、Ctrl+矢印、Ctrl+クリック、テキスト編集やターミナルのCtrl+C/X/V、日本語IMEのReturn/Space。OS側のキー割当は変更しない。

## 既存機能と不足の比較

以下の場所は `Source/NimbleCommander/NimbleCommander/States/FilePanels/` を基準とする。

| 機能 | 既存実装 | 不足・確認事項 |
|---|---|---|
| 複数ファイル一括起動 | Actions/OpenFile.mmが選択項目をFileOpenerへ渡す | 同一VFSホスト条件あり。実機で確認 |
| クリップボード移動 | Actions/InsertFromPasteboard.mmがCopyingへdocopy=falseで投入 | 取り込み元はNativeHost、旧NSFilenamesPboardType。Windows式cutとは別仕様 |
| フルパス表示 | PanelViewHeader.mmにパス欄あり | 先頭省略の単一行、検索中は隠れる。常時完全表示を要求するなら改善が必要 |
| パス直接入力 | Actions/GoToFolder.mm、GoToFolderSheetController、Cmd+Shift+G | ヘッダ自体は編集不可。既存ダイアログを活用 |
| 隠しファイル | sorting_view_hidden、Cmd+Shift+. | 日本語UIと保存の実機確認 |
| ユーザーLibrary | Actions/GoToFolder.mmのGoToLibraryFolder | 権限はOSに従う。アクセス制御を迂回しない |
| シンボリックリンク | Source/VFS、Source/Operations、Actions内リンク操作 | Copying/Optionsのpreserve_symlinks既定true。各操作の意味を維持 |
| ソートと表示の保存 | PanelControllerPersistency.mm、PanelDataOptionsPersistence、PanelViewPresentationSettings.mm | 再起動・タブ・VFSごとの復元範囲を実機確認 |

VFSとOperationsを維持し、UIから既存アクションへ接続する。非ネイティブVFSで利用できない機能を黙ってネイティブパス扱いしない。

## 段階的な実装計画

1. 無改造ビルドと単体テストの基準確立。起動・権限・警告を記録し、必要ならCI導入を別変更にする。
2. 用語集とカタログ一覧を作成。メニュー→主要ファイル操作→設定→補助ダイアログの順にjaを追加。英語のフォールバックを保持する。
3. ja/enの実機表示、IME、文字幅、書式引数、件数表現を検証。必要なレイアウト修正だけを独立コミットにする。
4. 既存Hotkeys上のプリセット設計と競合解決。Enter/F2/Spaceから小さく導入。切取は取消・失敗・外部アプリ連携を定義してから実装する。
5. 既存パス欄とGo To Folderを改善。長いパスとVFS表現を保持する。
6. 複数操作の不足を実機で再評価し、必要なものだけ追加。破壊操作は一時fixtureに限定する。

各変更をfeatureブランチでレビュー可能な単位にし、関連単体テストとja/enの確認結果を記録する。初回調査後は次フェーズの指示を待つ。

## ライセンス・公開の確認

- `LICENSE.md` はGNU GPL version 3であり保持する。
- Michael Kazakovのソース内著作権表示と上流Git履歴・タグを保持する。
- Forkであることと上流リンクを日本語READMEに明示。英語READMEとWHATS_NEW.mdは保持する。
- サードパーティのライセンスと通知も保持し、将来の配布前に各依存の義務を別途確認する。
- 今回はバイナリやリリースを公開しない。将来の配布時には対応ソース、改変の表示、ライセンス・通知等の提供方法を確認する。
- 公開対象は文書のみ。個人名・認証情報・ローカル固有パス・生ビルドログ・生成物を含めない。
- 公開Fork `you-sk/nimble-commander` の作成承認を得て作成済み。GitHub APIでowner、public、fork=true、parent/sourceが公式上流であることを確認。originはFork、upstreamは公式上流（push URLは無効化）。完全cloneと18タグを保持し、git fsck --connectivity-onlyは成功。push前に差分・追跡対象と送信先を確認する。
