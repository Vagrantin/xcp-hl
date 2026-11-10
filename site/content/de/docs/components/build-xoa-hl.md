---
title: build-xoa-hl
weight: 5
translationKey: build-xoa-hl
aliases: ["/de/developers/build-xoa-hl.html"]
---

Packer-Pipeline, die die XOA-hl-VM-Appliance auf XCP-ng erstellt und das von XO Lite CE bereitgestellte XVA-Image erzeugt.
{class="lead"}

**Repository:** [Vagrantin/build-xoa-hl](https://github.com/Vagrantin/build-xoa-hl)
· Sprache: Bash / Packer JSON / Kickstart · Lizenz: AGPL-3.0

## Zweck {#purpose}

Dieses Repository erstellt die **XOA HomeLab Edition VM-Appliance**: eine AlmaLinux-9-VM, die Packer **auf einem echten XCP-ng-Host** installiert und mit dem [`xoa-hl`](/docs/components/xoa-hl)-RPM ausstattet. Das Ergebnis ist ein komprimiertes **XVA-Image**, das die Bereitstellungsschaltfläche von XO Lite CE importiert.

Beim Build ist die Appliance generisch: Sie enthält zwei einmalige Dienste für den ersten Start. Diese lesen Bereitstellungsdaten (Netzwerk, Administratorzugangsdaten) aus XenStore, wenn XO Lite sie bereitstellt. So funktioniert ein einziges Image für alle Benutzer.

---

## Repository-Struktur {#repo-structure}

```
build-xoa-hl/
├── build.config.sample        ← infrastructure config template (copy → build.config)
├── scripts/
│   ├── setup-xoa-builder.sh   ← build entry point: generates Kickstart + Packer JSON, runs build
│   ├── xoa-first-boot.sh      ← in-VM phase 1: XenStore → network + env file
│   └── xoa-credentials.sh     ← in-VM phase 2: sets XO admin credentials via xo-cli
├── systemd/
│   ├── xoa-first-boot.service
│   └── xoa-credentials.service
├── bin/                       ← vendored VMware VDDK tarball (V2V support)
└── artefact/                  ← build/debug artefacts: logs, installed-RPM list, memo
```

---

## Voraussetzungen {#prerequisites}

- Ein Linux-Buildrechner mit `apt` und sudo (entwickelt unter Linux Mint). Das Einrichtungsskript installiert seine Abhängigkeiten selbst: Packer (HashiCorp-apt-Repository), das Packer-Plugin [`ddelnano/xenserver`](https://github.com/ddelnano/packer-plugin-xenserver), `wget`, `curl`, `jq`, `ufw`.
- Ein erreichbarer **XCP-ng-Host** mit root-Zugangsdaten, einem SR namens `Local storage` und einem benannten VM-Netzwerk.
- Eine veröffentlichte [`xoa-hl`](/docs/components/xoa-hl)-Version auf GitHub (das RPM der neuesten Veröffentlichung wird automatisch ermittelt).
- Eine ausgefüllte `build.config`, kopiert aus `build.config.sample`: IP/Zugangsdaten des XCP-ng-Hosts, Netzwerkname, VM-Name und root-Passwort, AlmaLinux-ISO-URL und RPM-URLs für `xe-guest-utilities`.

{{< callout type="warning" >}}
`build.config` enthält **Zugangsdaten im Klartext** (XCP-ng-root-Passwort, VM-root-Passwort). Committen Sie sie niemals; nur `build.config.sample` gehört in git.
{{< /callout >}}

---

## Build-Einstiegspunkt scripts/setup-xoa-builder.sh {#build-entry-point-scriptssetup-xoa-buildersh}

Läuft auf dem Buildrechner und erzeugt alles, was Packer benötigt:

1. **`build.config` laden** (ohne Datei werden integrierte Standardwerte verwendet).
2. **Voraussetzungen installieren**: apt-Pakete, HashiCorp Packer und das Packer-Plugin `ddelnano/xenserver`.
3. **Ports 8000–9000/tcp öffnen** (ufw). Packer stellt die Kickstart-Datei über seinen integrierten HTTP-Server auf einem Port dieses Bereichs für die VM bereit.
4. **AlmaLinux-ISO-Prüfsumme ermitteln**: Liest die `CHECKSUM`-Datei des Mirrors im BSD-Format, mit Fallback auf `SHA256SUMS` im GNU-Format; bricht den Build ab, wenn keine gültige SHA256-Prüfsumme gefunden wird (außer sie ist in `build.config` festgelegt).
5. **Neueste xoa-hl-RPM-URL ermitteln**: Durchsucht `api.github.com/repos/Vagrantin/xoa-hl/releases` nach der neuesten Veröffentlichung mit `.rpm`-Artefakt. Verwendet nicht `releases/latest`: Dies kann noch auf einer `xoa-image-*`-Veröffentlichung von vor [#22](https://github.com/Vagrantin/xcp-hl/issues/22) landen, die nur ein XVA enthält.
6. **`inst.ks` erzeugen**, die Kickstart-Antwortdatei: DHCP auf `eth0`, EXT4-Partitionierung (kein LVM), SELinux und Firewall deaktiviert, minimaler Paketsatz; `%post` aktiviert sshd/chrony, installiert `epel-release`, `wget`, `nc`, `vim` und erstellt den Benutzer `xo` (in `wheel`).
7. **`almalinux-build.json` erzeugen**, die Packer-Vorlage (siehe unten).
8. **Build ausführen**: `packer validate`, danach `PACKER_LOG=1 packer build almalinux-build.json`.

---

## Packer-Vorlage almalinux-build.json {#packer-template-almalinux-buildjson}

Ein einzelner Builder vom Typ `xenserver-iso`: Packer lädt das AlmaLinux-ISO auf den XCP-ng-Host, startet eine VM (2 GB RAM, 10-GB-Datenträger) mit `inst.ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/inst.ks` in der Kernel-Befehlszeile, wartet auf SSH und führt anschließend die Provisioner aus:

1. `dnf update -y`.
2. **xe-guest-utilities** und **xe-guest-utilities-xenstore** installieren (RPM-URLs aus `build.config`), erforderlich für XenStore-Zugriff beim ersten Start.
3. **Node.js 24** installieren (NodeSource).
4. Das **xoa-hl-RPM** installieren; es bringt den gesamten XOA-hl-Stack mit (siehe [`xoa-hl`](/docs/components/xoa-hl): Das RPM enthält das fertig gebaute Xen Orchestra unter `/opt/xo`; sein `%post` aktiviert `redis` und `xo-server`).
5. `xoa-first-boot.sh` / `xoa-credentials.sh` nach `/root/` und die beiden systemd-Units nach `/etc/systemd/system/` hochladen, anschließend beide Units aktivieren.
6. **Image verkleinern**: WLAN-Firmware, firewalld, sssd, NetworkManager-Zusätze, rsyslog, docs/man/info-Seiten und nicht englische Gebietsschemata entfernen; `dnf autoremove` und `clean all`.
7. **Identität entfernen**: `/etc/machine-id` leeren, damit jede bereitgestellte VM eine eigene ID erzeugt.

Wichtige Builder-Einstellungen: `format: xva_compressed` (XVA-Ausgabe), `keep_vm: never` (die gebaute VM wird vom XCP-ng-Host gelöscht) und `vm_name` (`XOA-hl`), das Packer als name-label der VM im XVA hinterlegt. Dieses Label zeigt XO Lite nach der Bereitstellung an; es bestimmt auch den Namen der Ausgabedatei `<vm_name>.xva`.

---

## Automatische Konfiguration beim ersten Start {#first-boot-self-configuration}

Zwei einmalige Dienste sind im Image enthalten. XO Lite schreibt die Bereitstellungsdaten beim Bereitstellen der Appliance in XenStore (`/local/domain/<domid>/vm-data/*`).

### Phase 1: xoa-first-boot.service {#phase-1-xoa-first-bootservice}

Läuft **vor dem Netzwerkstart** (`Before=network.target`, gesteuert durch `ConditionPathExists=!/var/lib/xoa-first-boot.done`). Das Skript:

- liest die `vm-data`-Schlüssel mit `xenstore-read`: `ip`, `netmask`, `gateway`, `dns`, `ntp-servers`, `system-account-xoa-password` und den JSON-Block `admin-account` (E-Mail und Passwort);
- speichert sie in `/etc/xoa-first-boot.env` (Modus 600);
- schreibt eine NetworkManager-Schlüsseldatei (`/etc/NetworkManager/system-connections/xoa-provisioned.nmconnection`), mit statischer IP, falls angegeben, andernfalls DHCP;
- protokolliert ausführlich nach `/var/log/xoa-first-boot.log` für die Diagnose vor Ort.

### Phase 2: xoa-credentials.service {#phase-2-xoa-credentialsservice}

Läuft einmal **nach** `network-online.target` und `xo-server.service`, gesteuert durch `!/var/lib/xoa-credentials.done`. Das Skript:

- wartet bis zu 3 Minuten auf xo-server an Port 443;
- setzt das SSH-Passwort des Systembenutzers `xo` auf den vorgegebenen Wert;
- registriert `xo-cli` mit den initialen Zugangsdaten an `wss://127.0.0.1`, ruft dann `user.changePassword` und `user.set` auf, um die vorgegebenen Administrator-E-Mail und das Passwort anzuwenden;
- **entfernt sich selbst** beim Beenden (trap): schreibt die Abschlussmarkierung, deaktiviert und entfernt beide Units und Skripte und löscht die Umgebungsdatei mit den Geheimnissen.

{{< callout type="info" >}}
Wenn Bereitstellungsdaten fehlen oder Phase 2 fehlschlägt, behält die Appliance die initialen Standardwerte `admin@admin.net` / `admin`. Ändern Sie diese nach der Bereitstellung über die XO-Weboberfläche.
{{< /callout >}}

---

## Ausgaben {#outputs}

- Das komprimierte XVA-Image in `output-xva/` im Buildverzeichnis auf dem Buildrechner.
- Die gebaute VM selbst, auf dem XCP-ng-Host behalten (`keep_vm: always`).
- In der automatisierten Pipeline eine **GitHub-Veröffentlichung in diesem Repository** (`Vagrantin/build-xoa-hl`) mit Tag `xoa-image-<date>-<sha7>` und Artefakt `XOA-hl.xva`, das die Bereitstellungsschaltfläche von XO Lite ermittelt.

---

## Automatisierte Builds: der Orchestrator {#automated-builds-the-orchestrator}

In der täglichen Pipeline wird `setup-xoa-builder.sh` durch die Crate `xoa-vm-agent` aus [`buildorchestration`](https://github.com/Vagrantin/buildorchestration) ersetzt. Sie führt dieselben Schritte programmatisch aus und zusätzlich:

1. Überspringt den Build, wenn HEAD des Repositorys bereits dem zuletzt gebauten SHA entspricht.
2. Startet zuerst den Workflow `build-xoa.yml` in `Vagrantin/xoa-hl` über `workflow_dispatch` und wartet auf die RPM-Veröffentlichung.
3. Führt `packer validate` und `packer build` mit erzeugten Dateien `inst.ks` / `almalinux-build.json` aus.
4. Veröffentlicht das XVA als GitHub-Release mit Tag `xoa-image-<date>-<sha7>` auf **`Vagrantin/build-xoa-hl`**, also diesem Repository (`<sha7>` ist der `xoa-hl`-Commit, aus dem das Image gebaut wurde. Dieser Commit liegt im anderen Repository, deshalb wird das Tag auf `main` erstellt und der Quellcommit im Release-Text erfasst). Image-Veröffentlichungen werden in der [Versionsmatrix](/docs/reference/release-matrix#xoa-hl-releases) dokumentiert.

{{< callout type="info" >}}
Bis [#22](https://github.com/Vagrantin/xcp-hl/issues/22) wurden Images auf `Vagrantin/xoa-hl` veröffentlicht. Diese Veröffentlichungen bleiben dort, damit bereits ausgelieferte ISOs sie weiter auflösen können. Deshalb müssen Werkzeuge, die `xoa-hl` nach RPMs durchsuchen, weiterhin Tags mit `xoa-image-*` überspringen.
{{< /callout >}}

---

## Mitarbeit {#contributing}

Um ein Problem zu melden oder eine Änderung vorzuschlagen, erstellen Sie ein Issue unter [Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
