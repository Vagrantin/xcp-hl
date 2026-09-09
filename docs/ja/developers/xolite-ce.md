---
layout: default
title: xolite-ce
parent: 開発者向け
grand_parent: 日本語
nav_order: 2
lang: ja
---

# xolite-ce
{: .no_toc }

XO Lite 向けのコミュニティパッチと、RPM のビルドのパイプラインです。
{: .fs-6 .fw-300 }

**リポジトリ：** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· 言語：TypeScript / Vue 3（パッチ）· RPM の spec · ライセンス：AGPL-3.0

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## XO Lite とは

XO Lite は、すべての XCP-ng ホストに同梱される軽量な単一ページの管理
アプリケーションです。ホストから直接配信され、ブラウザーの中だけで動きます。
実装は Vue 3 / TypeScript / Vite の SPA です。

標準の XCP-ng ホストでは、XO Lite に **「Deploy XOA」** の画面
（`DeployXoaView.vue`）があり、公式の Xen Orchestra のイメージを
ダウンロードして取り込みます。XCP-hl はこの動作を置き換え、展開したい
XOA イメージを選べるようにします。

---

## パッチの内容

コミュニティによる変更は、**`git format-patch`** の 1 ファイルだけです。

```
xolite-ce/
└── patches/
    └── community-xoa-deploy.patch
```

このパッチが変更するのは `DeployXoaView.vue` だけです。内容は次のとおりです。

  - 3 つの選択肢を持つ **「XOA Image URL」のドロップダウン**：
  - **ホームラボ向けの XOA イメージ** *（既定）* — `xoa-proxy` を経由して
    ストリーム配信と gzip の展開を行います。資格情報はあらかじめ入力済みです
  - **Vates のイメージ** — Vates が公開する公式の URL を直接使います。
    XAPI は `xoa-proxy` を経由せずに取り込みます
  - **任意の URL** — `xoa-proxy` を経由します。資格情報の欄は空で、
    利用者が入力します

- **「Verify if SSL certificate is valid」**のトグルを追加します。これを
  無効にすると、上流のイメージサーバーの自己署名証明書を `xoa-proxy` が
  受け入れます。

- 資格情報の欄は、**Ronivay 氏のイメージを選んだときは読み取り専用**になり
  （既定値が入力済み）、**それ以外の選択肢では編集できます**。

---

## ビルドのパイプライン

### 全体の流れ

```
1. アップストリームの XCP-ng の ISO にある RPM から XO_VERSION を読み取る
2. 対応するリリースタグで vatesfr/xen-orchestra をクローンする
3. patches/community-xoa-deploy.patch を適用する
4. Yarn（Corepack）で依存を導入する
5. XO Lite をビルドする：yarn build:xo-lite
6. RPM 用のソースのアーカイブを作る
7. rpmbuild -ba SPECS/xo-lite-community.spec
8. RPM 署名用サブキーで rpmsign（GPG_PRIVATE_KEY + GPG_PASSPHRASE）
9. RPM と xcp-ng-ce-public.asc を GitHub リリースの成果物として公開する
```

### バージョンの判定

対象となる XO Lite のバージョンは、コードに直接書くのではなく、
アップストリームの XCP-ng の ISO にすでにある RPM から読み取ります。

```bash
XO_VERSION=$(rpm -qp --qf '%{VERSION}' xo-lite-*.rpm)
```

こうすることで、コミュニティ版の RPM は常にアップストリームのバージョンと
一致し、そのまま置き換えられるようになります。

### アーカイブの構成

`rpmbuild` に渡すソースのアーカイブは、次のような構成です。

```
xo-lite-{VERSION}/
├── dist/               ← Vite でビルドした成果物
├── CHANGELOG.md
├── LICENSE
└── xolite.html         ← scripts/xolite-loader.html から名前を変更
```

`xolite.html` というファイル名は必須です。これは XCP-ng ホストが配信し、
ブラウザーで XO Lite を読み込むための入口だからです。

### RPM の spec

`SPECS/xo-lite-community.spec` では次のように定義しています。

- `Name: xo-lite-community`
- `Version: %{XO_VERSION}`（ビルド時に埋め込み）
- `Provides: xo-lite`（アップストリームのパッケージへの依存を満たすため）
- `Conflicts: xo-lite`（アップストリームの RPM との同時インストールを防ぐ）
- ファイルの一覧：`dist/` の中身と `xolite.html`

---

## ローカルでの開発

### 事前に必要なもの

- Node.js 20 以上と Yarn（`corepack enable` で有効にします）
- `rpmbuild`（RHEL/CentOS/Fedora では `rpm-build` パッケージ）
- `rpmsign`（`rpm-sign` パッケージ）
- コミュニティの GPG 公開鍵を自分のキーリングにインポートしておくこと

### 手順

```bash
# 1. リポジトリをクローンする
git clone https://github.com/Vagrantin/xolite-ce.git
cd xolite-ce

# 2. 対象のタグでアップストリームの xen-orchestra をクローンする
XO_VERSION=<バージョン>
git clone --depth 1 --branch v${XO_VERSION} \
    https://github.com/vatesfr/xen-orchestra.git upstream

# 3. コミュニティのパッチを適用する
cd upstream
git am ../patches/community-xoa-deploy.patch
cd ..

# 4. 依存を導入する
cd upstream
corepack enable
yarn install
cd ..

# 5. XO Lite をビルドする
cd upstream
yarn build:xo-lite
cd ..

# 6. 画面を確認する
scp -r lite/dist/ xcp-ng-host:/opt/xensource/www/
```

### 新しいアップストリームのバージョン向けにパッチを更新する

```bash
# 新しくクローンしたアップストリームで手作業により変更し、
# 新しいパッチを生成します：
git diff HEAD > ../patches/community-xoa-deploy.patch
# あるいは、きれいなコミットとして format-patch を使います：
git format-patch HEAD~1 -o ../patches/
```

---

## GPG 署名

`xo-lite-community` の RPM は、XCP-ng Community Edition の鍵ペアの
**RPM 署名用サブキー**で署名しています。同じサブキーは `xoa-proxy` の RPM の
署名にも使っており、コミュニティのすべての RPM で 1 つのサブキーを共有して
います。

公開鍵（`xcp-ng-ce-public.asc`）は、どのリリースにも同じものが添付されて
います。一度インポートすれば、コミュニティのどの RPM でも検証できます。

ローカルで RPM を検証するには次のようにします。

```bash
# 方法 1 — 鍵サーバーから取得する
gpg --keyserver keys.openpgp.org --recv-keys 2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A

# 方法 2 — リリースページからインポートする
gpg --import xcp-ng-ce-public.asc

# RPM の署名を確認する
rpm --checksig xo-lite-community-*.rpm
```

---

## CI のワークフロー（GitHub Actions）

ワークフローは `main` への push で実行されます。

主なステップは次のとおりです。

```yaml
- name: Detect XO version
  run: echo "XO_VERSION=$(rpm -qp --qf '%{VERSION}' ...)" >> $GITHUB_ENV

- name: Clone upstream at tag
  run: git clone --depth 1 --branch v${{ env.XO_VERSION }} ...

- name: Apply patch
  run: git am patches/community-xoa-deploy.patch

- name: Build XO Lite
  run: |
    corepack enable
    yarn install
    yarn build:xo-lite

- name: Build RPM
  run: rpmbuild -ba SPECS/xo-lite-community.spec

- name: Sign RPM
  run: |
    echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --import
    echo "${{ secrets.GPG_PASSPHRASE }}" | gpg --passphrase-fd 0 --batch \
      --pinentry-mode loopback --yes --armor
    rpm --addsign RPMS/x86_64/xo-lite-community-*.rpm

- name: Publish release
  uses: softprops/action-gh-release@v1
  with:
    files: |
      RPMS/x86_64/xo-lite-community-*.rpm
      xcp-ng-ce-public.asc
```

---

## 開発に参加する

1. [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce) を
   フォークします。
2. 画面のパッチを変更する場合は
   `patches/community-xoa-deploy.patch` を編集します。
3. パッケージングを変更する場合は
   `SPECS/xo-lite-community.spec` を編集します。
4. 上のローカルでの開発手順を実行して、変更を確認します。
5. `main` に対してプルリクエストを作ります。
