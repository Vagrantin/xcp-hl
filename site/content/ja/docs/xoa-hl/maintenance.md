---
title: "アプライアンスの保守"
linkTitle: "アプライアンスの保守"
description: "バージョンを記録し、更新の時間帯を準備して、結果を確認します。"
weight: 80
translationKey: xoa-manual-maintenance
translationStatus: draft
sourceRevision: sha256:932a5f12913363b83e6146fc55c12988da0d9d6c7e314afb19653f8b4996cea1
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

アプライアンスを更新する前に、設定のエクスポート、コンソールへのアクセス、Web 画面が再接続した後の結果確認を準備します。

{{< callout type="info" >}}
イメージ `xoa-image-20261009-5f33c81`、パッケージ `v5.113.2_e281c536-ce38`、XO 5.113.2 のソースを確認したプレビューです。使い捨てのアプライアンスでの中断・再起動テストは未完了です。後のパッケージでは動作が異なる可能性があります。
{{< /callout >}}

## 1. 更新前の状態を記録する

**ブラウザー**で管理者として **About** (`/#/about`) を開きます。**XOA-HL version**、**XOA-HL VM version**、アプライアンスのアドレス、元のイメージタグを記録します。VM バージョンはイメージのビルドを識別します。アプリケーションを更新しても、そのイメージの識別情報は置き換わりません。

許可されたコンソールまたは SSH アクセスがある場合、次の読み取り専用コマンドを**アプライアンス内**で実行します。必要に応じて root 権限を使います。

```bash
rpm -q xoa-hl nodejs
cat /etc/xoa-hl-vm-release
timedatectl
systemctl list-timers 'xoa-hl-*'
```

出力を[リリース一覧](/docs/reference/release-matrix/)と[リリースノート](/docs/reference/changelog/)とともに保存します。一覧は配布されたコンポーネントを示すもので、検証済みの互換性を示すものではありません。

## 2. 保守時間帯を準備する

- [XO 設定をエクスポート](/docs/xoa-hl/configuration-backup/)し、ファイルとパスフレーズをアプライアンスの外に保存します。
- `/root/.config/xo-server/config.toml` の独自の変更、TLS 関連ファイル、`/etc/xoa-hl/update.conf` は別途記録します。Web 画面からのエクスポートにはこれらのファイルは含まれません。
- Web 画面が使えなくても XO Lite からアプライアンスのコンソールに接続できることを確認します。
- バックアップ、復元、その他の管理処理が完了していることを確認します。サービスの再起動と、必要に応じた後のアプライアンス再起動に十分な時間を確保します。

アプライアンスの更新処理は XOA-HL VM 内で動きます。ホストの更新は別の操作です。[既存の更新ガイド](/docs/guides/updates/)で対象とコマンドを確認してください。

## 3. モードとチャネルを選ぶ

**Settings → XOA-HL Updates** (`/#/settings/xoa-hl-updates`) を開きます。**Check for update** と **Update now** の操作は[標準の更新手順](/docs/guides/updates/)を参照してください。

| モード | 実施内容 |
| --- | --- |
| Manual only | 毎回、手動で確認とインストールを開始する。初期状態の既定値 |
| Check automatically | 定期的に確認し、インストールの実施時刻は手動で決める |
| Install automatically | 保守時間帯での定期インストールを明示的に承認する |

スケジュールは**アプライアンスのタイムゾーン**を使い、開始時刻の後に選択したランダム遅延が加わります。表示されたタイムゾーンを `timedatectl` と照合してください。ホストやブラウザーのタイムゾーンは基準ではありません。頻度、週次の場合の曜日、時刻、遅延を保存し、保存結果とタイマー一覧を確認します。

通常の保守では **stable** チャネルを使います。**Testing** は候補パッケージを追加するため、使い捨ての検証用アプライアンスで使います。チャネルを切り替えても、パッケージのインストールや、インストール済み候補版のダウングレードは実行されません。

管理された更新処理は `nodejs` を除外して `dnf` による全体更新を実行します。アプリケーションパッケージのインストールはトランザクション終了後に `xo-server` を再起動するため、Web 画面の切断だけでは失敗と判断できません。

## 4. 結果を確認する

Web 画面に再接続して **About** を開き、アプリケーションが期待するバージョンになっていることを確認します。対象ホストのインベントリが接続されていることと更新結果を確認します。結果が不明な場合は、アプライアンスで次の読み取り専用の確認を行います。

```bash
systemctl status xo-server xoa-hl-update.service --no-pager
journalctl -u xoa-hl-update.service -u xo-server --since '1 hour ago' --no-pager
tail -n 100 /var/lib/xoa-hl/update.log
cat /var/lib/xoa-hl/auto-update.status
cat /run/xoa-hl/status
```

| 記録 | 意味 |
| --- | --- |
| `/run/xoa-hl/status` | 最新の確認結果 `UP_TO_DATE`、`AVAILABLE`、`ERROR`。再起動をまたいで保持されない |
| `/var/lib/xoa-hl/update.log` | 管理されたインストールの出力と成功・失敗の終了マーカー。次の試行で上書きされる |
| `/var/lib/xoa-hl/auto-update.status` | 自動実行のみの記録。`startedAt` と `finishedAt` (UTC) を実施時刻と照合する |
| `result=check_failed` または `result=failed` | 確認またはインストールのログを調べる。どちらも成功ではない |
| `rebootNeeded=yes`、`no`、`unknown` | 自動実行での判定。`unknown` は再起動不要を意味しない |

手動インストールは自動実行の記録を**更新しません**。確認サービスの正常終了だけでなく、判定結果も読む必要があります。次の試行前に必要なログを保存してください。

## 5. 切断や実行時間帯の見逃しに対処する

ブラウザーだけが切断された場合は、再試行前にコンソールでサービスとログを確認します。別の `dnf` を開始したり、進行中のトランザクションを停止したり、更新処理を解放するために再起動したりしないでください。管理された確認・インストールは共通のロックを使いますが、シェルから直接開始した処理はこの連携の対象外です。

**自動再起動はありません**。自動インストールの時間帯を逃しても、起動直後には実行されません。アプライアンスの起動が中断した場合や結果が不明な場合はログを保存し、次の更新を予定する前に[トラブルシューティング](/docs/xoa-hl/troubleshooting/)を参照してください。トランザクションや管理処理が実行中でないことを確認し、インストールした変更に再起動が必要と判断した後にのみ再起動します。その後、ログイン、バージョン、インベントリを再確認します。

パッケージのダウングレードは、検証済みのアプライアンス復旧手順ではありません。ベース OS、XO データ、独自の設定ファイルは復元されません。ロールバックを計画する前に[設定と復旧の制約](/docs/xoa-hl/configuration-backup/)を確認してください。

## ソース

`xoa-hl@5f33c81` で確認したソース：[スケジュール](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/docs/automatic-updates.md)、[インストール処理](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-update.sh)、[自動実行の記録](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-auto-update.sh)、[確認結果](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-check-update.sh)、[パッケージの処理](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec)、[チャネルのパッチ](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/patches/zzzzzzzz-xoa-hl-update-channel.patch)。
