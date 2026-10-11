---
title: アプライアンスサービスの設定
description: 運用者の設定を確認し、検査したサービス変更を準備します。
weight: 71
translationKey: xoa-manual-configuration
translationStatus: draft
sourceRevision: sha256:968057a7d1a41033c98ff1ff829858fec7d897e9c34b4151899d6bd7b7f814eb
glossaryTerms: ["appliance", "host", "pool"]
---

xo-server の設定は、管理画面からエクスポートする設定や記録とは別に管理します。

{{< callout type="info" >}}
イメージ `xoa-image-20261009-5f33c81`、パッケージ `v5.113.2_e281c536-ce38`、XO 5.113.2 のソースを確認したリファレンスです。後続リリースでは動作が変わる可能性があります。実際のアプライアンスでの検証と人による翻訳レビューは未完了です。
{{< /callout >}}

## 設定の場所

| 場所 | ce38 での役割 | 扱い方 |
| --- | --- | --- |
| `/opt/xo/packages/xo-server/config.toml` と `sample.config.toml` | パッケージの既定値とコメント付きの参考設定 | 参照用。パッケージの更新で置き換わる |
| `/root/.config/xo-server/config.toml` | ファイルがない場合だけ作成する運用者の設定 | 編集前に非公開でバックアップ。RPM の初期設定処理では保持する |
| `/root/.config/xo-server/config.z-auto.json` | サーバーが書き込む設定 | 上書き関係を調べる際に存在を確認。無条件で置き換えない |
| Redis データベース | XO のアプリケーション記録 | 文書化した管理画面のエクスポートとインポートの範囲に従う |
| `/etc/xoa-hl/update.conf` | HomeLab 更新のモード、スケジュール、チャネル | Settings → XOA-HL Updates と更新ガイドを優先する |
| `/opt/xo/xoahl.crt` と `xoahl.key` | TLS 証明書と秘密鍵 | 別途保管。問題報告に秘密鍵を添付しない |

配布された systemd ユニットは root で実行し、XDG のユーザー設定を使います。ローダーは `/etc/xo-server/config.*` やローカルの `.xo-server.*` も読み込み、複数のファイルをマージできます。有効な値を判断する前に、ユニットのカスタム設定と他の設定ファイルを確認します。このページは配布されたユニットを対象とし、独自のサービスアカウントは対象外です。

[設定エクスポート](/docs/xoa-hl/configuration-backup/)には運用者の TOML、TLS ファイル、更新設定は含まれません。変更は[保守](/docs/xoa-hl/maintenance/)と[アップデート](/docs/guides/updates/)を参照してください。

## 例：アプライアンス URL を通知する

`http.publicUrl` はプールの検出に使う URL を指定します。リスナー、証明書、DNS レコードは作成しません。DNS と信頼された証明書が一致する実際の HTTPS URL を選び、まずブラウザーでのアクセスを確認します。変更前に[管理担当と検出](/docs/xoa-hl/hosts-pools/)を参照してください。

使い捨ての検証環境で、**既存の** `[http]` テーブルに設定を追加します。次の最小例は配布された HTTPS リスナーと Redis URI を保持します。カスタマイズ済みのファイルをそのまま置き換える例ではありません。

```toml
[http]
publicUrl = "https://xoa.lab.example"

[[http.listen]]
port = 443
cert = "/opt/xo/xoahl.crt"
key = "/opt/xo/xoahl.key"

[redis]
uri = "redis://127.0.0.1:6379/0"
```

別の `[http]` テーブルを追加したり、既存のリスナーを削除したりしないでください。実際の証明書と鍵のパスを維持します。RPM はインストール時に初期の自己署名証明書と鍵を生成し、共通の鍵は配布しません。鍵や証明書、または `/var/lib/xoa-hl/tls-generated` マーカーがない場合は生成されるので、更新前に実際の TLS 状態を記録します。証明書の交換、リバースプロキシ、Redis の移行は個別の検証が必要です。

## 構文を確認して保守時間に適用する

元の運用者設定を非公開でアプライアンス外に保存し、アクセス権も記録します。コンソール接続を準備し、バックアップ、復元、管理ジョブの終了を待ちます。編集後、アプライアンス内で root としてパーサーを実行します。

```bash
cd /opt/xo/packages/xo-server
node --input-type=module -e "import fs from 'node:fs'; import TOML from '@iarna/toml'; TOML.parse(fs.readFileSync('/root/.config/xo-server/config.toml', 'utf8')); console.log('TOML syntax OK');"
```

`TOML syntax OK` は構文が正しいことだけを示します。アクセス権、TLS の信頼、マージ結果、到達性は確認しません。ここで説明するパーサーとマージ動作は合成設定でテストしましたが、公開アプライアンス上では未検証です。再起動前に構文エラーを解消します。

合意した保守時間に適用して確認します。

```bash
systemctl restart xo-server
systemctl status xo-server --no-pager
journalctl -u xo-server --since '10 minutes ago' --no-pager
```

再起動で管理画面の接続が切れます。想定したアドレスへ接続し直し、ログイン、ホストのインベントリ、次回のマーク後の検出を確認します。起動に失敗した場合はコンソールで保存した設定を戻し、再度構文を確認して 1 回再起動します。結果が不明なら[トラブルシューティング](/docs/xoa-hl/troubleshooting/)を参照してください。共有するログから機密情報を除去します。

## ソース

[bootstrap](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/scripts/build-xo.sh), [RPM lifecycle](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SPECS/xoa-hl.spec), [service](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xo-server.service), [configuration loader](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [defaults](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [sample](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/sample.config.toml), [pool discovery](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs).
