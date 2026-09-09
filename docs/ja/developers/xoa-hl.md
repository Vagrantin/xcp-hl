---
layout: default
title: xoa-hl
parent: 開発者向け
grand_parent: 日本語
nav_order: 4
lang: ja
---

# xoa-hl
{: .no_toc }

XOA-HL のソフトウェアのビルドです。Xen Orchestra にホームラボ向けの変更を
加え、アーカイブと軽量な RPM としてパッケージ化します。
{: .fs-6 .fw-300 }

**リポジトリ：** [Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl)
· 言語：Bash / RPM の spec · ライセンス：AGPL-3.0

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 目的

このリポジトリは **Xen Orchestra HomeLab Edition**（XOA-HL）をビルドします。
オープンソースの
[`xen-orchestra`](https://github.com/vatesfr/xen-orchestra) のサーバーと
XO 5 の Web 画面を、固定したアップストリームのコミットから取得し、
ホームラボ向けに手を入れて、XCP-ng 用にパッケージ化したものです。ビルドの
たびに、2 つの成果物を GitHub のリリースとして公開します。

| 成果物 | 内容 |
|---|---|
| `xoa-hl-<version>.tar.gz` | 不要物を削除し、ビルド済みにした xen-orchestra のモノレポ |
| `xoa-hl-<version>-1.*.noarch.rpm` | インストール時にアーカイブを取得する、軽量なインストーラー RPM |

この RPM を [`build-xoa-hl`](build-xoa-hl.html) が XOA の VM アプライアンス
に入れます。

---

## リポジトリの構成

```
xoa-hl/
├── container/
│   └── Containerfile           ← AlmaLinux 9 のビルド用イメージ（Node 24、yarn、rpm 関連ツール）
├── scripts/
│   └── build-xo.sh             ← ビルド本体：取得 + パッチ + yarn build + tar
├── patches/
│   └── menu-hide-items.patch   ← Vates のサブスクリプションが必要なメニュー項目を隠す
├── SPECS/
│   └── xoa-hl.spec             ← 軽量な noarch RPM（%post でアーカイブをダウンロード）
├── SOURCES/
│   └── xo-server.service       ← /opt/xo から xo-server を起動する systemd ユニット
└── .github/workflows/
    └── build-xoa.yml           ← CI：アーカイブ + RPM + GitHub リリース
```

---

## バージョンの固定

ビルドの対象は固定したアップストリームのコミットで、
`scripts/build-xo.sh` の先頭で指定します。

```bash
XO_REPO="https://github.com/vatesfr/xen-orchestra.git"
XO_COMMIT="e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c" # 5.113.2、XO 5.x の最後のリリース
XO_VERSION="5.113.2"
```

リリースのバージョン文字列は、この 2 つを組み合わせたものです。
`<XO_VERSION>_<短い SHA>` の形で、たとえば `5.113.2_e281c536` になります。
これは `out/VERSION` に書き出され、CI がそれを読んでアーカイブ、RPM、
リリースタグ（`v<version>`）に名前を付けます。

{: .note }
アップストリームの更新は、`XO_COMMIT` と `XO_VERSION` を書き換えて
**意図的に**行います。自動では行いません。`5.113.2` は、アップストリームが
XO 6 に移る前の、XO 5.x の最後のリリースです。

---

## ビルドの流れ（scripts/build-xo.sh）

ビルドは AlmaLinux 9 のコンテナの中で `/build` を対象に動きます。

1. **固定した SHA で浅く取得する。** `git init` +
   `git fetch --depth 1 origin $XO_COMMIT` + `checkout FETCH_HEAD` の順です。
   `--depth 1` で SHA を直接指定することで、約 1 GB の履歴全体を取得せずに
   済み、再現性も保てます。
2. **パッチを適用する。** `patches/*.patch` をすべて
   `git apply --verbose` で適用します。現在は
   `menu-hide-items.patch` の 1 つだけで、Vates のサブスクリプションが
   ないと使えないメニュー項目を隠します。
3. **`packages/xo-server/xoahl.config.toml` を書き出す。** これは RPM が
   あとで利用者の設定として入れる実行時の設定です。443 番ポートでの HTTPS、
   `/opt/xo/xoahl.crt` と `/opt/xo/xoahl.key`、Redis は
   `redis://127.0.0.1:6379/0` を指定します。
4. **自己署名の TLS 証明書を生成する。** `openssl req -x509`
   （RSA 4096、10 年、CN は `xoa.local`）で `xoahl.key`（モード 600）と
   `xoahl.crt`（モード 644）を作り、アーカイブに含めます。
5. **導入とビルド。** `yarn` のあと、すべての workspace（サーバーと XO 5 の
   Web 画面）で `yarn build` を実行します。
6. **不要物の削除。** `.git`、`.github`、`.changesets`、`docs`、
   `packages/xo-server-test*`、`packages/xo-server-cloud` を削除します。
7. **devDependencies の除去。** `yarn workspaces focus --production`
   （代替手段は `yarn install --production`）を使い、workspace の
   シンボリックリンクは保ちます。
8. **パッケージ化。** 不要物を削除したモノレポ全体を
   `tar czf out/xoa-hl-<version>.tar.gz` でまとめます（`**/*.map` は除外）。

---

## 軽量な RPM（SPECS/xoa-hl.spec）

RPM は意図的に軽くしてあります。`%files` が配置するのは
`/usr/lib/systemd/system/xo-server.service` **だけ**です。それ以外は
インストール時に `%post` で行います。

1. リリースのアーカイブを
   `https://github.com/Vagrantin/xoa-hl/releases/download/v<version>/…`
   からダウンロードし、`/opt/xo` に展開します。
2. TLS の鍵と証明書を `/opt/xo/xoahl.key` と `/opt/xo/xoahl.crt`
   （設定が参照するパス）へ移動します。
3. **初回インストール時にだけ利用者の設定を用意します。**
   `/root/.config/xo-server/config.toml` が存在しない場合にかぎり、
   `xoahl.config.toml` をそこにコピーします。アップグレード時には手を
   触れず、運用側の変更をそのまま残します。
4. `xo-cli` を `PATH` から使えるようにします（`/usr/local/bin/xo-cli` への
   シンボリックリンク）。
5. `systemctl enable redis --now` を実行し、`xo-server` を有効にして
   起動します。

`%preun` は `xo-server` を停止して無効にし、`%postun` は `xo-cli` の
シンボリックリンクと `/opt/xo` を削除します。

{: .important }
xo-server は `~/.config/xo-server/config.toml` を読みます（XDG の探索順）。
これはパッケージ側の `config.toml` より優先されます。`%post` での設定の
用意がないと、アーカイブの中身にかかわらず HTTPS の待ち受けと Redis の URI
が反映されません。

実行時の依存：`nodejs >= 24`、`redis`、`curl`、および Xen Orchestra が
リモートストレージに必要とするマウント関連のツール（`nfs-utils`、
`cifs-utils`、`ntfs-3g`、`lvm2`）です。

---

## ビルド環境

`container/Containerfile` がビルド用のイメージを定義します。AlmaLinux 9 に
gcc/make/git/patch、Python 3、Node.js 24（NodeSource）、yarn、
`rpm-build`/`rpmdevtools` を入れたものです。アーカイブと RPM はどちらも
同じイメージでビルドします。

ビルドは **GitHub Actions でのみ**行い、ローカルでビルドする手順は用意して
いません。CI は push のたびに Docker でイメージをビルドし、その中で
`build-xo.sh` を実行します。アーカイブと `VERSION` ファイルはランナー上の
`out/` にでき、リリースの成果物として公開されます。

---

## CI のワークフロー（GitHub Actions）

`.github/workflows/build-xoa.yml` は `push` と `workflow_dispatch` で
実行されます。

1. コンテナのイメージをビルドし、その中で `build-xo.sh` を実行します
   （`patches/`、`scripts/`、`out/` をマウントします）。
2. `out/VERSION` を読んでバージョン文字列を決めます。
3. 同じイメージの中で、そのバージョン文字列から `_version` を定義して
   `rpmbuild -bb SPECS/xoa-hl.spec` を実行します。
4. アーカイブと noarch の RPM を含む、`v<version>` というタグの GitHub
   リリースを公開します。

オーケストレーターの `xoa-vm-agent` が作る **VM イメージのリリース**
（タグの接頭辞は `xoa-image-`、成果物は `xoa-almalinux.xva`）は、イメージを
ビルドするリポジトリである [`build-xoa-hl`](build-xoa-hl.html) で公開します。
[#22](https://github.com/Vagrantin/xcp-hl/issues/22) を参照してください。

{: .warning }
移動より前に公開されたイメージのリリースは、ここに残してあります。すでに
配布済みの ISO がそれらを解決し続けられるようにするためです。したがって、
このリポジトリで RPM を探すツールは、今も `xoa-image-*` のタグを飛ばす必要が
あります。現在の `releases/latest` はそのうちの 1 つを指しています。

{: .note }
アーカイブは、RPM をどこかにインストールする**前に**リリースへ公開して
おく必要があります。RPM の `%post` は、そのリリースの URL から
ダウンロードするからです。

---

## 他のコンポーネントとの関係

- [`build-xoa-hl`](build-xoa-hl.html)：この RPM を AlmaLinux 9 の
  アプライアンスに入れ、XVA イメージにまとめます。
- [`xolite-ce`](xolite-ce.html)：XO Lite の展開ボタンがこのアプライアンスを
  導入します。
- [`xoa-proxy`](xoa-proxy.html)：アプライアンスのイメージを配信するときに
  使う HTTPS/gzip の橋渡し役です。
- [`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator)
  （`buildorchestration` リポジトリ内）：その `xoa-vm-agent` が
  `build-xoa.yml` を実行し、VM イメージのビルドを始める前に RPM の
  リリースを待ちます。

---

## 開発に参加する

問題の報告や変更の提案は、
[Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues) で issue を
作ってください。

現在ビルドを担当しているのは、`buildorchestration` リポジトリの
サブディレクトリーであるオーケストレーター
[`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator)
です。その `xoa-vm-agent` が `build-xoa.yml` を実行し、できあがった
リリースを利用します。
