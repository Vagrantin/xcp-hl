---
layout: default
title: リリース一覧表
parent: 日本語
nav_order: 6
lang: ja
---

# リリース一覧表

XCP-hl の ISO は、それぞれ別々にバージョン管理されたコンポーネントから
作られています。この表は、どのバージョンの組み合わせで
リリースされたか、そして手を入れたコンポーネントがどのアップストリームの
リリースから分岐したかを記録したものです。

各バージョンは、それを作ったリポジトリのリリースページにリンクしています。
バージョンの下には、ISO がインストールするパッケージを、稼働中のホストで
`rpm -q` を実行したときの表記のまま載せています。ホストと行を突き合わせる
のに使ってください。

```bash
rpm -q xoa-proxy xo-lite-ce
```

| ISO のバージョン | ビルド日 | xolite-ce | アップストリーム（xo-lite） | xoa-proxy |
|---|---|---|---|---|
{% for r in site.data.releases %}| [{{ r.iso_version }}](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/tag/{{ r.iso_version }}) | {{ r.build_date }} | [{{ r.components.xolite_ce.version }}](https://github.com/Vagrantin/xolite-ce/releases/tag/{{ r.components.xolite_ce.version }}){% if r.components.xolite_ce.rpm %}<br>`{{ r.components.xolite_ce.rpm }}`{% endif %} | [{{ r.components.xolite_ce.upstream }}]({{ r.components.xolite_ce.upstream_url }}) | [{{ r.components.xoa_proxy.version }}](https://github.com/Vagrantin/xoa-proxy/releases/tag/{{ r.components.xoa_proxy.version }}){% if r.components.xoa_proxy.rpm %}<br>`{{ r.components.xoa_proxy.rpm }}`{% endif %} |
{% endfor %}

[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) にアップストリームの
列がないのは、これがこのプロジェクトのために書かれた独自のコードで、フォーク
ではないからです。そのためバージョンも独自のものです。タグは
`v<cargo のバージョン>.<ビルド回数>` という形です（たとえば `v0.1.1.8` は
Cargo のバージョン `0.1.1` に対する 8 回目のビルドです）。RPM のリリース欄
には、CI の実行番号とビルド元のコミットが入ります
（`55.gc525575.static`）。`v-proxy-automated-*` というタグの 2 行は、この
方式より前のものです。タグはビルドの実行を表す識別子で、バージョンは RPM
にしか書かれていません。

## XOA HL のリリース
{: #xoa-hl-releases }

XOA-HL のイメージは ISO に**組み込まれていません**。XO Lite の展開ボタンが、
展開の時点で最新の VM イメージのリリースを解決します。つまりアプライアンスは
ISO とは別にバージョン管理されます。この表は、公開された各イメージ、その中に
入っている [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) のソフトウェアの
リリース、そしてそのリリースの分岐元となったアップストリームの Xen Orchestra
のバージョンを記録しています。イメージは
[#22](https://github.com/Vagrantin/xcp-hl/issues/22) 以降、
[`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) で公開して
います。それより前の項目は、当初の公開先である `xoa-hl` へリンクします。

| イメージのリリース | ビルド日 | xoa-hl（ソフトウェア） | アップストリーム（Xen Orchestra） |
|---|---|---|---|
{% for r in site.data.xoa_releases %}| [{{ r.image_tag }}](https://github.com/Vagrantin/{{ r.repo | default: "build-xoa-hl" }}/releases/tag/{{ r.image_tag }}) | {{ r.build_date }} | [{{ r.xoa_hl_version }}](https://github.com/Vagrantin/xoa-hl/releases/tag/{{ r.xoa_hl_version }}) | [{{ r.upstream_xo }}]({{ r.upstream_url }}) |
{% endfor %}
