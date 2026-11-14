---
title: その他の XCP-ng クライアント
weight: 6
translationKey: other-clients
aliases: ["/ja/other-clients.html", "/ja/docs/guides/other-clients/"]
---

XCP-ng ホストを管理する方法は XO Lite と Xen Orchestra だけではありません。
ここでは、知っておくと役に立つ他のコミュニティ製ツールを紹介します。

---

## XenAdminQt

[XenAdminQt](https://github.com/benapetr/XenAdminQt) は、従来の XenAdmin
デスクトップクライアントを C++/Qt6 で書き直したものです。Windows 専用の
.NET ではなく、macOS と GNU/Linux（原理的には Qt が動くすべての環境）で
使えます。XCP-ng や XenServer を支えているのと同じ xapi の JSON-RPC API と
やり取りするため、ネイティブのデスクトップアプリからホストや VM のコンソール
と性能のメトリクスを利用できます。ライセンスは BSD-2-Clause で、まだアルファ
版ですが、XCP-ng 用にネイティブでマルチプラットフォームのデスクトップ
クライアントが欲しい方には有力な選択肢です。開発と保守を続けている
[benapetr](https://github.com/benapetr) 氏に感謝します。

## XenCenter (xenadmin) XCP - Jumphp

[XenCenter (xenadmin) XCP - Jumphp](https://jumphp.net/xencenter-xenadmin-xcp-jumphp)
は、XenCenter (xenadmin) を JumPHP に移植したクライアントで、XCP-ng と
XenServer のサーバを管理できます。プール、ホスト、VM、ストレージ、ネットワーク、
性能を扱えます。ブラウザ（Web アプリや PWA）とデスクトップで動作し、スマート
フォンでも使えます。ソースコードは
[git.jumphp.net](https://git.jumphp.net/duchnoun/xencenter-xenadmin-xcp-jumphp)
にあります。開発と保守を続けている duchnoun 氏に感謝します。

---

ここに載せるとよさそうな XCP-ng のクライアントをご存じですか。
[xcp-hl](https://github.com/Vagrantin/xcp-hl) で issue を作ってください。
