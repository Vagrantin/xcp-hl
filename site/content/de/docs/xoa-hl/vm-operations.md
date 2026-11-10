---
title: "VMs verwalten: Konsole, Snapshots, Kopien, Arbeitsspeicher und Löschen"
linkTitle: "VMs verwalten"
description: "Konsole verwenden, VMs starten und stoppen, Snapshots erstellen, VMs kopieren, vergrößern und löschen."
weight: 40
translationKey: xoa-manual-vm-operations
translationStatus: reviewed
sourceRevision: sha256:8b4bb1976ace6e6ecdb9f020d03a69d61f3233f9989145281bbf60a598155abf
glossaryTerms: ["vm", "snapshot", "backup", "sr"]
---

Alltägliche VM-Aufgaben: Konsole verwenden, eine VM starten und stoppen, Snapshots erstellen und zurücksetzen, Klone und Kopien anlegen, CPU und Arbeitsspeicher ändern und eine VM löschen. Üben Sie jede Aufgabe als Administrator der **XOA-HL-Appliance** an einer Test-VM ohne Produktionsdaten. Bevor Sie eine wichtige VM ändern, stellen Sie eine unabhängige [Sicherung und eine getestete Wiederherstellung](/docs/xoa-hl/backup-restore/) sicher.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet. Spätere Versionen können abweichen.
{{< /callout >}}

**D3-Beobachtungen:** am 28.10.2026, XOA-HL `v5.113.2_e281c536-ce47` (`ca44911`) auf einem verschachtelten XCP-HL-v8.3-ce44-Host. Die Tests verwendeten entbehrliche Klone eines Gasts mit PV-Treibern, aber ohne Verwaltungsagenten. Das [Laborprotokoll](https://github.com/Vagrantin/xcp-hl/issues/198#issuecomment-6459388202) deckt die unten genannten Beobachtungen zu Betriebszustand, Snapshot und Zurücksetzen im angehaltenen Zustand, Fast clone, Datenträgern, Größenänderung und Löschen ab. Die übrigen Verfahren beruhen weiterhin auf einer Quellcodeprüfung. Die späteren D3-Ergebnisse zu Snapshots und Schutz sind unten verlinkt. Speicher-Snapshots, gemeinsam genutzte Datenträger und Fehler bei der Bereinigung wurden nicht getestet.

## VM-Konsole verwenden {#vm-console}

Die Konsole zeigt den VM-Bildschirm in Ihrem Browser. Sie benötigen die Berechtigung **operate** für die VM: Eine Viewer-Freigabe reicht nicht. Der Gast benötigt für die Konsole keine IP-Adresse, aber Ihr Browser muss die Appliance und diese den Host erreichen können. Behalten Sie die Netzwerkisolation der Test-VM bei.

1. Öffnen Sie **Console** der VM (`/#/vms/<id>/console`). Prüfen Sie die richtige VM und ihren Zustand **Running**. Bei jedem anderen Zustand, einschließlich pausiert oder suspendiert, zeigt die Registerkarte **Console is only available for running VMs.** Starten Sie die VM mit einer geplanten [Energieaktion](#vm-power); erzwingen Sie niemals einen Neustart nur für Konsolenzugriff.
2. Warten Sie auf den erwarteten Bildschirm, etwa eine Anmeldeaufforderung, den Installer oder eine bekannte Anwendung. Hier eingegebene Zugangsdaten gehören zum Gast, nicht zu XOA-HL oder zum Host.
3. Bewegen Sie den Zeiger in den Konsolenbereich, um Tastatur und Maus an den Gast zu senden. Bewegen Sie ihn hinaus, um sie samt XO-Tastenkürzeln zurückzuerhalten. Testen Sie die Eingabe mit einer harmlosen Zeichenfolge wie `console-test` in einem Texteditor im Testgast und löschen Sie diese danach. Testen Sie niemals in einem Shellbefehl oder Passwortfeld. Ein sichtbarer Bildschirm belegt keine funktionierende Eingabe.
4. Auf großen Bildschirmen beginnen die Zoomregler bei **100%**. Sie ändern die Anzeige im Browser, nicht die Bildschirmauflösung des Gasts, und können auf kleinen Bildschirmen verborgen sein. **Hide info** und **Show info** verbergen oder zeigen nur die XO-Kopfzeile; sie stoppen den Gast nicht und wechseln nicht in den Vollbildmodus.
5. Verlassen Sie danach die Registerkarte. Dies schließt die Konsolenverbindung, stoppt aber den Gast nicht. Wurde die VM während der Verbindung neu gestartet, öffnen Sie die Registerkarte erneut für einen aktuellen Bildschirm. XO bemerkt eine Trennung nach einem Neustart möglicherweise nicht; automatische Wiederverbindungsversuche belegen keinen gesunden Gast.

**Prüfung:** Sie sehen den richtigen laufenden Gast, die Testeingabe erreicht ihn, XO-Bedienelemente funktionieren nach Verlassen der Konsole wieder, und die VM ist weiterhin im erwarteten Zustand.

### Zwischenablage und Schaltflächen für externe Clients {#clipboard-and-remote-client-buttons}

- Das Zwischenablage-Textfeld sendet seinen Inhalt nach kurzer Pause an die Gast-Zwischenablage. **Copy** kopiert den Feldinhalt in die Zwischenablage Ihres eigenen Computers. Die Schaltfläche für mehrzeiligen Text öffnet **Send to clipboard**. Testen Sie mit harmlosem Text und prüfen Sie das Einfügen im Gast gesondert. Geben Sie weder Passwörter noch private Daten in das Feld oder in Bildschirmfotos ein.
- **SSH**, **SSH as…** und **RDP** öffnen den `ssh://`- beziehungsweise `rdp://`-Handler Ihres Computers mit der vom Gast gemeldeten IP-Adresse. Die Schaltflächen erscheinen, sobald eine IP-Adresse gemeldet wird. Dies belegt weder einen installierten Client noch einen laufenden Gastdienst oder ein durchlässiges Netzwerk. Diese Schaltflächen reparieren oder ersetzen die Konsole nicht.
- **Ctrl+Alt+Del** fragt nach Bestätigung und sendet diese Tastenkombination an den Gast. Je nach Gast kann das einen Neustart auslösen. Brechen Sie dies für diesen Test ab; es ist kein Verbindungstest. Die ISO-Auswahl ändert das eingehängte Gastmedium: Lesen Sie vor einer Änderung [Erste VM erstellen](/docs/xoa-hl/create-vm/).

### Leere oder nicht reagierende Konsole beheben {#fix-a-blank-or-unresponsive-console}

1. **Die VM läuft nicht oder die Konsole ist deaktiviert.** Lesen Sie zuerst Zustand und Meldung. Eine laufende VM mit `disable_pv_vnc=1` zeigt **Console is disabled for this VM** statt des Bildschirms. Fragen Sie den Verantwortlichen dieser Einstellung, bevor Sie die VM ändern. Werkzeuginstallation oder Neustart aktiviert die Konsole nicht wieder.
2. **Die Verbindung öffnet sich nie oder bricht laufend ab.** Prüfen Sie Ihre operate-Berechtigung und die Hostverbindung. Suchen Sie in den Browser-Entwicklerwerkzeugen die WebSocket-Anfrage mit Endung `/api/consoles/<id>` und notieren Sie Fehler beziehungsweise Status. Ein vorgeschalteter Reverse-Proxy muss WebSocket-Upgrades erlauben, nicht nur normale Seitenanfragen. Prüfen Sie Browser-zu-Appliance-Zugriff einschließlich TLS getrennt vom Appliance-zu-Host-Zugriff. Gast-IP, SSH-Server und Gast-Firewall gehören nicht zum Konsolenpfad. Beheben Sie das Problem mit dem Verantwortlichen dieses Pfads. Veröffentlichen Sie niemals einen VNC-Port und deaktivieren Sie Zertifikatsprüfungen nicht als schnelle Behelfslösung.
3. **Die Verbindung öffnet sich, aber der Bildschirm bleibt leer oder eingefroren.** Prüfen Sie die richtige VM, den erwarteten Bildschirminhalt und kürzliche Energieaktionen. Öffnen Sie die Registerkarte nach einem Neustart erneut. Ein leerer Bildschirm kann vom Gast oder der Verbindung stammen; sichern Sie daher die Beobachtung vor einer gastspezifischen Maßnahme. Starten Sie die VM nicht wiederholt neu, installieren Sie sie nicht neu und ändern Sie ihr Startmedium nicht bloß wegen eines schwarzen Bildschirms.
4. **Der Bildschirm funktioniert, Eingabe oder Zwischenablage jedoch nicht.** Bewegen Sie den Zeiger aus der Konsole und wieder hinein und wiederholen Sie den Editortest. Prüfen Sie, ob Browser oder Betriebssystem Tasten abfangen und ob der Gast den Zwischenablagevorgang unterstützt. Behandeln Sie SSH- und RDP-Probleme gesondert. Nennen Sie in Ihrem [Problembericht](/docs/xoa-hl/troubleshooting/#report-a-problem) Browser und Version, VM- und Host-IDs, Zeitpunkt, Betriebszustand, genaue Meldung und Verbindungsfehler ohne private Daten. Halten Sie rohe Browseraufzeichnungen privat: Cookies, Token, Zwischenablagetext und Gastbildschirme können sensibel sein.

## VM starten, stoppen und neu starten {#vm-power}

Öffnen Sie zuerst den Reiter **General** der VM (`/#/vms/<id>/general`) und prüfen Sie, ob ein Verwaltungsagent erkannt wird. Ohne ihn kann XO den Gast weder sauber herunterfahren noch neu starten. Siehe [Status und Installation der Gastwerkzeuge](/docs/xoa-hl/guest-tools/#guest-tools-status).

Beim einzigen Gast ohne Verwaltungsagenten im D3-Durchlauf wartete ein sauberes Stoppen 1200 Sekunden und schlug dann mit `VM_SHUTDOWN_TIMEOUT` fehl. Die VM blieb **Running**. Ein Neustart wurde sofort mit "VM lacks feature" abgelehnt. Ein erzwungenes Stoppen setzte die VM innerhalb von Sekunden auf **Halted**.

Ist die VM angehalten, wählen Sie **Start** und prüfen Sie Zustand und Konsole. Installieren Sie vor einem sauberen Stoppen oder Neustart die Gastwerkzeuge und prüfen Sie den Agenten, oder fahren Sie den Gast von innen herunter. Verwenden Sie ein erzwungenes Stoppen nur, wenn sich der Gast nicht herunterfahren lässt. Es entspricht dem Ziehen des Netzsteckers und kann Daten verlieren.

Lesen Sie jede Bestätigung, bevor Sie fortfahren. Klicken Sie während einer laufenden Aufgabe nicht erneut. Prüfen Sie danach VM-Zustand, Konsole und Anwendung. Eine Erfolgsmeldung beweist nicht, dass die Anwendung gesund ist.

## Snapshot, Klon, Kopie oder Sicherung? {#protection-types}

| Option | Nutzen und Grenze |
| --- | --- |
| Snapshot | Die VM zu einem Zeitpunkt, zusammen mit ihren Datenträgern gespeichert. Keine unabhängige Sicherung |
| Fast clone | Eine weitere VM, die Speicher mit dem Original teilt. Kein Schutz beim Verlust dieses Speichers |
| Full copy | Eine weitere VM mit kopierten Datenträgern auf einem gewählten SR. Daten, Ort und Isolation vor Verwendung prüfen |
| Backup | Eine getrennte Wiederherstellungskopie. Durch isolierte Wiederherstellung nachweisen |

Snapshots und Klone benötigen mit zunehmenden VM-Änderungen mehr Speicher. Prüfen Sie den freien SR-Platz und löschen Sie nur eindeutig identifizierte Testobjekte. Ein Snapshot einer laufenden VM ist nicht garantiert anwendungskonsistent.

## Snapshot einer angehaltenen VM erstellen <span class="hx:absolute" id="3-take-and-check-a-stopped-snapshot"></span> {#stopped-snapshot}

Verwenden Sie eine Test-VM mit gewöhnlichen Datenträgern (keine gemeinsam genutzten Datenträger oder durchgereichten Geräte) und funktionierender Konsole. Pausieren Sie Sicherungs- und Replikationszeitpläne und warten Sie auf laufende Aufgaben. Behalten Sie eine unabhängige Wiederherstellungskopie benötigter Daten. Snapshots laufender VMs, Arbeitsspeicher-Snapshots und Anwendungskonsistenz werden hier nicht behandelt.

1. Erstellen Sie im Gast eine harmlose Datei mit Inhalt `snapshot-A` und notieren Sie ihre Prüfsumme. Fahren Sie den Gast sauber herunter und prüfen Sie **Halted**.
2. Notieren Sie VM-UUID, jeden Datenträger (VDI) mit ID, SR und Größe, vorhandene Snapshot-UUIDs und freien SR-Platz. [Entfernen Sie anschließend jede Netzwerkschnittstelle (VIF) der Test-VM](/docs/xoa-hl/storage-networks/) und prüfen Sie die leere Liste. Verwenden Sie von nun an die Konsole.
3. Prüfen Sie jeden Datenträgernamen. Ein Datenträger mit `[NOSNAP]` im Namen kann von Snapshots ausgeschlossen sein; dies ist Teil des Datenträgernamens, kein VM-Tag. Ausgeschlossene Datenträger, gemeinsam genutzte Datenträger und durchgereichte Geräte benötigen ein anderes Verfahren. Benennen Sie Datenträger nicht um, um eine bestehende Richtlinie zu umgehen. Planen Sie Platz für den Snapshot, spätere Schreibvorgänge und den zusätzlichen Snapshot vor dem Zurücksetzen.
4. Öffnen Sie **Snapshots** (`/#/vms/<id>/snapshots`) und wählen Sie einmal **New snapshot**. Der Snapshot entsteht sofort ohne Namensabfrage. Der Standardname besteht aus VM-Name und Zeitstempel. Verwenden Sie nicht **New snapshot with memory**.
5. Warten Sie und aktualisieren Sie die Ansicht. Finden Sie die neue Zeile anhand von **Creation date** und kopieren Sie ihre UUID mit der Kopierschaltfläche der Zeile. Notieren Sie diese UUID: Name oder Zeitpunkt allein reichen nicht.
6. Setzen Sie **Name** auf `lab-snapshot-A` und **Description** auf eine kurze Testnotiz. Aktualisieren und prüfen Sie beide Werte. Vergleichen Sie Snapshot-Datenträger und SRs mit Ihren Aufzeichnungen; prüfen Sie Fehler und freien Platz. Snapshot-Datenträger erhalten neue IDs: Vergleichen Sie daher abgedeckte Datenträger und Größen, nicht deren IDs.

**Prüfung:** Ein identifizierter Snapshot deckt die vorgesehenen Datenträger ab; die Original-VM ist angehalten und ohne VIF.

Scheitert Erstellung oder Umbenennung, sichern Sie vor einem erneuten Versuch den Fehler sowie die tatsächlichen VM-, Snapshot- und Datenträgerlisten. Eine fehlende ID oder Benachrichtigung belegt nicht, dass nichts erstellt wurde; fehlgeschlagenes Umbenennen macht den Snapshot nicht rückgängig.

## Zu einem Snapshot zurückkehren <span class="hx:absolute" id="4-revert-only-the-test-vm"></span> {#snapshot-revert}

In D3 wurde ein Snapshot erstellt, während die Test-VM **Halted** war. Ein danach hinzugefügter Datenträger war nach dem Zurücksetzen verschwunden. Die VM blieb **Halted**, und der Snapshot blieb erhalten. Das belegt keine Konsistenz von Gastdateien oder Anwendungen.

Im [zweiten Snapshot-Test](https://github.com/Vagrantin/xcp-hl/issues/198#issuecomment-6460786269) wurde ein reiner Datenträger-Snapshot erstellt, während die VM **Running** war. Das Zurücksetzen auf die angehaltene VM brachte die VM wieder in den Zustand **Running**. Prüfen Sie VM und Netzwerkisolation vor dem Zurücksetzen: Ein Snapshot kann seinen gespeicherten Betriebszustand wiederherstellen. Ein Speicher-Snapshot (Suspend) wurde nicht getestet.

{{< callout type="warning" >}}
Das Zurücksetzen ersetzt den aktuellen VM-Zustand einschließlich Einstellungen, die alte Netzwerkschnittstellen zurückbringen können. Änderungen seit dem Snapshot können verloren gehen. Ein Snapshot, der bei laufender VM erstellt wurde, kann diese VM beim Zurücksetzen starten, selbst wenn das Objekt des reinen Datenträger-Snapshots als Halted erscheint. Prüfen Sie die Netzwerkisolation der VM, bevor Sie das Zurücksetzen bestätigen; verlassen Sie sich nicht auf den Betriebszustand des Snapshot-Objekts. Die folgende Übung verwendet nur diese isolierte Test-VM und einen im angehaltenen Zustand erstellten Snapshot. Prüfen Sie ihre VIFs erneut vor dem Start. Ein Snapshot auf demselben SR schützt nicht vor dessen Verlust.
{{< /callout >}}

1. Starten Sie die isolierte Test-VM, ändern Sie die Datei auf `snapshot-B` und notieren Sie die neue Prüfsumme. Fahren Sie sie sauber herunter und prüfen Sie **Halted**. Notieren Sie aktuelle Datenträger, VIFs und Snapshots.
2. Prüfen Sie anhand der UUID, dass der vorgesehene Snapshot `lab-snapshot-A` aus dem vorherigen Abschnitt ist. Es darf kein Snapshot eines Sicherungsauftrags oder einer anderen VM sein.
3. Wählen Sie unter **Snapshots** in dieser Zeile **Revert VM to this snapshot** und lesen Sie die Bestätigung **Revert your VM**. Lassen Sie **Snapshot before** aktiviert und prüfen Sie zuerst freien Platz. Diese standardmäßig aktivierte Option sichert vor dem Zurücksetzen den aktuellen Zustand in einem getrennten Snapshot. Dies ist keine unabhängige Sicherung und garantiert kein Zurückrollen. Brechen Sie ab, wenn VM, Isolation oder freier Platz unklar sind.
4. Bestätigen Sie einmal und warten Sie. Aktualisieren Sie die Ansicht und notieren Sie UUID des zurückgesetzten Snapshots, UUID des neuen Vorher-Snapshots, Betriebszustand, Datenträger, VIFs und Fehler. Scheitert der Vorher-Snapshot, fordert XO das Zurücksetzen nicht an. Scheitert das Zurücksetzen später, kann der Vorher-Snapshot bestehen bleiben. Prüfen Sie vor einem erneuten Versuch den tatsächlichen Zustand; deaktivieren Sie **Snapshot before** nicht, um einen ungeklärten Fehler zu umgehen.
5. Prüfen Sie vor dem Start **Halted** und eine leere VIF-Liste. Ist eine VIF zurückgekehrt, entfernen Sie sie bei angehaltener VM. Ein bei laufender VM erstellter Snapshot kann diese nach dem Zurücksetzen selbstständig starten oder fortsetzen; solche Snapshots werden hier nicht behandelt.
6. Starten Sie die VM und öffnen Sie die Konsole. Prüfen Sie Dateiinhalte `snapshot-A` mit ursprünglicher Prüfsumme sowie funktionierende Datenträger und Anwendung. Fahren Sie die VM herunter und notieren Sie das Ergebnis. Der zusätzliche Vorher-Snapshot enthält `snapshot-B`. Diesen Zustand zurückzuholen ist eine getrennte, kontrollierte Wiederherstellung, keine Rückgängig-Schaltfläche.

### Test-Snapshot löschen {#snapshot-cleanup}

Lassen Sie die VM angehalten, nachdem Sie das Ergebnis notiert und benötigte unabhängige Wiederherstellungskopien behalten haben. Löschen Sie nur einen Test-Snapshot, dessen UUID und Eigentümer Sie notiert haben.

1. Wählen Sie unter **Snapshots** in dieser Zeile **Remove this snapshot**. Lesen Sie **Delete snapshot** und bestätigen Sie ausschließlich diesen einen Snapshot. Verwenden Sie nicht **Remove selected snapshots**, löschen Sie keinen Snapshot eines Sicherungsauftrags und verwechseln Sie dies nicht mit **Remove** der VM.
2. Warten Sie und aktualisieren Sie Snapshots, VM-Datenträger und freien SR-Platz. Prüfen Sie, dass der Snapshot verschwunden ist, alle aufzubewahrenden Snapshots und die VM noch vorhanden sind und kein Fehler vorliegt.

Die Datenträgerbereinigung kann Fehler protokollieren, ohne den gesamten Löschvorgang scheitern zu lassen. Eine verschwundene Zeile oder Erfolgsmeldung belegt weder abgeschlossene Bereinigung noch sofort freigegebenen Platz. Notieren Sie verbliebene IDs und [melden Sie ungeklärte Überreste](/docs/xoa-hl/troubleshooting/). Löschen Sie vermeintlich verwaiste Datenträger niemals pauschal. Ein gelöschter Snapshot ist nicht wiederherstellbar.

## Isolierten Fast Clone erstellen {#fast-clone}

In D3 erzeugte die angehaltene VM einen Fast clone mit eigener Identität, einem Datenträger und einer übernommenen Netzwerkkarte. Der Klon startete, nachdem diese Netzwerkkarte entfernt wurde. Für einen laufenden Klon oder eine vollständige Kopie ist in diesem Durchlauf kein Ergebnis dokumentiert.

1. Wählen Sie bei einer angehaltenen Test-VM **Fast clone**. Finden Sie die neue VM (ihr Standardname endet auf `_clone`), notieren Sie ihre ID und benennen Sie sie um.
2. Lassen Sie den Klon angehalten, während Sie [jede geerbte Netzwerkschnittstelle entfernen](/docs/xoa-hl/storage-networks/) oder eine geprüfte Isolation außerhalb von XO einrichten. Eine neue MAC-Adresse ändert weder kopierte IP-Adressen noch Zugangsdaten oder Anwendungsidentitäten.
3. Starten Sie den Klon und prüfen Sie seine Konsole. Verbinden Sie ein Netzwerk erst nach Bereinigung duplizierter Identitäten und Prüfung der Isolation wieder.

Erscheint nach einem Fehler kein Klon, prüfen Sie vor einem erneuten Versuch Inventar und Aufgaben. Dies testet weder Livemigration, Arbeitsspeicher-Snapshots noch Wiederherstellung nach SR-Verlust.

### Vollständige Kopie im selben Pool erstellen {#full-copy}

Verwenden Sie **Copy**, nicht die eigene Aktion **Fast clone**, wenn Sie gewöhnliche Datenträgerkopien auf einem ausgewählten SR möchten. Der Kopierdialog bietet ebenfalls **Fast clone** an; lassen Sie hier **Full copy** ausgewählt. Weder Fast Clone noch vollständige Kopie im selben Pool sind eine unabhängige Sicherung oder getestete Notfallwiederherstellung.

1. Verwenden Sie eine Test-VM mit gewöhnlichen Datenträgern ohne gemeinsame Datenträger oder durchgereichte Geräte. Notieren Sie im Gast eine harmlose Datei und deren Prüfsumme. Fahren Sie ihn sauber herunter und prüfen Sie **Halted**. Notieren Sie VM-ID, ID, SR und Größe jedes Datenträgers, VIFs und Snapshots. Der Snapshot-Verlauf ist nicht Teil dieses Tests.
2. Finden Sie ein anderes beschreibbares **VM-Datenträger-SR im selben Pool**. Prüfen Sie ID, freien Platz und Erreichbarkeit für den Host, der die Kopie ausführen soll. Eine ISO-Bibliothek ist ungeeignet. Planen Sie Platz für Kopien und deren Wachstum: Der Dialog reserviert und prüft keinen Platz. Ist das Ziel-SR nicht verfügbar, beheben Sie vor dem Beginn den Speicherzugriff.
3. Wählen Sie auf der Quell-VM **Copy**. Setzen Sie in **Copy VM** den **Name** auf einen eindeutigen Testnamen wie `lab-vm-full-copy`. Die Vorgabe lautet `{name}_COPY`; ein leeres Feld behält den Originalnamen. Prüfen Sie die Auswahl **Full copy**.
4. Wählen Sie unter **Select SR** das SR anhand notierter ID und Pool, nicht anhand eines ähnlichen Namens. Andere Pools können in der Liste erscheinen; ihre Auswahl wechselt zu Export und Import, was dieser Test nicht behandelt. Lassen Sie **Compression** auf **Disabled**: Innerhalb eines Pools wird die Kopie nicht komprimiert.
5. Bestätigen Sie einmal und warten Sie auf die Aufgabe. Aktualisieren Sie die Ansicht und finden Sie die neue VM anhand ihrer eigenen ID und des gewählten Namens. Prüfen Sie **Halted**, Datenträgeranzahl, Größen, neue IDs und SR jedes Datenträgers. Prüfen Sie, dass Quell-VM und ihre Datenträger unverändert sind. Läuft die neue VM oder gibt es Abweichungen, halten Sie an und stellen Sie vor dem Fortfahren die Isolation wieder her.
6. Lassen Sie die neue VM angehalten, während Sie [jede geerbte VIF entfernen](/docs/xoa-hl/storage-networks/). Prüfen Sie vor dem ersten Start die leere Liste. Verlassen Sie sich nicht auf neue MAC-Adressen: Gast-IP-Adressen, Zugangsdaten und Anwendungsidentitäten werden kopiert.
7. Starten Sie ausschließlich die isolierte Kopie, öffnen Sie ihre Konsole und prüfen Sie Dateiprüfsumme, Datenträger und Anwendung. Bereinigen Sie duplizierte Identitäten vor jedem Netzwerkanschluss und lassen Sie das Original während der Prüfung isoliert oder angehalten.
8. Fahren Sie die Kopie herunter. Notieren Sie das Ergebnis und entfernen Sie mit [Test-VM löschen](#delete-vm) nur die Kopie samt Datenträgern. Behalten Sie Quelle und unabhängige Sicherungen.

Bei Fehler, Verbindungsverlust oder unterbrochener Anfrage sichern Sie vor dem nächsten Versuch Aufgabe, Fehler sowie VM-, Datenträger- und Snapshot-Listen beider Seiten. Eine unvollständige Kopie wird nicht automatisch zurückgesetzt; eine fehlende VM-ID belegt nicht, dass nichts erstellt wurde. Prüfen Sie Platz und Hostzugriff auf das SR, gleichen Sie genaue IDs ab und [melden Sie ungeklärte Überreste](/docs/xoa-hl/troubleshooting/). Wiederholen Sie niemals blind und löschen Sie vermeintlich verwaiste Datenträger nicht pauschal.

Nicht behandelt: Kopien laufender oder suspendierter VMs, Kopien in einen anderen Pool, Vorlagenkopien, gemeinsame oder durchgereichte Datenträger, Snapshot-Verlauf und Wiederherstellung nach SR-Verlust.

## CPU und Arbeitsspeicher ändern {#resize-vm}

Die Grenzen des Hosts werden beim Start der VM geprüft, nicht beim Speichern des Werts. Auf dem einzigen D3-Host gelang das Speichern von 64 vCPUs und 1 TiB Arbeitsspeicher bei einer angehaltenen VM. Der anschließende Start schlug mit "no hosts available" fehl, und sie blieb **Halted**. Starten Sie die VM nach einer Änderung immer. Startet sie nicht, sichern Sie den Fehler und stellen Sie die alten Werte und Grenzen wieder her, bevor Sie es erneut versuchen. Die Seite kann nach dem Speichern einige Sekunden lang alte Werte zeigen; warten Sie und laden Sie neu, um sie zu bestätigen. In D3 aktualisierte sich das Inventar nach etwa vier Sekunden.

Planen Sie ein Wartungsfenster und verwenden Sie einen Testgast mit zugänglicher Konsole. Notieren Sie vor jeder Änderung VM-ID, Gastzustand sowie aktuelle CPU- und Speicherwerte und Grenzen. Prüfen Sie Host- und Poolkapazität und den Gastbedarf; diese Anleitung empfiehlt weder CPU-Anzahl noch Speichergröße.

{{< callout type="warning" >}}
Fahren Sie zuerst den Gast sauber herunter und prüfen Sie **Halted**. Bearbeiten Sie eine laufende VM und lässt sich ein Wert nicht live ändern, kann XO einen normalen oder erzwungenen Neustart anbieten. Brechen Sie dies hier ab und fahren Sie zuerst herunter. Eine höhere Grenze reserviert keine Hostressourcen; weniger Arbeitsspeicher kann den Gaststart verhindern.
{{< /callout >}}

1. Öffnen Sie **Advanced** (`/#/vms/<id>/advanced`) und notieren Sie **CPU limits** und **Memory limits (min/max)**. Die CPU-Zeile zeigt aktuellen und maximalen Wert. Das Maximum lässt sich bei angehaltener VM bearbeiten. Für mehr CPUs als das aktuelle Maximum erhöhen Sie dieses zuerst.
2. Öffnen Sie **General** (`/#/vms/<id>/general`). Klicken Sie auf die CPU-Anzahl, geben Sie die neue ganze Zahl ein und drücken Sie **Enter**. Warten Sie, aktualisieren Sie die Ansicht und prüfen Sie den Wert vor der nächsten Änderung. Diese Felder können auch beim Klicken an anderer Stelle speichern; Wegklicken ist deshalb kein sicheres Abbrechen.
3. Klicken Sie den Speicherwert an, legen Sie Betrag und Einheit fest und drücken Sie **Enter**. Dies ist das konfigurierte **dynamische Maximum**, nicht die vom Gast verwendete Speichermenge. Abhängig von bestehenden Grenzen aktualisiert XO eine feste Speichereinstellung oder die dynamischen Speichergrenzen.
4. Aktualisieren Sie **General** und **Advanced** und notieren Sie alle resultierenden Werte. Die CPU-Anzahl darf ihr Maximum nicht überschreiten. Speichergrenzen müssen geordnet bleiben: statisches Minimum ≤ dynamisches Minimum ≤ dynamisches Maximum ≤ statisches Maximum. XO kann zugehörige Grenzen anpassen; nehmen Sie deshalb nicht an, dass nur das angeklickte Feld geändert wurde.
5. Starten Sie die Test-VM und prüfen Sie Konsole, im Gast sichtbare CPU und Speicher sowie die Anwendung. Startet sie nicht oder sind die Werte falsch, lassen Sie sie angehalten, sichern Sie den Aufgabenfehler und stellen Sie die notierten Einstellungen im selben Fenster wieder her. Prüfen Sie jede Grenze erneut und versuchen Sie es erst nach Klärung der Ursache wieder.

Zeigt eine Bearbeitung einen Fehler, prüfen Sie vor dem erneuten Versuch die tatsächlichen Werte. Zusammenhängende Änderungen werden nicht als ein unteilbarer Schritt angewendet; eine verweigerte Änderung belegt daher nicht, dass die alten Werte zurück sind. Halten Sie [Fehlerbehebung](/docs/xoa-hl/troubleshooting/) und Ihre Notizen bereit.

Nicht behandelt: Ressourcenänderungen im laufenden Zustand (Hot-Plug), dynamischer Speicher unter Last und CPU-Topologieoptimierung.

## Test-VM löschen {#delete-vm}

In D3 entfernte das Löschen einer angehaltenen Test-VM diese VM, ihren Snapshot und ihren Datenträger, ohne verbleibende Objekte. Getrennt davon blieb ein leerer Datenträger nach dem Abhängen im gewählten SR; das Löschen dieses Datenträgers entfernte ihn. Abhängen und Löschen haben unterschiedliche Ergebnisse. Gemeinsam genutzte Datenträger und Fehler bei der Bereinigung wurden nicht getestet.

Im selben [ce47-Test](https://github.com/Vagrantin/xcp-hl/issues/198#issuecomment-6460786269) wurde das normale Löschen einer geschützten VM abgelehnt und die VM blieb erhalten, ein erzwungenes Löschen entfernte sie jedoch. Der Löschschutz ist eine Sicherung gegen Versehen, keine Zugriffskontrolle. Wird ein geschütztes Löschen abgelehnt, halten Sie an und untersuchen Sie die Ursache; erzwingen Sie es nicht.

{{< callout type="warning" >}}
**Remove** löscht die VM. Das ist nicht dasselbe wie das Trennen oder Aushängen eines Datenträgers. Die Bestätigung dieser Version bietet keine Option zum Behalten der Datenträger: Das Löschen entfernt auch die VM-Snapshots und versucht, ihre angeschlossenen Datenträger zu löschen. Müssen Daten oder Snapshots erhalten bleiben, halten Sie vor der Bestätigung an und planen Sie deren Erhalt. Ein Snapshot dieser VM ist keine unabhängige Wiederherstellungskopie.
{{< /callout >}}

1. Prüfen Sie, dass das Ziel die Test-VM ist, nicht Appliance, ursprünglicher Gast, Vorlage oder eine ähnlich benannte VM. Notieren Sie ID, angeschlossene Datenträger mit IDs und SRs sowie Snapshots.
2. Prüfen Sie Sicherungs- und Replikationszeitpläne und ob eine andere VM einen ihrer Datenträger verwendet. Erstellen Sie für wertvolle Daten zuerst eine unabhängige [Sicherung und testen Sie eine isolierte Wiederherstellung](/docs/xoa-hl/backup-restore/).
3. Fahren Sie den Gast normal herunter und prüfen Sie **Halted**. Das Löschen kann eine noch laufende oder suspendierte VM hart stoppen; verwenden Sie **Remove** daher niemals zum Herunterfahren.
4. Öffnen Sie **Advanced** und wählen Sie **Remove**. Lesen Sie die Warnung zu VM und Datenträgern und bestätigen Sie ausschließlich diese VM. Bietet XO danach an, eine geschützte oder blockierte VM trotzdem zu entfernen, brechen Sie ab und klären Sie ihren Schutz. Genehmigen Sie keinen erzwungenen Wiederholungsversuch.
5. Warten Sie und aktualisieren Sie VM-, Snapshot- und SR-Datenträgerlisten. Prüfen Sie die notierten IDs sowie Aufgabe und Fehler. Gemeinsame Datenträger, die noch an einer anderen VM hängen, werden übersprungen; dies schützt jedoch nicht jeden Datenträger. Snapshot- oder Datenträgerbereinigungsfehler können protokolliert werden, ohne den gesamten Löschvorgang scheitern zu lassen. Eine verschwundene VM oder Erfolgsmeldung belegt deshalb keine abgeschlossene Bereinigung.
6. Prüfen Sie, dass Original-VM, andere Gäste und unabhängige Sicherungen weiterhin funktionieren. Prüfen Sie verbleibende Testobjekte einzeln anhand Ihrer Notizen und der [Datenträgeranleitung](/docs/xoa-hl/storage-networks/). Löschen Sie vermeintlich verwaiste Datenträger niemals pauschal und wiederholen Sie keine erzwungene Aktion, um Platz freizugeben. Es gibt kein Rückgängig: Gelöschte Gastdaten lassen sich nur aus einer getrennt getesteten Wiederherstellungskopie zurückholen.

Scheitert das Löschen teilweise oder brechen Sie eine blockierte Löschung ab, sichern Sie verbliebene VM-, Datenträger- und Snapshot-Listen sowie den Fehler. Besteht die VM noch, prüfen Sie auch ihre Rechte, IP-Poolreservierungen und Ressourcenmengenzugehörigkeit: XO beginnt einige Verwaltungsänderungen vor der Prüfung des VM-Schutzes. Eine Verweigerung belegt deshalb nicht, dass diese Datensätze unverändert sind. Erstellen Sie keine ähnlich benannte VM unter der Annahme, sie sei dasselbe Objekt. [Melden Sie das Problem](/docs/xoa-hl/troubleshooting/) vor jeder weiteren Bereinigung mit Versionen und IDs ohne private Daten.

{{< details title="Quellen" closed="true" >}}
- **Konsole**: [Registerkarte und Bedienelemente](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-console.js), [Canvas-Eingabe, Skalierung und Wiederverbindung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/react-novnc.js), [Authentifizierte operate-Zugriffsschranke](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/index.mjs), [Hostkonsolen-Proxy](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/proxy-console.mjs).
- **Vollständige Kopie**: [Kopierdialog, Vorgaben und Namensmuster](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/copy-vms-modal/index.js), [Kopier- und Klonanfragen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [VM-/SR-Rechte und Poolzweig](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [XAPI-Wrapper für Kopien, Klone und Fernkopien](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [Auswahl beschreibbarer SRs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/select-objects.js).
- **Energieaktionen und Snapshots**: [Energie- und Snapshot-Aktionen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [VM-Aktionsleiste](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/action-bar.js), [Snapshot-Registerkarte](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-snapshots.js), [Bestätigung des Zurücksetzens](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/revert-snapshot-modal/index.js), [Betriebszustand beim Zurücksetzen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
- **CPU, Speicher und Löschen**: [Bedienelemente unter General](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-general.js), [Grenzen und Remove unter Advanced](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [Speicherverhalten der Direktbearbeitung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/editable/index.js), [VM-API-Rechte und Neustart-/Löschparameter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [Reihenfolge der Grenzen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/utils.mjs), [Löschvorgaben, gemeinsame Datenträger und Bereinigung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [Oberflächenbezeichnungen und Warnungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Snapshot-Abdeckung und Löschen**: [Datenträgernamensabgleich und Bereinigung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs).
{{< /details >}}

## CPU und Arbeitsspeicher im laufenden Betrieb ändern (VM03) {#running-resources}

Geltungsbereich: XO 5.113.2 auf `e281c536`, Quellen von XOA-HL ce40/ce47. Dies ist ein Verfahren für einen entbehrlichen Gast; die Abnahme auf einer Installation und im Gast wird gesondert dokumentiert.

1. Behalten Sie eine getestete unabhängige Sicherung. Verwenden Sie einen Administrator, gewöhnliche Datenträger, eine funktionierende Konsole und einen Gast mit Unterstützung für CPU-Hotplug und Ballooning. Notieren Sie CPU-Anzahl, verfügbaren Arbeitsspeicher und Anwendungszustand im Gast, VM-UUID, aktuelle und maximale CPUs, alle vier Speichergrenzen und den freien Speicher des Hosts. Verwenden Sie keine Überbuchung des Hosts als Test.
2. Reservieren Sie im angehaltenen Zustand eine kleine Obergrenze, zum Beispiel 2 maximale CPUs und 1 GiB statisches Maximum für einen Gast mit 1 CPU und 512 MiB. Halten Sie unter **Advanced** `static min <= dynamic min <= dynamic max <= static max` ein. Starten Sie und bestätigen Sie diese Ausgangslage im Gast. Änderungen der maximalen CPU-Anzahl und des statischen Speichers erfordern für diese Übung ein Wartungsfenster im angehaltenen Zustand.
3. Ändern Sie im laufenden Betrieb unter **General** die aktuellen CPUs von 1 auf 2. Warten Sie, laden Sie beide Reiter neu und prüfen Sie die im Gast aktiven CPUs und die Arbeitslast. Überschreiten Sie nicht das notierte Maximum. Eine gespeicherte Startanzahl allein beweist keine live verfügbare CPU.
4. Setzen Sie unter **Advanced** das dynamische Minimum auf 512 MiB und das dynamische Maximum auf 768 MiB, innerhalb der reservierten statischen Grenzen. Prüfen Sie nach jeder Änderung beide Grenzen. Der Speicherwert unter **General** wird bei festem Speicher und bei DMC unterschiedlich verarbeitet; verwenden Sie für diesen Test die ausdrücklichen dynamischen Felder. Beobachten Sie Gastspeicher und Anwendungszustand, nachdem sich das Ballooning eingependelt hat.
5. Notieren Sie Ergebnisse von Host und Gast getrennt. Stellen Sie die notierten Grenzen und die CPU-Anzahl wieder her, mit einem sauberen Herunterfahren, wenn das Entfernen im laufenden Betrieb scheitert oder der Gast nicht sicher zurückkehren kann. Starten Sie und prüfen Sie erneut die ursprüngliche Arbeitslast.

**Fehler:** Halten Sie bei einem Fehler, Speicherdruck im Gast oder einer unerwarteten Änderung einer zugehörigen Grenze an. Lesen Sie jede Grenze, die CPU-Anzahl und die Aufgabe zurück, bevor Sie es erneut versuchen. Erzwingen Sie keinen Neustart und verringern Sie den Speicher nicht immer weiter, damit ein API-Aufruf gelingt. Weder DMC noch ein erfolgreicher API-Aufruf garantieren Kapazität für Anwendungen im Gast.

**Laborergebnis, 03.11.2026 (teilweise):** Beobachtet auf dem verschachtelten ce44-Host mit dem ce40-Appliance-Image (Anwendung 5.113.2_e281c536-47) über die JSON-RPC-API der Appliance, an einem entbehrlichen Gast ohne Gastwerkzeuge. Eine CPU-Änderung im laufenden Betrieb über das Maximum hinaus wurde abgelehnt (`VM state is running but should be halted`). Eine CPU-Änderung im laufenden Betrieb bei einem Gast ohne Hotplug-Unterstützung schlug mit `VM lacks feature` fehl; die Startanzahl blieb bis zur nächsten Änderung auf dem neuen Wert, während die aktive Anzahl bei 1 blieb, lesen Sie also beide zurück. Ein Maximum über der CPU-Anzahl des Hosts verhindert den Start (`Not enough CPUs`). Die dynamischen Speichergrenzen änderten sich bei laufender VM. Das statische Maximum kann im laufenden Betrieb nicht geändert werden, und das Feld `memory` ändert nur das dynamische Maximum. Die Reaktion von CPU und Ballooning im Gast wurde nicht beobachtet; dieser Modus bleibt daher offen.

## Laufende oder angehaltene (suspendierte) VM kopieren (VM07) {#active-copy}

Geltungsbereich: dieselbe Quellbasis XO5/ce40/ce47. Verwenden Sie das vorhandene [Verfahren für eine vollständige Kopie](#full-copy) mit diesen zustandsspezifischen Schritten.

1. Verwenden Sie einen entbehrlichen Gast mit einer auf den Datenträger geschriebenen Stichprobendatei samt Prüfsumme, genug beschreibbarem SR-Platz im selben Pool und ohne gemeinsam genutzte oder durchgereichte Geräte. Entfernen Sie alle VIFs, bevor Sie ihn starten. Lassen Sie Sicherungsjobs deaktiviert und inventarisieren Sie vorhandene Snapshots.
2. Schreiben Sie für **Running** die Gastdaten auf den Datenträger und wählen Sie dann **Copy**, **Full copy**, einen eindeutigen Namen und genau das SR im selben Pool. Komprimierung wird im selben Pool nicht verwendet. Das Backend erstellt einen Snapshot der laufenden VM, kopiert ihn und versucht dann, den Snapshot zu bereinigen. Das ist weder ein Stilllegen der Anwendung noch ein Speicher-Checkpoint.
3. Testen Sie **Suspended** gesondert: Suspendieren Sie die isolierte Quelle über die Energieaktion, bestätigen Sie den Zustand und fordern Sie dann eine weitere benannte vollständige Kopie an. Diese Version lehnt das ab (siehe Laborergebnis unten). Gehen Sie nicht davon aus, dass eine Kopie den suspendierten Speicher oder den Betriebszustand der Quelle erhält.
4. Notieren Sie für jedes Ergebnis die VM-IDs von Quelle und Kopie, Datenträger-IDs, SRs, Betriebszustand und Reste temporärer Snapshots. Lassen Sie jede Kopie angehalten und entfernen Sie alle übernommenen VIFs vor jedem Start oder Fortsetzen. Ist sie nicht angehalten, halten Sie an und untersuchen Sie das, bevor Sie fortfahren. Starten Sie über die Konsole und vergleichen Sie die Prüfsumme der Stichprobe. Bestätigen Sie, dass die Quelle in ihrem vorgesehenen Zustand nutzbar bleibt.

**Fehler:** Inventarisieren Sie teilweise erstellte VMs, Datenträger und Snapshots vor Bereinigung oder neuem Versuch. Behalten Sie die Quelle und die unabhängige Sicherung. Eine abgeschlossene Aufgabe allein belegt weder Datenträgerkonsistenz noch den Erhalt des Snapshot-Verlaufs.

**Laborergebnis, 03.11.2026 (teilweise):** Über die API erzeugte eine laufende Quelle eine angehaltene Kopie mit eigenem Datenträger und neuer MAC-Adresse; die Quelle blieb Running, und kein temporärer Snapshot blieb zurück. Die Kopie behielt das VIF der Quelle; entfernen Sie es also vor jedem Start. Eine Quelle im Zustand Suspended wird abgelehnt (`VM state is suspended but should be halted`): Setzen Sie sie zuerst fort oder stoppen Sie sie, und erwarten Sie keine suspendierte Kopie. Gaststart und Prüfsumme der Kopie wurden nicht ausgeführt; dieser Modus bleibt daher offen.

## Live- und Speicher-Snapshots (VM09) {#active-snapshots}

Geltungsbereich: dieselbe Quellbasis XO5/ce40/ce47. Verwenden Sie einen isolierten, entbehrlichen Gast ohne VIFs, mit gewöhnlichen einbezogenen Datenträgern, Konsolenzugriff, freier SR- und Hostkapazität und deaktivierten Jobs. Notieren Sie UUID, Datenträgerabdeckung, Prüfsumme der Ausgangsdatei und vorhandene Snapshots.

1. Schreiben Sie bei laufendem Gast eine Stichprobendatei mit `live-A` auf den Datenträger. Wählen Sie unter **Snapshots** **New snapshot**. Notieren Sie die neue UUID und die Datenträgerabdeckung. Das ist ein Datenträger-Snapshot, keine Garantie für Anwendungskonsistenz.
2. Ändern Sie die Stichprobe in `live-B`, schreiben Sie sie auf den Datenträger, fahren Sie den Gast sauber herunter und verwenden Sie dann das [Verfahren zum Zurücksetzen](#snapshot-revert) mit aktiviertem **Snapshot before**. Ein Live-Punkt kann die VM beim Zurücksetzen starten; die Isolation muss also bereits im gespeicherten Punkt bestehen. Prüfen Sie Zustand, VIFs, Konsole und die Prüfsumme von `live-A`.
3. Lassen Sie in einem gesonderten Test den isolierten Gast mit einer nicht gespeicherten, harmlosen Markierung in einem Editor im Gast laufen. Wählen Sie **New snapshot with memory**. Notieren Sie die UUID und ob tatsächlich ein Checkpoint mit Arbeitsspeicher existiert. Das Backend kann bei `VM_BAD_POWER_STATE` auf einen Datenträger-Snapshot zurückfallen; die Schaltfläche allein beweist keinen gespeicherten Arbeitsspeicher.
4. Ändern Sie die Markierung und die Datenträger-Stichprobe, und setzen Sie dann mit einem Vorher-Punkt und genug Kapazität auf genau diesen Checkpoint zurück. Prüfen Sie die wiederhergestellte RAM-Markierung, die Prüfsumme auf dem Datenträger, die Konsole, die Arbeitslast und den tatsächlichen Betriebszustand. Werten Sie einen Erfolg nur auf dem Datenträger nicht als Erfolg beim Arbeitsspeicher.
5. Löschen Sie nach der Abnahme nur die notierten Testpunkte und prüfen Sie verbleibende Snapshots, Datenträger und Kapazität. Lassen Sie von Sicherungen verwaltete Punkte unberührt.

**Fehler:** Sichern Sie Aufgabenfehler und Inventare; prüfen Sie den Zustand der Quell-VM vor einem neuen Versuch. Checkpoints mit ausgeschlossenen oder gemeinsam genutzten Datenträgern oder Passthrough, Stilllegen von Anwendungen und Sicherungskonsistenz benötigen eigene Nachweise.

**Laborergebnis, 03.11.2026 (teilweise):** Bei einem laufenden Gast hatte ein Datenträger-Snapshot den Betriebszustand Halted und kein Suspend-VDI. **New snapshot with memory** erzeugte einen Snapshot mit dem Betriebszustand Suspended und einem Suspend-VDI. Das Zurücksetzen auf einen der beiden ließ die VM Running. Der Testgast hat keine Gastwerkzeuge; RAM-Markierung und Gastdaten wurden daher nicht geprüft, und dieser Modus bleibt offen.

## Ausgewählte Datenträger beim Löschen behalten (VM11) {#retain-disks}

Geltungsbereich: dieselbe Quellbasis XO5/ce40/ce47. Die API zum Löschen von VMs hat einen booleschen Wert `deleteDisks` für die ganze VM, keine Liste pro Datenträger. Behalten Sie ausgewählte Datenträger, indem Sie zuerst deren VBDs abhängen, während die entbehrliche VM angehalten ist.

1. Erstellen und prüfen Sie eine unabhängige Wiederherstellungskopie. Notieren Sie VM-UUID, alle VBD- und VDI-IDs, SR, Größe, Snapshots und welche Datenträger erhalten bleiben müssen. Verwenden Sie gewöhnliche, nicht gemeinsam genutzte Datenträger und stoppen Sie alle zugehörigen Jobs.
2. Verwenden Sie unter **Disks** für jeden zu behaltenden Datenträger **Remove VDI from this VM**, nicht **Destroy VDI**. Die Zeilenaktion entfernt das VBD sofort; beim Löschen der VM gibt es kein Kontrollkästchen zum Behalten einzelner Datenträger. Laden Sie neu: Das VBD muss fehlen, aber genau dieses VDI muss in seinem SR weiterhin existieren. Ein bloßes Trennen eines Datenträgers genügt nicht.
3. Löschen Sie die identifizierte angehaltene VM mit der normalen Bestätigung. Das kann ihre Snapshots und verbleibenden infrage kommenden Datenträger rekursiv entfernen. Brechen Sie jede Aufforderung zum Erzwingen ab und untersuchen Sie die Ursache.
4. Prüfen Sie, dass die VM fehlt, die behaltenen VDIs weiterhin existieren und nur die vorgesehenen entbehrlichen angehängten Datenträger entfernt wurden. Hängen Sie ein behaltenes VDI an eine separate, angehaltene und isolierte Wiederherstellungs-VM an, starten Sie sie und prüfen Sie die Prüfsumme der Stichprobe; hängen Sie es danach ab, ohne es zu löschen.

**Fehler:** Halten Sie an, wenn der Dialog nicht zwischen dem Entfernen der Anbindung und dem Löschen von Daten unterscheidet. Notieren Sie nach jedem Fehler die Inventare teilweise vorhandener VMs, VDIs und Snapshots. Schließen Sie nie aus einer verschwundenen VM-Zeile oder einem getrennten Datenträger auf deren Erhalt.

Festgelegte Implementierung: [packages/xo-server/src/api/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [packages/xo-server/src/api/vbd.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vbd.mjs), [packages/xo-server/src/xapi/mixins/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs), [packages/xo-server/src/xapi/index.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [@xen-orchestra/xapi/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs), [packages/xo-web/src/xo-app/vm/tab-advanced.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [packages/xo-web/src/xo-app/vm/tab-disks.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js).

**Laborergebnis, 03.11.2026 (nur Speicherebene):** Über die API entfernte das Entfernen des VBD eines zweiten Datenträgers und das anschließende Löschen der VM mit `deleteDisks` auf true die VM und ihren Systemdatenträger und ließ das abgehängte VDI in seinem SR. Das Anhängen des behaltenen Datenträgers an eine Wiederherstellungs-VM und die Prüfung seiner Daten wurden nicht ausgeführt; dieser Modus bleibt daher offen.
