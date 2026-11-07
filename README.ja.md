# Nimble Commander 日本語版Fork

[Nimble Commander](https://github.com/mikekazakov/nimble-commander) の日本語UI対応と操作性改善を目指すForkです。メインメニュー、主要なファイル操作ダイアログ、設定画面、検索・接続ダイアログ、ビューアを日本語化しています。組み込みString Catalogの日本語登録を完了し、全画面の表示校正を継続しています。

上流のデュアルペイン構成、VFS、既存のファイル操作と英語UIを維持し、小さな変更を積み重ねます。

- [英語README](README.md)
- [公式ビルド手順](Docs/Building.md)（Xcode 27.2、NimbleCommander-Unsignedスキーム）
- [初回調査・実装計画・既知の制約](Docs/DEVELOPMENT_PLAN_JA.md)
- [日本語UI用語集](Docs/LOCALIZATION_GLOSSARY_JA.md)
- [日本語化 第1段階の範囲と検証](Docs/LOCALIZATION_PHASE1_JA.md)
- [設定画面の日本語化と検証](Docs/LOCALIZATION_PREFERENCES_JA.md)
- [検索・接続・ビューアの日本語化と検証](Docs/LOCALIZATION_SEARCH_CONNECTIONS_VIEWER_JA.md)
- [日本語化の全体監査と残作業](Docs/LOCALIZATION_AUDIT_JA.md)
- [日本語UIの表示校正記録](Docs/JAPANESE_UI_PROOFREADING_JA.md)
- [起動時の案内・更新方針](Docs/FORK_STARTUP_POLICY_JA.md)
- [Forkの変更履歴](Docs/CHANGELOG_JA.md)
- [上流の変更履歴](WHATS_NEW.md)
- [GPL v3 ライセンス](LICENSE.md)

原著作者の著作権表示と上流履歴を保持します。特権ヘルパーには適切な署名が必要です。未署名ビルドの管理者操作には制約があります。バイナリの公開は初回調査の対象外です。

このForkでは上流公式版の自動更新確認と手動更新メニュー、起動時のアプリケーションフォルダへの移動案内を無効にしています。更新はこのForkのソースからビルドしてください。公式配布版を取得すると日本語化の変更は含まれません。
