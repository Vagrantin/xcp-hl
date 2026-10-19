---
title: "XOA-HL の概念と機能の範囲"
linkTitle: "概念"
description: "コンポーネント、バージョン番号、このリリースに含まれる機能を理解します。"
weight: 90
translationKey: xoa-manual-concepts
translationStatus: draft
sourceRevision: sha256:5f34ed54ff2d136c85d8ea8fca3bdebf785565736c3dad46a9c10bdb8638f5fe
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

操作対象のコンポーネントと、機能について確認できている範囲を説明します。

{{< callout type="info" >}}
イメージ `xoa-image-20261009-5f33c81`、パッケージ `v5.113.2_e281c536-ce38`、XO 5.113.2 のソースを確認したリファレンスです。後続リリースでは動作が変わる可能性があります。実際のアプライアンスでの検証と人による翻訳レビューは未完了です。
{{< /callout >}}

## コンポーネントとアドレス

| コンポーネント | 役割 | アドレス |
| --- | --- | --- |
| ハイパーバイザーホスト / プール | VM を実行し、XAPI を提供する | ホストの管理アドレス |
| XO Lite CE | ホストが配信する管理画面。アプライアンスの展開と検出 | ホストの HTTPS アドレス |
| XOA-HL アプライアンス | xo-server、XO 5 管理画面、Redis を実行する別の VM | アプライアンスの HTTPS アドレス |

流れは[構成と展開のガイド](/docs/start/#start-architecture)を参照してください。ホストやプールごとにサポート対象の管理担当を 1 つに保ち、接続を移す前に[管理担当と検出](/docs/xoa-hl/hosts-pools/)を確認します。ホストとアプライアンスのアップデートは対象とスケジュールが別です。[アップデートガイド](/docs/guides/updates/)を参照してください。

## オブジェクトと保護

**VM** は**プール**内のホストで動作します。**ストレージリポジトリ (SR)** は仮想ディスクを保存し、VM のネットワークインターフェイスはプールのネットワークに接続します。名前はラベルなので、自動化ではオブジェクト ID を使います。**スナップショット**は VM のある時点の状態をそのストレージ上に保持します。**バックアップ**は保護用データを設定済みのリモートへコピーします。スナップショットだけでは、そのストレージの喪失に備えられません。

[共通用語集](/docs/xoa-hl/glossary/)、[ディスクとネットワーク](/docs/xoa-hl/storage-networks/)、[完全バックアップと隔離した復元の試行手順](/docs/xoa-hl/backup-restore/)を参照してください。バックアップジョブが成功しても、復元テストが必要です。

## バージョンの識別

| このリファレンスの識別値 | 意味 |
| --- | --- |
| XO 5.113.2 / アップストリーム `e281c536` | 意図的に固定したアプリと画面のソース。XO 6 ではない |
| `xo-server` 5.193.1 | 同じコミットのサーバーパッケージ。別の番号体系 |
| `v5.113.2_e281c536-ce38` | HomeLab RPM リリースとパッチ一式 |
| `xoa-image-20261009-5f33c81` | イメージのビルド識別値。アプリ更新後も別の情報として残る |

[保守ガイド](/docs/xoa-hl/maintenance/)に従い、インストール済みの値を記録します。[リリース一覧](/docs/reference/release-matrix/)は一緒に配布された組み合わせを示し、統合テストの合格を示しません。ISO は後から展開時に決まるイメージを固定しません。

## ce38 の機能の範囲

| 領域 | ソースでの確認 | 検証の範囲 |
| --- | --- | --- |
| VM 電源、スナップショット、ディスク、ネットワーク | XO 5 の操作と画面のコードが存在する | 日常管理ガイドの使い捨て環境テストは未完了 |
| ユーザーとオブジェクト ACL | 公開ビルドは既定の OpenSource プランを維持し、ACL 画面のコードが存在する | 実際の画面と独立した一般ユーザーのセッションで確認する |
| 完全バックアップと復元 | NFS の試行手順をソース確認し、文書化している | 実際のバックアップと隔離した復元は未検証 |
| アプライアンスのアップデート | HomeLab API、stable/testing チャネル、設定可能なスケジュール | 対象リリースの更新ガイドに従う |
| Hub、Vates XOA セクション、バックアッププロキシ、XOSTOR のメニュー | ce38 のパッチで非表示にする | 非表示のメニューはサポートの保証でも、すべての API の不存在の証明でもない |

このリリースは 14 個の宣言済みパッチを含みます。すべてのアップストリーム機能の検証を意味するものではありません。Vates のサブスクリプション、商用サポート、XO 6 のインターフェイスは、この HomeLab パッケージの説明には当てはまりません。[権限](/docs/xoa-hl/permissions/)と対象作業のガイドを確認してください。

## リファレンスと貢献

[サービス設定](/docs/xoa-hl/configuration/)、[読み取り専用 CLI 自動化](/docs/xoa-hl/automation/)、[設定エクスポート](/docs/xoa-hl/configuration-backup/)は、それぞれ異なる設定やデータを扱います。実装と CI のみで行う製品ビルドについては [xoa-hl](/docs/components/xoa-hl/) と [build-xoa-hl](/docs/components/build-xoa-hl/) を参照してください。文書の変更提案にはリリース識別値を添えてください。

## ソース

[UPSTREAM_XO](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/UPSTREAM_XO), [patch metadata](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/metadata.toml), [menu patch](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/menu-hide-items.patch), [RPM](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [xo-server package](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/package.json), [XO build plan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js).
