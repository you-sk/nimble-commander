# 検索・接続・ビューアの日本語化

2026-11-05、macOS 27.0.1 / arm64、Xcode 27.2で実施。

## 変更内容

[用語集](LOCALIZATION_GLOSSARY_JA.md)に合わせ、日本語209項目を追加した。

- ファイル検索の条件、結果、正規表現・内容検索オプション、説明文、最近の検索。
- クイック検索の一致件数とSpotlight検索の入力ラベル。
- 接続管理、FTP、SFTP、WebDAV、ネットワーク共有の入力画面と接続エラーメッセージ。
- 共通のパスワード入力ダイアログ。接続以外の用途にも使われるため「項目」の表現を使う。
- ビューアのテキスト・16進・プレビュー、エンコーディング、構文の色分け、折り返し、ファイル内検索、位置指定、ウインドウタイトル。
- ViewerプロジェクトのknownRegionsにjaを追加。

変更はString CatalogとViewerの言語登録のみ。英語・他言語、ソース言語、XIB、検索・認証・接続・ビューアの処理、キー割り当て、保存値、VFSは変更していない。ホスト名の入力例、プロトコル、ポート番号、パターン構文等は保持した。

## 検証結果

### 静的確認

- 各変更カタログからjaを除いたJSONを変更前と比較し、既存の全言語・キー・状態・コメントが同一であることを確認。
- %@や%1$@等の書式引数の型・順序を照合し、一致を確認。
- ViewerResources.bundleとアプリ本体のja.lprojへの翻訳出力を確認。
- git diff --check成功。コード・XIB・設定初期値・ライセンスの差分なし。
- 生ログ、画面キャプチャ、生成物、認証情報、個人のローカルパスは公開対象に含めない。

### ビルドと単体テスト

リポジトリ直下で実行:

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

両方BUILD SUCCEEDED、終了コード0。アプリは既存設定に従うarm64/x86_64のUniversalビルド。

生成された単体テストを直接実行。通常の9本に加え、ViewerUTは`Debug/ViewerUT.app/Contents/MacOS/ViewerUT`を実行した。UnitTestsスキームに含まれるが、出力がアプリ形式であるため、Debug直下の*UTだけを列挙しても実行されない。

| テスト | ケース | アサーション | 結果 |
|---|---:|---:|---|
| BaseUT | 75 | 70,559 | 成功 |
| ConfigUT | 38 | 76 | 成功 |
| NimbleCommanderUT | 45 | 363 | 成功 |
| OperationsUT | 24 | 280 | 成功 |
| PanelUT | 50 | 1,295 | 成功 |
| TermUT | 109 | 7,821 | 成功 |
| UtilityUT | 122 | 1,898 | 成功 |
| VFSIconUT | 21 | 29 | 成功 |
| VFSUT | 62 | 42,609 | 成功 |
| ViewerUT | 43 | 1,207 | 成功 |
| 合計 | 589 | 126,137 | 全10本が終了コード0 |

FSEvents等のOS機能を利用できるサンドボックス外で実施。ViewerUTを含む既存の一時fixtureを使用。想定内失敗を含め失敗なし。IntegrationTestsスキームは未実行。

最終アプリビルドの警告は静的ライブラリのSwift標準ライブラリ埋込設定と出力指定のないRun Script等の既存項目。翻訳カタログのコンパイルエラーなし。

### 日本語・英語の表示確認

同じ最終Unsigned Debugアプリを、OS言語を変更せず`-AppleLanguages '(ja)' -AppleLocale ja_JP`と`-AppleLanguages '(en)' -AppleLocale en_US`で起動。画面キャプチャとアクセシビリティツリーで確認した。

| 画面 | 確認結果 |
|---|---|
| ファイル検索 | 両言語で条件・結果見出し・ボタンを確認。一時領域の*.txtを検索し、どちらも2件。日本語の内容「桜」で1件に絞れることも確認 |
| Spotlight | 両言語で入力ラベルとプレースホルダを確認。検索実行はしていない |
| 接続管理 | 日本語で一覧見出し・追加メニュー・閉じるを確認。追加画面はすべてキャンセル |
| FTP | 日本語・英語でサーバ・ユーザー名・パスワード・接続先パス・ポート・アクティブモードを確認 |
| SFTP | 日本語・英語で接続先、秘密鍵、パスフレーズ説明等を確認 |
| WebDAV | 日本語・英語でプロトコル、ベースパス、接続先ポート等を確認 |
| ネットワーク共有 | 日本語・英語で共有名、マウント先等を確認 |
| 検索結果からのビューア | 日本語本文・UTF-8・フッタ・閉じる・位置指定ラベルを確認 |
| 通常ビューア | 両言語でタイトル、テキスト表示、検索欄、フッタ、位置指定ポップアップを確認。日本語UIで「桜」、英語UIで「sakura」の検索・強調表示を確認 |
| 表示モード | 日本語でテキスト／16進／プレビューの項目を確認し、16進表示へ切り替えられることを確認 |

確認したダイアログにラベルの重なりや文字切れなし。テスト用テキストは日本語と英語を含む一時fixtureのみ。接続画面は保存・接続せず閉じ、認証情報の入力・変更や実サーバへの接続は行っていない。SFTP画面を開くと既存実装が既定の鍵パスを補完・検証するが、この処理は変更していない。

## 制約

- 実サーバとの認証・接続、OSのネットワークマウント、Dropbox認証は未検証。サーバやOSから返るエラー本文は元の表記の場合がある。
- パスワード要求、接続エラー、クイック検索の全件数分岐、ビューアの全オプションは個別にGUI表示していない。カタログ生成と書式引数の検証は実施した。
- 位置指定はラベルと入力ポップアップの表示を確認。任意の位置への移動精度の実機検証は対象外。
- Quick Lookのプレビュー描画はOS提供部分であり、今回の表示確認はテキスト・16進が中心。
- ビューア本文・ファイル名・パス・エンコーディング名・構文色分け言語名等のデータは翻訳しない。
