---
title: ホストとプールの管理
description: 接続一覧、管理担当の移行、古い XOA マーカーを確認する。
weight: 24
translationKey: xoa-manual-hosts-pools
translationStatus: draft
sourceRevision: sha256:a6577ca820beb79ac98cf82c2920df54641b60291785bb165ecbad082dfa96de
glossaryTerms: ["appliance", "host", "pool", "xo-lite", "backup"]
---

**XOA-HL アプライアンス**の管理者アカウントと、許可されたホストコンソールへのアクセスを用意します。アプライアンスのアドレス、ホストとプールの識別情報、現在の管理担当を記録します。最初の接続は[初回ログインとホスト接続](/docs/xoa-hl/first-login/)を参照してください。

{{< callout type="info" >}}
イメージ `xoa-image-20261009-5f33c81`、パッケージ `v5.113.2_e281c536-ce38`、XO 5.113.2 を対象としたソース確認済みのプレビューです。XO Lite のボタンは `xolite-ce v0.21.0-ce29`（上流 `xo-lite-v0.21.0`）も確認しています。管理移行と古いマーカーの実機テストは未完了です。
{{< /callout >}}

## 1. 接続されたプールを確認する

**Settings → Servers** (`/#/settings/servers`) を開きます。対象の接続が有効で接続済みであり、一覧に予定したホスト、プール、VM、ストレージが表示されることを確認します。保存された接続情報だけでは接続成功を確認できません。失敗したらエラーを読み、[接続ガイド](/docs/xoa-hl/first-login/)でアドレス、資格情報、証明書の扱いを確認します。

[#126](https://github.com/Vagrantin/xcp-hl/issues/126) に記録されたサポート対象の管理ルールは、**あるホストまたはプールを管理する XOA は 1 台**です。複数のアプライアンスは技術的には接続できますが、同時管理はサポートされません。アプライアンスが 1 つのプールしか管理できないという意味ではありません。接続前に担当を調整し、同じゲストに重複したバックアップスケジュールを残さないでください。

## 2. 別のアプライアンスに管理を移す

1. 作業時間を確保し、実行中の管理とバックアップを完了させ、旧担当の接続、スケジュール、保存先を記録します。[設定をエクスポート](/docs/xoa-hl/configuration-backup/)して保管します。エクスポートだけではジョブを移行または無効化しません。
2. 旧担当の関連スケジュールを無効にします。旧担当の **Settings → Servers** でプールへの接続を削除してから、新担当を接続します。XO の管理移行のためにホストをプールから外したり VM を削除したりしないでください。
3. 新しいアプライアンスにホストまたはプールへの接続を追加します。接続された一覧と必要な権限を確認します。設定の再作成や復元には、設定ガイドの隔離とインポートの注意事項を適用します。
4. 旧担当が再接続したりプールに対してジョブを実行したりしないことを確認します。保存先を確認し、隔離した復旧テストを行ってから、新担当の予定したスケジュールだけを有効にします。

どちらかの状態が不明なら移行を中断し、接続やタスクのエラーを保存します。複数ホストのプール作成、HA、ライブマイグレーションはこの検証の対象外です。この手順はプールの構成を変更しません。

## 3. XO Lite のボタンを理解する

XO はプールの `other-config` に `xo:clientInfo:<appliance-uuid>` を書き込みます。初期設定では接続時と **6 時間**ごとに更新し、その更新時に **48 時間**より古いマーカーを削除します。読み取り専用の XO 接続では書き込みません。接続を削除すると将来の書き込みは止まりますが、古いマーカーはすぐには消えません。

確認した XO Lite では、**Access XOA** は `lastConnected` が最も新しいマーカーを使います。`publicUrl` を優先し、なければ `eth0`（または最初の利用可能なインターフェース）の最初のアドレスを HTTPS で開きます。VM や Web サービスの稼働は確認しません。アドレスが見つからなければ **Deploy XOA** を表示します。XO Lite 自体は古いマーカーを期限切れにしないため、XO が接続しなければ古いボタンが残る場合があります。

古いアドレスを理由に 2 台目の管理アプライアンスを展開しないでください。既知のアドレスと管理担当を先に確認します。正しい担当が誤ったアドレスを公開しているなら、マーカーを繰り返し削除するのではなく URL やネットワーク設定を確認します。

## 4. 古いマーカーを確認して削除する

**ハイパーバイザーホスト**で root 権限を使い、まず次の読み取り専用コマンドを実行します。管理記録と照合し、プールと古いキーを正確に特定します。

```bash
xe pool-list params=uuid,name-label
xe pool-param-get uuid='<pool-uuid>' param-name=other-config
```

旧アプライアンスの接続を削除した後に限り、マーカーの値を記録し、必要なら**そのキーだけ**を削除します。両方のプレースホルダーを置き換えてください。`other-config` 全体を削除してはいけません。

```bash
xe pool-param-remove uuid='<pool-uuid>' param-name=other-config param-key='xo:clientInfo:<obsolete-appliance-uuid>'
```

読み取り専用の確認を繰り返し、XO Lite を再読み込みします。旧担当がまだ動いていれば、再接続時や次の更新でマーカーを書き戻す場合があります。キーが戻ったら、残っている接続を調べます。この操作は検出用メタデータを変更し、プール構成、VM の電源、バックアップデータは変更しません。今回のソース確認では実行していません。

## ソース

XO 5 の固定コミット `e281c536`：[サーバー画面](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js)、[プールのマーク処理](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs)、[初期設定の間隔](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml)。XO Lite：[ボタンのアドレス選択](https://github.com/vatesfr/xen-orchestra/blob/13f987ff3d34504a90b89178489e15fa2293d1b3/@xen-orchestra/lite/src/components/XoaButton.vue)、[コミュニティ版のビルドとパッチ対象](https://github.com/Vagrantin/xolite-ce/blob/ca72babb35f435b31d4726a7d1e90f42b9c06cb8/.github/workflows/build-xolite-ce.yml)。サポートルールとホストの限定的な削除手順は [#126](https://github.com/Vagrantin/xcp-hl/issues/126) に基づきます。
