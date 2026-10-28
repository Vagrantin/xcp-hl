---
title: "Ihre erste virtuelle Maschine erstellen"
linkTitle: "Ihre erste VM"
description: "Installations-ISO hochladen, eine VM erstellen und deren Betriebssystem installieren."
weight: 20
translationKey: xoa-manual-create-vm
translationStatus: draft
sourceRevision: sha256:8d6fcca90de19f82aff7f4431284f044f9e8f1e2499e67f494ffc106519fd72f
glossaryTerms: ["backup", "host", "pool", "snapshot", "sr", "vm"]
---

Erstellen Sie eine kleine Test-VM, installieren Sie deren Betriebssystem und prüfen Sie, dass sie von ihrer eigenen virtuellen Festplatte startet.

{{< callout type="info" >}}
**Gilt für** Image `xoa-image-20261022-a280852` (Xen Orchestra 5.113.2). Grundlage ist der veröffentlichte Code; ein vollständiger Labordurchlauf und gastspezifische Tests stehen noch aus. Die folgenden Größen sind Beispiele, keine Liste unterstützter Systeme.
{{< /callout >}}

## Vor dem Beginn {#before-you-begin}

- [Melden Sie sich an und verbinden Sie Ihren Host](/docs/xoa-hl/first-login/). Diese Anleitung verwendet ein XOA-HL-Administratorkonto.
- Laden Sie ein Installations-ISO vom Betriebssystemanbieter herunter. Prüfen Sie es mit der vom Anbieter veröffentlichten Prüfsumme.
- Ermitteln Sie zwei Speicherarten: ein **ISO-SR** für Installationsmedien und ein **beschreibbares SR** mit freiem Platz für VM-Festplatten. Nicht jeder Host besitzt die [XCP-HL-ISO-Bibliothek](/docs/features/#iso-storage).
- Brauchen Sie ein neues SR für VM-Festplatten? [Erstellen Sie zunächst NFS-Speicher auf einem leeren, dedizierten Export](/docs/xoa-hl/storage-networks/#nfs-vm-storage). Kehren Sie nach der VM-Installation zu dessen Festplattenprüfungen zurück.
- Wählen Sie ein Gastnetzwerk, das dem Installationsprogramm die benötigten Zugriffe ermöglicht. Lassen Sie ausreichend Host-Arbeitsspeicher und Speicherplatz für XOA-HL und Ihre übrigen VMs frei.

Sie verwalten die VM im **Browser**. Das Betriebssystem wird in der **Konsole der neuen VM** installiert, niemals auf dem XCP-HL-Host oder der XOA-HL-Appliance.

## 1. Installations-ISO bereitstellen {#1-get-the-installer-iso}

Ist bereits ein geprüftes Installationsmedium in einer ISO-Bibliothek vorhanden, verwenden Sie es und überspringen Sie diesen Schritt. Eine dedizierte NFS-Bibliothek verbinden Sie nach [NFS-ISO-Bibliothek verbinden](/docs/xoa-hl/storage-networks/#nfs-iso-library).

Das Hochladen aus dem Browser funktioniert nur, wenn das ISO-SR neue Dateien annimmt und genügend Platz hat. Ein Eintrag in der Importliste beweist das nicht: Manche Bibliotheken können Medien lesen, nehmen aber keine Uploads an.

1. Öffnen Sie **Import → Disk** (`/#/import/disk`). Lassen Sie **From URL** ausgeschaltet, um die heruntergeladene Datei hochzuladen.
2. Wählen Sie das **ISO-SR**, beispielsweise `XCP-HL ISO library`, falls vorhanden. Ziehen Sie die `.iso`-Datei in den Upload-Bereich.
3. Prüfen Sie Dateiname und Ziel. Wählen Sie **Import** und warten Sie auf den Abschluss.
4. Öffnen Sie die Festplattenliste des Ziel-SR und prüfen Sie, dass das ISO vorhanden ist. Fahren Sie nicht mit einem unvollständigen Upload fort.

Erscheint kein geeignetes ISO-SR, richten Sie zunächst eines ein. Der Import eines ISO in normalen VM-Festplattenspeicher macht diesen nicht zu einer ISO-Bibliothek.

## 2. VM erstellen {#2-create-the-vm}

Öffnen Sie **New → VM** (`/#/vms/new`) und wählen Sie Ihren **Pool**. Wählen Sie eine Vorlage zur Installation Ihres Betriebssystems, keine Vorlage mit bereits installiertem System.

Geben Sie der VM einen eindeutigen Namen wie `lab-first-vm`. Die folgenden Größen eignen sich für ein kleines Linux-Testsystem, sofern sie die Anbieteranforderungen erfüllen:

| Assistentenbereich | Auswahl |
| --- | --- |
| Info | Installationsvorlage, Name und Beschreibung. |
| Performance | Beispielsweise 2 vCPUs und 2 GiB RAM. Mehr hinzufügen, falls das Installationsprogramm es benötigt. |
| Installation | **ISO/DVD**, dann das Installations-ISO. |
| Interfaces | Gastnetzwerk. MAC-Adresse leer lassen, damit sie generiert wird, außer Ihr Netzwerk benötigt eine feste Adresse. |
| Disks | Beispielsweise eine 20-GiB-Festplatte auf einem beschreibbaren, vom Host erreichbaren SR. Die Systemfestplatte niemals auf das ISO-SR legen. |
| Advanced | Vorlagenstandards beibehalten, sofern der Gast keine dokumentierte Änderung verlangt. **Boot VM after creation** abwählen, damit Sie die VM selbst starten. |
| Summary | Pool, Vorlage, CPU, Arbeitsspeicher, Netzwerk und Speicher prüfen. |

Wählen Sie **Create**.

**Prüfung:** Eine VM mit Ihrem Namen erscheint, und ihre Einstellungen entsprechen Ihrer Auswahl. Ist **Create** ausgegraut, ist ein Pflichtbereich oder eine Ressourcenprüfung unvollständig. Prüfen Sie den Assistenten, bevor Sie es erneut versuchen.

Für Konsolenbedienelemente oder einen leeren beziehungsweise eingefrorenen Bildschirm siehe [VM-Konsole verwenden](/docs/xoa-hl/vm-operations/#vm-console).

## 3. Betriebssystem installieren {#3-install-the-operating-system}

1. Öffnen Sie die neue VM und prüfen Sie ihren Namen. Starten Sie sie und öffnen Sie den Reiter **Console**.
2. Prüfen Sie, dass das Installationsprogramm startet. Folgen Sie den Installationsschritten des Anbieters innerhalb dieses Gasts.
3. Fragt das Installationsprogramm nach dem Zieldatenträger, prüfen Sie, dass es sich um die **virtuelle Festplatte der neuen VM** handelt (hier 20 GiB). Enthält die Festplatte bereits Daten, halten Sie an und prüfen Sie die VM-Auswahl.
4. Öffnen Sie nach der Installation den Reiter **Disks** der VM und werfen Sie das Installations-ISO aus dem virtuellen CD-Laufwerk aus. Starten Sie den Gast normal neu und prüfen Sie, dass er von seiner virtuellen Festplatte startet.

{{< callout type="warning" >}}
Arbeiten Sie nur an der neuen Test-VM. Das Formatieren einer Festplatte oder ein erzwungenes Ausschalten kann Daten verlieren. Reagiert der Gast, fahren Sie ihn regulär herunter oder starten Sie ihn regulär neu. Stoppen Sie niemals die XOA-HL-Appliance oder den Host, um einen einzelnen Gast neu zu starten.
{{< /callout >}}

## 4. Ergebnis prüfen {#4-check-the-result}

- Der Gast startet ohne Installations-ISO, und Sie können sich über seine Konsole anmelden.
- CPU, Arbeitsspeicher, Festplatten und Netzwerk der VM entsprechen Ihrer Auswahl.
- IP-Adresse, Gateway, DNS und benötigte Verbindungen funktionieren innerhalb des Gasts. Die Konsole funktioniert auch ohne funktionierendes Gastnetzwerk.
- Sie haben Gast-Betriebssystemversion, Vorlage, VM-Name und XOA-HL-Versionen notiert.

Gastwerkzeuge hängen vom Betriebssystem ab. Für Ubuntu 24.04 siehe die nächsten Schritte unten.

Diese VM besitzt noch keine unabhängige Sicherung. Ein Snapshot auf demselben Speicher schützt nicht vor Verlust dieses Speichers. Bewahren Sie keine wichtigen Daten auf der VM auf, bevor Sie Sicherung und Wiederherstellung getestet haben.

## Bei Problemen {#if-something-goes-wrong}

| Problem | Prüfung |
| --- | --- |
| Das ISO fehlt im Assistenten | Prüfen, dass der Upload in ein ISO-SR abgeschlossen wurde und der gewählte Pool oder Host dieses SR erreichen kann. |
| **Create** ist ausgegraut | Pool, Vorlage, Name, Ressourcen, ISO, Netzwerk und Festplattenspeicher prüfen. Jeden Pflichtbereich ausfüllen. |
| Erstellen oder Starten der VM schlägt fehl | Aufgabenfehler lesen. Freien Host-Arbeitsspeicher, freien SR-Platz und Erreichbarkeit von Speicher und Netzwerk vom Host prüfen. Vor einem neuen Versuch prüfen, ob bereits eine VM erstellt wurde. |
| Das Installationsprogramm startet nach jedem Neustart erneut | ISO aus dem CD-Laufwerk dieser VM auswerfen. Prüfen, dass das System auf ihrer virtuellen Festplatte installiert wurde. |
| Der Gast hat kein Netzwerk | Gewähltes Netzwerk sowie IP-Adresse, Gateway und DNS des Gasts prüfen. Nicht das Host-Verwaltungsnetz ändern, um einen Gast zu reparieren. |

## Nächste Schritte {#next-steps}

1. [Test-VM sichern und eine Wiederherstellung prüfen](/docs/xoa-hl/backup-restore/).
2. Für einen Ubuntu-24.04-Gast (amd64) den [Verwaltungsagenten installieren](/docs/xoa-hl/guest-tools/#install-linux-agent). Andere Systeme benötigen eigene Verfahren.
3. Um einen installierten Gast wiederzuverwenden, [neue VMs aus einer Vorlage erstellen](/docs/xoa-hl/templates/#deploy-template).

Siehe auch [Glossar](/docs/xoa-hl/glossary/) und [Update-Anleitung](/docs/guides/updates/).

{{< details title="Quellen" closed="true" >}}
Abgeglichen mit XO@e281c536: [ISO-Import](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/disk-import/index.js), [VM-Assistent](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/new-vm/index.js), [VM-Reiter](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/index.js) and [CD-Auswurfbedienelement](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/iso-device.js); [In xoa-hl@a280852 angewandte Patches](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh).
{{< /details >}}
