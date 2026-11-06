---
title: "XOA-HL の概念と機能の範囲"
linkTitle: "概念"
description: "コンポーネント、バージョン番号、このバージョンに含まれる機能を理解します。"
weight: 90
translationKey: xoa-manual-concepts
translationStatus: reviewed
sourceRevision: sha256:9457bbb19ed144e4eabca2b0c7af226bd1db4d60fb67217e695f2165868fc341
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

このリファレンスでは、作業対象のコンポーネント、バージョン番号の意味、このバージョンに含まれる機能を説明します。手順はありません。機能を使う前や、問題を報告するときに参照してください。

{{< callout type="info" >}}
**対象:** イメージ `xoa-image-20261022-a280852`、パッケージ `v5.113.2_e281c536-ce40`（Xen Orchestra 5.113.2）。公開済みのコードに基づく手順で、検証環境でのテストはまだです。
{{< /callout >}}

## コンポーネントとアドレス {#components}

| コンポーネント | 役割 | アクセス先 |
| --- | --- | --- |
| ハイパーバイザーホストまたはプール | VM を実行し、管理用の XAPI を提供します | ホストの管理アドレス |
| XO Lite CE | ホストが提供するブラウザー用の管理画面です。アプライアンスを展開し、検出します | ホストの HTTPS アドレス |
| XOA-HL アプライアンス | xo-server、XO 5 の管理画面、Redis を実行する別の VM です | アプライアンスの HTTPS アドレス |

これらの関係は[構成と展開のガイド](/docs/start/#start-architecture)を参照してください。各ホストやプールは、サポートされた 1 つの管理ツールだけで管理します。接続を移す前に[ホストとプール](/docs/xoa-hl/hosts-pools/)を読んでください。ホストの更新とアプライアンスの更新は別のもので、対象とスケジュールもそれぞれ異なります。[アップデートガイド](/docs/guides/updates/)を参照してください。

## VM、ストレージ、保護 {#objects}

**VM** は**プール**内のホストで動作します。**ストレージリポジトリ（SR）**は仮想ディスクを保存します。VM のネットワークインターフェースは、プールのネットワークに接続します。名前はラベルにすぎないため、自動化ではオブジェクト ID を使います。

**スナップショット**は、ある時点の VM の状態を同じストレージに保存します。**バックアップ**は、データを別のバックアップ先（リモート）にコピーします。スナップショットだけでは、そのストレージを失ったときに守れません。また、バックアップジョブが成功しても、復元のテストが必要です。

詳しくは、[用語集](/docs/xoa-hl/glossary/)、[ストレージとネットワーク](/docs/xoa-hl/storage-networks/)、[VM のバックアップと復元](/docs/xoa-hl/backup-restore/)を参照してください。

## バージョン番号 {#versions}

| バージョン | 意味 |
| --- | --- |
| XO 5.113.2、アップストリームのコミット `e281c536` | アプリケーションと管理画面の Xen Orchestra のバージョンです。意図して選んだもので、XO 6 ではありません |
| `xo-server` 5.193.1 | 同じリリースでのサーバーパッケージのバージョンです。番号の付け方が異なります |
| `v5.113.2_e281c536-ce40` | XOA-HL パッケージのリリースと、そのパッチ一式です |
| `xoa-image-20261022-a280852` | アプライアンスのイメージのビルドです。別の番号で、アプリケーションを更新しても変わりません |

[アプライアンスの保守](/docs/xoa-hl/maintenance/)の説明に従い、インストール済みの値を記録します。[リリース一覧](/docs/reference/release-matrix/)は、一緒に配布されたバージョンを示すだけで、統合テストに合格したことは意味しません。インストール用の ISO では、アプライアンスのイメージは決まりません。イメージは後で、アプライアンスを展開するときに決まります。

## このバージョンに含まれる機能 {#feature-scope}

| 領域 | このバージョンのコード | 使う前に |
| --- | --- | --- |
| VM の電源、スナップショット、ディスク、ネットワーク | XO 5 の操作と画面があります | 日常作業のガイドは、検証環境でのテストがまだです |
| ユーザーとオブジェクトの権限（ACL） | 公開されたビルドは、アップストリームの既定のプラン（OpenSource）のままです。ACL の画面はコードにあります | インストール済みの画面を確認し、一般ユーザーでログインした別のセッションでテストします |
| 完全バックアップと復元 | コードに基づく NFS の手順を文書化しています | 実際のバックアップと、隔離した復元のテストはまだです |
| アプライアンスの更新 | XOA-HL の更新 API、`stable` と `testing` のチャネル、設定できるスケジュール | 使っているリリースの更新ガイドに従います |
| Hub、Vates XOA のセクション、バックアッププロキシ、XOSTOR のメニュー | このパッケージのメニュー用パッチで、これらの項目を非表示にしています | メニューを非表示にしても、サポートされた機能にはなりません。対応する API がなくなったことの証明にもなりません |

このパッケージのリリースは 16 個のパッチを宣言しています。これは、アップストリームのすべてのオプションをテストしたという意味ではありません。Vates のサブスクリプションのプラン、商用サポート、XO 6 のインターフェースは、このパッケージには当てはまりません。機能を使う前に、[ユーザーと権限](/docs/xoa-hl/permissions/)と、その作業のガイドを確認してください。

## 関連ページ {#related}

- [サービスの設定](/docs/xoa-hl/configuration/)：xo-server の設定ファイル。
- [xo-cli による自動化](/docs/xoa-hl/automation/)：有効期間の短いトークンで、コマンドラインからインベントリを読み取る。
- [設定のエクスポート](/docs/xoa-hl/configuration-backup/)：管理画面の設定と記録を保存する。
- [xoa-hl](/docs/components/xoa-hl/) と [build-xoa-hl](/docs/components/build-xoa-hl/)：パッケージの作り方。製品のビルドは CI でのみ行います。

このドキュメントの変更を提案するときは、使っているイメージとパッケージのバージョンを添えてください。

{{< details title="出典" closed="true" >}}
- **バージョン、パッチ、ビルド**：[アップストリームの XO のバージョン（`UPSTREAM_XO`）](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/UPSTREAM_XO)、[パッチの一覧](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/metadata.toml)、[メニューを非表示にするパッチ](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/menu-hide-items.patch)、[パッケージの定義](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec)、[xo-server パッケージのバージョン](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/package.json)、[管理画面のビルド](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js)。
{{< /details >}}
