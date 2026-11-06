---
title: "VM migrieren, exportieren und importieren"
linkTitle: "Migrieren und exportieren"
description: "Eine VM auf einen anderen Host ihres Pools verschieben, als XVA-Datei exportieren und eine Kopie importieren."
weight: 43
translationKey: xoa-manual-vm-transfer
translationStatus: draft
sourceRevision: sha256:a5665d0df57eca23794c955b06c1e75b2c10f373c55fe2b59f2c3a165ab2f756
glossaryTerms: ["vm", "host", "pool", "sr", "snapshot", "backup"]
---

Verwenden Sie eine entbehrliche VM ohne Produktionsdaten. Melden Sie sich bei der **XOA-HL-Appliance** als Administrator an und prüfen Sie die Verfügbarkeit von Hosts, Speicher und VM. Migration und Export verschieben oder kopieren eine vollständige VM; keines von beiden ersetzt eine unabhängige [Sicherung mit Wiederherstellungstest](/docs/xoa-hl/backup-restore/).

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; Migration, Export und Import sind noch nicht auf einem Laborsystem getestet. Spätere Versionen können abweichen.
{{< /callout >}}

## 1. Vorgang wählen {#1-choose-the-operation}

| Ziel | Vorgang | Ergebnis |
| --- | --- | --- |
| Dieselbe VM auf einem anderen Host ihres Pools ausführen | **Migrate** | Dasselbe VM-Objekt; Datenträger bleiben auf gemeinsamem Speicher oder werden auf ein gewähltes SR kopiert |
| Eine portable Datei einer angehaltenen VM aufbewahren | **Export** als XVA | Eine vom Browser gespeicherte Datei; ohne Zeitplan, Aufbewahrung oder Wiederherstellungsprüfung |
| Aus einer XVA-Datei eine getrennte VM erstellen | **Import** | Ein neues VM-Objekt mit kopierten Gastidentitäten; wie einen Klon isolieren |
| Nach Verlust wiederherstellen | [Sicherung und Wiederherstellung](/docs/xoa-hl/backup-restore/) | Eine unabhängige, durch isolierte Wiederherstellung geprüfte Kopie |

Diese Anleitung behandelt Migration zwischen Hosts **desselben Pools**, XVA-Export ohne Komprimierung und Import einer XVA-Datei. Poolübergreifende Migration, Neuzuordnung von Netzwerken, OVA-Dateien, URL-Import, reiner Datenträgerimport/-export und VMware-Import liegen außerhalb ihres Umfangs. Das HomeLab-Menü blendet den VMware-Importeintrag aus.

## 2. VM innerhalb ihres Pools migrieren {#2-migrate-a-vm-within-its-pool}

Vor dem Beginn zu prüfende Voraussetzungen:

- Der Pool hat mindestens zwei verbundene Hosts, und Sie besitzen Administrationsrechte für die VM und den Zielhost.
- Der Zielhost erreicht Netzwerke und Speicher der VM. Datenträger auf einem gemeinsamen SR benötigen keine Kopie. Ein Datenträger auf für das Ziel unerreichbarem Speicher, etwa einem lokalen SR, wird kopiert.
- Ein Wartungsfenster. Ein laufender Gast pausiert während einer Livemigration kurz; eine Datenträgerkopie dauert länger und benötigt freien Platz auf dem Ziel-SR.
- Eine Aufzeichnung von VM-ID, aktuellem Host, jedem Datenträger und seinem SR sowie einer Gastprüfung, etwa Konsolenanmeldung oder Anwendungstest.

1. Öffnen Sie die VM und wählen Sie **Migrate**. Dies wird für laufende und angehaltene VMs angeboten, nicht für suspendierte oder pausierte. Self-Service-Benutzer sehen die Aktion nicht.
2. Wählen Sie unter **Migrate VM** mit **Select a destination host:** einen anderen Host desselben Pools. Der aktuelle Host ist ausgenommen. Die Liste kann auch Hosts anderer verbundener Pools enthalten; wählen Sie diese in dieser Übung nicht.
3. Lesen Sie den Speicherabschnitt. Liegen alle Datenträger auf einem gemeinsamen SR, ist keine SR-Auswahl nötig. Andernfalls verlangt XO ein Haupt-SR (**Select main SR…**) und erlaubt pro VDI ein eigenes SR. Wählen Sie beschreibbare SRs mit genug freiem Platz; diese Datenträger werden kopiert.
4. **Select a migration network:** ist innerhalb eines Pools optional. XO wählt das konfigurierte Migrationsnetz des Pools vor, wenn der Zielhost dort eine Adresse hat. Jedes ausgewählte Netzwerk veranlasst XO, den Speichermigrationspfad statt einer einfachen Poolmigration zu verwenden. Behalten Sie den vorgeschlagenen Wert bei, sofern Ihr Poolentwurf kein anderes Netzwerk vorsieht.
5. Bestätigen Sie und warten Sie auf das Aufgabenende. Klicken Sie nicht erneut, solange die Migration aussteht.
6. Aktualisieren Sie **General** der VM. Prüfen Sie Host, Betriebszustand, Konsole, Gastnetz und Anwendung. Prüfen Sie nach einer Datenträgerkopie den neuen Ort jedes Datenträgers und den freien Platz beider SRs.

{{< callout type="warning" >}}
Meldet XAPI eine Inkompatibilität der VM mit dem Zielhost, bietet XO **Force migration** an. Brechen Sie dies in dieser Übung ab und untersuchen Sie CPU- und Hostkompatibilität. Eine erzwungene Migration kann den Gast unbrauchbar machen.
{{< /callout >}}

Meldet eine einfache Poolmigration, dass ein SR erforderlich ist, versucht XO sie automatisch als Speichermigration erneut. Dabei verwendet es mit dem Zielhost verbundene SRs oder das Standard-SR des Pools. Eine vermeintlich schnelle Migration kann dadurch zu einer Datenträgerkopie werden. Sichern Sie bei einem Migrationsfehler den Aufgabenfehler und prüfen Sie Host, Betriebszustand und Datenträger der VM auf jedem beteiligten SR vor einem erneuten Versuch. Wiederholen Sie nicht mit Zwang.

## 3. Angehaltene VM als XVA-Datei exportieren {#3-export-a-stopped-vm-as-an-xva-file}

Sie benötigen Administrationsrechte für die VM und genügend freien Platz auf dem Computer mit dem Browser.

1. Fahren Sie den Gast sauber herunter und bestätigen Sie **Halted**. Notieren Sie VM-ID, Namen, Datenträger und ihre Gesamtgröße.
2. Wählen Sie **Export**. Lassen Sie **Type** auf `xva`. Lassen Sie **Compression** auf der Voreinstellung **Disabled**. Weitere Möglichkeiten sind GZIP (sehr langsam) und auf XCP-ng-Hosts Zstd. Der Import komprimierter XVAs wird hier nicht behandelt.
3. Bestätigen Sie. **Download VM** zeigt einen Downloadlink, **OK** und **Cancel**. Link und **OK** öffnen dieselbe URL, laut Meldung einmalig und nur kurz gültig. Verwenden Sie nur eines davon: Wählen Sie den Link und schließen Sie danach den Dialog mit **Cancel**. Die URL enthält ein einmaliges Zugriffstoken: Behandeln Sie sie bis zur Verwendung als Geheimnis.
4. Der Browser speichert `<date> - <VM name>.xva`. Lassen Sie den Download vollständig durchlaufen; Abbrechen stoppt den Export. Prüfen Sie die Dateigröße auf Plausibilität gegenüber den notierten Datenträgergrößen.
5. Erfassen Sie auf dem Browsercomputer eine Prüfsumme, beispielsweise mit `sha256sum "<file>.xva"`. Prüfen Sie die Datei damit vor einem Import.

Standardmäßig laufen höchstens zwei XVA-Exporte pro Pool gleichzeitig. Ein weiterer Download scheitert, statt zu warten. Lassen Sie laufende Exporte enden und fordern Sie dann einen neuen Link an.

Eine XVA enthält Datenträger und Konfiguration der VM. Bewahren Sie sie entsprechend den enthaltenen Daten auf und löschen Sie sie nach Testende. Eine Exportdatei hat weder Zeitplan noch Aufbewahrung oder Wiederherstellungsprüfung und ist daher kein Sicherungsauftrag.

{{< callout type="warning" >}}
Eine laufende VM kann exportiert werden; XO exportiert dann jedoch einen temporären Snapshot namens `[XO Export] <VM name>`. Diese Kopie ist nicht anwendungskonsistent. XO löscht den Snapshot nach Downloadende. Scheitert das Löschen, wird nur eine Warnung protokolliert und der Snapshot kann auf dem SR verbleiben. Prüfen Sie nach einem Export im laufenden Zustand **Snapshots** der VM. Diese Anleitung verwendet stattdessen eine angehaltene VM.
{{< /callout >}}

## 4. XVA als isolierte Kopie importieren {#4-import-the-xva-as-an-isolated-copy}

1. Öffnen Sie **Import** > **VM** (`/#/import/vm`). Der Menüeintrag erscheint nur, wenn Sie mindestens einen Pool bedienen dürfen.
2. Wählen Sie unter **To Pool:** den Zielpool. **To SR:** schlägt das Standard-SR des Pools vor. Wählen Sie ein beschreibbares SR mit ausreichend freiem Platz.
3. Ziehen Sie die `.xva`-Datei in den Bereich **Drop OVA or XVA files here to import Virtual Machines.** Prüfen Sie Dateiname und Größe in der Liste. Dateien ohne `.xva`- oder `.ova`-Endung werden ignoriert. Lassen Sie **From URL** deaktiviert.
4. Wählen Sie **Import** und lassen Sie den Browsertab bis zum Uploadende offen. Bei einer einzelnen Datei öffnet XO nach Erfolg die Seite der neuen VM.
5. Lassen Sie die importierte VM angehalten. Notieren Sie ihre ID: Sie ist auch bei gleichem Namen ein anderes Objekt als die Quell-VM. Benennen Sie sie zur Vermeidung von Verwechslungen um.
6. Öffnen Sie vor dem ersten Start **Network** und [entfernen Sie jede virtuelle Schnittstelle](/docs/xoa-hl/storage-networks/) oder sorgen Sie für nachgewiesene externe Isolation. Die Kopie enthält dasselbe Gastbetriebssystem, dieselben IP-Einstellungen, Hostnamen, Zugangsdaten und Anwendungsidentitäten wie die Quelle.
7. Starten Sie die Kopie und prüfen Sie ihre Konsole sowie die notierten Testdaten.

XO verweigert den Start einer VM, deren Schnittstellen-MAC-Adresse eine ihrer eigenen oder die einer laufenden VM dupliziert. Der Fehlercode lautet `DUPLICATED_MAC_ADDRESS`. Erzwingen Sie den Start nicht; entfernen oder isolieren Sie zuerst die Schnittstelle.

Bei einem fehlgeschlagenen Import (**VM import failed**) können Objekte zurückbleiben. Prüfen Sie vor einem neuen Versuch die Datenträger des Ziel-SRs und die VM-Liste auf während des Versuchs erstellte Objekte. Entfernen Sie nur eindeutig identifizierte Überreste anhand des [Verfahrens zum Entfernen einer entbehrlichen VM](/docs/xoa-hl/vm-operations/#delete-vm).

## 5. Aufräumen {#5-clean-up}

1. Entfernen Sie die importierte Test-VM mit dem [Verfahren zum Entfernen einer entbehrlichen VM](/docs/xoa-hl/vm-operations/#delete-vm).
2. Löschen Sie die XVA-Datei vom Computer und aus allen temporären Ablageorten.
3. Prüfen Sie, dass die Quell-VM weiterhin auf dem erwarteten Host vorhanden ist und ihre Datenträger und Daten unverändert sind.

Stimmt etwas nicht, behalten Sie die Aufzeichnungen und [melden Sie das Problem](/docs/xoa-hl/troubleshooting/) mit Versionen und bereinigten IDs.

{{< details title="Quellen" closed="true" >}}
Geprüft anhand von XO-5-Commit `e281c536` mit den veröffentlichten HomeLab-Patches: [VM-Aktionsleiste](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [Migrations-, Export- und Importaktionen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [Migrationsdialog](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/migrate-vm-modal/index.js), [Standard-Migrationsnetz](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/utils.js), [Exportdialog](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/export-vm-modal/index.js), [Komprimierungsoptionen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-compression.js), [Importseite](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm-import/index.js), [VM-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [XAPI-Migration, Import- und Startprüfungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [Verarbeitung von Export-Snapshots](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [Exportparallelität](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml) und [Oberflächenbezeichnungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js). HomeLab-Menüänderungen: [VMware-Importeintrag](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/zzzzzzzzz-xoa-hl-hide-vmware-and-support-alert.patch).
{{< /details >}}
