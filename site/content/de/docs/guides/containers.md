---
title: Docker-Container
weight: 5
translationKey: containers
---

Führen Sie Docker-Container aus XOA-hl in einer dedizierten VM aus, ohne den Host oder die Appliance anzutasten.
{class="lead"}

{{< callout type="warning" >}}
**Nicht veröffentlicht.** Diese Anleitung beschreibt eine Funktion in Entwicklung. Kein veröffentlichtes XOA-hl-Image enthält sie. Den Stand finden Sie in [Issue #7](https://github.com/Vagrantin/xcp-hl/issues/7).
{{< /callout >}}

## Was Sie erhalten {#what-you-get}

XOA-hl erhält eine Seite **Containers** für Administratoren. Container laufen in einer **Docker-VM**: einer normalen VM, die aus einer vorbereiteten Vorlage erstellt wird und nur Docker ausführt.

- XCP-hl-Hosts und die XOA-hl-Appliance führen selbst nie Docker aus.
- Eine Docker-VM wird wie jede andere VM gesichert, als Snapshot festgehalten, gestartet und gestoppt.
- Jeder Container hat ein CPU-Limit und ein Speicherlimit, damit eine Anwendung den anderen keine Ressourcen entzieht.

## Bevor Sie beginnen {#before-you-begin}

- Melden Sie sich als Administrator bei XOA-hl an.
- Importieren Sie die Docker-VM-Vorlage in Ihren Pool und geben Sie ihr das Tag `xcp-hl-docker-template-v1`. Die Seite Containers weist darauf hin, wenn keine Vorlage gefunden wird.
- Verwenden Sie ein Netzwerk mit DHCP, das XOA-hl erreichen kann. Die Docker-VM braucht Internetzugang oder eine Registry in Ihrem Netzwerk, um Images herunterzuladen.

## Eine Docker-VM bereitstellen {#deploy-a-docker-vm}

1. Öffnen Sie **Containers**. Ohne Docker-VM zeigt die Seite eine kurze Anleitung und das Formular **Deploy Docker VM**.
2. Geben Sie einen Namen, die Anzahl der vCPUs und den Arbeitsspeicher ein. Bei einer Vorlage, einem Standardspeicher und einem Netzwerk wählt die Seite diese für Sie aus.
3. Wählen Sie **Deploy Docker VM** einmal. Die VM wird mit einer eigenen 32-GiB-Disk erstellt und gestartet.
4. Warten Sie beim ersten Start einige Minuten. Solange die VM nicht bereit ist, zeigt die Seite das an; stellen Sie keine zweite VM bereit.

## Einen Container ausführen {#run-a-container}

1. Geben Sie unter **Create container** einen Namen und ein Image ein, zum Beispiel `nginx:alpine`.
2. Behalten oder ändern Sie die Limits. Die Standardwerte sind 1 CPU und 256 MiB.
3. Wählen Sie **Create container**. Ein Image, das noch nicht auf der VM liegt, wird zuerst heruntergeladen, danach startet der Container von selbst. Der Download erscheint über der Liste, bis er endet.
4. Verwenden Sie **Start**, **Stop**, **Restart**, **Logs** und **Remove** für jeden Container. Nur ein gestoppter Container kann entfernt werden, und seine Volumes bleiben erhalten.

Die **Advanced options** nehmen einen Eintrag pro Zeile an:

| Feld | Format | Beispiel |
|---|---|---|
| Veröffentlichte Ports | `HOST:CONTAINER/tcp` | `8080:80/tcp` |
| Persistente Volumes | `NAME:/path` | `web:/usr/share/nginx/html` |
| Umgebung | `KEY=value` | `TZ=UTC` |

Ein veröffentlichter Port ist unter der Adresse der Docker-VM erreichbar, die auf der Seite steht. Legen Sie keine Passwörter in Umgebungsvariablen ab: andere Administratoren und Protokolle können sie anzeigen.

## Die Nutzung im Dashboard verfolgen {#dashboard}

Sobald eine Docker-VM existiert, zeigt das **Dashboard** Administratoren eine Karte **Docker containers**. Für jede Docker-VM nennt sie die laufenden und alle Container, die Last, den belegten Arbeitsspeicher und Datenträger sowie die von laufenden Containern reservierten Limits.

Die Karte hebt hervor, was Aufmerksamkeit braucht: eine gestoppte oder nicht antwortende Docker-VM, einen fehlgeschlagenen Download, fast vollen Arbeitsspeicher oder Datenträger und reservierte Limits über der Größe der VM.

## Limits und Ressourcen {#limits}

Ein Limit ist eine Obergrenze für einen Container, keine Reservierung. Die Summe der Limits kann die VM übersteigen; die Seite warnt Sie dann. Senken Sie ein Limit oder geben Sie der Docker-VM auf ihrer VM-Seite mehr vCPUs oder Arbeitsspeicher.

Den Speicherplatz teilen sich alle Images, Container und Volumes der Docker-VM. Entfernen Sie ungenutzte Images unter **Images**, um Platz freizugeben.

## Sichern und wiederherstellen {#back-up-and-recover}

- Sichern Sie die Docker-VM mit einem normalen XOA-hl-Backup-Job. Sie enthält die Images, die Container und die Volumes.
- Sichern Sie auch die XOA-hl-Appliance. Sie hält die Zugriffsschlüssel jeder Docker-VM, und diese lassen sich nicht neu erzeugen.
- Nach dem Löschen einer Docker-VM führt die Seite ihre Schlüssel unter **Unused access keys** auf. Entfernen Sie sie nur, wenn die VM wirklich fort ist: ein getrennter Pool lässt seine Docker-VMs gelöscht erscheinen.
- Ein Update von XOA-hl aktualisiert die Docker-VM nicht. Ihr System und Docker werden getrennt gepflegt.

## Nicht in dieser Version {#not-in-this-version}

Keine Compose-Dateien, kein Terminal in einem Container, keine privilegierten Container, keine aus der VM freigegebenen Ordner und keine gespeicherten Registry-Passwörter.

Diese Entscheidungen halten die erste Version klein und vorhersehbar.
