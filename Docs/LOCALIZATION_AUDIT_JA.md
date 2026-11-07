# 日本語化の全体監査と残りのカタログ対応

実施日: 2026-11-06。環境: macOS 27.0.1 / arm64、Xcode 27.2。

## 結果

開始時は55カタログ・1,415項目のうち、日本語未登録398項目、明示的な英語を残したneeds_reviewが3項目だった。今回398項目を追加し、3項目を更新した（計401項目）。現在は全1,415項目にjaのstringUnitがあり、未登録・未確認状態・書式検査エラーは0。

これはカタログの網羅率であり、全画面・全エラー分岐の実機検証完了を意味しない。製品名、UNIXフラグ、キー記号、パターン構文等は意図的に原表記を維持する。

主な追加対象:

- 一括改名と文字範囲選択、ファイル属性変更。
- フォルダ移動、お気に入り管理、ソート・列メニュー、ボリューム情報。
- パターンによる選択、外部ツールのパラメータ入力、ログ表示、通知・確認メッセージ。
- InfoPlistのアクセス理由と共通認証案内。著作権表示と製品名は原表記を保持。
- 旧登録・試用版の3メッセージは元の内容を翻訳。ライセンス条件や有効化処理は変更していない。

ソース処理、XIB、既存言語、操作条件、設定値、VFS、著作権・ライセンスの差分なし。Panel・Utility・RoutedIOのknownRegionsにjaを追加した。

既存のNSLocalizedStringが使う新規作成時の既定名も日本語化した。ユーザーが指定した名前や既存ファイル名は翻訳しない。属性の狭い列では「読取」「書込」「データ保護」の短い表記を使用し、UF_/SF_のツールチップは保持する。

## 再実行可能な監査

```sh
python3 Scripts/audit_japanese_localization.py --check
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s Scripts/tests -v
```

監査は標準ライブラリだけを使用し、リポジトリ相対パスのJSONを標準出力へ返す。ja登録、translated状態、NSString/printf引数、英語の複数形置換、一括改名の括弧内トークンを検査する。--checkでは不備があると非0で終了する。監査ツール自体は正常系・未登録・未確認・引数不一致・改名構文・複数形の6テストで検証し、全成功。

さらに、今回変更した各カタログからjaを除いたJSONを変更前と比較し、既存言語の値・状態・コメント等が不変であることを確認した。

### カタログ一覧

| カタログ（リポジトリ相対） | 項目数 | ja未登録 |
|---|---:|---:|
| Source/CUI/resources/mul.lproj/ProcessSheetController.xcstrings | 1 | 0 |
| Source/NimbleCommander/NimbleCommander/Bootstrap/mul.lproj/MainMenu.xcstrings | 191 | 0 |
| Source/NimbleCommander/NimbleCommander/GeneralUI/mul.lproj/AskForPasswordWindowController.xcstrings | 4 | 0 |
| Source/NimbleCommander/NimbleCommander/GeneralUI/mul.lproj/DetailedVolumeInformationSheetController.xcstrings | 19 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/Preferences.xcstrings | 91 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowExternalEditorsTab.xcstrings | 4 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowExternalEditorsTabNewEditorSheet.xcstrings | 12 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowGeneralTab.xcstrings | 4 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowHotkeysTab.xcstrings | 13 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowPanelsTab.xcstrings | 115 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowPanelsTabColoringFilterSheet.xcstrings | 9 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowPanelsTabOperationsConcurrencySheet.xcstrings | 10 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowTerminalTab.xcstrings | 9 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowThemesTab.xcstrings | 4 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowThemesTabAutomaticSwitchingSheet.xcstrings | 5 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowThemesTabColoringRulesControl.xcstrings | 4 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowThemesTabImportSheet.xcstrings | 5 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowToolsTab.xcstrings | 48 | 0 |
| Source/NimbleCommander/NimbleCommander/Preferences/mul.lproj/PreferencesWindowViewerTab.xcstrings | 24 | 0 |
| Source/NimbleCommander/NimbleCommander/Resources/InfoPlist.xcstrings | 6 | 0 |
| Source/NimbleCommander/NimbleCommander/Resources/Localizable.xcstrings | 219 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/FilePanelsContextMenu.xcstrings | 24 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/FilePanelsQuickSearch.xcstrings | 11 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/List/mul.lproj/PanelListViewColumnsMenu.xcstrings | 7 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/Views/mul.lproj/ConnectToServer.xcstrings | 12 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/Views/mul.lproj/FTPConnectionSheetController.xcstrings | 22 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/Views/mul.lproj/GoToFolderSheetController.xcstrings | 4 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/Views/mul.lproj/NetworkShareSheetController.xcstrings | 27 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/Views/mul.lproj/SFTPConnectionSheetController.xcstrings | 22 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/Views/mul.lproj/SpotlightSearchPopupViewController.xcstrings | 2 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/Views/mul.lproj/WebDAVConnectionSheetController.xcstrings | 19 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/mul.lproj/ExternalToolParameterValueSheetController.xcstrings | 2 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/mul.lproj/FavoritesWindowController.xcstrings | 8 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/mul.lproj/FindFilesSheetController.xcstrings | 43 | 0 |
| Source/NimbleCommander/NimbleCommander/States/FilePanels/mul.lproj/PanelViewHeaderSortPopup.xcstrings | 22 | 0 |
| Source/Operations/resources/Localizable.xcstrings | 80 | 0 |
| Source/Operations/source/AttrsChanging/mul.lproj/AttrsChangingDialog.xcstrings | 55 | 0 |
| Source/Operations/source/BatchRenaming/mul.lproj/BatchRenamingDialog.xcstrings | 147 | 0 |
| Source/Operations/source/BatchRenaming/mul.lproj/BatchRenamingRangeSelectionPopover.xcstrings | 3 | 0 |
| Source/Operations/source/Compression/mul.lproj/CompressDialog.xcstrings | 4 | 0 |
| Source/Operations/source/Copying/mul.lproj/CopyingDialog.xcstrings | 15 | 0 |
| Source/Operations/source/Copying/mul.lproj/CopyingDialogDisclosedView.xcstrings | 2 | 0 |
| Source/Operations/source/Copying/mul.lproj/FileAlreadyExistDialog.xcstrings | 18 | 0 |
| Source/Operations/source/Deletion/mul.lproj/DeletionDialog.xcstrings | 1 | 0 |
| Source/Operations/source/DirectoryCreation/mul.lproj/DirectoryCreationDialog.xcstrings | 4 | 0 |
| Source/Operations/source/Linkage/mul.lproj/AlterSymlinkDialog.xcstrings | 3 | 0 |
| Source/Operations/source/Linkage/mul.lproj/CreateHardlinkDialog.xcstrings | 3 | 0 |
| Source/Operations/source/Linkage/mul.lproj/CreateSymlinkDialog.xcstrings | 6 | 0 |
| Source/Panel/Localizable.xcstrings | 13 | 0 |
| Source/Panel/resources/mul.lproj/SelectionWithMaskPopupViewController.xcstrings | 1 | 0 |
| Source/RoutedIO/resources/Localizable.xcstrings | 2 | 0 |
| Source/Utility/resources/Localizable.xcstrings | 12 | 0 |
| Source/Viewer/resources/Localizable.xcstrings | 18 | 0 |
| Source/Viewer/resources/mul.lproj/InternalViewerController.xcstrings | 4 | 0 |
| Source/Viewer/resources/mul.lproj/NCViewerSheet.xcstrings | 2 | 0 |

## ビルド・テスト

```sh
xcodebuild -project Source/NimbleCommander/NimbleCommander.xcodeproj \
  -scheme NimbleCommander-Unsigned -configuration Debug \
  -destination 'platform=macOS,arch=arm64' \
  -derivedDataPath /tmp/nc-ja-localized-derived build
xcodebuild -project Source/NimbleCommander/NimbleCommander.xcodeproj \
  -scheme UnitTests -configuration Debug \
  -destination 'platform=macOS,arch=arm64' \
  -derivedDataPath /tmp/nc-ja-localized-derived build
```

最終アプリとUnitTestsのビルドは両方BUILD SUCCEEDED、終了コード0。アプリは既存設定に従いarm64/x86_64のUniversalビルド。警告は既存のシンボルなしobject、Swift標準ライブラリ埋込設定、出力指定のないRun Script等。翻訳カタログのコンパイルエラーなし。

OS機能を利用できるサンドボックス外で、既存の専用テストfixtureを使い、10本を直接実行（ViewerUTはアプリ内部の実行ファイル）。

| テスト | ケース | アサーション | 結果 |
|---|---:|---:|---|
| BaseUT | 75 | 70,559 | 成功 |
| ConfigUT | 38 | 76 | 成功 |
| NimbleCommanderUT | 45 | 363 | 成功 |
| OperationsUT | 24 | 280 | 成功 |
| PanelUT | 50 | 1,295 | 成功 |
| TermUT | 109 | 7,821 | 成功 |
| UtilityUT | 122 | 2,098 | 121成功、1件は上流の想定内失敗 |
| VFSIconUT | 21 | 29 | 成功 |
| VFSUT | 62 | 42,697 | 成功 |
| ViewerUT | 43 | 1,207 | 成功 |
| 合計 | 589 | 126,425 | 全10本が終了コード0 |

UtilityUTのTags RemoveTagFromAllItemsで索引更新の待ち回数が上限に達した。上流Source/Utility/tests/Tags_UT.mmで[!mayfail]指定されており、今回テストを除外・改変していない。予期しない失敗なし。IntegrationTestsスキームは未実行。

## 表示・一時fixtureでの確認

既に起動していた旧ビルドと区別するため、最終ビルドを一時領域にコピーし、検証コピーだけbundle identifierを変更してad-hoc署名した。ソースの識別子・プロジェクト署名設定・配布物は変更していない。コピーは公開しない。

同じコピーをja/enのAppleLanguagesとAppleLocaleの起動引数で個別起動。OS言語は変更していない。画面キャプチャとアクセシビリティツリーで確認した。

| 画面 | 日本語 | 英語 |
|---|---|---|
| 一括改名 | パターン、カウンタ、検索置換、変更前後の表を確認 | 元のラベルと構文を確認してキャンセル |
| ファイル属性 | 権限、フラグ、日時を確認。文字幅調整後に再確認してキャンセル | 元のラベルとフラグを確認してキャンセル |
| フォルダ移動 | ラベル・移動・キャンセルを確認 | 同じ画面の英語を確認 |
| お気に入り管理 | 名前・場所・タイトルを確認。保存済み名は原表記 | 同じ画面の英語を確認 |
| ボリューム情報 | 基本情報のラベルを確認 | 同じ画面の英語を確認 |
| パネル | 空き容量、ツールバー説明の日本語を確認 | 既存表示の維持を確認 |

一括改名は専用の一時テキスト2件で実施。[N]-確認.[E]のプレビューを確認して適用し、両ファイルの名前と本文の不変を確認した。属性・所有者・権限は変更していない。お気に入りのリセットや管理者認証、アクセス許可の変更は行っていない。

## カタログ外の監査と残作業

表示タイトルを直接設定するObjC呼び出しの検索では、テストのHello、非表示のSearch Menu、ソート種別を示すN等を確認した。これらは翻訳対象の通常文言とは分けて保持した。この検索はすべての英語直書きを完全に検出するものではない。

- 保存済みのテーマ・レイアウト・タグ・お気に入り名、ユーザー定義ツール、パスやOS・サーバ由来の文言には英語が残り得る。
- ログ画面、全改名テンプレートの実行、全属性フラグ、全通知・例外、OSの許可ダイアログ、旧試用版画面は個別に実機操作していない。カタログと書式・構文は検証済み。
- 日本語IME、長い名前、文字幅、アクセシビリティ、大きな文字サイズ等の網羅的な表示校正は継続課題。
- テストサーバでの接続・認証、ファイル操作全般の統合試験、CIへの監査組み込みは未実施。
- featureブランチの主開発ブランチへの統合、永続的な起動手順、キーバインド等の操作性改善は別作業。リリース・バイナリ公開はしていない。

生ログ、スクリーンショット、一時fixture、検証コピー、ローカル設定はコミット対象外。
