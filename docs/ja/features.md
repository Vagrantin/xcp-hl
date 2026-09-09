---
layout: default
title: 機能
parent: 日本語
nav_order: 2
lang: ja
---

# 機能 — v8.3-ce9
{: .no_toc }

現在のリリース · 2026 年 6 月 · XCP-ng 8.3 ベース
{: .fs-6 .fw-300 }

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## ベースになるプラットフォーム

XCP-hl は XCP-ng 8.3 の **ISO をそのまま置き換えられる**ものです。
アップストリームの機能はすべて引き継いでおり、違いは XO Lite、XOA、
そして展開のワークフローにあります。インストーラーより下の層は公式リリースと
まったく同じように動きます。

| 項目 | 値 |
|---|---|
| ベースのリリース | XCP-ng 8.3（アップストリームの最新のポイントリリース） |
| ハイパーバイザー | Xen 4.17 |
| Dom0 のカーネル | Linux 4.19（XCP-ng のカーネル） |
| 管理 API | XAPI（Xen API） |
| 既定のネットワーク | Open vSwitch（OVS） |
| インストーラー | XCP-ng のテキストインストーラー |

---

## 独自の変更点

### 手を入れた XO Lite

XO Lite は、すべての XCP-ng ホストに同梱される軽量な単一ページの管理画面
です。HomeLab Edition では、RPM をビルドする前にアップストリームの
`DeployXoaView.vue` コンポーネントを**ソースコードの段階で**書き換えるため、
パッチは最小限で済みます。

アップストリームの xo-lite のバージョンは、`xolite-ce` の `UPSTREAM_TAG`
ファイルで固定しています（現在は `xo-lite-v0.21.0`。正常に動くことが
分かっている最後のリリースです）。この値を意図的に上げたときだけ変わります。

**パッチによる変更点：**

- **「Deploy XOA」**ボタンが、新しい XOA の展開画面を指すようになります。
- XOA-HL イメージ。
- Vates 公式のイメージ。
- Ronivay 氏が提供するイメージ。
- 独自の XOA イメージを展開するための入力欄。

XO Lite のそれ以外の部分（VM の管理、コンソールへの接続、SR の閲覧、
ホストのメトリクス）はそのままです。

### xoa-proxy — ローカルでの XVA 配信

このために作られた **Rust 製の HTTP サーバー**（`xoa-proxy`）が ISO に同梱
され、ホスト上で動きます。次のことを行います。

- コミュニティの XOA イメージを配信します（gzip で圧縮された形式にも対応）。
- HTTP と HTTPS の両方に対応します（自己署名証明書を含む）。

### ホームラボ向けの XOA イメージ

プロキシが展開する XOA イメージは、XOA-HL
（[Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl)）を組み込んで
ビルドしています。

### Ronivay 氏の XOA イメージ

プロキシが展開する XOA イメージは、セルフホストの Xen Orchestra 向けに
よく保守されているコミュニティのインストーラー
[ronivay/XenOrchestraInstallerUpdater](https://github.com/ronivay/XenOrchestraInstallerUpdater)
からビルドしています。

| 項目 | 値 |
|---|---|
| XO のバージョン | XO の最新の安定版に追従 |
| 既定の管理ユーザー | `admin@admin.net` |
| 既定の管理パスワード | `admin` |
| SSH ユーザー | `xo` |
| SSH パスワード | `xopass` |

{: .warning }
最初のログインのあと、**既定のパスワードをすぐに変更してください**。

### Vates の XOA イメージ

XCP-ng の複数ホスト管理のために Vates が提供する公式イメージです。この場合、
資格情報は展開の段階で指定できます。

---

## GPG 署名

XCP-hl のすべての成果物は **XCP-ng HomeLab Edition の GPG 鍵**で署名して
います。

### 鍵の構成

鍵は**オフラインのマスターキーとサブキー**という形をとっています。

| 役割 | 説明 |
|---|---|
| マスターキー | 証明のみに使用。オフラインで保管し、署名には使いません |
| RPM 署名用サブキー | コミュニティのすべての RPM パッケージ（`xo-lite-community`、`xoa-proxy`）に署名します |
| ISO 署名用サブキー | ISO のチェックサムファイル（`xcp-ng-8.3-ceN.iso.sha256.asc`）に署名します |

| 項目 | 値 |
|---|---|
| マスターキーのフィンガープリント | `2F59 1DB9 D2C1 28C4 C3D9  63F4 6DA0 0DCA 5BBA 215A` |
| 公開先 | [keys.openpgp.org](https://keys.openpgp.org/search?q=xcp-ng-ce.lid530%40passmail.com) |
| メールアドレス | `xcp-ng-ce.lid530@passmail.com` |
| 公開鍵のファイル | `xcp-ng-ce-public.asc`（各リリースに添付） |

公開鍵のファイルには 2 つの署名用サブキーが両方とも入っています。一度
インポートすれば、RPM と ISO のチェックサムのどちらも検証できます。

---

## 使える機能のまとめ

### ハイパーバイザーとホストの管理

- **XCP-ng 8.3 の全機能** — すべての VM の種類（HVM、PV、PVH）、
  ライブマイグレーション（XenMotion）、Storage XenMotion。
- **ストレージリポジトリ（SR）** — ローカル LVM、NFS、iSCSI（LVM と EXT）、
  HBA/FC、XOSTOR（ハイパーコンバージド）、SMB、ISO SR。
- **すぐ使える ISO ライブラリー**：インストール時に専用の 20 GB
  パーティションを確保し、初回起動時に ISO SR として登録します。ストレージを
  手作業で設定しなくても、インストーラーのイメージをアップロードして VM を
  作れます。[ISO ストレージ](#iso-storage)を参照してください。
- **GPU / vGPU** — PCI パススルーと NVIDIA GRID vGPU に対応。
- **HA** — プールの高可用性。ホストの障害時に VM を自動で再起動します。

### ISO ストレージ
{: #iso-storage }

XCP-ng は初期状態ではインストーラーの ISO を置く場所がありません。ISO SR は
存在せず、作るにはパスを決め、ディレクトリーを作り、`xe sr-create` を手で
実行する必要があります。XCP-HL はこれを代わりに行います。

**用意されるもの。** 新規インストール時に 20 GB のパーティションを確保し、
`xcphl-iso` というラベルで ext4 にフォーマットして
`/var/opt/xen/xcp-hl-iso` にマウントし、**XCP-HL ISO library** という名前の
ISO SR として XAPI に登録します。Xen Orchestra からすぐ見えるので、ISO を
アップロードし（*Import → Disk* で ISO SR を選択）、追加の設定なしにそこから
VM を起動できます。

**必要なディスク容量。** XCP-HL は **100 GB** のディスクを求めます。内訳は
おおよそ次のとおりです。

| 用途 | 容量 |
|---|---|
| システム用パーティション（root、バックアップ、boot、ログ、swap） | 約 41.5 GB |
| ISO ライブラリー | 20 GB |
| ローカルストレージ SR（VM のディスク） | 約 38.5 GB |

100 GB に満たない場合は、VM のストレージを数 GB まで削るのではなく、
確保そのものを行いません。インストールは問題なく完了し、ディスクの構成は
XCP-ng 標準とまったく同じになります。ISO ライブラリーが作られないだけで、
その理由は `/var/log/installer` に記録されます。

**適用される範囲。** このパーティションはインストーラーが作るため、XCP-HL の
ISO からインストールしたホストにだけ存在します。XCP-ng 標準からインストール
したあとに XCP-HL のリポジトリを追加したホストは、既存のディスク構成が
そのまま残ります。稼働中のマシンのパーティションを切り直すことはありません。
そうしたホストでも、これまでどおり手作業で ISO SR を作れます。

既存の XCP-HL ホストをアップグレードしてもパーティションは残ります。
アップグレードでパーティションを切り直すことはなく、ISO SR はファイルシステム
のラベルから再び認識されます。

**既知の注意点。** SR の PBD を切り離して、再起動*せずに*つなぎ直すと、
XAPI は接続し直しますがファイルシステムはマウントされないままになります。
そのため、次に再起動してマウントされるまでライブラリーは空に見えます。
これは XCP-ng がローカル（`legacy_mode`）の ISO SR を扱う仕組みによるもので、
標準の XCP-ng Tools の SR でも同じことが起こります。再起動するか
`mount /var/opt/xen/xcp-hl-iso` を実行すれば元に戻ります。

### XO Lite（ブラウザーからの簡易管理）

インストール直後から `http://<ホストの IP アドレス>` で使えます。

- プールとホストの概要（CPU、メモリー、ストレージをひと目で確認）。
- VM の一覧：起動、停止、再起動、コンソールへの接続。
- SR とネットワークの基本的な確認。
- **ホームラボ向けの展開フロー**：XOA イメージをローカルに置いていれば、
  外部への接続なしでワンクリックで XOA を展開できます。

### Xen Orchestra（XOA の展開後）

XO Lite で「Deploy XOA」を実行すると、Xen Orchestra を一式使えるように
なります。

- **VM のライフサイクル管理** — 作成、クローン、マイグレーション、
  スナップショット。
- **エージェントレスのバックアップ** — フル、差分、継続レプリケーション、
  災害復旧。
- **スケジュール実行** — cron によるバックアップジョブと、設定可能な保持期間。
- **RBAC / 権限委譲** — ロール（Admin、Operator、Viewer）とリソースセット。
- **監視とアラート** — VM ごと・ホストごとのメトリクスとしきい値アラート。
- **REST API + xo-cli** — すべてのリソースにスクリプトから接続。
- **プールのローリングアップグレード** — XO から無停止でアップグレード。
- **XOSTOR** — XO の画面からハイパーコンバージドストレージを構成
  （3 ノード以上）。

{: .warning }
**一部の機能には Vates が配布するライセンスが必要です。**

---

## このリリースの既知の制限事項

| 制限 | 状況 |
|---|---|
| Xolite-ce — Deploy ボタンが常に押せる | [issue#4](https://github.com/Vagrantin/xolite-ce/issues/4) — 展開に成功したらボタンを「Access XOA」に切り替える |
| Xoa-proxy — ログが UTC のまま | [issue#3](https://github.com/Vagrantin/xoa-proxy/issues/3) — 調査中 |
| Xoa-proxy — crate の数を減らす | [issue#2](https://github.com/Vagrantin/xoa-proxy/issues/2) — 調査中 |
| Xoa-proxy — メモリー使用量を減らす | [issue#1](https://github.com/Vagrantin/xoa-proxy/issues/1) — xoa-proxy は Dom0 で動くため、メモリーへの影響を抑える必要があります |
| Xcp-hl — リリース公開時のバージョン付け | [issue#4](https://github.com/Vagrantin/xcp-hl/issues/4) — 成果物ごとにバージョンの付け方がそろっていません |

---

## 変更履歴

### v8.3-ce9（2026 年 6 月）
- xolite-ce `v0.21.0-ce6` — `UPSTREAM_TAG` ファイルで、アップストリームの
  xo-lite を `0.21.0` に固定しました（正常に動くことが分かっている最後の
  リリース。`0.22.0` と `0.23.0` ではビルドが壊れました）。
- xoa-proxy `v0.1.1.x` — RPM のバージョン付けを簡素化し（リリースの接尾辞
  `.static`）、GitHub のリリースノートを自動生成・分類するようにしました。
- 成果物の名前を統一：`xcp-ng-8.3-ceN.iso` + `.iso.sha256` +
  `.iso.sha256.asc` を `xcp-ng-ce-iso` の GitHub リリースとして公開します。

### v8.3-ce alpha2（2026 年 5 月）
- 最初の一般公開。
- 初めて実用になるリリース。
- Vates、Ronivay、または任意の URL から展開する基本的な機能を提供します。
- **GPG**：オフラインのマスターキーと、RPM 用・ISO 用の署名サブキー。
  公開鍵を keys.openpgp.org に登録しました。

### v8.3-ce（2026 年 4 月）
- XO Lite にパッチ：コミュニティ版の展開先と、読み取り専用の資格情報欄。
- Rust 製サーバー `xoa-proxy` を同梱：HTTP/HTTPS、gzip のストリーム配信。
- アップストリームの XCP-ng 8.3 に、コミュニティの RPM リポジトリを重ねて
  ISO を組み立て。
- GPG 鍵の基盤（4096 ビット RSA、単一の鍵 `RPM-GPG-KEY-xcp-ng-ce`）。
- GitHub Actions の CI/CD パイプライン：RPM のビルド → ISO のビルド →
  GitHub リリース。
