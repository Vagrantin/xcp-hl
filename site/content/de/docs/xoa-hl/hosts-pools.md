---
title: "Hosts und Pools verwalten: Beitritt, Statistiken und Hostwartung"
linkTitle: "Hosts und Pools"
description: "Verwaltende Appliance eines Pools prüfen, Hoststatistiken lesen und Poolbeitritt, Wartungsmodus sowie HA an Laborhosts testen."
weight: 60
translationKey: xoa-manual-hosts-pools
translationStatus: draft
sourceRevision: sha256:6ade76bbc4328f8c9c50e11f0871e5809dda89e8f6f6c2d1fda8e5c6c988f73e
glossaryTerms: ["appliance", "host", "pool", "xo-lite", "backup"]
---

Prüfen Sie die verwaltende Appliance jedes Pools, übertragen Sie die Verwaltung an eine andere Appliance, bereinigen Sie eine alte XO-Lite-Schaltfläche, lesen Sie Hoststatistiken und testen Sie Poolbeitritt, Wartungsmodus und Hochverfügbarkeit (HA) an Laborhosts. Melden Sie sich an der **XOA-HL-Appliance** als Administrator an und behalten Sie genehmigten Zugriff auf die Hostkonsole. Notieren Sie vor dem Beginn Appliance-Adresse, Host- und Pool-IDs sowie deren heutige verwaltende Appliance. Für die erste Verbindung siehe [Erste Anmeldung und Hostverbindung](/docs/xoa-hl/first-login/).

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet. Der Abschnitt zur XO-Lite-Schaltfläche behandelt außerdem `xolite-ce v0.21.0-ce29` (Upstream `xo-lite-v0.21.0`).
{{< /callout >}}

## Verbindung und Poolzuständigkeit prüfen {#connected-pool}

1. Öffnen Sie **Settings → Servers** (`/#/settings/servers`).
2. Prüfen Sie, dass die erwartete Verbindung aktiviert und verbunden ist.
3. Prüfen Sie, dass das Inventar den vorgesehenen Host, Pool, die VMs und den Speicher zeigt.

Ein gespeicherter Servereintrag belegt keine funktionierende Verbindung. Lesen Sie bei Verbindungsfehlern die Meldung und prüfen Sie Adresse, Zugangsdaten und Zertifikatsbehandlung mit der [Verbindungsanleitung](/docs/xoa-hl/first-login/).

Die unterstützte Regel aus [Issue #126](https://github.com/Vagrantin/xcp-hl/issues/126) lautet: **Genau eine XOA verwaltet einen bestimmten Host oder Pool**. Mehrere Appliances können sich technisch verbinden, aber die Verwaltung desselben Pools durch mehr als eine wird nicht unterstützt. Eine Appliance kann weiterhin mehrere Pools verwalten. Klären Sie die Poolzuständigkeit vor dem Hinzufügen einer Verbindung. Lassen Sie niemals doppelte Sicherungszeitpläne für dieselben Gäste laufen.

## Verwaltung an eine andere Appliance übertragen {#move-management}

Dies überträgt die Poolzuständigkeit von einer alten auf eine neue Appliance. Die Poolmitgliedschaft ändert sich nicht. Entfernen Sie niemals einen Host aus seinem Pool und löschen Sie keine VM, um die XO-Verwaltung zu übertragen.

1. Planen Sie ein Zeitfenster. Lassen Sie laufende Verwaltungs- und Sicherungsaufgaben enden.
2. Notieren Sie auf der alten Appliance Verbindungen, Zeitpläne und Sicherungsziele.
3. [Exportieren Sie ihre Konfiguration](/docs/xoa-hl/configuration-backup/) und verwahren Sie die Datei sicher. Exportieren allein verschiebt oder deaktiviert keinen Auftrag.
4. Deaktivieren Sie auf der alten Appliance die diesen Pool betreffenden Zeitpläne.
5. Entfernen Sie unter **Settings → Servers** der alten Appliance die Poolverbindung, bevor Sie die neue Appliance verbinden.
6. Fügen Sie auf der neuen Appliance die Host- oder Poolverbindung hinzu. Prüfen Sie verbundenes Inventar und vorgesehene Rechte.
7. Beachten Sie beim Neuerstellen oder Wiederherstellen von Einstellungen die Isolations- und Importvorkehrungen der [Anleitung zur Konfigurationssicherung](/docs/xoa-hl/configuration-backup/).
8. Prüfen Sie, dass die alte Appliance sich nicht erneut verbindet und keine Aufträge mehr gegen den Pool ausführt.
9. Prüfen Sie auf der neuen Appliance die Sicherungsziele und führen Sie einen isolierten Wiederherstellungstest aus. Aktivieren Sie anschließend ausschließlich die vorgesehenen Zeitpläne.

**Prüfung:** Nur die neue Appliance ist mit dem Pool verbunden und führt Aufträge dafür aus.

Ist der Zustand einer Appliance unklar, pausieren Sie die Übertragung und sichern Sie Verbindungs- und Aufgabenfehler. Zum Zusammenführen von Hosts in einen Pool siehe [Poolbeitritt testen](#pool-join).

## XO-Lite-Schaltfläche verstehen {#xo-lite-button}

Jede verbundene Appliance hinterlässt eine Markierung im Pool. XO Lite liest diese Markierungen für seine Schaltfläche **Access XOA**.

- XO schreibt `xo:clientInfo:<appliance-uuid>` in `other-config` des Pools. Mit Standardeinstellungen geschieht dies beim Verbinden und danach alle **6 Stunden**. Dabei entfernt XO auch Markierungen, die älter als **48 Stunden** sind.
- Eine schreibgeschützte XO-Verbindung schreibt keine Markierung.
- Das Entfernen einer Serververbindung beendet neue Schreibvorgänge, entfernt aber nicht sofort die vorhandene Markierung.
- **Access XOA** verwendet die Markierung mit dem neuesten Wert `lastConnected`. Geöffnet wird `publicUrl`, falls gesetzt, sonst die erste Adresse von `eth0` (oder der ersten verfügbaren Schnittstelle), über HTTPS.
- Die Schaltfläche prüft nicht, ob Appliance-VM oder Webdienst laufen. Findet XO Lite keine Adresse, bietet es stattdessen **Deploy XOA** an.
- XO Lite lässt alte Markierungen nicht selbst verfallen. Eine alte Schaltfläche kann bestehen bleiben, obwohl keine XO mehr verbunden ist.

Eine alte Adresse rechtfertigt keine zweite Appliance. Prüfen Sie zuerst die bekannte Appliance-Adresse und deren Poolzuständigkeit. Zeigt die richtige Appliance eine falsche Adresse, prüfen Sie URL- und Netzwerkeinstellungen, statt ihre Markierung wiederholt zu löschen.

## Veraltete XO-Lite-Markierung entfernen {#obsolete-marker}

Tun Sie dies erst nach dem Entfernen der Verbindung der alten Appliance (siehe [Verwaltung an eine andere Appliance übertragen](#move-management)). Geändert werden ausschließlich Erkennungsdaten, nicht Poolmitgliedschaft, VM-Betriebszustände oder Sicherungsdaten.

1. Führen Sie auf dem **Hypervisor-Host** als root diese lesenden Befehle aus:

   ```bash
   xe pool-list params=uuid,name-label
   xe pool-param-get uuid='<pool-uuid>' param-name=other-config
   ```

2. Vergleichen Sie Pool und den genauen veralteten Schlüssel mit Ihren Aufzeichnungen zur verwaltenden Appliance.
3. Notieren Sie den Wert dieser Markierung.
4. Entfernen Sie nur bei Bedarf **diesen einen Schlüssel**. Ersetzen Sie beide Platzhalter. Entfernen Sie niemals das gesamte `other-config`:

   ```bash
   xe pool-param-remove uuid='<pool-uuid>' param-name=other-config param-key='xo:clientInfo:<obsolete-appliance-uuid>'
   ```

5. Wiederholen Sie die lesenden Befehle und laden Sie XO Lite neu.

**Prüfung:** Der Schlüssel wird nicht mehr aufgeführt. Kehrt er zurück, ist noch eine alte Appliance verbunden: Sie schreibt ihre Markierung bei Wiederverbindung oder beim nächsten Durchlauf neu. Finden Sie diese verbliebene Verbindung.

## Hoststatistiken lesen {#host-statistics}

Das Lesen von Statistiken ändert nichts an Host, VMs, Netzwerken oder Speicher.

**Vor dem Beginn**

- Wählen Sie einen bekannten, verbundenen und laufenden Host. Notieren Sie ID, Pool, CPU-Anzahl und Speichergröße.
- Diese Registerkarte zeigt nur einen Host. Poolübersicht und Systemmonitor der Appliance zeigen andere Dinge.

1. Öffnen Sie **Stats** des Hosts (`/#/hosts/<id>/stats`). Prüfen Sie den richtigen Host, bevor Sie Diagramme lesen.
2. Beginnen Sie mit dem Standardzeitraum **Last 10 minutes**. Notieren Sie Zeitraum, aktuelle Uhrzeit, Browserzeitzone, Zeitpunkt des neuesten angezeigten Messwerts sowie Aufgaben- oder Verbindungsfehler.
3. Warten Sie mehrere Messintervalle und prüfen Sie neue Daten. Ein weiterhin sichtbares Diagramm belegt keine aktuelle Erfassung.
4. Wählen Sie zum Vergleich einen längeren Zeitraum. XO fordert **AVERAGE**-Messwerte an; ein Punkt eines langen Zeitraums kann daher eine kurze Spitze glätten. Kehren Sie für jüngste Änderungen zum kurzen Zeitraum zurück.
5. Lassen Sie **Stacked values** beim ersten Lesen jeder Reihe ausgeschaltet. Aktivieren Sie es nur zum Vergleich: Es ergänzt aufsummierte CPU- und Netzwerkreihen und kann die Skala ändern. Lesen Sie jedes Mal Legende, Einheit und vertikale Skala.
6. Notieren Sie einen Ausgangswert bei bekannter normaler Last. Vergleichen Sie dann eine bekannte Lastphase desselben Hosts mit gleichem Zeitraum und gleichen Einstellungen. Notieren Sie Reihen, Zeiten, Messabstände und tatsächliche Symptome.

Führen Sie keinen Stresstest in Produktion aus und ändern, migrieren oder starten Sie keinen Gast neu, nur um ein Diagramm zu bewegen. Eine Last auf einem Laborsystem benötigt eine eigene Betreiberfreigabe.

| Zeitraum | Erwartetes Mess- und Aktualisierungsintervall |
| --- | --- |
| Last 10 minutes | 5 Sekunden |
| Last 2 hours | 1 Minute |
| Last day | 1 Stunde; letzte 24 Stundenwerte |
| Last week | 1 Stunde |
| Last year | 1 Tag |

Der Zeitraumname bezeichnet die von XO angeforderte Historie, nicht deren vollständige Aufbewahrung durch den Host. Lange Zeiträume aktualisieren sich nicht alle fünf Sekunden. Vergleichen Sie Messungen mit gleichem Zeitraum und Messabstand. Beachten Sie die angezeigten Zeiten: Der letzte Punkt ist kein Momentanwert.

| Diagramm | Interpretation |
| --- | --- |
| CPU usage | Jede `Cpu`-Reihe ist ein Prozentwert. `All Cpus` ist deren Summe, kein Hostprozentwert: Vier CPUs zu 50% ergeben 200%. Prüfen Sie CPU-Anzahl und Einzelreihen, bevor Sie den Host als ausgelastet bewerten. |
| Memory usage | Gesamter Hostspeicher abzüglich freiem Speicher, als Bytegröße angezeigt. Dies ist weder das Speicherlimit eines Gasts noch der freie RAM einer Anwendung. Fehlen Freispeicherdaten, kann belegter Speicher als null erscheinen: Prüfen Sie unerwartete Nullwerte auf anderem Weg. |
| Network throughput | Nummerierte `eth`-Reihen für Empfang (`rx`) und Senden (`tx`). Ordnen Sie sie den Hostschnittstellen zu. Werte sind Bytegrößen. Umrechnung in Mbps oder Gbps, Bonds und VLANs werden hier nicht behandelt. Eine ruhige Reihe belegt keine gesunde Verbindung oder Gastkonnektivität. |
| Load average | Die eigene Hostmetrik `loadavg`. Kein CPU-Prozentwert und kein Maß für Datenträgerkapazität. Vergleichen Sie sie mit CPU, Speicher, Verkehr und tatsächlicher Last. Hier wird keine allgemeine sichere Schwelle festgelegt. |

**Prüfung:** Im kurzen Zeitraum schreitet der Zeitpunkt des neuesten Messwerts weiter voran.

| Problem | Prüfen |
| --- | --- |
| **No stats.**, endloses Laden, Lücken oder eine flache beziehungsweise Null-Linie | Notieren Sie Host, Zeitraum, Zeitpunkt und Fehler. Prüfen Sie Verbindung und laufenden Host. Laden Sie die Seite neu und wählen Sie wieder den kurzen Zeitraum. Die Registerkarte ruft keine Daten für nicht laufende Hosts ab. Nach einem fehlgeschlagenen Abruf startet bloßes Warten die Erfassung möglicherweise nicht neu. Fehlende Werte werden teilweise zu Nullen. Ein leeres Diagramm oder null belegt keinen unbelasteten oder gesunden Host. |
| Messzeiten bewegen sich weiterhin nicht | Nutzen Sie vor Kapazitätsentscheidungen die [Fehlerbehebung](/docs/xoa-hl/troubleshooting/) und genehmigte Prüfungen direkt auf dem Host. Setzen Sie Statistiken nicht zurück und starten Sie zur Diagrammreparatur keinen Produktionshost neu. |

Diagramme allein belegen keinen Platz für weitere VMs, HA-Failover oder sichere Migration. Messgenauigkeit, vollständige Historie, Uhrabgleich, Alarme, Dashboard- und Poolsummen, SR-Kapazität und Leistungsdiagnose werden hier nicht behandelt.

## Poolbeitritt mit zwei Laborhosts testen {#pool-join}

Ein Beitritt verschiebt einen Host in einen anderen Pool. Er **ändert die Hostmitgliedschaft** und kann fehlende Patches installieren. Üben Sie nur an zwei wiederaufbaubaren Laborhosts.

**Vor dem Beginn**

- Verwenden Sie zwei Laborhosts mit bekannter Version. Das Ziel ist der Master eines Pools, der nur diesen Host enthält. Die Quelle ist der einzige Host eines anderen Pools. Ein alleinstehender Host bildet einen Pool aus einem Host.
- Halten Sie getrennten Konsolenzugriff auf beide Hosts, einen schriftlichen Wiederherstellungs- und Neuaufbauplan sowie eine XOA-HL-Appliance für beide Verbindungen bereit.
- Verwenden Sie weder Produktionspool, HA-Pool, laufende Gäste, gemeinsame oder angeschlossene Arbeitslasten noch einen Host ohne unabhängige Datensicherung.
- Stimmen Sie mit Netzwerk- und Speicherverantwortlichen das Beitrittslayout im selben Netzwerk, DNS und Zeitsynchronisation, getrennten Verwaltungszugriff sowie Wiederherstellung über die Hostkonsole ab. Ein ähnlich benanntes Netzwerk oder SR auf beiden Hosts ist nicht zwangsläufig gemeinsam.

1. Öffnen Sie im **XOA-HL-Browser** **Settings → Servers**. Prüfen Sie eine funktionierende Verbindung für jeden der beiden Pools.
2. Notieren Sie beide Pool-IDs, Zielmaster- und Quellhost-IDs, Produktmarke, Version, Build und Patchstand, Verwaltungsadressen, Netzwerk- und Speicherinventar, VM-Anzahl und laufende Aufträge. Prüfen Sie, dass der Quellpool keinen weiteren Host hat.
3. Stoppen Sie für das Zeitfenster die Sicherungszeitpläne beider Pools. Behalten Sie ihre unabhängigen Wiederherstellungspunkte.
4. Öffnen Sie den **Zielpool** (`/#/pools/<target-pool-id>/general`), identifizieren Sie den Master und wählen Sie **Add hosts**.
5. Wählen Sie nur den vorgesehenen Quellhost. Die Liste blendet Hosts aus Pools mit mehreren Hosts aus. Sie zeigt die Patchunterschiede in beide Richtungen.
6. Wählen Sie **Cancel** und klären Sie die Ursache außerhalb dieses Tests, wenn eine Patchanzahl ungleich null ist, Marke oder Version abweichen, HA aktiv ist, eine VM oder ein SR auf der Quelle erhalten bleiben muss oder der Beitrittspfad unklar ist. Verwenden Sie diesen Dialog weder zur Patchinstallation noch zur Hostevakuierung.
7. Prüfen Sie im genehmigten Fenster im Dialog den genauen Zielpool und Quellhost und wählen Sie einmal **OK**. Die Oberfläche sendet `force: true`, was XAPI `pool.join_force` aufruft. Diese Bestätigung ändert die Pools; sie ist keine harmlose Kompatibilitätsprüfung.
8. Warten Sie auf die Aufgabe. Nach erfolgreichem Beitritt sollte die Quellverbindung verschwinden und die Zielverbindung ihr Inventar aktualisieren. Die Ansicht kann kurz getrennt erscheinen. Senden Sie nicht erneut, nur weil Aufgabe oder Seite noch nicht aktualisiert sind.
9. Aktualisieren Sie die Zielverbindung. Prüfen Sie unveränderte Zielpool-ID und Master, die Zugehörigkeit genau der zwei erwarteten Host-IDs und einen erklärbaren Zustand des alten Quellpools und seiner Verbindung.
10. Prüfen Sie auf jedem Host Netzwerke und PIFs, SR-Anbindungen (PBDs) und Verwaltungszugriff. Prüfen Sie Testspeicher und isoliertes Gastnetz von den richtigen Hosts. Suchen Sie unerwartete VMs, doppelte XOA-Verbindungen, Sicherungsaufträge oder XO-Lite-Markierungen.

**Prüfung:** Der Zielpool behält seinen Master und enthält genau die zwei erwarteten Hosts; beide bleiben über ihre Konsolen erreichbar.

Notieren Sie IDs vorher und nachher, Patchdifferenzzahlen, Aufgabenergebnis, Konsolenzugriff und jedes Prüfergebnis. Behalten Sie den verbundenen Laborpool, wenn dies das gewünschte Ergebnis ist. **Detach** wirft einen Host aus seinem Pool aus: eine eigene Änderung, kein automatisches Zurückrollen. Derselbe Pool belegt keine sichere Migration oder HA.

**Scheitert der Beitritt**, sichern Sie Aufgabe, Fehler, Konsolenzustand und beide Inventare. Der Server kann bereits Patches oder einen Teil des Beitritts angewendet haben. Halten Sie an und folgen Sie dem Wiederherstellungsplan des Hostverantwortlichen. Erzwingen Sie weder ein weiteres Zusammenführen noch das Auswerfen eines Hosts. Späteres Hostentfernen, HA, gemeinsamer Speicher und Livemigration werden hier nicht behandelt.

## Wartungsmodus auf einem Laborhost testen {#host-maintenance-mode}

Der Wartungsmodus deaktiviert einen Host und verschiebt seine laufenden VMs auf andere Poolhosts. Üben Sie nur in einem wiederaufbaubaren Laborpool. Dieser Test installiert keine Patches, startet keinen Host neu und prüft keine Verfügbarkeit während eines Updates. Für Updates siehe [Hostupdate-Anleitung](/docs/guides/updates/#updating-xcp-hl-the-host).

**Vor dem Beginn**

- Verwenden Sie einen **Laborpool mit zwei Hosts** und bekannter Version, dessen Netzwerk und gemeinsamer Speicher bereits eigene Tests bestanden haben. Verwenden Sie keine Produktionslast und keinen frisch verbundenen, ungeprüften Pool.
- Der Host für den Wartungsmodus ist **nicht der Master**.
- Halten Sie getrennten Konsolen- und Verwaltungszugriff auf beide Hosts, eine den Pool verwaltende XOA-HL-Appliance und einen genehmigten Wiederherstellungs- und Neuaufbauplan bereit.
- Verwenden Sie eine Test-VM mit geprüftem, unabhängigem Wiederherstellungspunkt. Sie muss die **einzige** gewöhnliche VM auf dem Quellhost sein. Ihr Speicher und Gastnetz müssen auf dem anderen Host verfügbar sein.
- [Migration im Pool](/docs/xoa-hl/vm-transfer/) muss für diese VM bereits funktionieren. Haben Sie dies noch nicht getestet, führen Sie diesen Test zuerst aus und notieren Sie danach den Quellhostzustand erneut. Halten Sie an, wenn Voraussetzungen oder Migrationsnetz unklar sind.

1. Notieren Sie in **XOA-HL** Pool, Master und beide Host-IDs, Versionen und Patchstände, Aktivierungs- und Betriebszustände, Verwaltungsadressen, Ausführungsort jeder VM, SR-Anbindungen (PBDs), Netzwerke und PIFs, freie Zielkapazität sowie laufende Aufgaben.
2. Beenden oder pausieren Sie Sicherungs- und Wiederherstellungsaufträge.
3. Notieren Sie über eine genehmigte Gastsitzung das aktuelle Anwendungs- und Netzwerkverhalten der Test-VM. Dies ist Ihre Ausgangsbasis.
4. Öffnen Sie **Advanced** des Quellhosts (`/#/hosts/<source-host-id>/advanced`). Prüfen Sie den genauen Host und Pool.
5. Wählen Sie **Enable maintenance mode**. Der Dialog **Maintenance mode** sagt, dass alle laufenden VMs auf andere Poolhosts migriert werden. Wählen Sie im genehmigten Fenster einmal **OK**. XO ruft `host.setMaintenanceMode` auf; dann deaktiviert XAPI den Host und ruft `host.evacuate` auf.
6. Erscheint **Bypass blocked migrations**, brechen Sie ab: Dieser Pfad entfernt die Migrationssperren der VMs.
7. Warten Sie auf das Aufgabenergebnis und aktualisieren Sie Host- und VM-Listen.
8. Prüfen Sie: Quellhost deaktiviert, Test-VM auf vorgesehenem Ziel, keine gewöhnliche VM mehr auf der Quelle und Anwendung sowie Netzwerk entsprechend der Ausgangsbasis. Notieren Sie Aufgabe, Fehler und Konsolenzugriff.
9. Wählen Sie unter **Advanced** desselben Hosts **Disable maintenance mode**. XO ruft `host.enable` auf.
10. Prüfen Sie aktivierten Host, gesunde Verwaltungswege sowie SR- und Netzwerkanbindungen und den Verbleib der VM auf dem Ziel.

**Prüfung:** Der Host ist wieder aktiviert und die Test-VM läuft weiterhin auf dem Ziel. Das Verlassen des Wartungsmodus verschiebt die VM **nicht** zurück. Lassen Sie sie auf dem Ziel oder planen Sie eine eigene, getestete Migration.

Verwenden Sie statt Wartungsmodus weder **Disable** des Hosts noch erzwungenen Neustart, Notabschaltung oder Patchschaltfläche. Aktivieren Sie Sicherungszeitpläne erst nach Prüfung ihres Umfangs und eines isolierten Wiederherstellungspunkts wieder. Behalten Sie IDs vorher und nachher, Zeiten, Gastprüfungen, Aufgabenausgabe, tatsächlichen Hostzustand und Ausführungsort jeder VM. Ein erfolgreicher Schalterwechsel oder bloße Poolmitgliedschaft belegen keine Bereitschaft für Patches oder HA.

**Scheitert die Evakuierung**, halten Sie an: Einige VMs können bereits verschoben sein. Nach einem Evakuierungsfehler aktiviert XO den Host normalerweise wieder, aber ein vorheriger Fehler kann ihn deaktiviert lassen. Lesen Sie tatsächlichen Aktivierungszustand und Ausführungsort jeder VM und folgen Sie dann dem Wiederherstellungsplan des Hostverantwortlichen. Wiederholen Sie den Schalterwechsel nicht, umgehen Sie keine Sperre und starten Sie den Host nicht neu, um einen unklaren Zustand zu beseitigen.

## HA-Bereitschaft in einem Laborpool prüfen {#ha-readiness}

Bei aktivierter Hochverfügbarkeit (HA) kann ein Host bei fehlender Heartbeat-Kommunikation ausgegrenzt und neu gestartet werden. Testen Sie dies nur in einem wiederaufbaubaren Laborpool. Hier wird kein Host absichtlich ausgefallen und kein VM-Neustart gemessen. Bevor Sie Verfügbarkeit beanspruchen, führen Sie einen getrennten, genehmigten Ausfalltest mit einer geschützten Test-VM durch.

**Vor dem Beginn**

- Verwenden Sie einen **Laborpool mit drei Hosts**, bekannter Version, Wiederaufbaumöglichkeit und bestandenen eigenen Prüfungen. Halten Sie gewöhnliche Arbeitslasten fern.
- Verwalten Sie ihn mit einer einzigen XOA-HL-Appliance **außerhalb** des Pools. Appliance und Zugriffsweg müssen außerhalb der Ausfalldomäne bleiben.
- Halten Sie getrennten Konsolen- und Stromzugriff für jeden Host und einen genehmigten Wiederherstellungsplan bereit.
- Lesen Sie die [XCP-ng-HA-Planungsanleitung](https://docs.xcp-ng.org/management/ha/). Sie empfiehlt drei Hosts und beschreibt Netzwerk- und Speicher-Heartbeat, Kapazitäts- und Fencing-Anforderungen. Gleichen Sie diese mit der tatsächlichen XCP-HL-Hostversion ab.
- Ein Beitritt zweier Hosts, eine erfolgreiche Migration oder ein gleichnamiges SR belegt keine HA-Bereitschaft des Pools.

1. Notieren Sie in **XOA-HL** genauen Pool, Master und drei Host-IDs, Hostversionen, Verwaltungsadressen und statische Verwaltungs-IPs, aktuellen HA-Status, VMs, laufende Aufgaben und die eine zuständige XOA-HL-Appliance.
2. Lassen Sie Speicher- und Netzwerkverantwortliche ein gemeinsames, beschreibbares Heartbeat-SR bestätigen, das auf allen drei Hosts angebunden und erreichbar ist. Ebenso müssen gesunde redundante Verwaltungs- und Speicherwege sowie genug Kapazität für geschützte Gäste nach Ausfall eines Hosts bestätigt sein.
3. Notieren Sie SR-ID und Anbindungen (PBDs), nicht nur den Namen. Sind Voraussetzungen oder Konsolenzugriff unklar, halten Sie hier an: Bisher haben Sie nur gelesen.
4. Öffnen Sie **Advanced** des Pools (`/#/pools/<pool-id>/advanced`). Betrachten Sie **Heartbeat SR** und **High Availability**.
5. Aktivieren Sie **High Availability**, um **Enabling high availability** zu öffnen. Der Dialog listet gemeinsame beschreibbare SRs dieses Pools. Vergleichen Sie das infrage kommende SR mit Ihren Speicheraufzeichnungen. Ein gelistetes SR belegt weder Hostanbindungen noch zuverlässigen Heartbeat oder Failover-Kapazität.
6. Wählen Sie **Cancel**, wenn Aufzeichnungen oder Wiederherstellungsplan unvollständig sind. Wählen Sie niemals ein SR nur deshalb, weil es gelistet ist.
7. Nur in einem genehmigten Laborfenster und bei erfüllten Voraussetzungen: Öffnen Sie den Dialog erneut, wählen Sie das notierte SR und einmal **OK**. XO ruft `pool.enableHa` und damit XAPI `pool.enable_ha` auf. Notieren Sie Aufgabe und Fehler.
8. Aktualisieren Sie den Pool. Prüfen Sie aktives **High Availability**, das erwartete SR unter **Heartbeat SR**, Erreichbarkeit aller drei Hosts und keine unerwarteten VMs oder Aufgaben.
9. Deaktivieren Sie bei gesundem Pool und gesicherten Notizen **High Availability**. Wählen Sie unter **Disabling high availability** einmal **OK**. XO ruft XAPI `pool.disable_ha` auf.
10. Prüfen Sie deaktiviertes HA, gesunde Hosts und SR-Wege sowie eigene Freigaben für weitere Arbeiten.

**Prüfung:** HA wurde mit dem erwarteten Heartbeat-SR jeweils einmal aktiviert und deaktiviert; alle drei Hosts blieben erreichbar.

Bei aktivem HA sind Host- und Pool-Patchschaltflächen blockiert. Starten Sie während dieses Tests weder Update noch Neustart. Behalten Sie Pool-, Host- und SR-IDs vorher und nachher, Anbindungen, Kapazitätsannahmen, Aufgabenausgabe, Konsolenzugriff und HA-Status.

**Scheitert die Aktivierung oder wird ein Host ausgegrenzt**, sichern Sie Konsolen-, Aufgaben- und HA-Protokolle und folgen Sie dem Wiederherstellungsplan des Verantwortlichen. Ist der Pool beeinträchtigt, halten Sie an und folgen Sie dessen Störungsverfahren: Der HA-Schalter ist kein allgemeiner Wiederherstellungsbefehl. Wiederholen Sie keinen Schalterwechsel, starten Sie keinen Host-Toolstack neu und verursachen Sie keine Netzwerk- oder Speicherstörung, um einen unklaren Zustand zu beseitigen.

{{< details title="Quellen" closed="true" >}}
- **Hoststatistiken**: [Hostregisterkarte und Aktualisierung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-stats.js), [Zeitraumauswahl und Messintervalle](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/stats.js), [Hoststatistik-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/host.mjs), [RRD-Mittelwerte, Metriken und Cache](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-stats.mjs), [Diagrammsummen, Skalen und Bezeichnungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo-line-chart/index.js), [Speicherberechnung und Byteformatierung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/utils.js).
- **Serververbindungen und XO-Lite-Schaltfläche**: [Serveroberfläche](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js), [Poolmarkierung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [Standardintervalle](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/config.toml), [Adressauswahl der XO-Lite-Schaltfläche](https://github.com/vatesfr/xen-orchestra/blob/13f987ff3d34504a90b89178489e15fa2293d1b3/@xen-orchestra/lite/src/components/XoaButton.vue), [XO-Lite-CE-Build und Patchziele](https://github.com/Vagrantin/xolite-ce/blob/ca72babb35f435b31d4726a7d1e90f42b9c06cb8/.github/workflows/build-xolite-ce.yml), [Unterstützte Regel und Markierungsbereinigung (Issue #126)](https://github.com/Vagrantin/xcp-hl/issues/126).
- **Poolbeitritt**: [Zielaktion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/action-bar.js), [Einzelhostauswahl und Patchanzahl](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/add-hosts-modal/index.js), [force-Flag im Oberflächenwrapper](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [Rechte- und Zusammenführungs-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs), [Versions- und Markenprüfungen, Patcharbeiten und sequenzielle Zusammenführung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/pool.mjs), [Beitritt und Verbindungsübergang](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/xen-servers.mjs), [XAPI join_force](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs).
- **Hostwartung**: [Advanced-Registerkarte und Schaltflächen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-advanced.js), [Bestätigung und Zweig für blockierte Migration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js), [Wartungs-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/host.mjs), [Deaktivieren, Evakuieren, Fehlerbehandlung und Aktivieren](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [Bestätigungstext](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/intl/messages.js).
- **Hochverfügbarkeit**: [Poolauswahl unter Advanced, Heartbeat-SR-Liste und Status](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-advanced.js), [Pool-API und Rechte](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/pool.mjs), [XAPI-Aufrufe](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [XCP-ng-HA-Planungsanleitung](https://docs.xcp-ng.org/management/ha/).
{{< /details >}}
