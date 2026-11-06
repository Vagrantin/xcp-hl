---
title: Versionsmatrix
weight: 1
translationKey: release-matrix
aliases: ["/de/release-matrix/"]
---

XCP-hl und XOA-hl werden separat veröffentlicht: das auf dem Host installierte ISO und die von XO Lite darauf bereitgestellte XOA-hl-Appliance. Diese Seite dokumentiert alle Veröffentlichungen beider Komponenten.
{class="lead"}

## XCP-hl {#xcp-hl-releases}

Jedes XCP-hl-ISO wird aus unabhängig versionierten Komponenten erstellt. Diese Tabelle dokumentiert exakt, welche Versionen gemeinsam ausgeliefert wurden und von welcher Upstream-Veröffentlichung die angepassten Komponenten abgeleitet wurden.

Jede Version verlinkt auf ihre Veröffentlichungsseite im jeweiligen Repository. Unter jeder Version steht das vom ISO installierte Paket genau so, wie `rpm -q` es auf einem laufenden Host ausgibt. So können Sie einen Host einer Zeile zuordnen:

```bash
rpm -q xoa-proxy xo-lite-ce xcp-hl-release
```

{{< release-matrix-iso >}}

Die Spalte `xcp-hl-release` wird aus dem in den ISO-Versionshinweisen dokumentierten RPM befüllt. Ältere ISO-Veröffentlichungen ohne diesen Herkunftsnachweis zeigen „Nicht erfasst“; ihre RPM-Identität wird nicht aus der aktuell neuesten Veröffentlichung abgeleitet.

[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) hat keine Upstream-Spalte: Der Code wurde eigens für dieses Projekt geschrieben und ist kein Fork. Seine Version ist daher eigenständig. Das Tag lautet `v<cargo version>.<build counter>` (beispielsweise ist `v0.1.1.8` die Cargo-Version `0.1.1` mit dem achten darauf basierenden Build). Das RPM-Release-Feld enthält die CI-Laufnummer und den zugrunde liegenden Quellcommit (`55.gc525575.static`). Die beiden Zeilen mit `v-proxy-automated-*` stammen aus der Zeit vor diesem Schema: Ihr Tag bezeichnet einen Buildlauf; nur das RPM nennt die ausgelieferte Version.

## XOA-hl {#xoa-hl-releases}

Das XOA-hl-Image ist **nicht** im ISO enthalten: Die Bereitstellungsschaltfläche von XO Lite ermittelt die neueste VM-Image-Veröffentlichung zum Bereitstellungszeitpunkt. Deshalb wird die Appliance unabhängig vom ISO versioniert. Diese Tabelle dokumentiert jedes veröffentlichte Image, die enthaltene [`xoa-hl`](https://github.com/Vagrantin/xoa-hl)-Softwareveröffentlichung und die Upstream-Version von Xen Orchestra, von der sie abgeleitet wurde. Seit [#22](https://github.com/Vagrantin/xcp-hl/issues/22) werden Images unter [`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) veröffentlicht. Frühere Einträge verlinken auf `xoa-hl`, wo sie ursprünglich veröffentlicht wurden.

Soweit erfasst, verlinkt die Softwarezelle auf das genaue RPM-Release-Tag und zeigt die von `rpm -q xoa-hl` gemeldete Paketidentität. Ältere Image-Zeilen enthalten nur die von Upstream abgeleitete Softwareversion. Daraus allein lässt sich der im Image enthaltene konkrete RPM-Build nicht bestimmen.

{{< release-matrix-xoa >}}
