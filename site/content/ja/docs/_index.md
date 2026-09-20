---
title: Documentation
weight: 1
next: /docs/start
translationKey: docs-overview
---

XCP-hl のインストール、運用、ビルドについてのすべて。

{{< callout type="info" >}}
日本語のコンテンツはすべて Jekyll から Hugo へ移行しました
（[#60](https://github.com/Vagrantin/xcp-hl/issues/60)）。このサイトはまだ
公開されていません — 本番環境は移行（フェーズ 5）まで
[vagrantin.github.io/xcp-hl](https://vagrantin.github.io/xcp-hl/) のまま
です。
{{< /callout >}}

## セクション

{{< cards >}}
  {{< card link="start" title="はじめに" subtitle="ダウンロード、インストール、XOA の展開、そしてホストへの Xen Orchestra の接続。" >}}
  {{< card link="guides/features" title="Guides" subtitle="リリースに含まれるもの、アップデートの仕組み、ホストの日々の運用について。" >}}
  {{< card link="components" title="コンポーネント" subtitle="XCP-hl を構成するリポジトリと、そのビルドパイプライン、それらがどう組み合わさっているか。" >}}
  {{< card link="reference/release-matrix" title="リファレンス" subtitle="リリース一覧表、変更履歴、ロードマップ。" >}}
  {{< card link="https://github.com/Vagrantin/xcp-hl" title="ソース" subtitle="リポジトリ、課題管理、ビルドパイプライン。" icon="github" >}}
{{< /cards >}}

## 予定している構成

以下のセクション構成は、プラットフォーム全体のドキュメントの目標です
（[#60](https://github.com/Vagrantin/xcp-hl/issues/60) のフェーズ 6）。
`start/`、`guides/`、`components/`、`reference/` は現時点で存在し、`build/`、
`qa/`、`contributing/` はこれからです。セクションを増やすことはフォルダーを
増やすことであり、手で管理する全体の並び順はありません。

| セクション | 内容 |
|---|---|
| `start/` | ダウンロード、インストール、初回起動、確認 |
| `guides/` | アップデート、ストレージ、ネットワーク、バックアップ、トラブルシューティング |
| `components/` | `xcp-ng-ce-iso`、`xolite-ce`、`xoa-proxy`、`xoa-hl`、`build-xoa-hl`、`xoa-deploy-patcher`、`xcp-hl-release` |
| `build/` | ビルドのオーケストレーション、CI、署名、リリース手順 |
| `qa/` | QA の仕組み、スモークテスト |
| `reference/` | リリース一覧表、変更履歴、ロードマップ、パッケージ名、GPG 鍵 |
| `contributing/` | コントリビュートの方法 |

## #60 の未解決の論点 — 解決済み

| # | 論点 | 決定 |
|---|---|---|
| 1 | フレームワーク | Hugo + Hextra |
| 2 | URL の方針 | 拡張子なしの URL とし、Jekyll 時代のすべてのパスからリダイレクトする — `site/README.md` を参照 |
| 3 | 「スタンドアロン」の意味 | `hugo --baseURL <url>` で生成した、任意の Web サーバーで配信できる tarball。`file://` で開く形式ではありません |
| 4 | 独自ドメイン | `xcp-hl.org`。まずこのリポジトリ自身の Pages サイトで検証します |
| 5 | サイトの場所 | `xcp-hl/docs/` のまま（移行時に `site/` へ）— 別リポジトリは作りません |
| 6 | 翻訳の方針 | 本番は 3 言語がそろうまで待ちます。プレ本番のプレビューでは、未翻訳のページを英語の原文へのリンクとして明示したうえで表示してかまいません — `site/README.md` の「Translation-pending pages」を参照 |

残っているのはフェーズ 4（スタンドアロンビルド）とフェーズ 5（移行）だけです。
