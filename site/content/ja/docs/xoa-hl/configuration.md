---
title: "アプライアンスサービスの設定"
linkTitle: "サービスの設定"
description: "サービスの設定ファイルを探し、アクセス経路と HTTPS 証明書を確認して、変更を安全に適用します。"
weight: 91
translationKey: xoa-manual-configuration
translationStatus: draft
sourceRevision: sha256:cf10324c828a27039571b3a119cc1feacd94fbe74d8a0815a3060736e0c32685
glossaryTerms: ["appliance", "host", "pool"]
---

XOA-HL アプライアンスの xo-server 設定ファイルを探し、管理用のアクセス経路と HTTPS 証明書を確認して、変更を安全に適用します。作業はアプライアンス内のシェルで root として行い、別のコンソールも使える状態にしておきます。これらのファイルは、管理画面からエクスポートする設定や記録とは別のものです。

{{< callout type="info" >}}
**対象:** イメージ `xoa-image-20261022-a280852`、パッケージ `v5.113.2_e281c536-ce40`（Xen Orchestra 5.113.2）。公開済みのコードに基づく手順で、検証環境でのテストはまだです。
{{< /callout >}}

## 設定ファイルを探す {#settings-files}

| 場所 | 内容 | 扱い方 |
| --- | --- | --- |
| `/opt/xo/packages/xo-server/config.toml` と `sample.config.toml` | パッケージの既定値と、コメント付きの例 | 読むだけにします。パッケージを更新すると置き換わります |
| `/root/.config/xo-server/config.toml` | 運用者自身の設定（運用者ファイル）。インストール時に、ファイルがない場合だけ作成されます | 編集する前に非公開のバックアップを取ります。パッケージのインストールではこのファイルは保持されます |
| `/root/.config/xo-server/config.z-auto.json` | サーバー自身が書き込む設定 | 上書きの元を調べるときに、このファイルがあるか確認します。無条件に上書きしないでください |
| Redis データベース | XO のアプリケーションの記録 | 管理画面のエクスポートとインポートを、文書化された範囲で使います |
| `/etc/xoa-hl/update.conf` | アプライアンスの更新のモード、スケジュール、チャネル | 代わりに **設定 → XOA-HL のアップデート** と更新ガイドを使います |
| `/opt/xo/xoahl.crt` と `xoahl.key` | アプライアンスの TLS 証明書と秘密鍵 | 別にコピーを保管します。問題報告に秘密鍵を添付しないでください |

同梱の systemd サービスは root で動作し、`/root/.config` の下のユーザー設定を読みます。xo-server は `/etc/xo-server/config.*` やローカルの `.xo-server.*` ファイルも読み、複数のファイルをマージします。どの値が有効かを判断する前に、サービスの独自の上書き設定と、他の設定ファイルを確認します。このページは同梱のサービスだけを扱い、独自のサービスアカウントは扱いません。

[設定のエクスポート](/docs/xoa-hl/configuration-backup/)には、運用者の TOML ファイル、TLS ファイル、更新の設定は含まれません。これらについては[アプライアンスの保守](/docs/xoa-hl/maintenance/)と[アップデート](/docs/guides/updates/)を参照してください。

## プール検出用のアプライアンス URL を設定する {#public-url}

`http.publicUrl` は、XO が接続中の各プールに記録するアプライアンスの URL を設定します。プールの検出に使われます。待ち受け、証明書、DNS レコードは作成しません。DNS が一致し、信頼された証明書を持つ、アプライアンスの実際の HTTPS URL を使います。まずブラウザーで開けることを確認します。変更する前に[ホストとプール](/docs/xoa-hl/hosts-pools/)を読んでください。

作り直せる検証用のアプライアンスで試します。**既存の** `[http]` テーブルに設定を追加します。次の最小限の例は、同梱の HTTPS の待ち受けと Redis のアドレスを残しています。独自に変更したファイルの代わりにはなりません。

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

2 つ目の `[http]` テーブルを追加したり、既存の待ち受けを削除したりしないでください。実際の証明書と鍵のパスを維持します。パッケージはインストール時に独自の自己署名証明書と鍵を作成します。共通の鍵は配布していません。鍵、証明書、または `/var/lib/xoa-hl/tls-generated` マーカーがないと、新しいペアが生成されます。そのため、更新の前にインストール済みの TLS の状態を記録します。証明書の交換、リバースプロキシ、Redis の移動はここでは扱いません。

## ネットワークを制限する前に管理経路を把握する {#management-network}

この確認は読み取るだけで、何も変更しません。同梱の設定は、ポート `443` で HTTPS を待ち受けます。運用者の設定、プロキシ、ファイアウォール、別のイメージによって、実際の経路は変わることがあります。管理画面がファイアウォールの規則を作ることはありません。

**始める前に**

- 許可する管理クライアント、サブネット、サービス、バックアップ先を、ネットワークとホストの担当者と合意します。
- 制限の影響を受けない、別のコンソールの経路を合意します。
- これを、ACL、VIF、ホストの PIF、スイッチのポリシーを変更する前に行います。

| 経路 | 記録して確認すること |
| --- | --- |
| 許可されたブラウザー → XOA-HL | アプライアンスの VM とアドレス、名前解決の結果、実際の HTTPS の接続先、証明書の識別情報を記録します。許可されたクライアントから改めてログインし、ホストの一覧を確認します。同梱の待ち受けは `443` ですが、インストール済みの設定と実際の接続先を確認します。`http.publicUrl` はアドレスを通知するだけで、ポートは開きません。 |
| XOA-HL → ホストとプール | **設定 → サーバ一覧** で、接続中のサーバーのアドレス、想定するプールとホストの ID、証明書の扱いを記録します。現在のホストの一覧を確認し、検証環境で既にテスト済みであれば、読み取り専用の[ホスト統計](/docs/xoa-hl/hosts-pools/#host-statistics)の最新の値も確認します。ブラウザーでログインできても、アプライアンスがホストに届くことの証明にはなりません。 |
| ブラウザー → XOA-HL 経由のコンソール → VM のホスト | コンソールが必要なら、[コンソールのガイド](/docs/xoa-hl/vm-operations/#vm-console)に従って、稼働中のテスト VM を 1 台開きます。ブラウザーでの結果と、VM が動いているホストを記録します。コンソールは、アプライアンスからそのホストへの別の WebSocket 接続を使います。ホストの一覧が表示できても、この接続の証明にはなりません。 |
| XOA-HL → バックアップ先と更新 | 各バックアップ先と、アプライアンスが使うパッケージ、DNS、時刻のサービスを、担当者とともに一覧にします。バックアップ先は[バックアップの手順](/docs/xoa-hl/backup-restore/)で、パッケージへのアクセスは[アプライアンスの更新ガイド](/docs/xoa-hl/maintenance/)でテストします。管理画面にログインできても、これらの経路の証明にはなりません。 |

リリースを特定した検証用のアプライアンスで、次のように行います。

1. 必要な経路ごとに、送信元のクライアント、宛先の名前またはアドレス、サービス、結果、時刻を記録します。
2. 許可されていないテスト用クライアントが管理画面のログインページに届かないことを、ネットワーク担当者に確認してもらいます。許可されたテストと、別のログを使います。ping が遮断されても、HTTPS の隔離も、管理が引き続き動くことも証明できません。
3. コンソールへのアクセスは、制限する予定の経路の外に置きます。
4. ポリシーの変更が別途承認された場合は、担当者が管理する規則を 1 つずつ変更します。変更のたびに、同じ許可と拒否のテストを繰り返します。
5. 作業時間を終える前に、ログイン、ホストの一覧、コンソール、バックアップを確認します。

**確認:** 必要な経路はすべて引き続き使え、許可されていないクライアントはログインページに届きません。

必要な経路が失敗した場合や、アクセスを失った場合は、作業を止めます。別のコンソールから、ネットワーク担当者が文書化した切り戻しの手順を使います。近道として、XOA の接続を削除したり、ホストの管理 PIF を変更したりしないでください。実際の待ち受け、クライアントの分離、プロキシや NAT の経路、ホストとバックアップ先のポート、切り戻しはここでは扱いません。このページだけを根拠に本番用の許可リストを作らないでください。

## HTTPS 証明書を交換する前に確認する {#tls-certificate-preflight}

この確認はファイルと接続を読み取るだけで、何も更新しません。同梱の設定は、インストール時に `/opt/xo/xoahl.crt` と `/opt/xo/xoahl.key` を使うポート `443` の HTTPS の待ち受けを書き込みます。その後の変更やリバースプロキシによって、TLS が別の場所で提供されることがあります。

パッケージは共通の秘密鍵を配布していません。インストール時に、どちらかのファイルか `/var/lib/xoa-hl/tls-generated` マーカーがないと、自己署名の `CN=xoa.local` のペアを生成します。後のパッケージ更新でも同じようにペアが再生成されることがあり、その後 `xo-server` が再起動されます（`%posttrans`）。更新を計画する前に、実際のパスとパッケージの状態を記録します。証明書を入れ替える手段として、マーカーを削除しないでください。

1. 別のコンソールと、ローカルの管理者アカウントが使えることを確認します。
2. インストール済みのイメージとパッケージ、有効な `http.listen` の値、マージされる設定の上書きを、非公開で記録します。`systemctl cat xo-server` を実行して、サービスの上書きを確認します。
3. アプライアンスの前にリバースプロキシ、ロードバランサー、その他の TLS の終端があるかを記録します。`http.publicUrl` はアドレスを通知するだけで、待ち受けや、ブラウザーが受け取る証明書を示すものではありません。待ち受けが複数ある場合や、ポート `443` に想定外のものがある場合は、作業を止めます。
4. **アプライアンス上で**、設定されている証明書、鍵、マーカーのメタデータだけを読み取ります。同梱のパスでは、次の読み取り専用のコマンドで、秘密鍵の中身を表示せずに、ファイルの権限と公開証明書の項目を表示できます。

   ```bash
   stat -c '%n %U:%G %a %s %y' /opt/xo/xoahl.crt /opt/xo/xoahl.key /var/lib/xoa-hl/tls-generated
   openssl x509 -in /opt/xo/xoahl.crt -noout -subject -issuer -dates -serial -fingerprint -sha256 -ext subjectAltName
   ```

   設定で別のファイルを使っている場合は、**実際に設定されている**ペアを使います。ファイルやマーカーがない場合は、更新や再起動の前に作業を止め、原因を調べます。新しいペアを生成しないでください。秘密鍵と設定全体を、スクリーンショット、ログ、Issue に含めないでください。
5. **許可されたクライアント**から、実際の HTTPS のアドレスを開き、新しいブラウザーのセッションでログインし直します。
6. OpenSSL が使え、担当者から信頼チェーンを受け取っている場合は、実際の DNS 名とポートで `openssl s_client -connect <name>:<port> -servername <name> -verify_hostname <name> -verify_return_error -brief </dev/null` を実行します。私設 CA の場合は、担当者が承認した `-CAfile <ca-path>` を追加します。これらのオプションを使う前に、インストールされている OpenSSL のバージョンを確認します。
7. 証明書のフィンガープリント、名前、チェーン、有効期限を、想定した接続先と比べます。

**確認:** ブラウザーが受け取る証明書と、その元のファイルを記録できています。インストール時に作成された自己署名証明書は、信頼の検証に失敗することがあります。その結果を記録しますが、検証を無効にしたり、信頼済みとして扱ったりしないでください。プロキシが TLS を扱う場合、その証明書はアプライアンスのファイルと異なることがあります。両方を別々に記録します。

**交換を計画する前に**、証明書とアプライアンスの担当者と次のことを合意します。

- 新しい証明書のチェーン、対応する秘密鍵、対象の名前、有効期限。
- 安全な保管場所、ファイルの所有者と権限。
- 別の復旧用コンソールと、現在の**証明書のペア、マーカー、運用者ファイル**の非公開のバックアップ。
- ジョブが終わった後の保守時間、変更する待ち受けまたはプロキシ、テスト済みの再起動と切り戻しの手順。
- 交換後に行うテスト。信頼された新しいブラウザーでのログイン、正しいフィンガープリント、ローカルの管理者が使えること、ホストとプールの一覧、コンソール。

設定ファイルが正しいこと、ファイルがあること、再起動が成功したことだけでは、クライアントが証明書を信頼することも、正しい証明書であることも証明できません。証明書の更新はここでは扱いません。この確認を本番の交換手順として使わないでください。

## 構文を確認してサービスを再起動する {#apply-change}

**始める前に**

- 元の運用者ファイルの非公開のコピーをアプライアンスの外に保管し、その権限を記録します。
- コンソールにアクセスできるようにしておきます。
- バックアップ、復元、管理のジョブが終わるまで待ちます。

ファイルを編集したら、アプライアンス内で root として次の確認を実行します。

```bash
cd /opt/xo/packages/xo-server
node --input-type=module -e "import fs from 'node:fs'; import TOML from '@iarna/toml'; TOML.parse(fs.readFileSync('/root/.config/xo-server/config.toml', 'utf8')); console.log('TOML syntax OK');"
```

`TOML syntax OK` は、構文が正しいことだけを示します。ファイルの権限、TLS の信頼、マージ後の値、到達性は確認しません。再起動の前に、エラーをすべて直します。

合意した保守時間に、サービスを再起動し、その状態と最近のログを確認します。

```bash
systemctl restart xo-server
systemctl status xo-server --no-pager
journalctl -u xo-server --since '10 minutes ago' --no-pager
```

再起動すると、管理画面の接続が切れます。想定したアドレスに接続し直します。

**確認:** ログインでき、ホストの一覧がそろっています。XO は一定の間隔で各プールに URL を書き込むため、次に書き込まれた後で、プールの検出を確認します。

サービスが起動しない場合は、コンソールから保存しておいた運用者ファイルを戻し、構文をもう一度確認して、1 回だけ再起動します。結果がはっきりしない場合は[トラブルシューティング](/docs/xoa-hl/troubleshooting/)を参照してください。ログを共有する前に、秘密の情報を取り除きます。

{{< details title="出典" closed="true" >}}
- **設定ファイルとサービス**：[初期設定のスクリプト](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh)、[パッケージのインストールと更新](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec)、[systemd サービス](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xo-server.service)、[設定の読み込み](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs)、[既定値](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml)、[コメント付きの例](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/sample.config.toml)、[プールの検出](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs)。
- **管理用のアクセス経路**：[サーバー接続](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs)、[VM のホストへのコンソールプロキシ](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs)。
- **HTTPS 証明書**：[生成されるペア、マーカー、更新後の再起動](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec)、[初期の待ち受け](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh)、[有効な待ち受けの設定](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs)、[OpenSSL x509 のマニュアル](https://docs.openssl.org/3.0/man1/openssl-x509/)、[OpenSSL s_client のマニュアル](https://docs.openssl.org/3.0/man1/openssl-s_client/)。
{{< /details >}}
