---
title: XOA-HL マニュアル
weight: 3
translationKey: xoa-manual-home
translationStatus: draft
sourceRevision: sha256:34f15a366aecbbc18f1e4e39b758b0383789841e060234fbaed5dce8b72b45b8
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

XOA-HL で行いたい作業を見つけられます。まずアプライアンスを展開し、その後アプライアンスとハイパーバイザーホストを更新します。

{{< callout type="info" >}}
このマニュアルは拡充中です。以下のリンクから既存のガイドを参照できます。VM、バックアップ、復元、トラブルシューティングの詳細なチュートリアルは準備中です。
{{< /callout >}}

## はじめに

- [XOA-HL を展開してホストを接続する](/docs/start/#start-deploy-xoa)。
- [ホスト、XO Lite、アプライアンスの関係を確認する](/docs/start/#start-architecture)。
- [各リリースに含まれるコンポーネントを確認する](/docs/reference/release-matrix/)。

XOA-HL には専用のアドレスがあります。Xen Orchestra にはアプライアンスのアドレス、XO Lite にはホストのアドレスを使います。管理画面とこのドキュメントの表示言語は個別に設定します。

## インストール環境を保守する

- [XOA-HL アプライアンスをアップデートする](/docs/guides/updates/#xoa-hlアプライアンスのアップデート)。
- [ハイパーバイザーホストをアップデートする](/docs/guides/updates/#xcp-hlホストのアップデート)。
- [リリースの変更内容を読む](/docs/reference/changelog/)。

手順を実行する前に、ガイドの対象バージョンを確認してください。リリース一覧は一緒に配布されたコンポーネントを示すものであり、統合テストの結果を示すものではありません。

## 用語を確認する

[用語集を開く](glossary/)と、VM、ホスト、プール、ストレージ、スナップショット、バックアップの意味を確認できます。実装の詳細は[貢献者向けのコンポーネント解説](/docs/components/)を参照してください。

## 表示言語と問題の報告

言語セレクターで同じページを English、Français、日本語に切り替えられます。翻訳案を利用する前に[翻訳の状況](translation-status/)を確認してください。

[ドキュメントの問題を報告する](https://github.com/Vagrantin/xcp-hl/issues/new?title=Documentation%3A%20XOA-HL%20manual)。ページの URL、表示言語、アプライアンスのバージョン、修正が必要な手順を記載してください。パスワードや非公開のデータは含めないでください。
