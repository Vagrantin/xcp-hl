---
title: XOA-HL マニュアル
weight: 2
translationKey: xoa-manual-home
translationStatus: reviewed
sourceRevision: sha256:9690e24c060de4d8fcc693f5a8507c57cce56c189f0a4c0c5abd9829f4c4abae
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

XOA-HL は Xen Orchestra を動かすアプライアンス（構築済みの仮想マシン）です。ブラウザーから XCP-HL のホストと仮想マシンを管理できます。このマニュアルでは、XOA-HL の準備、VM の運用、保護、そして最新の状態を保つ方法を説明します。

{{< callout type="info" >}}
**対象バージョン:** XOA-HL `v5.113.2_e281c536-ce40`（Xen Orchestra 5.113.2）。各ガイドは公開済みのコードに基づいていますが、検証環境での通しのテストはまだ済んでいません。まずテスト用の VM で試してください。
{{< /callout >}}

## はじめに

XOA-HL を初めて使う場合は、次の 3 つのガイドを順番に進めてください。

{{< cards >}}
  {{< card link="first-login/" title="1. 初回ログイン" subtitle="ログインしてパスワードを変更し、表示言語を選んでホストを接続します。" >}}
  {{< card link="create-vm/" title="2. 最初の VM" subtitle="インストール用 ISO をアップロードし、テスト用の VM をインストールします。" >}}
  {{< card link="backup-restore/" title="3. バックアップと復元" subtitle="VM をバックアップし、復元したコピーが動くことを確認します。" >}}
{{< /cards >}}

まだ展開していない場合は、先に [XO Lite から XOA-HL を展開](/docs/start/#start-deploy-xoa)してください。ホスト、XO Lite、アプライアンスの関係は[アーキテクチャの概要](/docs/start/#start-architecture)で確認できます。

## 仮想マシン

- [VM の管理](/docs/xoa-hl/vm-operations/)：起動と停止、スナップショット、コピー、CPU とメモリ、削除。
- [VM のコンソールを使う](/docs/xoa-hl/vm-operations/#vm-console)、画面が真っ暗なときの対処。
- [スナップショットを作成して元に戻す](/docs/xoa-hl/vm-operations/#stopped-snapshot)。
- [Linux ゲストツールをインストールする](/docs/xoa-hl/guest-tools/)。
- [テンプレートを作成して使う](/docs/xoa-hl/templates/)。
- [VM の移行、エクスポート、インポート](/docs/xoa-hl/vm-transfer/)。

## ストレージとネットワーク

- [ディスクとネットワークインターフェースを追加する](/docs/xoa-hl/storage-networks/)。
- [VM ディスク用の NFS ストレージを作成する](/docs/xoa-hl/storage-networks/#nfs-vm-storage)。
- [VLAN ネットワークを作成する](/docs/xoa-hl/storage-networks/#host-vlan-network)。
- [ネットワークの問題を診断する](/docs/xoa-hl/troubleshooting/#network-connectivity)。

## バックアップと復旧

- [バックアップのスケジュールと保持数を設定する](/docs/xoa-hl/backup-restore/#backup-schedules)。
- [増分バックアップを使う](/docs/xoa-hl/backup-restore/#delta-backups)。
- [ファイル単位で復元する](/docs/xoa-hl/backup-restore/#file-restore)。
- [VM を別のプールにコピーする（DR レプリカ）](/docs/xoa-hl/backup-restore/#dr-replica)。
- [Windows Server の共有（SMB）にバックアップする](/docs/xoa-hl/backup-restore/#smb-remote)。
- [失敗したバックアップに対処する](/docs/xoa-hl/troubleshooting/#backup-failures)。

## ホスト、ユーザー、セキュリティ

- [ホストとプールの管理](/docs/xoa-hl/hosts-pools/)：接続、XO Lite のボタン、統計。
- [ホストをプールに参加させる](/docs/xoa-hl/hosts-pools/#pool-join)。
- [ホストをメンテナンスモードにする](/docs/xoa-hl/hosts-pools/#host-maintenance-mode)。
- [ユーザー、グループと権限の管理](/docs/xoa-hl/permissions/)。
- [クォータ付きでリソースを委任する](/docs/xoa-hl/permissions/#resource-set-delegation)。
- [サインインにワンタイムコードを追加する](/docs/xoa-hl/sign-in-otp/)。

## XOA-HL の運用を続ける

- [アプライアンスをアップデートする](/docs/guides/updates/#xoa-hlアプライアンスのアップデート)、[ホストをアップデートする](/docs/guides/updates/#xcp-hlホストのアップデート)。
- [保守を計画して結果を確認する](/docs/xoa-hl/maintenance/)。
- [XO の設定をエクスポートする](/docs/xoa-hl/configuration-backup/)。
- [プールのメタデータをバックアップする](/docs/xoa-hl/configuration-backup/#pool-metadata)。
- [問題をトラブルシューティングする](/docs/xoa-hl/troubleshooting/)。
- [各リリースの内容を確認する](/docs/reference/release-matrix/)、[変更履歴を読む](/docs/reference/changelog/)。

## リファレンス

- [概念と機能の範囲](/docs/xoa-hl/concepts/)
- [サービスの設定](/docs/xoa-hl/configuration/)
- [xo-cli による自動化](/docs/xoa-hl/automation/)
- [用語集](/docs/xoa-hl/glossary/)
- [コントリビューター向けのページ](/docs/components/)

## ヘルプとフィードバック

XOA-HL の画面とこのドキュメントの表示言語は、それぞれ別に設定します。ドキュメントの言語は、このページ上部のセレクターで切り替えます。[ページのレビュー状況](/docs/xoa-hl/translation-status/)で、レビュー済みのページを確認できます。

[ドキュメントの問題を報告する](https://github.com/Vagrantin/xcp-hl/issues/new?title=Documentation%3A%20XOA-HL%20manual)。ページのアドレス、修正が必要な手順、アプライアンスのバージョンを書いてください。パスワードや個人情報は絶対に含めないでください。
