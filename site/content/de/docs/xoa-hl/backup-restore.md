---
title: "VM sichern und wiederherstellen"
linkTitle: "Sicherung und Wiederherstellung"
description: "VM sichern, eine sichere Kopie wiederherstellen und anschließend Zeitpläne, inkrementelle Sicherungen, Dateiwiederherstellung, DR-Kopien und SMB testen."
weight: 30
translationKey: xoa-manual-backup-restore
translationStatus: draft
sourceRevision: sha256:b4f67c2357cf7a39bb06c2688686bbcaa192c9d8d8408f8e293955ce27ad06c9
glossaryTerms: ["appliance", "backup", "host", "snapshot", "sr", "vm"]
---

Schützen Sie Ihre Test-VM durch eine vollständige Sicherung auf separatem Speicher. Stellen Sie anschließend eine Kopie wieder her und prüfen Sie die Nutzbarkeit der Daten. Ein erfolgreicher Sicherungsjob ist nur die Hälfte des Tests: Die Wiederherstellung vervollständigt ihn.

{{< callout type="info" >}}
**Gilt für** XOA-HL `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2), Image `xoa-image-20261022-a280852`. Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet. Andere Remotes und Sicherungsmodi benötigen eigene Tests.
{{< /callout >}}

Die Abschnitte 1 bis 5 bilden das Tutorial: eine vollständige NFS-Sicherung und eine sichere Wiederherstellung. Die folgenden Abschnitte sind darauf aufbauende optionale Tests: Zeitpläne und Aufbewahrung, inkrementelle Sicherungen, Wiederherstellung einzelner Dateien, eine DR-Kopie in einem anderen Pool und ein SMB-Remote.

## Vor dem Beginn {#before-you-begin}

- [Erstellen und installieren Sie eine Test-VM](/docs/xoa-hl/create-vm/). Verwenden Sie ein XOA-HL-Administratorkonto: Die Sicherungsseiten erfordern es in dieser Version.
- Beschaffen Sie einen NFS-Export auf einem separaten Sicherungssystem, nicht auf dem Speicher von VM oder Appliance. Die Appliance muss ihn erreichen und dort Dateien erstellen, lesen und löschen können. Fragen Sie den Speicheradministrator nach Server, Exportpfad und erforderlichen Mount-Optionen.
- Prüfen Sie freien Platz an drei Stellen: Sicherungsziel, SR der VM (für temporäre Snapshots) und beschreibbares SR für wiederhergestellte Festplatten. Lassen Sie Platz für die eingestellte Aufbewahrung plus einen weiteren Lauf. Komprimierte Größen sind nicht garantiert.
- Erstellen Sie im Gast eine kleine harmlose Datei und notieren Sie Inhalt oder Prüfsumme. Fahren Sie den Gast anschließend regulär herunter und prüfen Sie, dass die VM gestoppt ist. Die Sicherung einer laufenden VM garantiert keine Anwendungskonsistenz.
- Reservieren Sie Ressourcen für eine zweite VM. Die wiederhergestellte Kopie bleibt gestoppt, bis **alle virtuellen Netzwerkschnittstellen (NICs) entfernt sind**. Dieser Test verwendet nur die Konsole; die Kopie benötigt kein Netzwerk.

Sie verwalten Sicherungen im **Browser**. Die Beispieldatei erstellen und prüfen Sie **im Gast**. Sie benötigen keine Shell auf Host oder Appliance.

## 1. Sicherungsziel hinzufügen {#1-add-the-backup-destination}

1. Öffnen Sie **Settings → Remotes** (`/#/settings/remotes`). Verwenden Sie ein geeignetes, bereits geprüftes Remote erneut oder erstellen Sie eines namens `lab-backup-nfs`.
2. Wählen Sie **NFS** und geben Sie Server, Exportpfad und erforderliche Mount-Optionen des Speicheradministrators ein. Belassen Sie erweiterte Felder auf Standardwerten, sofern Ihr Speicher keine Änderung erfordert. Verwenden Sie keinen lokalen Ordner innerhalb der Appliance.
3. Speichern Sie das Remote, aktivieren Sie es bei Bedarf und führen Sie **Test your remote** aus. Lesen Sie vor dem Fortfahren jeden Verbindungs- oder Testfehler.

**Prüfung:** Das Remote ist aktiviert, sein Test besteht und es erscheint kein Verbindungsfehler. Dies beweist Zugriff, nicht Wiederherstellbarkeit einer VM-Sicherung.

## 2. Vollständigen Sicherungsjob erstellen {#2-create-a-full-backup-job}

1. Öffnen Sie **Backup → New → VMs** (`/#/backup/new/vms`) und nennen Sie den Job `lab-first-vm-full`.
2. Wählen Sie nur Ihre Test-VM. Lassen Sie die intelligente Auswahl aus, damit der Job keine anderen VMs erfasst.
3. Wählen Sie unter Sicherungsmodi **Backup**. Dies ist der vollständige Exportmodus. Lassen Sie **Rolling snapshot**, **Delta backup**, **Disaster recovery** und **Continuous replication** aus.
4. Wählen Sie unter **Target remotes (for export)** das Remote `lab-backup-nfs`. Lassen Sie **Delete first** aus: Es kann ältere Kopien löschen, bevor der neue Export erfolgreich ist.
5. Fügen Sie einen Zeitplan hinzu. Setzen Sie **Backup retention** auf `2`, wählen Sie eine ausdrückliche Zeitzone wie `Asia/Tokyo` und prüfen Sie die Vorschau der nächsten Läufe. Aufbewahrung ist die Anzahl der für diesen Zeitplan behaltenen Sicherungen, keine Tagesanzahl.
6. Deaktivieren Sie diesen Zeitplan in der Zeitplantabelle, bevor Sie den Job speichern. Diese erste Sicherung führen Sie manuell aus. Der Zeitplan bleibt bis [Sicherungszeitpläne und Aufbewahrung testen](#backup-schedules) deaktiviert.
7. Speichern Sie und prüfen Sie die Übersicht: eine VM, richtiges Remote und deaktivierter Zeitplan. Lassen Sie erweiterte Sicherungseinstellungen für diesen ersten Test unverändert.

{{< callout type="warning" >}}
Aufbewahrung kann in späteren Läufen ältere Sicherungen löschen. Verwenden Sie ein dediziertes Laborziel und verringern Sie niemals die Aufbewahrung eines produktiven Jobs für dieses Beispiel. Ein Snapshot auf dem eigenen SR der VM ist keine unabhängige Sicherung.
{{< /callout >}}

## 3. Sicherung ausführen und prüfen {#3-run-and-check-the-backup}

1. Verwenden Sie unter **Backup → Overview** (`/#/backup/overview`) die Ausführungsaktion am deaktivierten Zeitplan des Jobs. Prüfen Sie, dass die Bestätigung Ihren Job und nur eine VM nennt, und bestätigen Sie.
2. Warten Sie auf Abschluss. Öffnen Sie das Protokoll und prüfen Sie das VM-Exportergebnis, nicht nur den Jobstart. Untersuchen Sie Warnungen, Fehler oder übersprungene Daten.
3. Öffnen Sie **Backup → Restore** (`/#/backup/restore`). Suchen Sie die Test-VM und prüfen Sie, dass die neue vollständige Sicherung mit erwarteter Zeit und Remote aufgeführt ist. Aktualisieren Sie die Liste bei Bedarf.

**Prüfung:** Der Lauf war erfolgreich und sein Wiederherstellungspunkt ist aufgeführt. Notieren Sie Job, Zeitplan, Remote, Sicherungszeit und installierte Versionen. Sie können den ursprünglichen Gast wieder starten. Lassen Sie den Zeitplan während des Wiederherstellungstests deaktiviert.

## 4. Gestoppte Kopie wiederherstellen {#4-restore-a-stopped-copy}

1. Wählen Sie unter **Backup → Restore** die Wiederherstellungsaktion Ihrer Test-VM und anschließend die gerade erstellte vollständige Sicherung.
2. Wählen Sie ein beschreibbares SR mit ausreichend freiem Platz. Gemeint ist VM-Festplattenspeicher, weder NFS-Remote noch ISO-SR.
3. Lassen Sie **Start VM after restore** **ausgeschaltet**. Aktivieren Sie **Generate new MAC addresses**, damit die Kopie eigene Netzwerkkartenadressen bekommt. Neue MAC-Adressen ändern weder statische Gast-IP-Adresse noch Hostname oder Anwendungsidentität.
4. Bestätigen Sie die Wiederherstellung und warten Sie auf Abschluss. Prüfen Sie das Wiederherstellungsprotokoll auf Fehler. Ermitteln Sie die neue VM anhand von UUID und wiederhergestellten Festplatten, nicht anhand ihres Namens.
5. Prüfen Sie, dass die wiederhergestellte VM gestoppt ist. Benennen Sie sie `lab-first-vm-restore-test` und notieren Sie ihre UUID neben der UUID der ursprünglichen VM.

**Prüfung:** Eine separate, gestoppte VM mit erwarteten Festplatten existiert. Starten Sie sie noch nicht. Läuft sie, stoppen Sie sie und prüfen Sie vor dem Fortfahren, welche Netzwerke sie erreichen konnte.

## 5. Kopie isolieren, starten und prüfen {#5-isolate-start-and-check-the-copy}

1. Öffnen Sie den Reiter **Network der wiederhergestellten Kopie** (`/#/vms/<restored-uuid>/network`). Entfernen Sie im gestoppten Zustand **alle** NICs und prüfen Sie die leere Liste. Der Status „getrennt“ reicht nicht: Eine NIC könnte sich beim nächsten Start erneut verbinden.
2. Prüfen Sie UUID und leere NIC-Liste erneut. Starten Sie dann die Kopie und öffnen Sie **Console**. Ändern Sie das Netzwerk der ursprünglichen VM nicht.
3. Prüfen Sie, dass der Gast startet, die Konsolenanmeldung funktioniert und die Beispieldatei den erwarteten Inhalt oder die Prüfsumme besitzt. Prüfen Sie weitere für die Wiederherstellung benötigte Daten. Ein startender Gast ist noch keine vollständige Anwendungswiederherstellung.
4. Fahren Sie den wiederhergestellten Gast regulär herunter. Notieren Sie Ergebnis, Sicherungszeit, Wiederherstellungsdauer und Versionen. Prüfen Sie nach Abschluss die UUID und löschen Sie nur die Testkopie und ihre wiederhergestellten Festplatten. Behalten Sie ursprüngliche VM und Sicherung.

**Prüfung:** Die wiederhergestellten Daten entsprechen dem Beispiel und die Kopie hatte beim Start keine NIC. Scheitert der Test, behalten Sie die Sicherung, stoppen Sie die Kopie und lesen Sie vor einem neuen Versuch die Protokolle.

## Sicherungszeitpläne und Aufbewahrung testen {#backup-schedules}

Dieser Test aktiviert den Zeitplan des Laborjobs, beobachtet drei automatische Läufe und deaktiviert ihn wieder. Führen Sie ihn erst nach erfolgreicher manueller Sicherung und Wiederherstellung oben aus.

**Vor dem Beginn**

- Nur Laborjob `lab-first-vm-full`, seinen einzelnen deaktivierten Zeitplan und die eine Test-VM verwenden.
- Test-VM für jeden Lauf heruntergefahren lassen. Ein laufender Gast benötigt einen eigenen Konsistenztest.
- Freien Platz und Remote-Zugriff erneut prüfen.
- Benötigte Wiederherstellungskopien **außerhalb dieses Jobs** aufbewahren: Die Aufbewahrung kann seine alten Sicherungen löschen.

1. Notieren Sie unter **Backup → Overview** die Job-ID und kopieren Sie die genaue Zeitplan-ID mit deren Zwischenablageschaltfläche.
2. Bearbeiten Sie den Job. Bearbeiten Sie unter **Schedules** die bestehende deaktivierte Zeile; löschen und erstellen Sie sie nicht neu. Geben Sie ihr einen eindeutigen Testnamen und behalten Sie **Backup retention** `2`. Lassen Sie **Delete first**, Langzeitaufbewahrung und automatische Wiederherstellungsprüfungen aus. Prüfen Sie, dass nur **Backup**-Modus, Test-VM und `lab-backup-nfs` ausgewählt sind.
3. Legen Sie mit der visuellen Zeitauswahl eine Testregel und ausdrückliche **Timezone** wie `Asia/Tokyo` fest. Lassen Sie zwischen Läufen mehr Zeit als die Dauer einer manuellen Sicherung plus Zeit zur Fehleruntersuchung. Prüfen Sie mindestens drei kommende Läufe und notieren Sie **Cron pattern**.
4. Notieren Sie auch die Browserzeitzone. Die Regel läuft in der gewählten Zeitzone, die Vorschau zeigt Zeiten jedoch in der Browserzeitzone; derselbe Zeitpunkt kann daher andere Uhrzeiten zeigen. Die Vorschau prognostiziert Termine und beweist keinen späteren Sicherungslauf.
5. Lassen Sie die Zeile **Disabled** und wählen Sie **Save**. Öffnen Sie den Job erneut und prüfen Sie Zeitplan-ID, Regel, Zeitzone, Aufbewahrung, VM und Remote. Job und Zeitplan werden getrennt gespeichert; bei Fehlern können Teiländerungen verbleiben. Fahren Sie erst fort, wenn alles stimmt.
6. Aktivieren Sie zurück in **Overview** nur diesen Zeitplan über seine Zustandsschaltfläche. Die Schaltfläche wirkt sofort; es gibt kein separates Speichern. Aktualisieren Sie und prüfen Sie **Enabled** in der Zeile.
7. Warten Sie ohne manuelle Ausführungsschaltfläche auf den nächsten Lauf. Öffnen Sie seine Details und prüfen Sie Job-/Zeitplan-IDs, Start-/Endzeiten, VM und Exportergebnis. Prüfen Sie unter **Restore** einen neuen Punkt auf dem richtigen Remote.
8. Warten Sie auf mindestens drei erfolgreiche Läufe dieses Zeitplans und vergleichen Sie nach jedem die Punktzeiten. Bei Aufbewahrung `2` sollten die beiden neuesten vollständigen Sicherungen dieser VM für diesen Zeitplan verbleiben. Prüfen Sie die tatsächliche Liste: Nehmen Sie keine Dateianzahl an und zählen Sie weder übersprungene noch fehlgeschlagene Läufe.
9. Deaktivieren Sie vor dem nächsten geplanten Lauf den Zeitplan in **Overview** und aktualisieren Sie zur Prüfung von **Disabled**. Das verhindert künftige Läufe, bricht jedoch eine laufende Sicherung nicht ab (die Abbruchschaltfläche ist in dieser Version deaktiviert). Lassen Sie eine laufende Sicherung fertig werden und prüfen Sie, dass zur nächsten geplanten Zeit nichts startet.
10. Stellen Sie einen Punkt eines geplanten Laufs nach Abschnitt 4 und 5 wieder her: gestoppte Kopie, vor dem ersten Start alle NICs entfernt, Prüfsumme verglichen, Kopie heruntergefahren. Entfernen Sie die Kopie nach dem [VM-Entfernungsverfahren](/docs/xoa-hl/vm-operations/). Notieren Sie abschließenden Zeitplanzustand, verbliebene Punkte und Wiederherstellungsergebnis.

**Gut zu wissen**

- Ist **Delete first** aus, schreibt ein Lauf zuerst die neue Sicherung und löscht dann alte. Schlägt das Löschen fehl, kann der Lauf trotz vorhandener neuer Sicherung als fehlgeschlagen erscheinen. Prüfen Sie vor erneutem Versuch die tatsächlichen Punkte und testen Sie eine Wiederherstellung, bevor Sie sich auf einen Punkt verlassen.
- Aufbewahrung zählt Sicherungen je VM, Modus und **Zeitplan-ID auf jedem Remote**. Sie zählt keine Tage, Namen oder Dateien. Ein anderer Zeitplan behält eigene Punkte. Ein gelöschter und neu erstellter Zeitplan erhält eine neue ID; alte Sicherungen fallen dadurch nicht unter die neue Richtlinie.
- Ein Start während eines noch laufenden identischen Jobs kann abgelehnt werden. Während abgeschalteter Appliance verpasste Läufe werden später nicht nachgeholt.
- Deaktivieren, Bearbeiten oder Löschen eines Jobs bricht eine laufende Sicherung nicht ab.

**Fehlt ein Lauf oder schlägt er fehl**, sichern Sie Job-, Zeitplan- und Remote-IDs, erwartete und tatsächliche Zeiten, Fehler und Punkteliste. Gehen Sie bis zur Klärung davon aus, dass weiterhin ein automatischer Lauf starten kann. Prüfen Sie Serverbetrieb und Uhrzeit, danach Aktivierung, VM-Auswahl, Remote-Zugriff und freien Platz. Führen Sie den Job nach Behebung einmal manuell ohne andere laufende Jobs aus, prüfen Sie den neuen Punkt und testen Sie eine Wiederherstellung vor erneuter Zeitplanaktivierung.

Nicht behandelt: E-Mail-Warnungen, Sommerzeitwechsel, Wiederherstellung nach Ausfall, Langzeitaufbewahrung und produktive Aufbewahrungsrichtlinien.

## Inkrementelle Sicherungen verwenden {#delta-backups}

Eine inkrementelle (Delta-)Sicherung kopiert nur Änderungen seit der vorherigen Sicherung. Dieser Test erstellt einen separaten Delta-Job, erzeugt drei Wiederherstellungspunkte und prüft, dass ein älterer Punkt nach der Aufbewahrungsbereinigung weiterhin wiederherstellbar ist. Führen Sie ihn nach erfolgreicher vollständiger Sicherung und Wiederherstellung oben aus und behalten Sie diese vollständige Sicherung.

**Vor dem Beginn**

- Test-VM mit gewöhnlichen virtuellen Festplatten verwenden: keine gemeinsam genutzten oder durchgereichten Festplatten und keine Arbeitsspeichersicherung. VM- und Festplatten-UUIDs (VDIs), Größen sowie Pfad und Prüfsumme der Beispieldatei notieren. Festplatten während des Tests nicht ändern.
- Speicherverantwortlichen um einen neuen leeren NFS-Export bitten und als separates Remote hinzufügen, beispielsweise `lab-delta-nfs`.
- Platz für Snapshots auf dem Quell-SR, eine vollständige Sicherung plus spätere Änderungen auf dem Remote und wiederhergestellte Kopien auf einem beschreibbaren SR reservieren.
- Administratorkonto verwenden. Fehlen **Delta Backup** oder dessen Einstellungen in Ihrer Installation, anhalten und die sichtbare Version melden. Nicht die Lizenz ändern oder Anweisungen für XO 6 mit seiner anderen Oberfläche folgen.

Ein Delta-Punkt benötigt seine Metadaten und die Kette übergeordneter Festplattendateien (VHD). Eine einzelne VHD-Datei ist keine VM-Sicherung. Die vollständige Sicherung des Tutorials kann nicht die Basis dieser neuen Kette sein.

### Delta-Job erstellen {#create-the-delta-job}

1. Fügen Sie das Remote wie in Abschnitt 1 hinzu und testen Sie es. Öffnen Sie **Backup → New → VMs** (`/#/backup/new/vms`), nennen Sie den Job `lab-delta-chain`, wählen Sie nur die Test-VM und lassen Sie die intelligente Auswahl aus.
2. Wählen Sie nur **Delta Backup**. Lassen Sie **Backup**, **Rolling Snapshot**, **Disaster Recovery** und **Continuous Replication** aus. Wählen Sie nur `lab-delta-nfs` und lassen Sie **Delete first** aus. Bearbeiten Sie nicht den vorherigen vollständigen Job.
3. Setzen Sie unter **Advanced settings** das **Full backup interval** auf `2`. Lassen Sie **Use NBD to transfer disk if available** und **Purge snapshot data when using CBT.** aus. Aktivieren Sie **Merge backups synchronously**. Lassen Sie übrige erweiterte Optionen ungenutzt und löschen Sie niemals von diesem Job behaltene Snapshots.
4. Fügen Sie einen Zeitplan mit **Backup retention** `2`, ausdrücklicher Zeitzone und geprüfter Vorschau hinzu. Lassen Sie **Force full backup** aus: Es macht jeden Lauf zu einer vollständigen Sicherung. Langzeitaufbewahrung auslassen. Zeitplan deaktivieren und speichern. Job erneut öffnen, jede Einstellung prüfen und Job-, Zeitplan- und Remote-IDs notieren. Zeitplan während des gesamten Tests deaktiviert lassen.

**Full backup interval** bestimmt die Kettenlänge. Bei `2` erstellt ein neuer Job eine vollständige, dann eine inkrementelle und anschließend wieder eine vollständige Sicherung. Es ist weder eine Tagesanzahl noch die Zahl aufbewahrter Punkte. Fehlende Vorgänger, geänderte Festplatten oder Fehler können die Reihenfolge ändern; prüfen Sie daher die Protokolle.

### Drei Wiederherstellungspunkte erstellen {#make-three-restore-points}

Schreiben Sie vor jedem Lauf die Beispieldatei im Gast und fahren Sie ihn regulär herunter. Starten Sie jeden Lauf manuell und nur ohne laufende Sicherung oder Zusammenführung. Notieren Sie pro Lauf Lauf-ID, Zeit, Export-**Type**, Warnungen und neuen Punkt. Prüfen Sie alle Aufgabenstatus und Seiten und sichern Sie nötigenfalls das rohe JSON.

| Lauf | Im Gast vor dem Herunterfahren | Erwartetes Ergebnis |
| --- | --- | --- |
| 1 | Version A schreiben und Prüfsumme A notieren | Vollständiger Export; Punkt A aufgeführt |
| 2 | VM starten, Version B schreiben, Prüfsumme B notieren, herunterfahren | Inkrementeller Export; Punkt B aufgeführt. B vor Lauf 3 wiederherstellen (unten) |
| 3 | VM starten, Version C schreiben, Prüfsumme C notieren, herunterfahren | Vollständiger Export (Intervall `2`); Bereinigung prüfen, Punkte B und C bleiben |

Die Wiederherstellungsliste kann den Punkt eines Delta-Jobs auch bei vollständigem Export als **incremental** bezeichnen. Prüfen Sie Export-**Type** im Protokoll, nicht diese Bezeichnung oder Dateigröße. War Lauf 2 vollständig, bewahren Sie die Nachweise auf, prüfen Sie Vorgänger-Snapshots, Festplatten, Intervall und **Force**-Einstellungen und zählen Sie ihn nicht als inkrementelle Übertragung. Löschen Sie niemals einen Vorgänger, um den Test zu erzwingen.

### Inkrementellen Punkt vor und nach der Bereinigung wiederherstellen {#restore-an-incremental-point-before-and-after-cleanup}

1. Wählen Sie unter **Backup → Restore** (`/#/backup/restore`) Punkt B auf `lab-delta-nfs` und ein beschreibbares SR mit genügend Platz. Schließen Sie **jede Festplatte** ein: Der Dialog erlaubt das Überspringen von Festplatten; prüfen Sie daher jede.
2. Lassen Sie **Start VM after restore** und **Use differential restore** aus. Aktivieren Sie **Generate new MAC addresses**. Differenzielle Wiederherstellung verwendet Quell-Snapshots erneut und ist ein anderer Test.
3. Isolieren und prüfen Sie die Kopie wie in Abschnitt 4 und 5: neue UUIDs notieren, gestoppt lassen, **jede** NIC entfernen, starten und die Datei in der Konsole mit Prüfsumme B vergleichen. Regulär herunterfahren. Kopie nach dem [VM-Entfernungsverfahren](/docs/xoa-hl/vm-operations/) entfernen.
4. Stellen Sie nach Lauf 3 und seiner Bereinigung Punkt B erneut als neue isolierte Kopie wieder her und prüfen Sie Prüfsumme B. Stellen Sie Punkt C separat wieder her und prüfen Sie Prüfsumme C. Dies beweist die Funktionsfähigkeit des älteren inkrementellen Punkts nach der Aufbewahrung. Verbleibende Punkte notieren und Zeitplan deaktiviert lassen.

**Gut zu wissen**

- Aufbewahrung wählt Punkte dieser VM und dieses Zeitplans auf diesem Remote. Zusammenführungsgrenzen oder fehlgeschlagene Bereinigung können zusätzliche Punkte belassen.
- Bei ausgeschaltetem **Delete first** werden alte Punkte nach der Übertragung gelöscht. Die Bereinigung vor einem Lauf kann trotzdem Daten zusammenführen oder löschen.
- Synchrone Zusammenführung macht einen Lauf nicht atomar und beweist keine funktionierende Wiederherstellung.
- Sicherungs-JSON- oder VHD-Dateien niemals manuell löschen, umbenennen, verschieben oder bearbeiten und Snapshots niemals zum Aufräumen einer Kette löschen.

**Schlägt etwas fehl** (fehlender Vorgänger, Übertragungs- oder Zusammenführungsfehler, fehlgeschlagene Wiederherstellung), sichern Sie Lauf-JSON, Punkt-IDs und eine Liste unvollständiger VMs und Festplatten. Führen Sie den Job nicht weiter aus, da jeder Lauf die Kette verändern kann. Korrigieren Sie Zugriff, Platz oder Zuständigkeit mit dem Sicherungsverantwortlichen und wiederholen Sie den Test. Verwenden Sie Dienstneustarts, Erzwingen oder Reparaturaktionen nicht als allgemeine Lösung. Ist keine Wiederherstellung möglich, behalten Sie die unabhängige vollständige Sicherung und lassen Sie den Vorfall offen.

Nicht behandelt: laufende Gäste, NBD und CBT, verschlüsselte oder andere Remotes, differenzielle Wiederherstellung und Wiederherstellung bei echten Ausfällen.

## Einzelne Datei aus einer Delta-Sicherung wiederherstellen {#file-restore}

Laden Sie eine Datei aus einem Delta-Punkt auf Ihren Computer herunter. Dieser Test verwendet Punkt B des obigen inkrementellen Tests nach erfolgreicher VM-Wiederherstellung. Er legt die Datei nicht wieder in der VM ab. Die vollständigen Sicherungen des Tutorials erscheinen auf dieser Seite nicht.

**Vor dem Beginn**

- Linux-Test-VM mit einer Festplatte und einer gewöhnlichen lesbaren Partition verwenden.
- Vor Sicherung B Pfad, Inhalt und SHA-256 einer kleinen Beispieldatei notieren, etwa `/home/lab/recovery-b.txt`.
- Punkt B und seine Kette auf dem Remote behalten. Ausreichend Platz für das Archiv auf Ihrem Computer sicherstellen.
- Administratorkonto verwenden und prüfen, dass **File Restore** in Ihrer Installation existiert.
- Für diesen ersten Test produktive VMs, private Daten, verschlüsselte oder RAID-Volumes, symbolische Links und Ordner vermeiden. Dieser Test beweist keine Unterstützung sämtlicher Dateisysteme, LVM-Anordnungen oder Remotes.

1. Öffnen Sie **Backup → File Restore** (`/#/backup/file-restore`). Suchen Sie die Test-VM und öffnen Sie ihre Dateiwiederherstellungsaktion. Klicken Sie nicht auf benachbarte Löschschaltflächen. Fehlt VM oder Punkt, aktualisieren Sie und prüfen Sie, dass `lab-delta-nfs` aktiviert ist. Wechseln Sie nicht zur früheren vollständigen Sicherung.
2. Wählen Sie **Punkt B** anhand von Zeit und Job, dann die Festplatte. Warten Sie auf die Partitionssuche und wählen Sie die Partition der Beispieldatei. Eine Festplatte ohne Partitionstabelle kann ihr Dateisystem direkt anzeigen. Scheitert die Suche, halten Sie an: Sicherungsdateien nicht manuell einhängen oder bearbeiten.
3. Navigieren Sie von `/` zur Beispieldatei und wählen Sie **nur diese Datei**. Verwenden Sie weder Ordnerauswahl noch Alles-auswählen. Prüfen Sie den Pfad und behalten Sie **tgz** (Standard; **zip** funktioniert ebenfalls, kann aber langsamer sein). Starten Sie den Download und warten Sie auf Browser-Abschluss. Ein blockiertes Pop-up oder unvollständiger Download ist kein Erfolg.
4. Notieren Sie auf Ihrem Computer Archivname, Größe und SHA-256. Listen Sie den Inhalt auf, entpacken Sie nur die Beispieldatei in einen neuen leeren Ordner und vergleichen Sie Inhalt und SHA-256 mit Version B. Behandeln Sie Archivpfade als nicht vertrauenswürdig und entpacken Sie niemals über laufende Daten. Ursprüngliche VM, Punkt B und Zeitplan unverändert lassen.

**Prüfung:** Das Archiv lässt sich öffnen, enthält nur die Beispieldatei und diese entspricht Prüfsumme B. Ein passender Dateiname oder Inhalt von Version C ist keine Übereinstimmung.

Scheitert ein Schritt, bewahren Sie die Nachweise auf und stoppen Sie weitere Sicherungsläufe, bis der Sicherungsverantwortliche sie untersucht hat. Löschen Sie keine Kettendateien, Quell-Snapshots oder Teildateien, um einen Punkt erscheinen zu lassen. Das Zurückkopieren der wiederhergestellten Datei in einen Gast ist eine separate Aufgabe, die die Zustimmung des Verantwortlichen benötigt.

## VM in einen anderen Pool kopieren (DR-Replikat) {#dr-replica}

**Disaster Recovery** (DR) kopiert eine ganze VM auf ein SR in einem anderen Pool. Dies unterscheidet sich von NFS-Sicherung und **Continuous Replication** (CR), die nur Änderungen überträgt. Die Kopie, Replikat genannt, bleibt gestoppt und ist gegen Starten gesperrt. **Entsperren oder starten Sie das Replikat nicht.** Zur Nutzung klonen Sie es. Dieser Test prüft einen solchen Klon an einem isolierten Ort. Automatisches Failover, Ausfall des Quellpools und Rückkehr (Failback) werden nicht getestet.

**Vor dem Beginn**

- Test-VM auf Pool A und zweiten Testpool B unter derselben XOA-HL-Appliance verwenden.
- Verantwortlichen von Pool B um ein dediziertes beschreibbares SR `lab-dr-sr` mit Platz für zwei vollständige Kopien und einen Klon bitten. Es muss auf anderem Speicher als Pool A liegen und darf keine ISO-Bibliothek sein. UUIDs beider Pools und SRs, freien Platz und SR-Erreichbarkeit der Hosts notieren.
- Unabhängige NFS-Sicherung aus dem Tutorial behalten.
- VM mit einer Festplatte ohne gemeinsame oder durchgereichte Festplatten verwenden. Vor jedem Lauf Beispieldatei schreiben (A, dann B, dann C), SHA-256 notieren und Gast regulär herunterfahren.
- Konsolenzugriff und einen Ort auf Pool B **ohne produktives Netzwerk** planen. Vor dem Start alle NICs des Klons entfernen.
- Fehlen DR oder Ziel-SR in Ihrer Installation, anhalten.

1. Öffnen Sie **Backup → New → VMs** (`/#/backup/new/vms`) und erstellen Sie Job `lab-dr-full`. Wählen Sie nur die Test-VM, intelligente Auswahl auslassen. Nur **Disaster Recovery** wählen; **Backup**, **Delta Backup**, **Continuous Replication** und **Rolling Snapshot** auslassen. Unter **Target SRs (for replication)** nur `lab-dr-sr` wählen. **Delete first** auslassen, damit alte Replikate nicht vor der Übertragung entfernt werden. Andere Jobs nicht bearbeiten.
2. Einen Zeitplan mit **Replication retention** `2`, ausdrücklicher Zeitzone und geprüfter Vorschau hinzufügen. Snapshot-Aufbewahrung und Zustandsprüfungen ungenutzt lassen. Zeitplan deaktivieren und speichern. Job erneut öffnen und VM, Ziel-SR, Modus, Aufbewahrung, deaktivierten Zustand und IDs prüfen.
3. Bei geschriebener Beispieldatei A und heruntergefahrenem Gast den Job einmal aus **Backup → Overview** ausführen. Alle Aufgaben und Warnungen prüfen. Auf Pool B das neue **gestoppte** Replikat anhand UUID, Job und Zeit im Namen, Kennzeichnung **Disaster Recovery** und Festplatte finden. Nicht starten.
4. Mit Beispieldatei B, dann C wiederholen, jeweils nach vollständigem Abschluss des vorigen Laufs. Lauf-/Replikat-IDs, Zeiten, Festplatten und Fehler notieren. Nach Lauf 3 verbliebene Replikate prüfen: normalerweise B und C. Ein grüner Job beweist keine korrekten Daten, und fehlgeschlagenes Löschen wird nicht rückgängig gemacht.
5. Das **Replikat B** wählen, nicht Quell-VM, Replikat C oder einen NFS-Punkt. Einen **Fast clone** mit eindeutigem Namen auf Pool B erstellen; Replikat gestoppt lassen. Neue VM- und Festplatten-IDs des Klons notieren und prüfen, dass er gestoppt und nicht gegen Starten gesperrt ist. Scheitert das Klonen oder ist der Klon gesperrt, anhalten; Sperre nicht umgehen.
6. **Jede** NIC aus dem gestoppten Klon entfernen und leere Netzwerkliste prüfen. Nur den Klon starten, Konsole öffnen und Beispieldatei mit Prüfsumme B vergleichen. Regulär herunterfahren. Ein Klon von C lässt sich genauso testen.
7. Replikate B und C sowie NFS-Sicherung behalten. Nur Testklone nach dem [VM-Entfernungsverfahren](/docs/xoa-hl/vm-operations/) entfernen.

**Prüfung:** Drei vollständige Läufe erreichten richtigen Pool und SR; B und C bleiben erhalten oder Abweichungen lassen sich erklären; der isolierte B-Klon hat eigene IDs, startete ohne NIC und enthält genau Beispieldatei B.

Scheitert Übertragung, Platzprüfung, Löschen, Klonen oder Datenprüfung, stoppen Sie weitere Läufe und geben Sie das Inventar an Sicherungs- und Speicherverantwortliche. Entfernen Sie niemals die Startsperre eines Replikats, löschen Sie keinen Punkt nur anhand seines Namens und löschen Sie keine vom Sicherungsjob verwalteten Snapshots.

Nicht behandelt: CR-Ketten, geplante Läufe, Netzwerkumschaltung, Verhindern doppelten VM-Betriebs, Failback und echte Ausfälle.

## Windows-Server-Sicherung über SMB testen {#smb-remote}

Testen Sie ein SMB-Remote mit vollständiger Sicherung und isolierter Wiederherstellung. Die XO-Oberfläche warnt, dass SMB-Remotes für **Windows Server** gedacht sind, und empfiehlt NFS für Linux Samba und die meisten NAS-Geräte. Dieser Test behandelt weder andere SMB-Server noch SMB-Speicher für ISOs oder VM-Festplatten, Cloud-Remotes oder produktive Nutzung. XO hängt die Freigabe über CIFS ein und das XOA-HL-Paket enthält `cifs-utils`; das Einhängen wurde aber noch nicht auf einer echten Appliance geprüft.

**Vor dem Beginn**

- Windows-Server-Administrator um eine **dedizierte Testfreigabe** auf anderem Speicher als Quell-VM und Appliance bitten, mit genügend Platz für Sicherung und Wiederherstellungstest.
- Dediziertes Konto anfordern, das Dateien dort erstellen, lesen und löschen kann, mit Netzwerkzugriff nur von der Appliance. Servername, Freigabename, optionalen Unterordner, Domäne und Zugangsdaten über sicheren Kanal beziehen.
- Passwort nur in sein eigenes Feld eingeben. XO erstellt eine interne Remote-URL mit Zugangsdaten; XO-Konfigurationsexporte daher als Geheimnisse behandeln. URL niemals teilen und keine Zugangsdaten in Screenshot, Issue, Protokollauszug oder eigene Mount-Option aufnehmen.
- Unabhängige NFS-Sicherung aus dem Tutorial behalten. Dieselbe kleine gestoppte Test-VM mit einer Festplatte, neuer Beispieldatei und Prüfsumme verwenden. Beschreibbares SR und einen nur per Konsole erreichbaren Ort für die Kopie reservieren.

1. Erstellen Sie unter **Settings → Remotes** (`/#/settings/remotes`) `lab-backup-smb` vom Typ **SMB**. Geben Sie unter **Address\\Share** Server und Freigabe getrennt durch einen Rückstrich ein. **Subfolder** ist ein optionaler Pfad innerhalb der Freigabe, kein zweiter Freigabepfad. Dedizierten Benutzernamen, Passwort und Domäne eingeben (das Formular beginnt mit `WORKGROUP`; Wert des Administrators verwenden). **Custom mount options**, Proxy und Verschlüsselung auf Standardwerten lassen. Speichern und Remote-ID, Aktivierung, Typ, Server, Freigabe, Unterordner und Fehleranzeige prüfen. Das Passwort bleibt verborgen: Nicht versuchen, es aus der angezeigten URL zu lesen.
2. Führen Sie **Test your remote** auf diesem Remote aus. Der Test schreibt eine zufällige 10-MiB-Datei, liest sie zurück, vergleicht sie und versucht sie zu löschen. Erfolgssymbol, Ergebnis und jeden fehlgeschlagenen Schritt prüfen. Bei Fehler den Administrator anhand des genauen Namens nach einer verbliebenen `.test`-Datei suchen lassen. Ein bestandener Test beweist nur diesen Schreib-/Lesezyklus, keine VM-Wiederherstellung oder dauerhafte Geschwindigkeit.
3. Erstellen Sie unter **Backup → New → VMs** (`/#/backup/new/vms`) einen separaten Job `lab-smb-full`: nur gestoppte Test-VM, nur Modus **Backup** (vollständig), nur Ziel-Remote `lab-backup-smb` und **Delete first** aus. Einen Zeitplan mit ausdrücklicher Zeitzone und **Backup retention** `2` hinzufügen, deaktiviert lassen, speichern und IDs prüfen. NFS-Job nicht ändern.
4. Führen Sie den deaktivierten Zeitplan einmal manuell aus **Backup → Overview** aus. VM-Export und Remote-Ergebnis im Protokoll prüfen, danach unter **Backup → Restore** den vollständigen Punkt auf `lab-backup-smb` finden. Zeiten, IDs, Größe und SMB-Mount-, Anmelde- oder Platzfehler notieren. Ein verbliebener Snapshot auf Quell-SR oder bestandener Remote-Test ist keine VM-Sicherung.
5. Stellen Sie diesen Punkt auf das reservierte SR mit ausgeschaltetem **Start VM after restore** wieder her. Neue VM- und Festplatten-UUIDs notieren. An gestoppter Kopie **jede NIC** entfernen und leere Netzwerkliste prüfen. Nur diese Kopie über **Console** starten, Beispieldatei-Prüfsumme vergleichen und herunterfahren. Ursprüngliche VM, NFS-Sicherung und SMB-Punkt behalten, bis das Ergebnis erfasst ist. Anschließend nur Testkopie nach dem [VM-Entfernungsverfahren](/docs/xoa-hl/vm-operations/) entfernen.

**Prüfung:** Der Remote-Test besteht, die vollständige Sicherung erreicht die Freigabe und die isolierte Kopie startet ohne NIC mit korrekten Daten.

Scheitert Zugriff, Schreiben, Lesen, Löschen, Export oder Wiederherstellung, halten Sie an. Geben Sie Sicherungs- und Serververantwortlichen Fehler ohne Zugangsdaten, genaue IDs, Freigabeinhalte und unvollständige VMs. Wiederholen Sie niemals gegen eine produktive Freigabe und löschen Sie keine Sicherungspfade nur anhand des Namens.

Nicht behandelt: Passwortrotation, Freigabeausfälle, Aufbewahrung über viele Läufe, Domänenvertrauen, SMB-Versionen und Sicherheitseinstellungen, Geschwindigkeit sowie andere SMB-Server.

## Bei Problemen {#if-something-goes-wrong}

| Problem | Prüfung |
| --- | --- |
| Der NFS-Test scheitert | Erreichbarkeit des Servers von der Appliance, Exportpfad, Exportberechtigungen und Mount-Optionen prüfen. Browser-Erreichbarkeit des NAS reicht nicht. |
| Sicherung scheitert oder kein Punkt erscheint | VM- und Exportprotokolle lesen. Remote-Zugriff, freien Platz dort und auf dem VM-SR sowie ausgewählte VM prüfen. Ein verbliebener Snapshot ist keine Sicherung. |
| Wiederherstellungspunkt fehlt | Remote auf Aktivierung ohne Fehler prüfen, Liste aktualisieren und tatsächlichen Export dieser VM durch den Job prüfen. |
| Wiederherstellung scheitert | Protokoll lesen und Lesbarkeit des Remote sowie Platz und Host-Erreichbarkeit des Ziel-SR prüfen. Vor neuem Versuch nach unvollständiger VM suchen. Niemals nur nach Namen löschen. |
| DR-Replikat oder Klon scheitert | Lauf-, VM- und Festplatten-IDs, Ziel-SR-Platz und -Zugriff sowie Sperrzustand notieren. Replikate gestoppt lassen. Startsperre nicht umgehen und Aufbewahrung nicht blind erneut ausführen. |
| SMB-Remote oder Wiederherstellung scheitert | Mit Windows-Server-Verantwortlichem fehlgeschlagenen Testschritt, Job-/Wiederherstellungsprotokolle, Server und Freigabe, Kontozugriff, freien Platz und Teilobjekte prüfen. Unabhängige NFS-Sicherung behalten. Niemals Zugangsdaten in einen Bericht einfügen. |
| Wiederhergestellte VM hat kein Netzwerk | Erwartet: Für diesen Konsolentest wurden alle NICs entfernt. Produktive Netzwerkanbindung benötigt eine separate Prüfung von Gast-IP-Adresse und Dienstidentitäten. |
| Datei weicht ab oder Gast startet nicht | Richtigen Punkt und Schreiben der Datei vor der Sicherung prüfen. Protokolle und Sicherung behalten. Der Test ist nicht bestanden. |

Für Laufstatus, Teilexporte und sicheren neuen Versuch siehe [Fehlgeschlagene Sicherung untersuchen](/docs/xoa-hl/troubleshooting/#backup-failures).

## Nächste Schritte {#next-steps}

Entscheiden Sie nach erfolgreichem Wiederherstellungstest über tatsächliche Sicherungshäufigkeit, Aufbewahrung, Kapazitätsüberwachung und Anwendungskonsistenz der Sicherungen. Aktivieren Sie einen Zeitplan erst nach Prüfung von Zeitzone und nächsten Läufen. Siehe auch [Update-Anleitung](/docs/guides/updates/) und [Glossar](/docs/xoa-hl/glossary/). Konfigurationswiederherstellung und Continuous Replication benötigen eigene Verfahren.

{{< details title="Quellen" closed="true" >}}
- **Zeitpläne**: [Zeitplaneditor, Tabelle und Speicherreihenfolge](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [Zeitauswahl und Vorschauformatierung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/scheduling.js), [Zeitplan-API, Start und Stopp](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/scheduling.mjs), [Cronjob-Verhalten](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/cron/index.js), [Schutz vor parallelen Jobs und Protokollidentität](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/jobs/index.mjs), [Aufbewahrung vollständiger Sicherungen und Bereinigungsreihenfolge](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs).
- **Sicherung und Wiederherstellung**: [Sicherungsrouten und Administratorzugriff](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/index.js), [Remote-Formular](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [Remote-Test](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/index.js), [Jobmodi und Speichern](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [Zeitplan und Aufbewahrung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [Manueller Lauf](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/overview/tab-jobs.js), [Wiederherstellungsbedienelemente](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/restore-backups-modal-body.js), [NIC-Entfernung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [Festgelegte Upstream-Version](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/UPSTREAM_XO), [Patch- und Build-Auswahl](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
- **Inkrementelle Sicherungen**: [Inkrementeller Export und Basisauswahl](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/IncrementalXapi.mjs), [Remote-Übertragung und Aufbewahrung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/IncrementalRemoteWriter.mjs), [Snapshot-Aufbewahrung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/_AbstractXapi.mjs), [Bereinigungs- und Zusammenführungsausführung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_MixinRemoteWriter.mjs), [Lesen der Wiederherstellungskette](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [Wiederherstellungsimplementierung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/ImportVmBackup.mjs), [Exporttyp in Protokollen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js).
- **Wiederherstellung einzelner Dateien**: [Dateiwiederherstellungsoberfläche und Delta-Filter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/index.js), [Auswahl von Sicherung, Festplatte, Partition und Datei](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/file-restore/restore-file-modal.js), [Administrator-Datei-APIs und Archivantwort](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/backup-ng.mjs), [Schreibgeschützte Partition und tgz/zip-Adapter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/RemoteAdapter.mjs), [Browserdownload](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
- **DR-Replikat**: [Jobmodus, Ziel-SR und Zeitplan](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/index.js), [Aufbewahrungseinstellung für Replikation](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/new/new-schedule.js), [Vollständiger Export und SR-Schreibmodul](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_vmRunners/FullXapi.mjs), [Replikatimport, Startsperre und Bereinigung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullXapiWriter.mjs), [Replikat-Identitätsfilter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/_listReplicatedVms.mjs), [Klon-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **SMB-Remote**: [Remote-Formular und Windows-Server-Warnung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/remotes/remote.js), [SMB-Parser und Formatierer](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-remote-parser/src/index.js), [CIFS-Verarbeitung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/smb.js), [Mount- und Remote-Optionen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/_mount.js), [10-MiB-Remote-Test](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/fs/src/abstract.js), [Remote-Lebenszyklus](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/remotes.mjs), [XOA-HL-Laufzeitabhängigkeit](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
- **Bekanntes Problem**: [Überschriften der Remote-Testergebnisse (xoa-hl#38)](https://github.com/Vagrantin/xoa-hl/issues/38).
{{< /details >}}
