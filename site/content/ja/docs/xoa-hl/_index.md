---
title: XOA-HL マニュアル
weight: 3
translationKey: xoa-manual-home
translationStatus: draft
sourceRevision: sha256:6562e27998eebc48b99a8356860e15fa7d65675335a705ed9428b553e33964a3
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

XOA-HL で行いたい作業を見つけられます。まずアプライアンスを展開し、その後アプライアンスとハイパーバイザーホストを更新します。

{{< callout type="info" >}}
初心者向けの展開、初回ログイン、VM 作成、完全バックアップ、隔離した復元の手順を、ソース確認済みのプレビューとして利用できます。使い捨ての検証環境での確認と人による翻訳レビューは未完了です。保守、設定エクスポート、トラブルシューティングもソース確認済みのプレビューとして利用できます。復旧とロールバックの検証は未完了です。
{{< /callout >}}

## はじめに

- [ログインしてホストを接続し、表示言語を選ぶ](/docs/xoa-hl/first-login/)。
- [最初の仮想マシンを作成して OS をインストールする](/docs/xoa-hl/create-vm/)。
- [VM をバックアップして隔離した復元をテストする](/docs/xoa-hl/backup-restore/)。
- [XOA-HL を展開してホストを接続する](/docs/start/#start-deploy-xoa)。
- [ホスト、XO Lite、アプライアンスの関係を確認する](/docs/start/#start-architecture)。
- [各リリースに含まれるコンポーネントを確認する](/docs/reference/release-matrix/)。

XOA-HL には専用のアドレスがあります。Xen Orchestra にはアプライアンスのアドレス、XO Lite にはホストのアドレスを使います。管理画面とこのドキュメントの表示言語は個別に設定します。

## 日常の管理

- [VM の操作とリソース変更、スナップショット、クローン、フルコピー、削除時の注意点](/docs/xoa-hl/vm-operations/)。
- [ISO ライブラリの接続、テスト用ディスクの追加と VM ネットワークの管理](/docs/xoa-hl/storage-networks/).
- [VM のプール内での移行、エクスポート、隔離したコピーのインポート](/docs/xoa-hl/vm-transfer/)。
- [バックアップのスケジュールと保持数を確認する](/docs/xoa-hl/backup-restore/#backup-schedules)。
- [ホストとプールの管理担当、XO Lite の検出、ホスト統計を確認する](/docs/xoa-hl/hosts-pools/)。
- [ユーザーとグループを作成してオブジェクトの権限を確認する](/docs/xoa-hl/permissions/).
- [ワンタイムコード (OTP) でローカルアカウントのサインインを保護する](/docs/xoa-hl/sign-in-otp/).

これらはソース確認済みのプレビューで、使い捨て環境での検証は未完了です。データ保護には[完全バックアップと隔離した復元の試行手順](/docs/xoa-hl/backup-restore/)を参照してください。他のバックアップや DR モードはリリースごとの個別検証が必要です。

## インストール環境を保守する

- [保守を計画して結果を確認する](/docs/xoa-hl/maintenance/)。
- [XO 設定をエクスポートして隔離したインポートを準備する](/docs/xoa-hl/configuration-backup/)。
- [トラブルシューティングと問題報告](/docs/xoa-hl/troubleshooting/)。
- [XOA-HL アプライアンスをアップデートする](/docs/guides/updates/#xoa-hlアプライアンスのアップデート)。
- [ハイパーバイザーホストをアップデートする](/docs/guides/updates/#xcp-hlホストのアップデート)。
- [リリースの変更内容を読む](/docs/reference/changelog/)。

手順を実行する前に、ガイドの対象バージョンを確認してください。リリース一覧は一緒に配布されたコンポーネントを示すものであり、統合テストの結果を示すものではありません。

## リファレンスと自動化

- [概念、バージョン、機能の範囲を確認する](/docs/xoa-hl/concepts/).
- [アプライアンスサービスを設定する](/docs/xoa-hl/configuration/).
- [xo-cli で API メソッドを検出してインベントリを読む](/docs/xoa-hl/automation/).

## 用語を確認する

[用語集を開く](glossary/)と、VM、ホスト、プール、ストレージ、スナップショット、バックアップの意味を確認できます。実装の詳細は[貢献者向けのコンポーネント解説](/docs/components/)を参照してください。

## 表示言語と問題の報告

言語セレクターで同じページを English、Français、日本語に切り替えられます。翻訳案を利用する前に[翻訳の状況](translation-status/)を確認してください。

[ドキュメントの問題を報告する](https://github.com/Vagrantin/xcp-hl/issues/new?title=Documentation%3A%20XOA-HL%20manual)。ページの URL、表示言語、アプライアンスのバージョン、修正が必要な手順を記載してください。パスワードや非公開のデータは含めないでください。
