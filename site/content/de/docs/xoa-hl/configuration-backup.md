---
title: "XO-Konfiguration exportieren"
linkTitle: "Konfigurationsexport"
description: "XO-Konfiguration exportieren, einen Import sicher testen und Pool-Metadaten sichern."
weight: 81
translationKey: xoa-manual-configuration-backup
translationStatus: draft
sourceRevision: sha256:72e05e0e98f3c43537742df9848f514ff5c7dc8c05ff135dff73c2622ccdedef
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Speichern Sie vor der Appliance-Wartung die XO-Konfiguration in einer Datei und bewahren Sie sie getrennt von Ihren VM-Sicherungen auf. Testen Sie die Datei anschließend auf einer entbehrlichen Appliance. Pool-Metadaten benötigen einen eigenen Sicherungsjob, wie unten beschrieben. Sie arbeiten im **Browser**, angemeldet bei XOA-HL als XO-Administrator.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet. Diese Seite beschreibt keinen unterstützten Wiederherstellungs- oder Downgrade-Weg.
{{< /callout >}}

## Inhalt des Exports {#export-contents}

Der Export speichert die XO-Konfiguration: Benutzer und Gruppen, Zugriffsregeln, Serververbindungen, Remotes, Jobs, Zeitpläne, Authentifizierungstoken und Plugin-Einstellungen. Behandeln Sie die Datei als Geheimnis: Sie kann Serverpasswörter, Remote-Zugangsdaten und Token enthalten.

| Inhalt | Schutz |
| --- | --- |
| XO-Konfiguration | Dieser Export unter **Settings → Config** |
| Gastfestplatten und -daten | Separate [VM-Sicherung und -Wiederherstellung](/docs/xoa-hl/backup-restore/) |
| Host- und Pool-Metadaten | Separate [Pool-Metadatensicherung](#pool-metadata). Nicht in diesem Export enthalten |
| Appliance-Betriebssystem, RPM-Pakete und Laufzeitprotokolle | Nicht im Export enthalten |
| Server-TOML-Datei, TLS-Dateien, Update-Einstellungen und Zeitzone | Nicht im Export enthalten. Separat erfassen |

Ein abgeschlossener Export beweist nicht, dass die Datei Ihre Installation wiederherstellen kann. Bewahren Sie die Image- und Anwendungsversionen zusammen mit ihr auf.

## 1. Export herunterladen und aufbewahren {#1-download-and-store-the-export}

1. Melden Sie sich im **Browser** als XO-Administrator an. Notieren Sie die [installierten Versionen](/docs/xoa-hl/maintenance/#record-versions).
2. Öffnen Sie **Settings → Config** (`/#/settings/config`). Wählen Sie unter **Export** die Option **Download current config**.
3. Geben Sie eine einzigartige Passphrase ein und bestätigen Sie. Bleibt sie leer, ist der Export unverschlüsselt.
4. Bewahren Sie die Passphrase getrennt auf, damit sie beim Verlust der Appliance noch verfügbar ist.
5. Blockiert der Browser das neue Fenster, erlauben Sie den Download. Prüfen Sie, dass eine nicht leere Datei gespeichert wurde: `config.json.gz`, bei Verschlüsselung mit zusätzlichem `.enc`. Benennen Sie sie nicht so um, dass sie wie eine VM-Sicherung aussieht.
6. Verschieben Sie die Datei auf geschützten Speicher außerhalb der Appliance. Notieren Sie Datum, Dateigröße, Versionen und Verschlüsselungsstatus.
7. Behalten Sie den vorherigen Export, bis der neue einen Importtest auf einer isolierten Appliance besteht.

**Prüfung:** Datei und Passphrase sind ohne ursprüngliche Appliance erreichbar. Hängen Sie die Datei niemals an ein öffentliches Issue und fügen Sie ihren entschlüsselten Inhalt niemals in einen Bericht ein.

## 2. Import auf einer isolierten Appliance testen {#import-test}

{{< callout type="warning" >}}
Ein Import kann gespeicherte Server wieder verbinden und gespeicherte Zeitpläne aktivieren. Er kann vorhandene Einträge verändern und kollidierende Benutzer ersetzen. Für den gesamten Import gibt es keine Rücknahme: Nach einem Fehler können Teiländerungen verbleiben. Ermitteln Sie niemals an einer produktiven Appliance die Wirkung eines ungeprüften Exports.
{{< /callout >}}

**Vor dem Beginn**

- Eine entbehrliche Appliance mit denselben notierten Image- und Paketversionen verwenden.
- Ihr Netzwerk vor dem Import einschränken: Der Testbrowser erreicht sie, sie erreicht aber weder produktive Hosts noch Sicherungs-Remotes oder externe Dienste.
- Einschränkung außerhalb von XO erzwingen. Vorheriges Deaktivieren von Verbindungen oder Zeitplänen reicht nicht, da der Import sie wiederherstellen kann.
- Zustand der frischen Appliance notieren. Zugangsdaten aus der exportierten Konfiguration bereithalten: Der Import kann Konten verändern.

1. Öffnen Sie **Settings → Config**. Wählen Sie die Exportdatei oder ziehen Sie sie hinein, wählen Sie **Import** und geben Sie die Export-Passphrase ein. Warten Sie auf Erfolgs- oder Fehlermeldung.
2. Ist der Import erfolgreich, melden Sie sich ab und mit einem Administratorkonto aus dem Export erneut an.
3. Vergleichen Sie Benutzer, Berechtigungen, Remotes, Server, Jobs und Zeitpläne mit Ihren Aufzeichnungen der Quelle. Bei blockiertem Netzwerk sind Serververbindungsfehler zu erwarten.
4. Deaktivieren Sie importierte Zeitpläne und entfernen oder ersetzen Sie produktive Ziele, bevor Sie Zugriff auf entbehrliche Testressourcen erlauben. Prüfen Sie diese Einstellungen vor jedem Test erneut.
5. Bei fehlgeschlagenem Import Fehler und `xo-server`-Protokolle ohne Geheimnisse festhalten. Verwerfen Sie die Appliance und beginnen Sie den nächsten Versuch mit einer frischen. Nehmen Sie nicht an, dass ein fehlgeschlagener Import nichts verändert hat.

**Prüfung:** Der exportierte Administrator kann sich anmelden; Benutzer, Berechtigungen, Remotes, Jobs und Zeitpläne entsprechen den Aufzeichnungen. Eine Erfolgsmeldung allein beweist keine Wiederherstellbarkeit. Falsche Passphrasen, kollidierende Benutzer und unterbrochene Importe werden hier nicht behandelt.

## Schutz der Pool-Metadaten einrichten {#pool-metadata}

Ein separater Job **Pool metadata** sichert die Metadaten eines Pools. XO liest vom gewählten Pool einen XAPI-Stream `/pool/xmldbdump`. Es schreibt `data` und `metadata.json` auf ein Remote unter `xo-pool-metadata-backups/<schedule>/<pool>/<timestamp>/`. Dies ist weder der Export unter **Settings → Config** noch eine VM-Festplattensicherung, ein Appliance-Image oder ein getesteter Weg zur Host-Wiederherstellung. Die Metadaten können Infrastrukturdetails verraten: Beschränken Sie den Remote-Zugriff und hängen Sie diese Dateien niemals an ein öffentliches Issue.

**Vor dem Beginn**

- Einen eigenen, entbehrlichen und neu erstellbaren Pool verwenden, der mit XOA-HL verbunden ist. Für diesen Test niemals einen produktiven Pool ändern oder wiederherstellen.
- Ein dediziertes, beschreibbares NFS-Sicherungs-Remote verwenden, das nicht vom Speicher dieses Pools abhängt, damit ein einzelner Ausfall nicht beide betrifft.
- Separaten Plan zur [VM-Sicherung und -Wiederherstellung](/docs/xoa-hl/backup-restore/) für Gastdaten behalten.
- Installiertes Image und Paket prüfen. Prüfen, dass der Administrator die Metadatensicherungs-Bedienelemente sieht: In dieser Version kann die Oberfläche sie hinter einer Planprüfung verbergen. Fehlen sie, anhalten.
- Pool-UUID, Master- und Host-Identitäten, Remote-ID und freien Platz notieren.

### Deaktivierten Job erstellen {#create-a-disabled-job}

1. Öffnen Sie **Backup → New** und wählen Sie **XO config & Pool metadata Backup** (`/#/backup/new/metadata`). Nennen Sie den Job `lab-pool-metadata`.
2. Aktivieren Sie nur **Pool metadata**, lassen Sie **XO config** aus.
3. Wählen Sie den entbehrlichen Pool ausdrücklich aus. Wählen Sie nur das dedizierte Remote. Fügen Sie keine weiteren Pools oder Remotes hinzu.
4. Fügen Sie einen Zeitplan mit ausdrücklicher Zeitzone hinzu. Setzen Sie **Pool retention** auf `2` und lassen Sie den Zeitplan deaktiviert.
5. Speichern Sie. Lesen Sie Job- und Zeitplan-IDs, Pool, Remote, Modus, Aufbewahrung und deaktivierten Zustand zurück. Behält der Editor sie nicht bei, halten Sie an.

### Job dreimal ausführen {#run-the-job-three-times}

1. Starten Sie den Job manuell über seinen gespeicherten Zeitplan. Notieren Sie die Zeit: Dies ist Lauf A.
2. Warten Sie auf den Abschluss. Prüfen Sie im Jobprotokoll jeden Pool und jedes Remote einschließlich Unteraufgaben. Ein Gesamterfolg beweist keine vollständige Remote-Kopie.
3. Notieren Sie Lauf-ID, Status und UUID des Quellpools.
4. Wiederholen Sie dies für Läufe B und C zu unterschiedlichen Zeiten. Starten Sie jeden Lauf erst nach Abschluss des vorherigen.

### Aufbewahrte Punkte prüfen {#check-the-kept-points}

1. Öffnen Sie **Backup → Restore → Metadata** (`/#/backup/restore/metadata`). Betrachten Sie die **Pool**-Einträge aktivierter Remotes, ihre Zeiten und verfügbaren Punkte. **Wählen Sie weder Restore noch Delete.**
2. Bei Aufbewahrung `2` bleiben nur die Punkte der Läufe B und C erhalten. Vergleichen Sie sie mit Ihren Aufzeichnungen zu A, B und C.
3. Kann der Speicheradministrator das Remote direkt öffnen, lassen Sie jeden aufbewahrten Punkt prüfen: `data` und `metadata.json` sind nicht leer, und Job-, Zeitplan- sowie Pool-Identitäten stimmen. Dateigrößen und Hashes geschützt aufbewahren. Inhalte nicht veröffentlichen.
4. Unvollständige Punkte oder unerwartete Bereinigungsergebnisse zur Untersuchung aufbewahren.

Der Job schreibt diese Dateien ohne Prüfsumme. Ein aufgelisteter Punkt oder eine erfolgreiche Aufgabe beweist nicht, dass XAPI ihn importieren kann.

**Prüfung:** Der Zeitplan ist weiterhin deaktiviert, die drei Läufe nennen vorgesehenen Pool und Remote, und aufbewahrte B-/C-Punkte samt Dateien entsprechen Ihren Aufzeichnungen. Schlagen Export, Remote-Schreibzugriff, Bereinigung oder Auflistung fehl, führen Sie den Job nicht weiter aus und bewahren Sie Protokolle und Inventar auf. Löschen Sie Sicherungsordner niemals nur aufgrund ihres Namens.

### Vor jeder Pool-Wiederherstellung {#before-any-pool-restore}

Eine Pool-Wiederherstellung sendet `data` des gewählten Punkts an `/pool/xmldbdump` auf dem Zielpool. Sie verändert den Pool; eine Möglichkeit zur Rücknahme wurde nicht nachgewiesen. Vor jeder Wiederherstellung muss der Pool-Verantwortliche bereitstellen:

- einen isolierten, entbehrlichen Zielpool
- einen zu Versionen und Identitäten passenden Wiederherstellungsplan
- eine separate Rückfallkopie von Image oder Metadaten
- gesperrten Zugriff auf produktive Netzwerke und Speicher
- ein Verfahren zur anschließenden Prüfung von Host-/Pool-Verbindung und Inventar

Wählen Sie erst nach Prüfung dieser Voraussetzungen genau einen Punkt und einen Zielpool. Ein verfügbarer Punkt oder erfolgreicher Export beweist keine Wiederherstellbarkeit. XO-Konfigurationsexporte und Gastsicherungen getrennt halten. Die Wiederherstellung selbst, Massenwiederherstellung und Wiederherstellung auf einem anderen Pool werden hier nicht behandelt.

## Grenzen von Wiederherstellung und Rücknahme {#recovery-limits}

Bei einem echten Verlust bewahren Sie die ausgefallene Appliance und die Nachweise auf. Ermitteln Sie exakte Versionen und verwenden Sie einen Wiederherstellungsplan, der für diese Versionen einen isolierten Test bestanden hat. Verbinden Sie niemals zwei Kopien mit aktiven Zeitplänen mit denselben produktiven Zielen.

Ein älteres RPM-Paket ist keine vollständige Rücknahme. Ein Downgrade macht weder Betriebssystemupdates rückgängig noch stellt es XO-Daten oder die oben separat genannten Dateien wieder her. Versionsübergreifende Importe und Wiederherstellung per Downgrade wurden für diese Version nicht getestet. Scheitert ein Update, siehe [Wartung](/docs/xoa-hl/maintenance/#update-problems) und [Fehlersuche](/docs/xoa-hl/troubleshooting/).

{{< details title="Quellen" closed="true" >}}
- **Konfigurationsexport**: [Konfigurationsansicht](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/config/index.js), [API nur für Administratoren und Dateiformat](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/xo.mjs), [Verschlüsselung und Importmodul](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/config-management.mjs), [Server-Wiederverbindung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [Zeitplanaktivierung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [Benutzerkonflikte](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs).
- **Pool-Metadatensicherung**: [Metadatenjob-Editor und Planprüfung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/metadata/index.js), [Administrator-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/metadata-backup.mjs), [Pool-Export und Remote-Dateien](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_PoolMetadataBackup.mjs), [Modi und Remotes](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/Metadata.mjs), [Aufbewahrungsbereinigung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [Wiederherstellungspunktliste](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/metadata.js), [XAPI-Import-Endpunkt](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RestoreMetadataBackup.mjs).
{{< /details >}}
