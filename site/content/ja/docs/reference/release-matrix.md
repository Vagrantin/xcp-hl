---
title: リリース一覧表
weight: 1
translationKey: release-matrix
---

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

{{< release-matrix-iso >}}

[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) にアップストリームの
列がないのは、これがこのプロジェクトのために書かれた独自のコードで、フォーク
ではないからです。そのためバージョンも独自のものです。タグは
`v<cargo のバージョン>.<ビルド回数>` という形です（たとえば `v0.1.1.8` は
Cargo のバージョン `0.1.1` に対する 8 回目のビルドです）。RPM のリリース欄
には、CI の実行番号とビルド元のコミットが入ります
（`55.gc525575.static`）。`v-proxy-automated-*` というタグの 2 行は、この
方式より前のものです。タグはビルドの実行を表す識別子で、バージョンは RPM
にしか書かれていません。

## XOA HL のリリース {#xoa-hl-releases}

XOA-HL のイメージは ISO に**組み込まれていません**。XO Lite の展開ボタンが、
展開の時点で最新の VM イメージのリリースを解決します。つまりアプライアンスは
ISO とは別にバージョン管理されます。この表は、公開された各イメージ、その中に
入っている [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) のソフトウェアの
リリース、そしてそのリリースの分岐元となったアップストリームの Xen Orchestra
のバージョンを記録しています。イメージは
[#22](https://github.com/Vagrantin/xcp-hl/issues/22) 以降、
[`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) で公開して
います。それより前の項目は、当初の公開先である `xoa-hl` へリンクします。

{{< release-matrix-xoa >}}
