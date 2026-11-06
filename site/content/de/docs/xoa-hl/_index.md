---
title: "XOA-HL-Handbuch"
weight: 2
translationKey: xoa-manual-home
translationStatus: draft
sourceRevision: sha256:9690e24c060de4d8fcc693f5a8507c57cce56c189f0a4c0c5abd9829f4c4abae
glossaryTerms: ["appliance", "backup", "host", "pool", "snapshot", "sr", "vm", "xo-lite"]
---

XOA-HL ist die Appliance, eine einsatzbereite virtuelle Maschine, auf der Xen Orchestra läuft. Sie verwalten damit Ihre XCP-HL-Hosts und virtuellen Maschinen im Browser. Dieses Handbuch zeigt, wie Sie die Appliance einrichten, VMs betreiben, sie schützen und alles aktuell halten.

{{< callout type="info" >}}
**Gilt für** XOA-HL `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Diese Anleitungen folgen dem veröffentlichten Code, wurden jedoch noch nicht vollständig auf einem Laborsystem getestet. Üben Sie zunächst mit Test-VMs.
{{< /callout >}}

## Hier beginnen {#start-here}

Neu bei XOA-HL? Arbeiten Sie diese drei Anleitungen der Reihe nach durch.

{{< cards >}}
  {{< card link="first-login/" title="1. Erste Anmeldung" subtitle="Melden Sie sich an, legen Sie Ihr Passwort fest, wählen Sie eine Sprache und verbinden Sie Ihren Host." >}}
  {{< card link="create-vm/" title="2. Ihre erste VM" subtitle="Laden Sie eine Installations-ISO hoch und installieren Sie eine Test-VM." >}}
  {{< card link="backup-restore/" title="3. Sicherung und Wiederherstellung" subtitle="Sichern Sie die VM und prüfen Sie anschließend, ob eine wiederhergestellte Kopie funktioniert." >}}
{{< /cards >}}

Noch nicht bereitgestellt? [Stellen Sie XOA-HL zunächst über XO Lite bereit](/docs/start/#start-deploy-xoa). Wie Host, XO Lite und Appliance zusammenarbeiten, erläutert die [Architekturübersicht](/docs/start/#start-architecture).

## Virtuelle Maschinen {#virtual-machines}

- [VMs verwalten](/docs/xoa-hl/vm-operations/): starten und stoppen, Snapshots, Kopien, CPU und Arbeitsspeicher, löschen.
- [VM-Konsole verwenden](/docs/xoa-hl/vm-operations/#vm-console) und einen leeren Bildschirm beheben.
- [Snapshot erstellen und zurücksetzen](/docs/xoa-hl/vm-operations/#stopped-snapshot).
- [Linux-Gastwerkzeuge installieren](/docs/xoa-hl/guest-tools/).
- [Vorlagen erstellen und verwenden](/docs/xoa-hl/templates/).
- [VM migrieren, exportieren und importieren](/docs/xoa-hl/vm-transfer/).

## Speicher und Netzwerke {#storage-and-networks}

- [Festplatten und Netzwerkschnittstellen hinzufügen](/docs/xoa-hl/storage-networks/).
- [NFS-Speicher für VM-Festplatten erstellen](/docs/xoa-hl/storage-networks/#nfs-vm-storage).
- [VLAN-Netzwerk erstellen](/docs/xoa-hl/storage-networks/#host-vlan-network).
- [Netzwerkproblem untersuchen](/docs/xoa-hl/troubleshooting/#network-connectivity).

## Sicherung und Wiederherstellung {#backup-and-recovery}

- [Sicherungen planen und Aufbewahrung festlegen](/docs/xoa-hl/backup-restore/#backup-schedules).
- [Inkrementelle Sicherungen verwenden](/docs/xoa-hl/backup-restore/#delta-backups).
- [Einzelne Datei wiederherstellen](/docs/xoa-hl/backup-restore/#file-restore).
- [VM in einen anderen Pool kopieren (DR)](/docs/xoa-hl/backup-restore/#dr-replica).
- [Auf eine Windows-Server-Freigabe sichern (SMB)](/docs/xoa-hl/backup-restore/#smb-remote).
- [Fehlgeschlagene Sicherung beheben](/docs/xoa-hl/troubleshooting/#backup-failures).

## Hosts, Benutzer und Sicherheit {#hosts-users-and-security}

- [Hosts und Pools verwalten](/docs/xoa-hl/hosts-pools/): Verbindungen, XO-Lite-Schaltfläche und Statistiken.
- [Host zu einem Pool hinzufügen](/docs/xoa-hl/hosts-pools/#pool-join).
- [Host in den Wartungsmodus versetzen](/docs/xoa-hl/hosts-pools/#host-maintenance-mode).
- [Benutzer, Gruppen und Berechtigungen verwalten](/docs/xoa-hl/permissions/).
- [Ressourcen mit einem Kontingent delegieren](/docs/xoa-hl/permissions/#resource-set-delegation).
- [Einmalcode zur Anmeldung hinzufügen](/docs/xoa-hl/sign-in-otp/).

## XOA-HL betriebsbereit halten {#keep-xoa-hl-running}

- [Appliance aktualisieren](/docs/guides/updates/#updating-xoa-hl-the-appliance) und [Host aktualisieren](/docs/guides/updates/#updating-xcp-hl-the-host).
- [Wartung planen und Ergebnis prüfen](/docs/xoa-hl/maintenance/).
- [XO-Konfiguration exportieren](/docs/xoa-hl/configuration-backup/).
- [Pool-Metadaten sichern](/docs/xoa-hl/configuration-backup/#pool-metadata).
- [Probleme beheben](/docs/xoa-hl/troubleshooting/).
- [Lieferumfang der einzelnen Versionen ansehen](/docs/reference/release-matrix/) und [Änderungsprotokoll lesen](/docs/reference/changelog/).

## Referenz {#reference}

- [Konzepte und Funktionsumfang](/docs/xoa-hl/concepts/)
- [Diensteinstellungen](/docs/xoa-hl/configuration/)
- [Automatisierung mit xo-cli](/docs/xoa-hl/automation/)
- [Glossar](/docs/xoa-hl/glossary/)
- [Seiten für Mitwirkende](/docs/components/)

## Hilfe und Rückmeldungen {#help-and-feedback}

Die XOA-HL-Oberfläche und diese Dokumentation haben getrennte Spracheinstellungen. Über die Auswahl oben auf dieser Seite ändern Sie die Dokumentationssprache. Der [Prüfstatus der Seiten](/docs/xoa-hl/translation-status/) zeigt, welche Seiten geprüft wurden.

[Dokumentationsproblem melden](https://github.com/Vagrantin/xcp-hl/issues/new?title=Documentation%3A%20XOA-HL%20manual). Geben Sie die Seitenadresse, den zu korrigierenden Schritt und Ihre Appliance-Version an. Fügen Sie niemals Passwörter oder private Daten bei.
