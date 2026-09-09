---
layout: default
title: xcp-ng-ce-iso
parent: 開発者向け
grand_parent: 日本語
nav_order: 3
lang: ja
---

# xcp-ng-ce-iso
{: .no_toc }

ISO を組み立てるパイプラインです。コミュニティがビルドした RPM を受け取り、
起動できる XCP-hl の ISO を公開します。
{: .fs-6 .fw-300 }

**リポジトリ：** [Vagrantin/xcp-ng-ce-iso](https://github.com/Vagrantin/xcp-ng-ce-iso)
· 言語：Bash / YAML · ライセンス：AGPL-3.0

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 目的

このリポジトリは、[`xolite-ce`](xolite-ce.html) が作った署名済みの
`xo-lite-ce` RPM と、[`xoa-proxy`](xoa-proxy.html) が作った署名済みの
`xoa-proxy` RPM を、公式のツールチェーン
[`create-install-image`](https://github.com/xcp-ng/create-install-image)
を使って標準の XCP-ng 8.3 のベースに重ね、できあがった ISO を GitHub の
リリースとして公開します。

---

## ツールチェーン — create-install-image

XCP-ng の公式のインストール用 ISO は、`create-install-image` という
ツールチェーンで組み立てられます。XCP-hl はフォークを持たず、これを
そのまま使います。

このツールチェーンには 2 つのスクリプトがあります。

| スクリプト | 実行ユーザー | 作られるもの |
|---|---|---|
| `create-installimg.sh` | **root** | `install.img`（SquashFS の ramdisk） |
| `create-iso.sh` | 非 root | 最終的な `.iso` ファイル |

この 2 つは、この順番で別々に実行する必要があります。`create-iso.sh` は
MD5 の刻印のために `--sign-script` 引数を受け取ります。

---

## リポジトリの構成

```
xcp-ng-ce-iso/
├── configs/
│   ├── base/
│   │   └── CUSTOMREPO.tmpl     ← コミュニティのリポジトリのテンプレート
│   └── 8.3/                    ← XCP-ng 8.3 の設定（対象）
├── community-repo/
│   └── x86_64/
│       └── repodata/           ← createrepo_c が生成
├── scripts/
│   └── debug/                  ← デバッグ用の補助スクリプト（CI で重ねて使用）
├── Dockerfile.build             ← ビルド環境
└── .github/workflows/
    └── build-iso.yml
```

### CUSTOMREPO.tmpl

コミュニティのリポジトリを定義するテンプレートは、ビルドの前に
`configs/base/` から `configs/8.3/` へコピーしておく必要があります。

```bash
cp configs/base/CUSTOMREPO.tmpl configs/8.3/CUSTOMREPO.tmpl
```

このファイルは、コミュニティの RPM リポジトリの場所をインストーラーに
伝えます。`--define-repo` オプションで、両方のビルドスクリプトに渡します。

### コミュニティの RPM リポジトリの構成

`yum` は、リポジトリのファイルに設定したベース URL に、ホストの
アーキテクチャー（`x86_64/`）を自動で付け足します。そのため、コミュニティの
リポジトリはアーキテクチャーのサブディレクトリーの下に `repodata/` を置く
構成にする必要があります。

```
community-repo/
└── x86_64/
    ├── xo-lite-ce-*.rpm
    ├── xoa-proxy-*.rpm
    ├── xcp-hl-release-*.rpm
    └── repodata/
        ├── repomd.xml
        └── ...
```

リポジトリのメタデータは、アーキテクチャーのサブディレクトリーに対して
生成します。

```bash
createrepo_c community-repo/x86_64/
```

---

## パッケージがインストール後のホストに届く仕組み
{: #how-packages-reach-the-installed-host }

{: .important }
`install.img` は**インストーラー自身の ramdisk** であり、インストール後の
ホストのファイルシステムではありません。`packages.lst` にパッケージを
追加しても、それはインストーラーの環境に入るだけで、他のどこにも入りません。

インストール後のホストは、ISO の `Packages/` ディレクトリーをもとに
`host-installer` が作ります。そこでは `xcp-ng-deps` と、その依存関係を
たどった一式がインストールされます。したがって、RPM をメディアに置くだけ
では足りません。その依存関係の中でどこからも必要とされなければ、ISO の
リポジトリに置かれたまま使われません。

コミュニティのパッケージは、次の連鎖で入ります。

```
xcp-ng-deps
    └── xo-lite を要求 ──► xo-lite-ce が提供
                                 ├── xoa-proxy を要求
                                 └── xcp-hl-release を要求
```

この `Requires:` だけが入口です。以前は `xcp-hl-release` を
`--extra-packages` で名前を指定して置いてもいましたが、このオプションは
パッケージを ISO のリポジトリに置くだけで、インストール対象には選びません。
依存関係ができた時点で不要になり、どの仕組みでパッケージが届いているのかを
分かりにくくするだけでした。

知っておくとよい影響が 1 つあります。`Requires:` が追加される前の
`xolite-ce` のリリースを指定すると、`xcp-hl-release` の入っていない ISO が
できます。ビルドの検証のステップが、そのまま出荷せずにこれを検出します。

ISO からインストールしたホストでの確認方法：

```bash
rpm -q xcp-hl-release
ls /etc/yum.repos.d/xcp-hl.repo
```

---

## Docker のビルド環境

ビルドは `xcp-ng-build-env:8.3` の中で動きます。初期設定のあと、
`xcp-ng-build-ready` としてコミットしたものです。

```bash
# 初回：準備したイメージをコミットする
docker run --name xcpng-build xcp-ng/xcp-ng-build-env:8.3 /bin/true
docker commit xcpng-build xcp-ng-build-ready
```

---

## ビルドの手順

### 1. コミュニティのリポジトリを用意する

```bash
# xolite-ce の最新リリースから署名済みの RPM をダウンロードする
gh release download --repo Vagrantin/xolite-ce \
    --pattern "xo-lite-ce-*.rpm" \
    --dir community-repo/x86_64/

# xoa-proxy の最新リリースから署名済みの RPM をダウンロードする
gh release download --repo Vagrantin/xoa-proxy \
    --pattern "xoa-proxy-*.rpm" \
    --dir community-repo/x86_64/

# リポジトリのメタデータを生成する
createrepo_c community-repo/x86_64/
```

### 2. コミュニティの公開鍵をインストーラーの chroot に注入する

ISO 署名用サブキー（このリポジトリの `GPG_PRIVATE_KEY`）は、パイプラインの
最初にランナーのキーリングへインポートされます。そのあと**公開**側の鍵を
そのキーリングから取り出し、インストーラーの chroot のテンプレートへ
注入します。こうすることで、利用者が手作業で鍵をインポートしなくても、
インストール中にインストーラーがコミュニティの RPM を検証できます。

{: .important }
コンテナの中で `rpm --import` を実行すると、書き込まれるのは
**コンテナ側**の RPM データベースであり、`install.img` に入る chroot の
インストール先ではありません。正しい場所を指すよう、必ず `--root` を
指定してください。

```bash
# ランナーのキーリングから公開鍵をエクスポートする
gpg --armor --export "${GPG_KEY_ID}" > /tmp/RPM-GPG-KEY-xcp-ng-ce

# ツールチェーンのインストール先のテンプレートへコピーする
mkdir -p create-install-image/templates/installimg/base/etc/pki/rpm-gpg/
cp /tmp/RPM-GPG-KEY-xcp-ng-ce \
   create-install-image/templates/installimg/base/etc/pki/rpm-gpg/

# ビルド時にインストーラーの chroot へインポートする
rpm --root="${ROOTFS}" --import /etc/pki/rpm-gpg/RPM-GPG-KEY-xcp-ng-ce
```

### 3. create-installimg.sh を実行する（root）

```bash
# ビルド用コンテナの中で root として実行する必要があります
sudo ./create-installimg.sh \
    --define-repo base \
    --define-repo updates \
    --define-repo community \
    [その他のオプション]
```

`--define-repo` には、`base`、`updates`、`community` の 3 つすべてを
指定する必要があります。

### 4. ISO のビルド番号を刻む

`host-installer` はメディアの `.treeinfo` にある `[build] number` を読み、
インストール後のホストの `/etc/xensource-inventory` に `BUILD_NUMBER` と
して書き込みます。アップストリームでは `cloud` というプレースホルダーが
入っており、インストール後のホストには、どのメディアから入れたかを示すもの
が他にありません。ボリュームラベルはインストール後には残らず、
`/var/log/installer/` のログにも書かれていないからです。

`create-iso.sh` がテンプレートを ISO へコピーする前に、ce の連番を刻んで
おきます。置き換えられるのは `@@...@@` の形のトークンだけなので、そのままの
値は手を加えられずに通ります。

```bash
sed -i "s/^number = .*/number = ${CE_COUNTER}/" \
    create-install-image/templates/iso/8.3/.treeinfo
```

できあがった ISO からインストールしたホストでは、次のようになります。

```bash
$ grep BUILD_NUMBER /etc/xensource-inventory
BUILD_NUMBER='ce23'

# xapi がこのインベントリを読むため、リモートからも確認できます
$ xe host-param-get uuid=<ホストの uuid> param-name=software-version
... build_number: ce23; ...
```

### 5. create-iso.sh を実行する（非 root）

```bash
./create-iso.sh \
    --sign-script implantisomd5 \
    --define-repo base \
    --define-repo updates \
    --define-repo community \
    [その他のオプション]
```

### 6. isohybrid による後処理

{: .important }
UEFI に対応していない物理ハードウェアで ISO を起動するには、この手順が
**必須**です。

```bash
isohybrid --uefi output.iso
```

結果は次のコマンドで確認します。

```bash
fdisk -l output.iso
xorriso -report_el_torito output.iso
```

### 7. チェックサムと署名

各リリースでは、ISO と一緒に 3 つのファイルを配布します。チェックサムの
ファイル名は、対象となる ISO に合わせています。

```
xcp-ng-ce-8.3.iso
xcp-ng-ce-8.3.iso.sha256
xcp-ng-ce-8.3.iso.sha256.asc
```

チェックサムのファイルには ISO の SHA256 のハッシュが入っています。`.asc`
のファイルは、そのチェックサムのファイルに対する GPG の分離署名で、ISO
署名用サブキーで作られています。この 2 つで、2 段階の検証の連鎖ができます。

```
ISO 署名用サブキー
    └── 署名 ──► xcp-ng-ce-8.3.iso.sha256   （ISO のハッシュが入っている）
                      └── ハッシュが一致 ──► xcp-ng-ce-8.3.iso
```

```bash
# チェックサムのファイルを作る
sha256sum xcp-ng-ce-8.3.iso > xcp-ng-ce-8.3.iso.sha256

# ISO 署名用サブキーで署名する
gpg --batch --pinentry-mode loopback \
    --detach-sign --armor \
    xcp-ng-ce-8.3.iso.sha256
# → xcp-ng-ce-8.3.iso.sha256.asc ができます
```

### 8. リリースを検証する（利用者向けの手順）

{: .note }
検証の前に、3 つのファイルを**同じディレクトリー**にダウンロードして
ください。`sha256sum -c` は、現在のディレクトリーからファイル名で ISO を
探します。

```bash
# 1. 3 つのファイルを同じディレクトリーにダウンロードする
cd ~/Downloads
# GitHub のリリースページから xcp-ng-ce-8.3.iso、xcp-ng-ce-8.3.iso.sha256、
#     xcp-ng-ce-8.3.iso.sha256.asc をダウンロードします

# 2. コミュニティの GPG 鍵をインポートする（最初の 1 回だけ）
gpg --keyserver keys.openpgp.org \
    --recv-keys 2F591DB9D2C128C4C3D963F46DA00DCA5BBA215A
```

**手順 3 — チェックサムのファイルがこのプロジェクトの署名であることを
確認する：**

```bash
gpg --verify xcp-ng-ce-8.3.iso.sha256.asc \
             xcp-ng-ce-8.3.iso.sha256
```

期待される出力（大事なのは `Good signature` の行です）：

```
gpg: Signature made ...
gpg: Good signature from "XCP-ng home lab Edition <xcp-ng-ce.lid530@passmail.com>"
```

`BAD signature` と表示された場合、チェックサムのファイルは改ざんされて
います。先へ進まないでください。

**手順 4 — ISO が署名されたチェックサムと一致することを確認する：**

```bash
sha256sum -c xcp-ng-ce-8.3.iso.sha256
```

期待される出力：

```
xcp-ng-ce-8.3.iso: OK
```

`FAILED` と表示された場合、ISO のファイルは壊れているか差し替えられて
います。削除してダウンロードし直してください。

---

## install.img の内部

{: .warning }
`install.img` は **bzip2 で圧縮した cpio（`newc`）のアーカイブ**であり、
SquashFS ではありません。`create-installimg.sh` は
`find . | cpio -o -H newc | bzip2` で作るため、`unsquashfs` や
`mksquashfs` は使えません。

中身はインストーラーの ramdisk であり、インストール後のホストのファイル
システムではありません。
[パッケージがインストール後のホストに届く仕組み](#how-packages-reach-the-installed-host)
を参照してください。

### 展開と再作成

```bash
# 展開する
mkdir installimg-root
bzip2 -dc install.img | (cd installimg-root && cpio -idm)

# installimg-root/ の中で変更する
# ...

# 再作成する（アップストリームに合わせて cpio newc と bzip2）
(cd installimg-root && find . | cpio -o -H newc) | bzip2 > install.img.new
```

展開せずに中身を一覧するには次のようにします。

```bash
bzip2 -dc install.img | cpio -it
```

### ISO ストレージのパーティションのための host-installer へのパッチ
{: #host-installer-patching }

XCP-HL はインストール時に 20 GB の ISO 用パーティションを確保します。
そのためには `host-installer` 自体に手を入れる必要があります。これは、
フォークした `host-installer` の RPM を配布するのではなく、**ビルド時に
`install.img` の中のファイルにパッチを当てる**ことで実現しています。

理由は次のとおりです。`xo-lite-ce` は仮想的な機能を提供する
（`Provides: xo-lite`）ことで依存関係の解決に勝てますが、`host-installer`
は XCP-ng の `base`/`updates` リポジトリにすでに存在する実在のパッケージ
です。同じ名前の置き換えを公開するには、稼働中のホストが参照するチャンネル
で epoch を上げる必要があり、それを安全に置ける場所がありません。ramdisk に
パッチを当てれば、変更はインストーラーの環境に閉じ込められ、その環境は
インストールが終われば破棄されます。

これを実現しているのが `xcp-ng-ce-iso/patches/` にある 2 つのパッチで、
CI の `Patch toolchain with git` のステップで適用されます。

| パッチ | 対象 | 目的 |
|---|---|---|
| `installer-iso-sr-hook.patch` | `scripts/create-installimg.sh` | yum によるインストールのあと、既存のインストーラーのブランディングのブロックの隣に `patch -p1 -d "$ROOTFS/opt/xensource/installer"` のステップを追加します |
| `host-installer-iso-sr.patch` | `$ROOTFS/opt/xensource/installer/` | 変更の本体：パーティション分割、`mkfs`、fstab、インベントリ、それに初回起動用のスクリプトとユニット |

2 つめのパッチは
[`host-installer` のフォーク](https://github.com/Vagrantin/host-installer)
（ブランチ `feat/xcp-hl-iso-storage`）から生成します。そこでは変更を
アップストリームに対する実際のコミットとして管理しており、そのリポジトリの
`test/` のテストを実行できます。

```bash
cd host-installer
git diff 10.10.38-8.3..feat/xcp-hl-iso-storage \
    -- backend.py constants.py answerfile.py xcp-hl/ \
    > ../xcp-ng-ce-iso/patches/host-installer-iso-sr.patch
```

このブランチを新しいアップストリームのタグへリベースしたら、そのつど生成し
直してください。適用できなくなったパッチは、パッチの当たっていない
インストーラーを黙って出荷するのではなく、ビルドをはっきり失敗させます。
また、あとの CI のステップで、ビルドした `install.img` を展開して
`backend.py` を検索し、変更が実際に入ったことを確認します。

**パッチの内容。** `constants.py` に `iso_size`（20480 MB）と
`min_primary_disk_size_with_iso`（100 GB）が追加されます。`backend.py`
では、用意するパーティションの表に `ISO` の項目を加えます。ローカルの SR が
これまでどおりディスクの末尾を使えるよう、LVM のパーティションの直前に
サイズを決めて作成し、`xcphl-iso` という固定のラベルで ext4 に
フォーマットし、fstab の行と `ISO_PARTITION` というインベントリのキーを
書き込み、初回起動用のスクリプトと systemd のユニットをインストール先の
ルートに置きます。

SR の登録には XAPI が必要で、XAPI はインストール後のホストでしか動きません。
そのため、その部分は初回起動時に行います。これは、同じやり方でローカルの
主要な SR を作る `storage-init.service` を参考にしています。その後の再起動で
SR を接続し直すのに、こちらで何かする必要はありません。XAPI は起動時に、
接続が外れているすべての PBD を接続します
（`Create_storage.plug_unplugged_pbds`）。通常は API が使えるようになって
から 10 秒ほどで行われます。

### answerfile.xml の埋め込み（任意）

インストーラーで `file:///` として参照される `answerfile.xml` は、ISO の
CD-ROM のルートではなく、（`install.img` から展開された）**ramdisk の
ルート**を指します。無人インストール用に応答ファイルを埋め込むには、上記の
展開と再作成の手順で `install.img` の中に置いてください。

GPG に関する確認は、応答ファイルの属性で無効にできます。

```xml
<installation gpgcheck="false" repo-gpgcheck="false">
  ...
</installation>
```

---

## CI のワークフロー（GitHub Actions）

このワークフローは**手動の dispatch のみ**で動きます。`iso-agent` が
リリースのタグを push し、そのタグの ref に対してワークフローを実行し、
組み込むコンポーネントの正確なリリースタグを渡します。タグを push しただけ
ではビルドされなくなりました。`releases/latest` でコンポーネントを解決すると、
公開されたばかりのコンポーネントのリリースと競合し、古い RPM を組み込んで
しまうことがあったためです。

環境について重要な要件は次のとおりです。

```yaml
env:
  TMPDIR: /tmp       # ここと Dockerfile の両方で設定する必要があります
  HOME: /tmp         # 非 root で create-iso.sh を実行するために必要です
```

主なステップは次のとおりです。

```yaml
- name: Derive versions from tag
  run: |
    TAG="${{ github.ref_name }}"                            # 例：v8.3-ce4
    XCPNG_VER=$(echo "${TAG}" | sed 's/^v//;s/-ce.*//')    # → 8.3
    echo "XCPNG_VER=${XCPNG_VER}" >> $GITHUB_ENV

- name: Import ISO signing key
  # このリポジトリの GPG_PRIVATE_KEY には ISO 署名用サブキーが入っています。
  # xolite-ce / xoa-proxy の GPG_PRIVATE_KEY とは別の鍵です
  run: |
    echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --batch \
      --pinentry-mode loopback \
      --passphrase "${{ secrets.GPG_PASSPHRASE }}" --import

- name: Export public key for installer chroot
  run: |
    gpg --armor --export "${GPG_KEY_ID}" > /tmp/RPM-GPG-KEY-xcp-ng-ce
    cp /tmp/RPM-GPG-KEY-xcp-ng-ce \
       create-install-image/templates/installimg/base/etc/pki/rpm-gpg/

- name: Set up Docker build environment
  run: docker build -t xcp-ng-build-ready -f Dockerfile.build .

- name: Download xolite-ce RPM
  run: |
    gh release download --repo Vagrantin/xolite-ce \
      --pattern "xo-lite-ce-*.rpm" \
      --dir community-repo/x86_64/

- name: Download xoa-proxy RPM
  run: |
    gh release download --repo Vagrantin/xoa-proxy \
      --pattern "xoa-proxy-*.rpm" \
      --dir community-repo/x86_64/

- name: Prepare community repo
  run: createrepo_c community-repo/x86_64/

- name: Copy CUSTOMREPO.tmpl
  run: cp configs/base/CUSTOMREPO.tmpl configs/8.3/

- name: Run create-installimg.sh (root)
  run: |
    docker run --rm --privileged \
      -v $PWD:/build \
      -v $PWD/create-install-image:/create-install-image \
      xcp-ng-build-ready \
      bash -c "cd /create-install-image && sudo ./create-installimg.sh ..."

- name: Run create-iso.sh (non-root)
  run: |
    docker run --rm \
      -e HOME=/tmp \
      -v $PWD:/build \
      xcp-ng-build-ready \
      bash -c "cd /create-install-image && ./create-iso.sh ..."

- name: Restore working directory ownership
  run: sudo chown -R $(id -u):$(id -g) .

- name: isohybrid post-processing
  run: isohybrid --uefi output.iso

- name: implantisomd5
  run: implantisomd5 output.iso

- name: Generate and sign checksum
  run: |
    CHECKSUM_FILE="${OUTPUT}.sha256"
    sha256sum "${OUTPUT}" > "${CHECKSUM_FILE}"
    echo "CHECKSUM_FILE=${CHECKSUM_FILE}" >> $GITHUB_ENV
    gpg --batch --pinentry-mode loopback \
      --detach-sign --armor "${CHECKSUM_FILE}"
    gpg --verify "${CHECKSUM_FILE}.asc" "${CHECKSUM_FILE}"

- name: Publish GitHub Release
  uses: softprops/action-gh-release@v2
  with:
    tag_name: ${{ github.ref_name }}
    files: |
      ${{ env.OUTPUT }}
      ${{ env.CHECKSUM_FILE }}
      ${{ env.CHECKSUM_FILE }}.asc

- name: Remove GPG private key
  if: always()
  run: shred -u /tmp/community-signing.key || true
```

{: .note }
Docker のボリュームのマウントは `create-install-image` を指す必要が
あります。マウント先が、実際にクローンしたディレクトリー名と一致している
ことを確認してください。

---

## 開発に参加する

1. [Vagrantin/xcp-ng-ce-iso](https://github.com/Vagrantin/xcp-ng-ce-iso) を
   フォークします。
2. 上記のローカルの Docker の手順で変更を確認します。
3. CI での問題調査のためにデバッグ用スクリプトを重ねて使うには、フォークの
   GitHub Actions の設定で `DEBUG_BUILD` の変数を有効にします。
4. `main` に対してプルリクエストを作ります。
