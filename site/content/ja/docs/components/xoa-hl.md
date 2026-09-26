---
title: xoa-hl
weight: 4
translationKey: xoa-hl
aliases: ["/ja/developers/xoa-hl.html"]
---

XOA-hl のソフトウェアのビルドです。Xen Orchestra にホームラボ向けの変更を
加え、RPM としてパッケージ化します。
{class="lead"}

**リポジトリ：** [Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl)
· 言語：Bash / RPM の spec · ライセンス：AGPL-3.0

## 目的

このリポジトリは **Xen Orchestra HomeLab Edition**（XOA-hl）をビルドします。
オープンソースの
[`xen-orchestra`](https://github.com/vatesfr/xen-orchestra) のサーバーと
XO 5 の Web 画面を、固定したアップストリームのコミットから取得し、
ホームラボ向けに手を入れて、XCP-ng 用にパッケージ化したものです。ビルドの
たびに、1 つの成果物を GitHub のリリースとして公開します。

| 成果物 | 内容 |
|---|---|
| `xoa-hl-<version>-<N>.g<commit>.xcpng8.3.el9.x86_64.rpm` | ビルド済みの Xen Orchestra（約 70 MiB）、その systemd ユニット、アプライアンス自身をアップデートするための仕組み |

この RPM を [`build-xoa-hl`](/docs/components/build-xoa-hl) が XOA の VM アプライアンス
に入れます。最新の 5 つのリリースは署名付きの yum リポジトリとしても再公開
され、稼働中のアプライアンスはそこからアップデートを受け取ります
（[アップデート](/docs/guides/updates)を参照）。

---

## リポジトリの構成

```
xoa-hl/
├── UPSTREAM_XO                 ← 固定したアップストリームの xen-orchestra（コミット + バージョン）
├── container/
│   └── Containerfile           ← AlmaLinux 9 のビルド用イメージ（Node 24、yarn、rpm 関連ツール）
├── scripts/
│   ├── build-xo.sh             ← ビルド本体：取得 + パッチ + yarn build + tar
│   └── validate-patches.sh     ← patches/ を metadata.toml と照合する
├── patches/
│   ├── metadata.toml           ← 各パッチの目的と、変更する対象のファイル
│   ├── menu-hide-items.patch   ← Vates のサブスクリプションが必要なメニュー項目を隠す
│   ├── xcp-hl-updates.patch    ← XCP-hl のリポジトリを Patches タブに加える
│   └── xoa-hl-update-api.patch ← アプライアンス独自の「XOA-HL Updates」設定ページ
├── SPECS/
│   └── xoa-hl.spec             ← RPM：/opt/xo のビルド済み XO + systemd ユニット
├── SOURCES/                    ← systemd ユニット、アップデート用スクリプト、sudoers の規則、.repo ファイル
├── pages/                      ← 公開する yum リポジトリのインデックスページと .repo ファイル
└── .github/workflows/
    ├── build-xoa.yml           ← CI：ビルド + RPM + GitHub リリース
    └── pages-repo.yml          ← 最近の RPM を署名付きの yum リポジトリとして再公開
```

---

## バージョンの固定

ビルドの対象は固定したアップストリームのコミットで、リポジトリの直下にある
`UPSTREAM_XO` ファイルで指定します。

```bash
XO_COMMIT=e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c
XO_VERSION=5.113.2
```

バージョン文字列は、この 2 つを組み合わせたものです。
`<XO_VERSION>_<短い SHA>` の形で、たとえば `5.113.2_e281c536` になります。
`build-xo.sh` がこれを `out/VERSION` に書き出し、CI が RPM のバージョンとして
使います。リリースは `v<version>-ce<N>` というタグ（たとえば
`v5.113.2_e281c536-ce17`）を push して作ります。`N` が RPM のリリース番号に
なるので、ビルドごとに別のパッケージになり、`dnf` でアップデートできます。

{{< callout type="info" >}}
アップストリームの更新は、`UPSTREAM_XO` を書き換えて**意図的に**行います。
自動では行いません。`5.113.2` は、アップストリームが XO 6 に移る前の、
XO 5.x の最後のリリースです。
{{< /callout >}}

---

## ビルドの流れ（scripts/build-xo.sh）

ビルドは AlmaLinux 9 のコンテナの中で `/build` を対象に動きます。

1. **固定した SHA で浅く取得する。** `git init` +
   `git fetch --depth 1 origin $XO_COMMIT` + `checkout FETCH_HEAD` の順です。
   `--depth 1` で SHA を直接指定することで、約 1 GB の履歴全体を取得せずに
   済み、再現性も保てます。
2. **パッチを適用する。** `patches/*.patch` のそれぞれに
   `patches/metadata.toml` の項目があるか（その逆も）を確認してから、
   `git apply --verbose` で 1 つずつ適用します。パッチは 3 つです。
   - `menu-hide-items`：Vates のサブスクリプションがないと使えない
     メニュー項目を隠します。
   - `xcp-hl-updates`：Xen Orchestra がホストの `updater.py` プラグインに
     送る問い合わせに XCP-hl のリポジトリを加え、XCP-hl のパッケージが
     Patches タブに出るようにします。
   - `xoa-hl-update-api`：アプライアンス独自のアップデート用 API と、
     **XOA-HL Updates** の設定ページを加えます。
3. **`packages/xo-server/xoahl.config.toml` を書き出す。** これは RPM が
   あとで利用者の設定として入れる実行時の設定です。443 番ポートでの HTTPS、
   `/opt/xo/xoahl.crt` と `/opt/xo/xoahl.key`、Redis は
   `redis://127.0.0.1:6379/0` を指定します。
4. **自己署名の TLS 証明書を生成する。** `openssl req -x509`
   （RSA 4096、10 年、CN は `xoa.local`）で `xoahl.key`（モード 600）と
   `xoahl.crt`（モード 644）を作ります。
5. **導入とビルド。** `yarn` のあと、すべての workspace（サーバーと XO 5 の
   Web 画面）で `yarn build` を実行します。
6. **不要物の削除。** `.git`、`.github`、`.changesets`、`docs`、
   `packages/xo-server-test*`、`packages/xo-server-cloud` を削除します。
7. **devDependencies の除去。** `yarn workspaces focus --production`
   （代替手段は `yarn install --production`）を使い、workspace の
   シンボリックリンクは保ちます。
8. **パッケージ化。** 不要物を削除したモノレポ全体を
   `tar czf out/xoa-hl-<version>.tar.gz` でまとめます（`**/*.map` は除外）。
   このアーカイブは RPM のビルドの入力に使うだけで、公開はしません。

---

## RPM（SPECS/xoa-hl.spec）

RPM には、ビルド済みの Xen Orchestra そのもの（約 70 MiB）が入っています。
`node_modules` にネイティブのアドオンが含まれるため、`noarch` ではなく
`x86_64` です。インストールされるものは次のとおりです。

| パス | 内容 |
|---|---|
| `/opt/xo` | ビルド済みの xen-orchestra 一式と、TLS の鍵と証明書 `xoahl.key` / `xoahl.crt` |
| `/usr/local/bin/xo-cli` | `PATH` から使える `xo-cli` |
| `/usr/lib/systemd/system/xo-server.service` | `/opt/xo` から xo-server を起動する |
| `/usr/lib/systemd/system/xoa-hl-check-update.service` と `xoa-hl-update.service` | アプライアンスのアップデートを確認し、適用する |
| `/usr/libexec/xoa-hl/` | この 2 つのユニットが実行するスクリプト |
| `/etc/yum.repos.d/xoa-hl.repo` | アプライアンス専用の yum リポジトリ |
| `/etc/sudoers.d/xoa-hl` | xo-server がアップデート用の 2 つのユニットを起動できるようにする |
| `/var/lib/xoa-hl/` | アップデートのログの書き出し先 |

インストール時に `%post` は次のことを行います。

1. **初回インストール時にだけ利用者の設定を用意します。**
   `/root/.config/xo-server/config.toml` が存在しない場合にかぎり、
   `xoahl.config.toml` をそこにコピーします。アップグレード時には手を
   触れず、運用側の変更をそのまま残します。
2. `systemctl enable redis --now` を実行し、`xo-server` を有効にして
   再起動します。

`%preun` が `xo-server` を停止して無効にするのは、最終的なアンインストールの
ときだけで、アップグレードのときは行いません。上のファイルはすべて
パッケージに属しているので、`dnf remove` ですべて削除されます。`%postun` は
systemd を再読み込みするだけです。

{{< callout type="error" >}}
xo-server は `~/.config/xo-server/config.toml` を読みます（XDG の探索順）。
これはパッケージ側の `config.toml` より優先されます。`%post` での設定の
用意がないと、パッケージの中身にかかわらず HTTPS の待ち受けと Redis の URI
が反映されません。
{{< /callout >}}

実行時の依存：`nodejs >= 24`、`redis`、および Xen Orchestra が
リモートストレージに必要とするマウント関連のツール（`nfs-utils`、
`cifs-utils`、`ntfs-3g`、`lvm2`）です。パッケージには `Epoch: 1` が付いて
いるため、今の番号の付け方より前のビルドよりも新しいものとして扱われます。

---

## ビルド環境

`container/Containerfile` がビルド用のイメージを定義します。AlmaLinux 9 に
gcc/make/git/patch、Python 3、Node.js 24（NodeSource）、yarn、
`rpm-build`/`rpmdevtools` を入れたものです。アーカイブと RPM はどちらも
同じイメージでビルドします。

ビルドは **GitHub Actions でのみ**行い、ローカルでビルドする手順は用意して
いません。CI は Docker でイメージをビルドし、その中で `build-xo.sh` を
実行します。アーカイブと `VERSION` ファイルはランナー上の `out/` にでき、
RPM のビルドに使われます。

---

## CI のワークフロー（GitHub Actions）

`.github/workflows/build-xoa.yml` は、`v*-ce<N>` のタグの push と
`workflow_dispatch` で実行されます。

1. すべてのシェルスクリプトの構文を確認します。`scripts/*.sh` は `bash` で、
   RPM に入る `SOURCES/*.sh` は `sh` で確認します。
2. コンテナのイメージをビルドし、その中で `build-xo.sh` を実行します
   （`patches/`、`scripts/`、`out/`、`UPSTREAM_XO` をマウントします）。
3. `out/VERSION` を読み、タグの `N` を RPM のリリース番号にします。
4. 同じイメージの中で、アーカイブを `SOURCES/` に置いて
   `rpmbuild -bb SPECS/xoa-hl.spec` を実行します。
5. タグと同じ名前の GitHub リリースを作り、RPM を公開します。

ビルドが成功するたびに、`.github/workflows/pages-repo.yml` が最新の 5 つの
リリースの RPM を集め、署名付きのメタデータとともに yum リポジトリとして
`https://vagrantin.github.io/xoa-hl/8.3/x86_64/` に公開します。アプライアンスの
`xoa-hl.repo` が指しているのはこのリポジトリです。

オーケストレーターの `xoa-vm-agent` が作る **VM イメージのリリース**
（タグの接頭辞は `xoa-image-`、成果物は `XOA-hl.xva`）は、イメージを
ビルドするリポジトリである [`build-xoa-hl`](/docs/components/build-xoa-hl) で公開します。
[#22](https://github.com/Vagrantin/xcp-hl/issues/22) を参照してください。

{{< callout type="warning" >}}
移動より前に公開されたイメージのリリースは、ここに残してあります。すでに
配布済みの ISO がそれらを解決し続けられるようにするためです。したがって、
このリポジトリで RPM を探すツールは、今も `xoa-image-*` のタグを飛ばす必要が
あります。
{{< /callout >}}

---

## 他のコンポーネントとの関係

- [`build-xoa-hl`](/docs/components/build-xoa-hl)：この RPM を AlmaLinux 9 の
  アプライアンスに入れ、XVA イメージにまとめます。
- [`xolite-ce`](/docs/components/xolite-ce)：XO Lite の展開ボタンがこのアプライアンスを
  導入します。
- [`xoa-proxy`](/docs/components/xoa-proxy)：アプライアンスのイメージを配信するときに
  使う HTTPS/gzip の橋渡し役です。
- [`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator)
  （`buildorchestration` リポジトリ内）：その `xoa-vm-agent` が
  `build-xoa.yml` を実行し、VM イメージのビルドを始める前に RPM の
  リリースを待ちます。

---

## 開発に参加する

問題の報告や変更の提案は、[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues)で
issue を作ってください。
