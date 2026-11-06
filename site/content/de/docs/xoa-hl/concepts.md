---
title: "Konzepte und Funktionsumfang"
linkTitle: "Konzepte"
description: "Komponenten, Versionsnummern und Funktionsumfang dieser Version verstehen."
weight: 90
translationKey: xoa-manual-concepts
translationStatus: draft
sourceRevision: sha256:9457bbb19ed144e4eabca2b0c7af226bd1db4d60fb67217e695f2165868fc341
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

Diese Referenzseite erklärt, mit welcher Komponente Sie arbeiten, was die Versionsnummern bedeuten und was diese Version umfasst. Sie enthält keine auszuführenden Schritte. Lesen Sie sie, bevor Sie sich auf eine Funktion verlassen oder ein Problem melden.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet.
{{< /callout >}}

## Komponenten und Adressen {#components}

| Komponente | Aufgabe | Erreichbar unter |
| --- | --- | --- |
| Hypervisor-Host oder Pool | Führt VMs aus und stellt die XAPI-Verwaltungsschnittstelle bereit | Verwaltungsadresse des Hosts |
| XO Lite CE | Vom Host bereitgestellte Browseroberfläche. Stellt die Appliance bereit und findet sie | HTTPS-Adresse des Hosts |
| XOA-HL-Appliance | Separate VM mit xo-server, der XO-5-Weboberfläche und Redis | HTTPS-Adresse der Appliance |

Das Zusammenspiel erläutert die [Architektur- und Bereitstellungsanleitung](/docs/start/#start-architecture). Verwalten Sie jeden Host oder Pool nur mit einem unterstützten Manager. Lesen Sie [Hosts und Pools](/docs/xoa-hl/hosts-pools/), bevor Sie eine Verbindung verlagern. Host- und Appliance-Updates sind getrennt und haben eigene Ziele und Zeitpläne: siehe [Update-Anleitung](/docs/guides/updates/).

## VMs, Speicher und Schutz {#objects}

Eine **VM** läuft auf einem Host in einem **Pool**. Ein **Storage Repository (SR)** speichert virtuelle Festplatten. Die Netzwerkschnittstelle einer VM verbindet sie mit einem Pool-Netzwerk. Namen sind nur Bezeichnungen: Verwenden Sie in Automatisierungen Objekt-IDs.

Ein **Snapshot** speichert den Zustand einer VM zu einem bestimmten Zeitpunkt auf demselben Speicher. Eine **Sicherung** kopiert Daten auf ein separates Sicherungsziel (Remote). Ein Snapshot allein schützt nicht vor Verlust dieses Speichers, und auch nach einem erfolgreichen Sicherungsauftrag ist ein Wiederherstellungstest nötig.

Weitere Informationen: [Glossar](/docs/xoa-hl/glossary/), [Speicher und Netzwerke](/docs/xoa-hl/storage-networks/) und [VM sichern und wiederherstellen](/docs/xoa-hl/backup-restore/).

## Versionsnummern {#versions}

| Version | Bedeutung |
| --- | --- |
| XO 5.113.2, Upstream-Commit `e281c536` | Xen-Orchestra-Version der Anwendung und Weboberfläche. Bewusst gewählt: Dies ist nicht XO 6 |
| `xo-server` 5.193.1 | Server-Paketversion derselben Veröffentlichung. Sie verwendet eine andere Nummerierung |
| `v5.113.2_e281c536-ce40` | XOA-HL-Paketversion mit ihrem Patch-Satz |
| `xoa-image-20261022-a280852` | Build des Appliance-Images. Eine eigene Nummer: Ein Anwendungsupdate ändert sie nicht |

Notieren Sie die installierten Werte wie unter [Appliance-Wartung](/docs/xoa-hl/maintenance/) beschrieben. Die [Versionsmatrix](/docs/reference/release-matrix/) nennt gemeinsam ausgelieferte Versionen; sie bescheinigt keine bestandenen Integrationstests. Das Installations-ISO legt das Appliance-Image nicht fest: Das Image wird später bei der Bereitstellung ausgewählt.

## Funktionsumfang dieser Version {#feature-scope}

| Bereich | Im Code dieser Version | Vor der Nutzung |
| --- | --- | --- |
| VM-Betriebszustand, Snapshots, Festplatten und Netzwerke | Die XO-5-Aktionen und -Ansichten sind vorhanden | Die Alltagsanleitungen sind noch nicht auf einem Laborsystem getestet |
| Benutzer und Objektberechtigungen (ACLs) | Der veröffentlichte Build behält den Upstream-Standardplan (OpenSource). Die ACL-Ansichten sind im Code vorhanden | Installierte Oberfläche prüfen und in einer getrennten Sitzung als normaler Benutzer testen |
| Vollständige Sicherung und Wiederherstellung | Ein NFS-Verfahren ist auf Grundlage des Codes dokumentiert | Eine echte Sicherung und isolierte Wiederherstellung sind noch nicht getestet |
| Appliance-Updates | XOA-HL-Update-API, Kanäle `stable` und `testing` sowie einstellbare Zeitpläne | Der Update-Anleitung für Ihre Version folgen |
| Menüs Hub, Vates-XOA-Bereich, Backup-Proxys und XOSTOR | Ein Menü-Patch dieses Pakets blendet diese Einträge aus | Ein ausgeblendetes Menü begründet keine unterstützte Funktion. Es beweist auch nicht, dass die entsprechende API entfernt wurde |

Diese Paketversion deklariert 16 Patches. Das bedeutet nicht, dass jede Upstream-Option getestet wurde. Vates-Abonnements, kommerzieller Support und XO-6-Oberflächen gelten nicht für dieses Paket. Prüfen Sie vor Nutzung einer Funktion [Benutzer und Berechtigungen](/docs/xoa-hl/permissions/) und die passende Aufgabenanleitung.

## Verwandte Seiten {#related}

- [Diensteinstellungen](/docs/xoa-hl/configuration/): Konfigurationsdateien von xo-server.
- [Automatisierung mit xo-cli](/docs/xoa-hl/automation/): Inventar mit einem kurzlebigen Token über die Kommandozeile lesen.
- [Konfigurationsexport](/docs/xoa-hl/configuration-backup/): Einstellungen und Datensätze der Weboberfläche sichern.
- [xoa-hl](/docs/components/xoa-hl/) und [build-xoa-hl](/docs/components/build-xoa-hl/): Herstellung des Pakets. Produkt-Builds laufen ausschließlich in CI.

Nennen Sie bei Änderungsvorschlägen für diese Dokumentation die verwendeten Image- und Paketversionen.

{{< details title="Quellen" closed="true" >}}
- **Versionen, Patches und Build**: [Upstream-XO-Version (`UPSTREAM_XO`)](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/UPSTREAM_XO), [Patch-Liste](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/metadata.toml), [Menü-Patch zum Ausblenden von Einträgen](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/menu-hide-items.patch), [Paketdefinition](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [xo-server-Paketversion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/package.json), [Build der Weboberfläche](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/gulpfile.js).
{{< /details >}}
