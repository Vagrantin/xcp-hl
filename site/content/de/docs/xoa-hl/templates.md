---
title: "VM-Vorlagen erstellen und verwenden"
linkTitle: "Vorlagen"
description: "Eine vorbereitete VM-Kopie in eine Vorlage umwandeln und daraus neue VMs erstellen."
weight: 42
translationKey: xoa-manual-templates
translationStatus: draft
sourceRevision: sha256:23d0b04b060005b00afe691ae01412a11eab4ff1a913833849d8381a9d041307
glossaryTerms: ["backup", "pool", "sr", "vm"]
---

Wandeln Sie eine angehaltene VM-Kopie in eine Vorlage um, erstellen Sie daraus zwei VMs und prüfen Sie, dass jede ihre eigenen Datenträger und Daten erhält. Die ursprüngliche VM bleibt unverändert.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet. Diese Schritte verwenden einen bereits installierten Datenträger erneut: Sie bereiten kein Gastbetriebssystem für die allgemeine Wiederverwendung vor.
{{< /callout >}}

## Vor dem Beginn {#before-you-begin}

- Melden Sie sich bei der **XOA-HL-Appliance** als Administrator an. Die Umwandlung erfordert Administratorrechte sowohl für die VM als auch für deren Pool; Zugriff auf die VM allein reicht nicht.
- Verwenden Sie einen bereits installierten Testgast mit gewöhnlichen Datenträgern: keine gemeinsam genutzten Datenträger und keine durchgereichten Geräte. Wandeln Sie niemals die Appliance oder die ursprüngliche VM um.
- Erstellen Sie mit [Vollständige Kopie im selben Pool erstellen](/docs/xoa-hl/vm-operations/#full-copy) eine getrennte Arbeitskopie. Notieren Sie die UUIDs von Original und Kopie, die VDI-ID, das SR und die Größe jedes Datenträgers sowie die Prüfsumme einer harmlosen Beispieldatei im Gast. Prüfen Sie, dass die Kopie isoliert startet, und fahren Sie sie anschließend normal herunter.
- Entfernen Sie an der Arbeitskopie **alle** Netzwerkschnittstellen, werfen Sie das Installations-ISO aus, deaktivieren Sie automatisches Einschalten und schließen Sie sie von geplanten Aufträgen aus.
- Halten Sie genug Host-Arbeitsspeicher und beschreibbaren SR-Platz für die Vorlage und zwei Test-VMs frei.
- Halten Sie Konsolenzugriff und die Gast-Anmeldedaten bereit. Das Umbenennen einer VM oder Ändern ihrer MAC-Adresse ändert weder kopierte Passwörter, Hostnamen, IP-Einstellungen oder Schlüssel noch Anwendungsidentitäten. Verwenden Sie diese Kopien ausschließlich über die Konsole.

Sie arbeiten im Browser an der Appliance-Adresse. Datei- und Prüfsummenprüfungen erfolgen in der **Gastkonsole**, nicht auf dem Host oder in der Appliance. Eine Vorlage auf derselben Infrastruktur ist keine Sicherung: Bewahren Sie Ihre [Sicherungen](/docs/xoa-hl/backup-restore/) getrennt auf. Bei einem neuen Ubuntu-24.04-Gast [installieren Sie die Gastwerkzeuge](/docs/xoa-hl/guest-tools/) vor dem Kopieren.

## Angehaltene Kopie in eine Vorlage umwandeln {#convert-template}

1. Prüfen Sie die Arbeitskopie: ihre UUID, den Zustand **Halted**, die leere Netzwerkschnittstellenliste und die zuvor notierten Datenträger.
2. Vergeben Sie einen eindeutigen Namen wie `lab-template-v1` und eine Beschreibung mit Gastbetriebssystem und Version, Vorbereitungsdatum und Beispielprüfsumme. Aktualisieren Sie die Ansicht und prüfen Sie diese Werte.
3. Öffnen Sie **Advanced** (`/#/vms/<copy-uuid>/advanced`) und wählen Sie **Convert to template**. Die Schaltfläche funktioniert nur bei angehaltener VM. Die Bestätigung warnt vor der dauerhaften Änderung: Brechen Sie ab, wenn dies nicht die vorgesehene Kopie ist.
4. Bestätigen Sie einmal und warten Sie auf den Abschluss.
5. Öffnen Sie **Home** und wählen Sie den Objekttyp **Template** (`/#/home?t=VM-template`). Entfernen Sie gegebenenfalls Filter, klappen Sie die Zeile auf und lesen Sie die vollständige UUID.

**Prüfung:** Die Vorlage hat **dieselbe UUID** wie die Arbeitskopie, den festgelegten Namen und die Beschreibung; die ursprüngliche VM ist weiterhin vorhanden. Beim Umwandeln entsteht keine weitere Kopie: Die Arbeitskopie selbst wird zur Vorlage.

Bevor XO die VM als Vorlage markiert, versucht es, Wechselmedien auszuwerfen. Scheitert dies, können bereits vorgenommene Medienänderungen trotz fehlgeschlagener Umwandlung bestehen bleiben. Aktualisieren Sie Objekttyp, Medien und Aufgabe vor einem erneuten Versuch. Das Zurückwandeln einer Vorlage in eine VM und ein automatisches Zurücksetzen werden hier nicht behandelt.

## Angehaltene VM aus der Vorlage erstellen {#deploy-template}

1. Öffnen Sie **New → VM** (`/#/vms/new`), wählen Sie denselben Pool und Ihre Vorlage. Nennen Sie die VM `lab-template-test-1`. Prüfen Sie die UUID hinter `template=` in der Seitenadresse, nicht nur den Vorlagennamen.
2. Prüfen Sie CPU, Arbeitsspeicher, die Vorlagendatenträger, ihre Größen und beschreibbaren Ziel-SRs. Behalten Sie dieselben Datenträger und Größen bei.
3. Wählen Sie unter **Install settings** die Option **No config drive**. Dieser Test verwendet den installierten Datenträger erneut: Er startet keinen Installer und verlässt sich nicht darauf, dass cloud-init die Gastidentität ändert. Fehlen Datenträger oder diese Option, halten Sie an und prüfen Sie die ausgewählte Vorlage.
4. Entfernen Sie unter **Interfaces** jede vorgeschlagene Schnittstelle und prüfen Sie die leere Liste. Selbst eine Vorlage ohne Schnittstellen kann vom Assistenten die Standardnetzwerke des Pools erhalten.
5. Deaktivieren Sie unter **Advanced** die Option **Boot VM after creation** und lassen Sie automatisches Einschalten deaktiviert.
6. Deaktivieren Sie unter **Summary** die Option **Fast clone**. Prüfen Sie, dass genau eine VM mit den erwarteten Datenträgern, Ressourcen und SRs sowie **null Schnittstellen** entsteht. Wählen Sie dann einmal **Create**. Der Assistent aktiviert Start nach Erstellung und Fast Clone standardmäßig; verlassen Sie sich daher nicht auf frühere Einstellungen. Ohne Fast Clone kopiert XO die Datenträger vollständig, was SR-Platz benötigt.
7. Warten Sie, aktualisieren Sie die Ansicht und notieren Sie die UUID der neuen VM.

**Prüfung:** Vor jedem Start ist die neue VM **Halted**, ihre Registerkarte Network ist leer, und die Datenträger haben die erwartete Anzahl, Größen und SRs sowie andere VDI-IDs als Vorlage und Original. Vorlage und Original sind weiterhin vorhanden. Eine Erfolgsmeldung oder ein neuer Name beweist dies nicht. Ist eine Schnittstelle aufgetaucht oder die VM gestartet, stoppen Sie sie und prüfen Sie vor dem Fortfahren, was sie erreichen konnte.

## Eigene Kopie für jede VM prüfen {#verify-deployments}

1. Starten Sie nach den obigen Prüfungen ausschließlich `lab-template-test-1`. Prüfen Sie in deren [Konsole](/docs/xoa-hl/vm-operations/#vm-console), dass der Gast startet und die Anmeldung funktioniert; prüfen Sie dann Datenträgeraufteilung und Beispielprüfsumme.
2. Ändern Sie nur die Beispieldatei auf einen neuen Testwert, notieren Sie ihn und fahren Sie den Gast normal herunter.
3. Wiederholen Sie [Angehaltene VM aus der Vorlage erstellen](#deploy-template) mit **derselben Vorlage** als `lab-template-test-2`. Prüfen Sie jede Einstellung erneut.
4. Prüfen Sie im angehaltenen Zustand die andere VM-UUID, andere VDI-IDs und das Fehlen von Schnittstellen. Starten Sie die VM über ihre Konsole und prüfen Sie, dass die Beispieldatei noch die ursprüngliche Prüfsumme hat, nicht den neuen Wert aus Test 1. Fahren Sie sie normal herunter.
5. Notieren Sie UUIDs und VDI-IDs beider VMs, die Vorlagen-UUID, die Gastergebnisse und installierten Versionen. Lassen Sie die Test-VMs angehalten.

**Prüfung:** Beide Gäste starten mit den erwarteten Daten, und die Änderung aus Test 1 ist nicht in Test 2 angekommen. Diese Dateiprüfung testet keine Anwendungswiederherstellung und beseitigt keine duplizierten Betriebssystemidentitäten. Verbinden Sie kein Produktionsnetzwerk, bevor der Gastverantwortliche diese bereinigt hat.

Zum Aufräumen [löschen Sie jede Test-VM](/docs/xoa-hl/vm-operations/), nachdem Sie sie identifiziert haben. Behalten Sie Vorlage, Original-VM und Sicherungen. Für eine neue Vorlagenversion bereiten Sie eine neue Kopie mit einem neuen versionierten Namen vor und wiederholen diese Prüfungen.

## Wenn etwas schiefgeht {#problems}

| Problem | Prüfen |
| --- | --- |
| Die Umwandlung wird verweigert | Lesen Sie den Fehler, prüfen Sie VM- und Poolrechte sowie den tatsächlichen Betriebszustand. Erzwingen Sie kein Stoppen eines wertvollen Gasts und wandeln Sie kein unidentifiziertes Objekt erneut um. Prüfen Sie nach einem Fehler Objekttyp und Wechselmedien derselben UUID. |
| Die Vorlage fehlt | Wählen Sie den Objekttyp Template, den richtigen Pool und passende Filter; aktualisieren Sie dann. Eine Vorlage erscheint nicht in der normalen VM-Liste. Erstellen Sie keine weitere Kopie, bevor Sie das Inventar geprüft haben. |
| Die VM-Erstellung scheitert | Sichern Sie den Fehler sowie die Liste von Vorlagen, VMs und VDIs vor einem erneuten Versuch. XO versucht nach einem Fehler aufzuräumen, aber eine verlorene Antwort oder fehlgeschlagene Bereinigung kann Objekte zurücklassen. Löschen Sie vermeintlich verwaiste Datenträger niemals pauschal. |
| Der Gast weicht ab oder startet nicht | Behalten Sie Vorlage und Protokolle. Prüfen Sie Vorlagen-UUID, kopierte Datenträger, Firmware, Ressourcen und Installationseinstellungen. Ändern Sie zur Behebung nicht das Host-Verwaltungsnetzwerk. |

Das Ändern eines Gasts innerhalb einer Vorlage, das Ausmustern oder Löschen von Vorlagen, die Bereitstellung in einem anderen Pool, Fast-Clone-Speicher, cloud-init und betriebssystemspezifische Vorbereitung werden hier nicht behandelt. Bleibt ein Problem bestehen, [melden Sie es](/docs/xoa-hl/troubleshooting/#report-a-problem) ohne sensible Daten.

{{< details title="Quellen" closed="true" >}}
- **Umwandlung**: [Aktion unter Advanced, nur für angehaltene VMs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-advanced.js), [Bestätigungsdialog](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [Rechte, Medien, Umwandlung und Bereinigung nach fehlgeschlagener Erstellung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs).
- **Assistent für neue VMs**: [Identität der Vorlagenzeile](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/home/template-item.js), [Assistentenvorgaben und übermittelte Einstellungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [Datenträgerkopie und Schnittstellenersetzung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs).
- **HomeLab-Build**: [xoa-hl-Buildskript](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
## Vorlage vorbereiten, pflegen und außer Betrieb nehmen (VM06) {#template-lifecycle}

Geltungsbereich: XO 5.113.2 `e281c536`, Quellen von XOA-HL ce40/ce47. Die Umwandlungs- und Kopiervorgänge von XO generalisieren kein Gastbetriebssystem. Dieses Verfahren unterstützt keinen universellen Befehl zur Generalisierung von Gästen.

1. Erstellen Sie vor der Umwandlung eine isolierte Arbeitskopie und notieren Sie Gastbetriebssystem, Version und Anwendungen. Folgen Sie dem Vorbereitungsverfahren des Betriebssystemherstellers für Hostname, Maschinenidentität, SSH-Hostschlüssel, statische Netzwerkkonfiguration, Zugangsdaten, cloud-init-Zustand sowie Anwendungs- und Lizenzidentitäten. Entfernen Sie private Daten. Beschaffen Sie für Windows zuerst einen betriebssystemspezifischen Sysprep-Plan und ein Windows-Labor; Linux-Ergebnisse können ihn nicht validieren.
2. Notieren Sie die genauen Befehle zur Gastvorbereitung und das beabsichtigte Verhalten beim ersten Start. Löschen Sie Maschinen-IDs oder Schlüssel nicht blind aus einem laufenden Original. Fahren Sie die vorbereitete Kopie herunter und verwenden Sie die vorhandenen Umwandlungsschritte. Gibt es kein gastspezifisches Verfahren, belassen Sie die Vorlage für reinen Konsolenbetrieb und kennzeichnen Sie sie als **nicht generalisiert**.
3. Wählen Sie für einen **Fast clone** die Vorlage in **New VM**, vergeben Sie einen eindeutigen Namen, wählen Sie **Fast clone**, behalten Sie die von der Vorlage geforderte Speicherbeziehung bei und lassen Sie den automatischen Start aus. Prüfen Sie die Zusammenfassung und erstellen Sie eine VM. Ein Fast clone hängt von seinem SR und seinen Basisdatenträgern ab; er ist keine vollständige unabhängige Kopie.
4. Lesen Sie unterschiedliche VM- und VDI-IDs sowie die Platzierung zurück. Entfernen Sie alle VIFs, starten Sie über die Konsole und prüfen Sie die Stichprobe und die beabsichtigten Identitäten beim ersten Start. Wiederholen Sie das mit einem zweiten Klon; vergleichen Sie die Identitäten untereinander und mit der Vorlage, bevor Sie die Netzwerknutzung freigeben. Eine geänderte MAC-Adresse allein reicht nicht.
5. Erstellen Sie zur Pflege aus Vorlage v1 eine angehaltene Arbeits-VM, isolieren Sie sie, spielen Sie Gastupdates ein, prüfen Sie Werkzeuge und Anwendung, wiederholen Sie die Vorbereitung und veröffentlichen Sie Vorlage v2 per Umwandlung. Testen Sie zwei Bereitstellungen von v2. Bearbeiten Sie keinen genutzten Basisdatenträger und gehen Sie nicht davon aus, dass eine Vorlage direkt gestartet und gepatcht werden kann.
6. Entfernen Sie v1 zur Außerbetriebnahme aus Ressourcensätzen und wählen Sie sie nicht mehr für neue VMs. Inventarisieren Sie abhängige Klone und unabhängige Wiederherstellungskopien, und löschen Sie dann nach einer Wiederherstellungsprüfung nur die identifizierte ausgemusterte Vorlage mit der normalen Bestätigung. Prüfen Sie, dass bestehende Klone weiterhin mit ihren Daten starten. Entfernen Sie Basis-VDIs nicht manuell und führen Sie keine Ketten zusammen.

**Fehler:** Bewahren Sie die ursprüngliche Vorlage, teilweise erstellte Klone und Inventare auf. Veröffentlichen Sie v2 nicht und nehmen Sie v1 nicht außer Betrieb nach fehlgeschlagener Vorbereitung, doppelter Identität, Startfehler oder ungeklärter Speicherabhängigkeit. Die gastspezifische Generalisierung bleibt offen, bis ihr genaues Betriebssystemverfahren und zwei erste Starts erfolgreich sind.

Festgelegte Implementierung: [packages/xo-server/src/api/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/vm.mjs), [packages/xo-web/src/xo-app/new-vm/index.js](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [packages/xo-server/src/xapi/mixins/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/mixins/vm.mjs), [@xen-orchestra/xapi/vm.mjs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/vm.mjs).

**Laborergebnis, 03.11.2026 (teilweise):** Über die API wurde eine VM in eine Vorlage umgewandelt, dann wurden zwei Fast clones und ein vollständiger Klon erstellt. Ein Klon einer Vorlage ist selbst eine Vorlage. Beide Fast clones teilten sich einen übergeordneten Datenträger `base copy` (`vhd-parent`), die vollständige Kopie hatte keinen. Das Löschen der Quellvorlage ließ alle drei Klone und ihre Datenträger intakt, und die gemeinsame Basiskopie blieb erhalten. Gastvorbereitung, zwei unterschiedliche erste Starts und die Generalisierungsschritte des Herstellers wurden nicht ausgeführt; VM06 bleibt daher offen.
