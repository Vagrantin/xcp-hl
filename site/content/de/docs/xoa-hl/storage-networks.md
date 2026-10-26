---
title: "Datenträger, Speicher, ISO-Bibliotheken und Netzwerke verwalten"
linkTitle: "Speicher und Netzwerke"
description: "Datenträger und Netzwerkschnittstellen hinzufügen, NFS-Speicher und ISO-Bibliotheken anbinden, lokalen Speicher hinzufügen und ein VLAN erstellen."
weight: 50
translationKey: xoa-manual-storage-networks
translationStatus: draft
sourceRevision: sha256:dc1dfa67e33ea10129415cf1f53a040988944af6b59b5e8a76b0fb63a2cbf854
glossaryTerms: ["vm", "sr", "host", "pool"]
---

Fügen Sie einer VM einen Datenträger oder eine Netzwerkschnittstelle hinzu, verbinden Sie NFS-Speicher für ISOs oder VM-Datenträger, machen Sie einen freien Hostdatenträger zu lokalem Speicher und erstellen Sie ein VLAN-Netz. Üben Sie als Administrator der **XOA-HL-Appliance** an einer angehaltenen Test-VM, niemals an der Appliance selbst. Notieren Sie vorher VM-ID, Datenträger und Netzwerkschnittstellen.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852`, Paket `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; noch nicht auf einem Laborsystem getestet.
{{< /callout >}}

## Objekte kennen {#objects}

| Objekt | Bedeutung |
| --- | --- |
| SR | Storage Repository: Speicherort virtueller Datenträger. Freien Platz prüfen |
| VDI | Ein virtueller Datenträger in einem SR |
| VBD | Verbindung zwischen VM und einem ihrer virtuellen Datenträger |
| VIF | Virtuelle Netzwerkschnittstelle einer VM |
| PIF | Netzwerkschnittstelle eines Hosts. Änderungen am Verwaltungsnetz können den Hostzugriff unterbrechen |

Eine VM-Netzwerkschnittstelle ist nicht die Verwaltungsschnittstelle des Hosts. Eine Netzwerkauswahl oder neue MAC-Adresse isoliert keine VM. Prüfen Sie vor dem Verbinden eines geklonten oder wiederhergestellten Gasts tatsächliches VLAN, Uplink und Routing.

## Kleinen leeren Datenträger hinzufügen {#add-disk}

1. Prüfen Sie die angehaltene Test-VM. Öffnen Sie **Disks** (`/#/vms/<id>/disks`) und wählen Sie **New disk**.
2. Wählen Sie ein beschreibbares SR desselben Pools, einen eindeutigen Testnamen und eine kleine Größe mit Einheit. Lassen Sie die Schreibschutzoption aus. Erstellen Sie den Datenträger einmal und warten Sie auf das Ende.
3. Prüfen Sie die neue Zeile: Name, Größe, SR und zugeordnete VM. Notieren Sie Datenträger-ID und verbleibenden freien SR-Platz vor dem Gaststart.

Identifizieren Sie den neuen Datenträger in der Gastkonsole anhand von Größe und Gerätedetails. XO erstellt ihn und hängt ihn an, partitioniert, formatiert oder mountet ihn aber nicht im Gast. Das ist eine eigene betriebssystemspezifische Aufgabe. Formatieren Sie niemals ein Gerät nur anhand eines vermuteten Gerätenamens.

Scheitert die Erstellung, prüfen Sie Aufgabe sowie VM- und SR-Datenträgerlisten vor dem nächsten Versuch: Ein teilweise ausgeführter Vorgang kann einen Datenträger zurücklassen. Sichern Sie den Fehler, prüfen Sie freien Platz und Konnektivität und nutzen Sie bei Bedarf die [Fehlerbehebung](/docs/xoa-hl/troubleshooting/). Verkleinern, Vergrößern oder Verschieben von Datenträgern wird hier nicht behandelt.

## Datenträger aushängen oder löschen {#detach-vs-delete}

Das Entfernen der VBD hängt den Datenträger von der VM ab; seine Daten (VDI) bleiben bestehen. Das Löschen der VDI zerstört Daten; dies ist eine eigene Aktion, die diese Ansicht bei angehängtem Datenträger nicht anbietet. Auch das Trennen einer Verbindung unterscheidet sich von ihrem Entfernen.

Stoppen Sie zum Aufräumen den Gast und identifizieren Sie den leeren Testdatenträger zweifelsfrei. Behalten Sie die VDI, falls ihr Inhalt noch nützlich sein könnte. Löschen Sie niemals Start-, gemeinsame oder unidentifizierte Datenträger zur Beseitigung einer Platzwarnung. [Sichern Sie wertvolle Gastdaten](/docs/xoa-hl/backup-restore/) getrennt.

## Isolierte Netzwerkschnittstelle hinzufügen {#add-vif}

1. Öffnen Sie auf der angehaltenen Test-VM **Network** (`/#/vms/<id>/network`) und wählen Sie **New device**.
2. Wählen Sie ein Netzwerk desselben Pools mit geprüfter Isolation. Lassen Sie die MAC-Adresse für automatische Erzeugung leer und wählen Sie **Create**.
3. Prüfen Sie vor dem VM-Start neue Schnittstelle, Netzwerk und MAC-Adresse. Prüfen Sie danach, dass der Gast sie erkennt und die vorgesehene Konnektivität besitzt.

Entfernen Sie zur Isolation eines Klons oder einer wiederhergestellten Kopie bei angehaltener VM **alle** geerbten VIFs; prüfen Sie vor dem ersten Start die leere Liste. Verwenden Sie die Löschaktion, nicht nur den Verbindungsschalter: Eine getrennte Schnittstelle ist keine isolierte. Ergänzen Sie erst dann ein Testnetz, wenn dessen Nichterreichbarkeit der Produktion bestätigt und kopierte Gastidentitäten bereinigt sind.

Erreicht die VM etwas Unerwartetes, stoppen Sie sie und prüfen Sie ausgewähltes Netzwerk und Isolation außerhalb von XO vor dem nächsten Versuch. Diese Schritte konfigurieren weder Hostschnittstellen (PIFs), Verwaltungsadressen, Bonds noch VLANs; ändern Sie dabei keinesfalls das Host-Verwaltungsnetz. Ein VLAN auf Hosts beschreibt [Labor-VLAN auf freiem Uplink erstellen](/docs/xoa-hl/storage-networks/#host-vlan-network). Für andere VM-Aufgaben siehe [VMs verwalten](/docs/xoa-hl/vm-operations/) oder [Hosts und Pools](/docs/xoa-hl/hosts-pools/).

## NFS-ISO-Bibliothek verbinden {#nfs-iso-library}

Ein ISO-SR enthält Installationsmedien. Es unterscheidet sich von einem beschreibbaren SR für VM-Datenträger und von einem Sicherungsziel. Diese Schritte verbinden einen bestehenden eigenen NFS-Export mit einem anhand der Herstellerprüfsumme geprüften Installations-ISO. Der Speicheradministrator bereitet den Export und die Datei vor; Sie arbeiten nur im Browser und ändern nichts am Host.

**Vor dem Beginn**

- Prüfen Sie, ob der Pool bereits ein geeignetes ISO-SR hat. Stimmen Identität, Hostzugriff und Medien, verwenden Sie dieses.
- Notieren Sie für eine neue Bibliothek NFS-Server, genauen Exportpfad, mit dem Speicheradministrator vereinbarte NFS-Version, Pool und Hosts sowie ISO-Dateiname und Prüfsumme.
- Jeder Host, der das ISO lesen soll, benötigt Zugriffserlaubnis auf den Export. Zugriff aus Browser oder Appliance belegt keine Erreichbarkeit von den Hosts.

1. Öffnen Sie als Administrator **New → Storage** (`/#/new/sr`). Wählen Sie einen Poolhost. Vergeben Sie einen eindeutigen Namen wie `lab-nfs-iso` und eine Beschreibung zur Identifikation des Testexports.
2. Wählen Sie unter **ISO SR** **NFS ISO**. Wählen Sie nicht **NFS** unter **VDI SR**: Das erstellt VM-Datenträgerspeicher. **Local** bezeichnet einen Ordner auf einem Hypervisor-Host, nicht auf Computer oder Appliance. Lokaler, SMB- und Blockspeicher werden hier nicht behandelt.
3. Tragen Sie unter **Server** den NFS-Server ein. Wählen Sie die vereinbarte NFS-Version (angeboten werden Standard, `4` und `4.1`) und dann das Suchsymbol neben dem Server. Ein Versionswechsel sucht nicht erneut; wiederholen Sie deshalb nach Änderungen die Suche. Lassen Sie **Comma delimited NFS options** ohne vereinbarte Optionen leer.
4. Wählen Sie unter **Path** den genauen Export an dessen Wurzel (Unterordner werden nicht behandelt). Warten Sie auf die Pfadprüfung. Fehlt der Export, scheitert die Prüfung oder listet **Storage usage** vorhandene SRs, halten Sie an und lesen Sie Fehler und IDs. Der Assistent führt auch für ISO-Bibliotheken NFS-Prüfungen aus; ein erkanntes SR ist daher nicht unbedingt eine ISO-Bibliothek. Binden Sie es nicht erneut an und akzeptieren Sie keine Warnung zur Erstellung über vorhandenem Speicher.
5. Prüfen Sie unter **Summary** Namen und Typ (`nfsiso`). Prüfen Sie Host, Server und Pfad oben erneut und wählen Sie einmal **Create**. Prüfen Sie bei Fehlern vor erneutem Versuch die SR-Liste des Pools: Eine fehlgeschlagene Anfrage kann ein teilweise erstelltes SR oder eine Hostanbindung hinterlassen.
6. Notieren Sie die neue SR-UUID. Der Backendtyp ist `iso` (`nfsiso` bezeichnet nur die Assistentenauswahl). Öffnen Sie **Hosts** (`/#/srs/<id>/hosts`) und prüfen Sie für jeden Host eine verbundene Anbindung mit richtigem Export. Ein gemeinsames SR belegt keinen Zugriff aller Hosts. Führen Sie VMs nur auf Hosts mit geprüftem Zugriff aus.
7. Verwenden Sie **Rescan all disks** des SRs, warten Sie auf das Ende und öffnen Sie **Disks** (`/#/srs/<id>/disks`). Prüfen Sie ISO-Name und Größe. Wiederholen Sie den Scan nach jeder vom Speicheradministrator hinzugefügten oder ersetzten Datei. Prüfen Sie die Herstellerprüfsumme an der Quelle: Ein erfolgreicher Scan oder gleicher Name belegt keine intakte Datei.

**Prüfung:** Wählen Sie im [Assistenten für neue VMs](/docs/xoa-hl/create-vm/) denselben Pool und prüfen Sie die erwarteten Medien unter **ISO/DVD**. Sind sie vorhanden, überspringen Sie den Browserupload. Vorhandene Medien lesen und neue hochladen sind verschiedene Fähigkeiten: Die Importliste belegt nicht, dass dieses SR neue ISOs annimmt. Öffnen Sie Berechtigungen niemals breit, um einen Upload zu ermöglichen.

| Problem | Prüfen |
| --- | --- |
| Kein Export gefunden oder Pfadprüfung fehlgeschlagen | Notieren Sie den Fehler. Prüfen Sie mit dem Speicheradministrator Server, Pfad, NFS-Version, Exporterkennung und Hostzugriff. Halten Sie an, wenn der Assistent den Export nicht findet. |
| SR vorhanden, aber ein Host getrennt | Prüfen Sie Anbindung, Pfad und Exportzugriff dieses Hosts. Ein anderer verbundener Host reicht nicht. Trennen Sie für Reparaturversuche nicht alle Hosts. |
| Scan funktioniert, ISO fehlt | Prüfen Sie vollständige Datei auf dem vereinbarten Export, Name und Größe sowie ausgewähltes SR. Beheben Sie die Quelle und scannen Sie erneut. Erstellen Sie das SR nicht wiederholt neu. |
| ISO fehlt unter ISO/DVD | Prüfen Sie Pool des Assistenten, SR-Typ ISO, vorhandene Medien und Hostanbindung. Ein NFS-SR für VM-Datenträger ist kein ISO-SR. |
| Erstellung scheitert oder unerwartetes SR erscheint | Sichern Sie Fehler, SR-UUID-Liste und Anbindungen. Identifizieren Sie unvollständige Objekte vor erneutem Versuch oder Bereinigung. Verwenden Sie niemals Forget, Remove oder Formatieren zur Beseitigung ungeklärter Fehler. |

Entfernen Sie kein ISO und trennen oder vergessen Sie dessen SR nicht, solange eine VM es verwendet. Notieren Sie nutzende VMs und werfen Sie das Medium im Testgast vor einer geplanten Bereinigung aus. SR-Entfernung und ISO-Uploads werden hier nicht behandelt.

## NFS-Speicher für VM-Datenträger erstellen {#nfs-vm-storage}

Verwenden Sie dies für ein **beschreibbares SR für VM-Datenträger**. Eine NFS-ISO-Bibliothek enthält Installationsmedien, ein NFS-Sicherungsziel Sicherungen: Keines ist das hier erstellte SR. Gemeinsamer Speicher allein ist keine Sicherung und bedeutet keine Migrations- oder Hochverfügbarkeitsbereitschaft (HA).

### Eigenen Export vorbereiten {#prepare-a-dedicated-export}

- Verwenden Sie einen leeren eigenen Laborexport mit Genehmigung des Speicheradministrators und Platz für Testdatenträger samt Reserve.
- Notieren Sie NFS-Server, genaue Exportwurzel, vereinbarte Version und Optionen sowie Pool und jeden nutzenden Host.
- Der Speicheradministrator muss diesen Hosts Lese- und Schreibzugriff erlauben und Serverplatz sowie Kontingente prüfen.
- Verwenden Sie weder ISO-Export noch Sicherungsziel oder einen Export mit unidentifizierten Daten wieder.

Melden Sie sich als Administrator der **XOA-HL-Appliance** an; Speichererstellung und -prüfung erfordern Administratorrechte am gewählten Host. Notieren Sie zuerst vorhandene SRs. Besteht der Speicher bereits im Pool, prüfen Sie UUID und Hostzugriff, statt ein weiteres SR zu erstellen. Zur SR-Erstellung ist keine VM erforderlich. Soll es Ihre erste VM aufnehmen, erstellen und prüfen Sie zuerst das SR, [erstellen und installieren Sie darauf die VM](/docs/xoa-hl/create-vm/) und kehren Sie zum Datenträgertest zurück. Verwenden Sie niemals XOA-HL selbst als Test-VM.

### SR erstellen und prüfen {#create-the-sr-and-check-it}

1. Öffnen Sie **New → Storage** (`/#/new/sr`), wählen Sie einen Poolhost und vergeben Sie einen eindeutigen Namen wie `lab-nfs-vdis` sowie eine Exportbeschreibung. Wählen Sie unter **VDI SR** **NFS**. Prüfen Sie, dass **NFS ISO** unter **ISO SR** nicht gewählt ist.
2. Tragen Sie **Server** ein, wählen Sie vereinbarte **NFS version** (Standard, `4` oder `4.1`) und das Suchsymbol des Servers. Lassen Sie **Comma delimited NFS options** ohne Vereinbarung leer. Suchen und wählen Sie nach Server- oder Versionsänderung den Pfad erneut: Eine reine Versionsänderung prüft den Export nicht erneut.
3. Wählen Sie unter **Path** die genaue Exportwurzel ohne Unterordner und warten Sie auf die Prüfung. Beachten Sie **Storage usage**. Erscheinen vorhandene SR-UUIDs oder genutzte Einträge, halten Sie an und identifizieren Sie diese mit dem Speicherverantwortlichen. Binden Sie sie nicht erneut an und erstellen Sie kein weiteres SR darüber. Bei NFS fragt XO **nicht** nach Bestätigung vorhandenen Speichers; eine fehlende Warnung belegt deshalb keinen leeren Export.
4. Prüfen Sie unter **Summary** Namen, Typ `nfs` und Pfad. Prüfen Sie Host, Server, Version und Optionen oben erneut und wählen Sie einmal **Create**. Warten Sie. Prüfen Sie bei Fehlern vor erneutem Versuch SR- und Hostanbindungslisten: Fehlgeschlagene Anfragen können Objekte zurücklassen.
5. Notieren Sie die neue SR-UUID. Prüfen Sie unter **General** (`/#/srs/<id>/general`) `Type: nfs`, Größe, belegten und freien Platz sowie Pool.
6. Öffnen Sie **Hosts** (`/#/srs/<id>/hosts`). Notieren Sie für jeden Host die Anbindung (PBD) und prüfen Sie **Connected** mit richtigem `server` und `serverpath` sowie gegebenenfalls `nfsversion` und `options`. Ein verbundener Host belegt keine Verbindung der anderen. Fehlt eine Anbindung oder ist sie getrennt, halten Sie vor dem Ablegen von VMs an. Der Status ist zugleich eine Schaltfläche: Lesen Sie ihn, ohne zu klicken.

### Datenträger auf dem neuen SR testen {#test-a-disk-on-the-new-sr}

1. Folgen Sie [Kleinen leeren Datenträger hinzufügen](#add-disk) auf der angehaltenen Test-VM und wählen Sie dieses SR. Notieren Sie VM-, Datenträger- und Anbindungs-IDs und prüfen Sie SR und Größe des Datenträgers.
2. Starten Sie den Gast nur auf einem Host mit geprüfter Anbindung. Identifizieren Sie den zusätzlichen Datenträger anhand von Größe und Gerätedetails. Partitionieren, Formatieren und Mounten erfordern ein betriebssystemspezifisches Verfahren und sichere Geräteidentifikation.
3. Bereitet ein Gastadministrator diesen **Testdatenträger** vor, schreiben Sie eine harmlose Beispieldatei darauf und notieren Sie deren Prüfsumme. Speichern Sie Ihre Arbeit, fahren Sie den Gast normal herunter, starten Sie ihn erneut und prüfen Sie denselben Datenträger, dieselbe Datei und Prüfsumme.

**Prüfung:** Datei und Prüfsumme sind nach dem Neustart unverändert. Ein leerer Datenträger oder erfolgreicher Scan belegt weder funktionierende noch dauerhafte Schreibvorgänge. Halten Sie dieses Ergebnis getrennt von einem Sicherungs- und Wiederherstellungstest. Bevor Sie die Nutzbarkeit im gesamten Pool behaupten, wiederholen Sie den Lese-/Schreibtest auf jedem Host über einen gesondert genehmigten Platzierungs- oder Migrationstest.

### Wenn etwas schiefgeht {#if-something-goes-wrong}

| Problem | Prüfen |
| --- | --- |
| Kein Export oder Prüfung scheitert | Sichern Sie genauen Fehler, ausgewählten Host, Server, Pfad und Version. Lassen Sie den Speicheradministrator Erkennung, Hostrechte und Konnektivität prüfen. Wechseln Sie zur Umgehung weder auf lokalen oder Blockspeicher noch auf breitere Rechte. |
| Vorhandenes SR erkannt oder Erstellung scheitert | Notieren Sie jede SR-UUID und Anbindung einschließlich unvollständiger Objekte. Klären Sie Eigentümer und Nutzung vor erneutem Versuch oder erneuter Anbindung. |
| Falscher Typ oder Pfad oder getrennter Host | Stoppen Sie neue Zuweisungen. Vergleichen Sie notierten Export mit jeder Hostanbindung. Trennen Sie zur Diagnose nicht alle Hosts und entfernen Sie kein SR. |
| Platzwarnung oder Schreibfehler im Gast | Prüfen Sie SR-Nutzung, freien Serverplatz und Kontingente, laufende Aufgaben und den genauen Gastdatenträger. Bewahren Sie Nachweise und Daten auf. Löschen Sie keine unidentifizierten Datenträger, Snapshots oder NAS-Dateien. |

Sichern Sie zum Aufräumen die abschließende Objektliste und fahren Sie die Test-VM normal herunter. Wenden Sie [Datenträger aushängen oder löschen](#detach-vs-delete) ausschließlich auf den sicher identifizierten Testdatenträger an. Behalten Sie SR und Export, bis deren Verantwortlicher jede Nutzung und jeden Wiederherstellungsbedarf erfasst hat. Zerstören, Vergessen oder erneute Anbindung eines SRs, NAS-Dateilöschung und Standard-Speicheränderung werden ebenso wenig behandelt wie SMB-/iSCSI-Speicher, NFS-Unterordner, Ausfälle, Leistung und poolweite Migration oder HA.

## Lokalen Speicher auf einem freien Datenträger erstellen {#local-disk-storage}

Machen Sie damit einen leeren freien physischen Datenträger in **einem Host** zu einem beschreibbaren SR für VM-Datenträger. Lokaler Speicher gehört nur diesem Host: VMs darauf können ohne Datenträgerverschiebung nicht auf andere Hosts wechseln; bei Hostverlust geht er verloren. Er ist keine Sicherung.

{{< callout type="warning" >}}
Die SR-Erstellung **löscht den gesamten eingegebenen Datenträger oder die Partition**. XO akzeptiert beliebige Gerätepfade. Es prüft weder einen leeren Datenträger noch, ob dieser Host-Systemdatenträger oder bestehendes SR ist.
{{< /callout >}}

### Datenträger auf dem Host identifizieren {#identify-the-disk-on-the-host}

Arbeiten Sie als root **auf dem XCP-HL-Host** mit dem Datenträger über dessen Konsole oder SSH.

1. Listen Sie Datenträger und Identitäten auf. Ersetzen Sie `/dev/sdX` durch den infrage kommenden Datenträger und `<host-uuid>` durch die UUID dieses Hosts.

   ```bash
   lsblk -o NAME,SIZE,TYPE,MODEL,SERIAL,MOUNTPOINT
   ls -l /dev/disk/by-id/
   blkid /dev/sdX
   pvs
   xe pbd-list host-uuid=<host-uuid> params=sr-uuid,device-config
   ```

2. Finden Sie den Datenträger, dessen Größe, Modell und Seriennummer dem hinzugefügten Gerät entsprechen. Er darf weder Partitionen noch Mountpoint zeigen, `blkid` darf nichts ausgeben und `pvs` ihn nicht auflisten.
3. Prüfen Sie, dass kein SR ihn verwendet: Kein `device-config`-Wert nennt diesen Datenträger.
4. Notieren Sie den stabilen Pfad unter `/dev/disk/by-id/`, etwa `/dev/disk/by-id/ata-<model>_<serial>`. Namen wie `/dev/sdb` können sich nach Neustarts ändern; der `by-id`-Pfad nicht.

Sind Inhalte unidentifiziert, halten Sie an. Löschen Sie den Datenträger nicht, um Platz zu schaffen.

### Typ wählen {#choose-the-type}

- **ext (local)** speichert jeden virtuellen Datenträger als Datei und belegt Platz erst beim Schreiben von Daten (Thin Provisioning).
- **LVM (local)** reserviert bei Erstellung die volle Größe jedes virtuellen Datenträgers (Thick Provisioning).

Beide speichern VM-Datenträger. Ohne Grund zur Abweichung verwenden Sie denselben Typ wie beim bestehenden lokalen SR des Hosts.

### SR erstellen und prüfen {#create-the-sr-and-check-it-1}

1. Öffnen Sie in der XOA-HL-Appliance **New → Storage** (`/#/new/sr`). Wählen Sie den **Host** mit dem Datenträger und vergeben Sie einen eindeutigen Namen wie `local-disk2` sowie eine Beschreibung mit Modell und Seriennummer. Wählen Sie unter **VDI SR** **ext (local)** oder **LVM (local)**.
2. Fügen Sie unter **Device** den notierten `by-id`-Pfad ein.
3. Prüfen Sie unter **Summary** Host, Namen und Typ und wählen Sie einmal **Create**.
4. Die Bestätigung lautet *This will erase the entire disk or partition (…) to create a new storage repository.* Prüfen Sie den Pfad in Klammern gegen Ihre Notiz und bestätigen Sie erst dann.
5. Notieren Sie die neue SR-UUID. Prüfen Sie unter **General** (`/#/srs/<id>/general`) den Typ (`ext` oder `lvm`), eine der Datenträgergröße nahe Größe und den Pool.
6. Öffnen Sie **Hosts** (`/#/srs/<id>/hosts`). Prüfen Sie genau eine Anbindung zum gewählten Host mit **Connected** und Ihrem `by-id`-Pfad als `device`.

**Prüfung:** Folgen Sie mit diesem SR [Datenträger auf dem neuen SR testen](#nfs-vm-storage): Testdatei und Prüfsumme überstehen einen Gastneustart. Starten Sie danach den Host im Wartungsfenster neu und prüfen Sie die erneute SR-Verbindung.

### Wenn etwas schiefgeht {#if-something-goes-wrong-1}

| Problem | Prüfen |
| --- | --- |
| Erstellung scheitert mit Gerätefehler | Sichern Sie den Fehler. Prüfen Sie Pfad und das Fehlen von Partitionen, Volumes und Mounts. Löschen Sie keinen Datenträger zwangsweise, dessen Inhalt unidentifiziert ist. |
| Größe falsch oder anderer Host angebunden | Legen Sie keine weiteren Datenträger auf diesem SR ab. Vergleichen Sie dessen `device` mit dem notierten Gerät. Sie könnten einen anderen Datenträger formatiert haben: Lassen Sie alles unverändert und holen Sie Hilfe. |
| SR nach Hostneustart getrennt | Prüfen Sie mit `ls -l /dev/disk/by-id/` den weiterhin vorhandenen `by-id`-Pfad und lesen Sie den Anbindungsfehler. Erstellen Sie kein neues SR auf demselben Datenträger: Das löscht ihn. |

Entfernen oder Zerstören eines lokalen SRs, RAID, Partitionen als SR-Geräte, **ZFS (local)** und VM-Verschiebung zwischen lokalen SRs werden hier nicht behandelt.

## Labor-VLAN auf freiem Uplink erstellen {#host-vlan-network}

Dies **ändert Host- und Poolkonfiguration**: Ein getaggtes Gastnetz wird im **XOA-HL-Browser** erstellt. Verwenden Sie einen Testpool, einen eigenen freien physischen Uplink und eine angehaltene Test-VM. Halten Sie durchgehend eine getrennte Hostkonsole bereit.

**Vor dem Beginn**

- Notieren Sie Pool, Master und jeden Host mit vorhandenen Netzwerk- und PIF-UUIDs, Gerätenamen, MAC-Adressen, VLANs, MTU, Verwaltungsmarkierungen, IP-Modi und Verbindungszuständen.
- Lassen Sie den Netzwerkadministrator VLAN-ID, getaggte Switchports, MTU `1500`, Gastadressen sowie erlaubte und verbotene Ziele genehmigen.
- Prüfen Sie den freien Uplink auf **jedem** Host: kein Verwaltungs-, Speicher-, Sicherungs- oder anderer Verkehr, keine Host-IP und keine Bond- oder bestehende VLAN-Mitgliedschaft. Vergleichen Sie Verkabelungs- und Switchaufzeichnungen; Gerätename oder fehlende Management-Markierung reichen nicht.
- Halten Sie an, wenn das Layout unbestätigt ist. Eine VLAN-Nummer allein isoliert nichts und konfiguriert weder Switchports, Routing, DHCP, DNS noch Firewalls.

### Netzwerk einmal erstellen {#create-the-network-once}

1. Öffnen Sie als Administrator **New → Network** (`/#/new/network`) und wählen Sie den Test-**Pool** (Pooladministratorrechte erforderlich). Lassen Sie **Bonded network** und **Private network** aus; Private network ist eine andere SDN-Funktion.
2. Wählen Sie unter **Info → Interface** die notierte freie **PIF des Poolmasters**. Die Liste zeigt Master-PIFs ohne VLAN und verbirgt Bondmitglieder, zeigt jedoch **auch** Verwaltungs-PIFs. Gleichen Sie UUID, Gerät und MAC mit Aufzeichnungen ab. Lassen Sie Interface nicht leer: Dies erstellt ein Netzwerk ohne Uplink, nicht das gewünschte VLAN.
3. Vergeben Sie klare **Name** und **Description** für das Labor. Setzen Sie **MTU** auf `1500` und **VLAN** auf die genaue genehmigte getaggte VLAN-ID. Lassen Sie VLAN nicht leer und verwenden Sie nicht `0`: Ein leeres Feld wird als `0` gesendet. Wählen Sie **No NBD Connection**; dieses Gastnetz benötigt kein NBD.
4. Prüfen Sie Pool, Master-PIF, VLAN, MTU und beide Netzwerktyp-Schalter und wählen Sie einmal **Create network**. Warten Sie auf Abschluss und **Network** des Pools (`/#/pools/<id>/network`). Sichern Sie bei Fehlern die Meldung und prüfen Sie Poolnetzwerke sowie PIFs jedes Hosts vor erneutem Versuch. XO versucht nach fehlgeschlagener Erstellung aufzuräumen; dies belegt keine vollständige Rücknahme aller Pooländerungen.

### Jeden Host prüfen {#check-every-host}

1. Kopieren Sie die neue Netzwerk-UUID aus ihrer Zeile in der Poolansicht und notieren Sie Namen, MTU und VLAN. PIF- und VLAN-Zusammenfassung dieser Zeile stammen ausschließlich vom **Master**.
2. Klappen Sie **PIFs** auf und vergleichen Sie Host, Gerät und MAC-Adresse mit Aufzeichnungen. Das Statussymbol zeigt den **physischen Link (Carrier)**. **Connected** unter Network eines Hosts zeigt die Anbindung der PIF. Keines belegt fließenden getaggten Verkehr. Klicken Sie nicht zum Lesen eines Status auf Verbinden oder Trennen.
3. Öffnen Sie für jeden Host **Network** (`/#/hosts/<id>/network`), finden Sie die PIF des neuen Netzes und notieren Sie UUID, Gerät, MAC, VLAN, MTU, Verwaltungsmarkierung, IP-Modus und Adresse sowie Status. Prüfen Sie genaue genehmigte VLAN-ID, MTU `1500`, angebundenen Zustand, erwarteten Link und keine Host-IP darauf.
4. Vergleichen Sie Verwaltungs- und Speicherkonnektivität mit den Ausgangsnotizen.

Fehlt eine PIF, ist sie getrennt oder unerwartet, halten Sie vor der Gastplatzierung an. Ändern Sie zur Behebung keine bestehenden VLAN-, MTU- oder IP-Felder und schalten Sie übergeordnete PIFs nicht um.

### Gastkonnektivität prüfen {#check-guest-connectivity}

1. Folgen Sie auf einer angehaltenen Test-VM [Isolierte Netzwerkschnittstelle hinzufügen](#add-vif) und wählen Sie genau dieses Netz. Notieren Sie VM- und VIF-UUIDs, MAC-Adresse, Netzwerk und geplanten Ausführungshost. Prüfen Sie, dass keine geerbte Schnittstelle den Laborentwurf umgeht.
2. Starten Sie die VM nur auf einem Host mit geprüfter PIF. Der Gastadministrator richtet über die Konsole die vereinbarte **ungetaggte Schnittstelle** und eindeutige IP-Einstellungen ein. Diese Schritte richten keinen VLAN-Trunk im Gast ein.
3. Prüfen Sie Gastadresse, Subnetz, Route und DNS getrennt. Testen Sie einen genehmigten Peer oder Dienst und die vom Administrator genannten verbotenen Ziele einschließlich Produktion. Ein fehlgeschlagener Ping belegt keine Isolation. Notieren Sie ausgeführte Tests und Ergebnisse.
4. Fahren Sie den Gast normal herunter, starten Sie ihn erneut und wiederholen Sie die Prüfungen.

**Prüfung:** Der Gast erreicht den genehmigten Peer, erreicht die verbotenen Ziele nicht und behält dies nach Neustart; Hostverwaltung, Speicher und XOA-HL bleiben durchgehend erreichbar. Ein Peer auf demselben Host testet weder physischen Uplink noch anderen Host: Hostübergreifender Verkehr und Migration benötigen jeweils eigene genehmigte Tests.

| Problem | Prüfen |
| --- | --- |
| Freie PIF fehlt oder falscher Pool | Prüfen Sie Master, physisches Gerät und Bond- oder VLAN-Zugehörigkeit. Halten Sie an. Wählen Sie zur Umgehung weder Verwaltungs- noch Speicher-PIF und ändern Sie nicht den Pool. |
| Fehler, doppeltes Netzwerk oder fehlende PIFs einzelner Hosts | Sichern Sie Zeiten, Fehler sowie genaue Netzwerk- und PIF-UUIDs aller Hosts. Prüfen Sie diese vor erneutem Versuch mit dem Verantwortlichen. Eine Benachrichtigung belegt keine rückgängig gemachten Änderungen. |
| Link aktiv, aber erwarteter Gastverkehr fehlt | Prüfen Sie Anbindungszustand, VIF-Zuordnung, Gast-IP, Route und DNS, genehmigten getaggten Switchpfad sowie Peer und Firewall. Raten Sie niemals durch Änderung von Host-Verwaltungs-IP, übergeordneter MTU oder VLAN. |
| Unerwarteter Produktionszugriff oder Verlust von Verwaltung beziehungsweise Speicher | Stoppen Sie den Testgast, behalten Sie Nachweise und verwenden Sie die getrennte Hostkonsole mit dem Wiederherstellungsplan des Netzwerkadministrators. Nehmen Sie bei unklarem Layout keine weiteren Browseränderungen vor. |

Sichern Sie zum Abschluss endgültige Aufzeichnungen und fahren Sie die Test-VM normal herunter. Entfernen Sie die identifizierte Test-VIF nur, wenn die obigen Schritte es verlangen. Behalten Sie Netzwerk, PIFs und Switchkonfiguration, bis deren Verantwortlicher jede Nutzung erfasst und einen Entfernungs- und Wiederherstellungsplan genehmigt hat. Netzwerklöschung, VLAN-/MTU-Änderung, PIF-Entfernung, Bonds, Verschiebung des Verwaltungsnetzes und Host-IP-Einstellungen werden hier nicht behandelt. Eine MTU-Änderung eines bestehenden Netzes kann dessen Schnittstellen trennen und erneut verbinden. Siehe auch [Hosts und Pools](/docs/xoa-hl/hosts-pools/), [Fehlerbehebung](/docs/xoa-hl/troubleshooting/) und [Netzwerkkonnektivität diagnostizieren](/docs/xoa-hl/troubleshooting/#network-connectivity).

{{< details title="Quellen" closed="true" >}}
- **Datenträger und Schnittstellen**: [Datenträgeroberfläche und SR-Auswahl](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-disks.js), [VM-Schnittstellenoberfläche](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [Datenträger- und Schnittstellenaktionen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/xo/index.js).
- **NFS-Speicher und ISO-Bibliotheken**: [Assistent für neue SRs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/sr/index.js), [SR-API und Prüfungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/sr.mjs), [SR-Neuscanaktion](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/action-bar.js), [Hostanbindungen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-host.js), [ISO-Import-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/disk.mjs), [ISO-Auswahl für neue VMs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js).
- **SR-Kapazität**: [XO5 `tab-general.js`](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/sr/tab-general.js).
- **VLAN-Netzwerke**: [VLAN-Assistent](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/network/index.js), [Netzwerk-API](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/network.mjs), [Pool-VLAN-Erstellung und Bereinigung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi/index.mjs), [Poolnetzwerkansicht](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js), [PIF-Carrier-Ansicht](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js), [Hostnetzwerkansicht](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js), [PIF- und Netzwerkfelder](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [MTU-Aktionen](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/xapi/network.mjs).
- **Lokaler Speicher**: [Formular für neues SR und Löschbestätigung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new/sr/index.js), [ext- und LVM-Erstellung](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/api/sr.mjs).
{{< /details >}}
