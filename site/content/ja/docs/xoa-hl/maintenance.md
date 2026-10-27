---
title: "アプライアンスの保守"
linkTitle: "アプライアンスの保守"
description: "インストール済みのバージョンを記録し、更新の時間帯を準備して、アプライアンスを更新し、結果を確認します。"
weight: 80
translationKey: xoa-manual-maintenance
translationStatus: draft
sourceRevision: sha256:ddfb161f1c342f444294e2d28611c181f99a15ecf6de459f1c4ee06b47658fee
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

XOA-HL アプライアンスを 4 つの手順で更新します。インストール済みのものを記録し、保守の時間帯を準備し、更新の方法を選び、結果を確認します。作業は**ブラウザー**で、XOA-HL に管理者としてログインして行います。一部の読み取り専用の確認は、コンソールまたは SSH を使って**アプライアンス内**で行います。

{{< callout type="info" >}}
**対象:** イメージ `xoa-image-20261022-a280852`、パッケージ `v5.113.2_e281c536-ce43` から `v5.113.2_e281c536-ce47`（Xen Orchestra 5.113.2）。2026-10-27 に検証用アプライアンスでテスト済みです。後のパッケージでは動作が異なる場合があります。
{{< /callout >}}

## 1. 更新前の状態を記録する {#record-versions}

1. ブラウザーで、管理者として **XOについて**（`/#/about`）を開きます。
2. **XOA-HL のバージョン**、**XOA-HL VM のバージョン**、アプライアンスのアドレス、元のイメージタグを控えます。VM のバージョンはイメージのビルドを示します。アプリケーションを更新しても変わりません。

許可されたコンソールまたは SSH のアクセスがある場合は、次の読み取り専用コマンドをアプライアンス内で実行します。必要に応じて root 権限を使います。

```bash
rpm -q xoa-hl nodejs
cat /etc/xoa-hl-vm-release
timedatectl
systemctl list-timers 'xoa-hl-*'
```

出力は[リリース一覧](/docs/reference/release-matrix/)と[リリースノート](/docs/reference/changelog/)と一緒に保存します。一覧は一緒に配布されたコンポーネントを示すもので、一緒にテストされたことを示すものではありません。

## 2. 更新の時間帯を準備する {#prepare-window}

- [XO 設定をエクスポート](/docs/xoa-hl/configuration-backup/)します。ファイルとパスフレーズはアプライアンスの外に保存します。
- `/root/.config/xo-server/config.toml`、TLS ファイル、`/etc/xoa-hl/update.conf` に加えた変更を別に記録します。Web 画面からのエクスポートには、これらのファイルは含まれません。
- Web 画面が使えない場合に備えて、XO Lite からアプライアンスのコンソールを開けることを確認します。
- バックアップ、復元、その他の管理処理が終わっていることを確認します。
- サービスの再起動と、必要に応じた後のアプライアンス再起動ができる長さの時間帯を確保します。

このページで更新するのは XOA-HL VM だけです。ホストの更新は別の作業です。正しい対象とコマンドは[更新ガイド](/docs/guides/updates/)を参照してください。

## 3. モードとチャネルを選ぶ {#update-mode-channel}

**設定 → XOA-HL のアップデート**（`/#/settings/xoa-hl-updates`）を開きます。手動で更新するときは、**アップデートを確認** と **今すぐアップデート** について[更新手順](/docs/guides/updates/)に従います。

**モード** を選びます。

| モード | 行うこと |
| --- | --- |
| 手動のみ | 確認とインストールを毎回自分で開始します。これが既定値です |
| 自動確認 | 確認はスケジュールで実行されます。インストールの時期は自分で決めます |
| 自動インストール | インストールがスケジュールで実行されます。保守時間帯でのインストールを明示的に承認した後にだけ使います |

スケジュールを使うモードでは、次のように設定します。

1. **アプライアンスのタイムゾーン** を確認します。スケジュールはこのタイムゾーンを使い、ホストやブラウザーのタイムゾーンは使いません。`timedatectl` の出力と照合します。
2. **頻度**、毎週の場合は **曜日**、**現地時刻での開始時刻** を設定します。実行はその時刻に始まり、ランダムな遅延はありません。
3. **自動アップデートの設定を保存** を選びます。
4. 保存された設定と、`systemctl list-timers 'xoa-hl-*'` のタイマー一覧を確認します。

**更新チャネル** は、通常の保守では **安定版** のままにします。**テスト** は候補パッケージを追加するため、使い捨てのテスト用アプライアンスでだけ使います。チャネルを変えても何もインストールされず、インストール済みの候補パッケージがダウングレードされることもありません。

管理された更新は、`nodejs` を除いて `dnf` による全体の更新を実行します。アプリケーションパッケージをインストールすると、トランザクションの後に `xo-server` が再起動するため、Web 画面が切断されることがあります。それだけでは更新の失敗を意味しません。

## 4. 結果を確認する {#check-result}

1. Web 画面に再接続し、**XOについて** を開きます。想定したアプリケーションのバージョンが表示されることを確認します。
2. 想定したホストが接続され、そのインベントリが表示されることを確認します。
3. 更新の結果を読みます。ページを開くと、スケジュールによるものを含め、保存済みの最後のチェック結果が表示されます。**前回の自動実行結果** では、失敗した自動実行が赤いバナーで表示されます。

結果がはっきりしない場合は、アプライアンス内で次の読み取り専用の確認を実行します。

```bash
systemctl status xo-server xoa-hl-update.service --no-pager
journalctl -u xoa-hl-update.service -u xo-server --since '1 hour ago' --no-pager
tail -n 100 /var/lib/xoa-hl/update.log
cat /var/lib/xoa-hl/auto-update.status
cat /run/xoa-hl/status
```

| ファイルまたは値 | 分かること |
| --- | --- |
| `/run/xoa-hl/status` | 最新の確認結果（`UP_TO_DATE`、`AVAILABLE`、`ERROR`）。アプライアンスを再起動すると消えます |
| `/var/lib/xoa-hl/update.log` | 管理されたインストールの出力で、最後に成功または失敗のマーカーがあります。次の試行で上書きされます |
| `/var/lib/xoa-hl/auto-update.status` | 自動実行の場合のみ。`startedAt` と `finishedAt`（UTC）を更新の時刻と照合します |
| `result=check_failed` または `result=failed` | 確認またはインストールが失敗しました。そのログを読みます。どちらも成功ではありません |
| `rebootNeeded=yes`、`no`、`unknown` | 自動実行による判定です。`unknown` は再起動が不要という意味ではありません このイメージでは常に `unknown` になります。再起動が必要かどうかは、root で `dnf needs-restarting -r` を実行して確認します。 |

手動のインストールでは、自動実行の記録は更新**されません**。確認サービスが正常に終了しても、問題を報告していることがあります。結果を必ず読んでください。再試行の前に、必要なログを保存します。

**確認:** **XOについて** に想定したバージョンが表示され、想定したホストが接続され、更新の結果が成功を示しています。

## 更新が正常に終わらない場合 {#update-problems}

**自動再起動はありません**。管理された確認とインストールは共通のロックを使いますが、シェルから開始した `dnf` コマンドはこのロックの対象外です。更新が実行中の可能性がある間は、別の `dnf` を開始したり、実行中のトランザクションを止めたり、更新処理を解放するために再起動したりしないでください。

| 症状 | 確認すること |
| --- | --- |
| ブラウザーだけが切断された | アプリケーションのインストールは `xo-server` を再起動します。再試行の前に、コンソールでサービスとログを確認します。 |
| 更新処理が実行中のままに見える | コンソールでサービスとログを確認します。別の `dnf` の開始、トランザクションの停止、解放のための再起動はしないでください。 |
| 自動インストールの時間帯を逃した | 逃したインストールは、アプライアンスの起動直後には実行されません。別の時間帯を計画します。 |
| アプライアンスの起動が中断した、または結果がはっきりしない | ログを保存し、次の更新を計画する前に[トラブルシューティング](/docs/xoa-hl/troubleshooting/)を参照します。 |
| 更新中にアプライアンスが停止した | 再起動し、ほかの作業の前にパッケージを確認します。新しい更新が成功と表示しても、壊れたパッケージが残ることがあります。[中断した更新の後でパッケージを修復する](/docs/xoa-hl/troubleshooting/#interrupted-update)の手順に従います。 |
| インストールした変更に再起動が必要かもしれない | トランザクションや管理処理が実行中でなく、変更に再起動が必要と判断した場合にだけ再起動します。その後、ログイン、バージョン、インベントリを再確認します。 |
| 以前のバージョンに戻したい | パッケージのダウングレードは、テスト済みの復旧手順ではありません。ベース OS、XO データ、独自のファイルは復元されません。先に[復旧の制約](/docs/xoa-hl/configuration-backup/#recovery-limits)を読んでください。 |

{{< details title="出典" closed="true" >}}
- **アプライアンスの更新処理**：[スケジュール](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/docs/automatic-updates.md)、[インストール処理](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-update.sh)、[自動実行の記録](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-auto-update.sh)、[確認結果](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-check-update.sh)、[パッケージの spec ファイル](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec)、[チャネルのパッチ](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzz-xoa-hl-update-channel.patch)、[自動更新ページの修正](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzzzzzz-xoa-hl-auto-update-ui-fixes.patch)。
{{< /details >}}
