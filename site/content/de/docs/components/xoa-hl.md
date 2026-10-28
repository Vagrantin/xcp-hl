---
title: xoa-hl
weight: 4
translationKey: xoa-hl
aliases: ["/de/developers/xoa-hl.html"]
---

XOA-hl-Softwarebuild: passt Xen Orchestra für Homelabs an und verpackt es als RPM.
{class="lead"}

**Repository:** [Vagrantin/xoa-hl](https://github.com/Vagrantin/xoa-hl)
· Sprache: Bash / RPM-Spezifikation · Lizenz: AGPL-3.0

## Zweck {#purpose}

Dieses Repository erstellt **Xen Orchestra HomeLab Edition** (XOA-hl): den vollständigen quelloffenen [`xen-orchestra`](https://github.com/vatesfr/xen-orchestra)-Server mit XO-5-Weboberfläche, abgerufen an einem festgelegten Upstream-Commit, für Homelabs angepasst und für XCP-ng verpackt. Jeder Build veröffentlicht ein Artefakt als GitHub-Release:

| Artefakt | Inhalt |
|---|---|
| `xoa-hl-<version>-<N>.g<commit>.xcpng8.3.el9.x86_64.rpm` | Das fertig gebaute Xen Orchestra (etwa 70 MiB), seine systemd-Units und die Werkzeuge zur Selbstaktualisierung der Appliance |

Dieses RPM installiert [`build-xoa-hl`](/docs/components/build-xoa-hl) in die XOA-VM-Appliance. Veröffentlichte RPM-Repositorys liefern Appliance-Updates; die [Update-Anleitung](/docs/guides/updates) beschreibt stable/testing-Kanäle für den jeweiligen Versionsumfang.

---

## Repository-Struktur {#repo-structure}

```
xoa-hl/
├── UPSTREAM_XO                 ← upstream xen-orchestra pin (commit + version)
├── container/
│   └── Containerfile           ← AlmaLinux 9 build image (Node 24, yarn, rpm tooling)
├── scripts/
│   ├── build-xo.sh             ← the build: fetch + patch + yarn build + tar
│   └── validate-patches.sh     ← checks patches/ against metadata.toml
├── patches/
│   ├── metadata.toml           ← what each patch does and which file it targets
│   ├── menu-hide-items.patch   ← hides Vates-subscription-only menu items
│   ├── xcp-hl-updates.patch    ← adds the XCP-hl repositories to the Patches tab
│   └── xoa-hl-update-api.patch ← the appliance's own "XOA-HL Updates" settings page
├── SPECS/
│   └── xoa-hl.spec             ← the RPM: pre-built XO under /opt/xo + systemd units
├── SOURCES/                    ← systemd units, update scripts, sudoers rule, .repo file
├── pages/                      ← index page + .repo file for the published yum repository
└── .github/workflows/
    ├── build-xoa.yml           ← CI: build + RPM + GitHub Release
    └── pages-repo.yml          ← republishes recent RPMs as a signed yum repository
```

---

## Versionsfestlegung {#version-pinning}

Der Build verwendet einen festen Upstream-Commit, definiert in `UPSTREAM_XO` im Wurzelverzeichnis des Repositorys:

```bash
XO_COMMIT=e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c
XO_VERSION=5.113.2
```

Die Versionszeichenfolge kombiniert beides: `<XO_VERSION>_<short SHA>`, beispielsweise `5.113.2_e281c536`. `build-xo.sh` schreibt sie nach `out/VERSION`, und CI verwendet sie als RPM-Version. Eine Veröffentlichung erfolgt durch Push eines Tags `v<version>-ce<N>`, beispielsweise `v5.113.2_e281c536-ce17`: `N` wird zur RPM-Release-Nummer. Damit ist jeder Build ein eigenständiges Paket, auf das `dnf` aktualisieren kann.

{{< callout type="info" >}}
Die Upstream-Version wird **bewusst** durch Bearbeiten von `UPSTREAM_XO` aktualisiert, niemals automatisch. `5.113.2` ist die letzte XO-5.x-Veröffentlichung vor dem Wechsel von Upstream zu XO 6.
{{< /callout >}}

---

## Buildablauf scripts/build-xo.sh {#build-flow-scriptsbuild-xosh}

Der Build läuft im AlmaLinux-9-Container und arbeitet unter `/build`:

1. **Flacher Abruf des festgelegten SHA**: `git init`, `git fetch --depth 1 origin $XO_COMMIT` und `checkout FETCH_HEAD`. Die Festlegung eines reinen SHA mit `--depth 1` vermeidet den Download der vollständigen Historie von etwa 1 GB und erhält die Reproduzierbarkeit.
2. **Patches anwenden**: Nach der gegenseitigen Prüfung, dass jedes `patches/*.patch` einen Eintrag in `patches/metadata.toml` hat und umgekehrt, wird jeder Patch mit `git apply --verbose` angewendet. In ce40 sind 16 Patches deklariert; Beispiele:
   - `menu-hide-items` blendet ausgewählte Menüpunkte außerhalb des HomeLab-Umfangs aus; das belegt nicht das Fehlen aller zugehörigen APIs.
   - `xcp-hl-updates` fügt die XCP-hl-Repositorys zu der Anfrage hinzu, die Xen Orchestra an das `updater.py`-Plugin des Hosts sendet. So erscheinen XCP-hl-Pakete in der Patches-Registerkarte.
   - `xoa-hl-update-api` ergänzt die eigene Update-API der Appliance und die Einstellungsseite **XOA-HL Updates**.
3. **`packages/xo-server/xoahl.config.toml` schreiben**, die Laufzeitkonfiguration, die das RPM später als Benutzerkonfiguration installiert: HTTPS an Port 443 mit `/opt/xo/xoahl.crt` / `/opt/xo/xoahl.key`, Redis unter `redis://127.0.0.1:6379/0`.
4. **TLS-Erzeugung bis zur RPM-Installation zurückstellen.** Der ce40-Build enthält keinen gemeinsam verwendeten privaten Schlüssel. `%post` erzeugt das erste Schlüsselpaar auf der Appliance (RSA 4096, 3650 Tage, CN `xoa.local`; Schlüsselmodus 600, Zertifikatsmodus 644).
5. **Installieren und bauen**: `yarn`, danach `yarn build` über alle Workspaces (Server und XO-5-Weboberfläche).
6. **Bereinigen**: `.git`, `.github`, `.changesets`, `docs`, `packages/xo-server-test*`, `packages/xo-server-cloud` entfernen.
7. **devDependencies entfernen**: `yarn workspaces focus --production` (Fallback: `yarn install --production`), wobei Workspace-Symlinks erhalten bleiben.
8. **Verpacken**: `tar czf out/xoa-hl-<version>.tar.gz` des gesamten bereinigten Monorepositorys, ohne `**/*.map`. Der Tarball ist ausschließlich Eingabe des RPM-Builds und wird nicht veröffentlicht.

---

## Das RPM SPECS/xoa-hl.spec {#the-rpm-specsxoa-hlspec}

Das RPM enthält das fertig gebaute Xen Orchestra selbst, etwa 70 MiB. Es ist `x86_64`, nicht `noarch`, da der `node_modules`-Baum native Erweiterungen enthält. Es installiert:

| Pfad | Inhalt |
|---|---|
| `/opt/xo` | Fertig gebautes xen-orchestra; TLS-Paar `xoahl.key` / `xoahl.crt` wird bei der Installation erzeugt |
| `/usr/local/bin/xo-cli` | `xo-cli` im `PATH` |
| `/usr/lib/systemd/system/xo-server.service` | Führt xo-server aus `/opt/xo` aus |
| `/usr/lib/systemd/system/xoa-hl-check-update.service` und `xoa-hl-update.service` | Prüfen auf Appliance-Updates und wenden sie an |
| `/usr/libexec/xoa-hl/` | Skripte der beiden Units |
| `/etc/yum.repos.d/xoa-hl.repo` | Eigenes yum-Repository der Appliance |
| `/etc/sudoers.d/xoa-hl` | Erlaubt xo-server das Starten der beiden Update-Units |
| `/var/lib/xoa-hl/` | Ablageort des Update-Protokolls |

Während der Installation führt `%post` Folgendes aus:

1. **Benutzerkonfiguration ausschließlich bei der Erstinstallation initialisieren**: Kopiert `xoahl.config.toml` nach `/root/.config/xo-server/config.toml`, wenn diese Datei nicht existiert. Beim Upgrade bleibt sie unverändert, damit Betreiberanpassungen erhalten bleiben.
2. TLS erzeugen, wenn das Paar oder die Markierung `/var/lib/xoa-hl/tls-generated` fehlt. Die Markierung erlaubt das Ersetzen früherer gemeinsam verwendeter Schlüssel.
3. `systemctl enable redis --now` ausführen und `xo-server` aktivieren. Update-Timer bleiben bis zur ausdrücklichen Konfiguration deaktiviert.

`%posttrans` startet `xo-server` nach Abschluss der Pakettransaktion neu.

`%preun` stoppt und deaktiviert `xo-server` nur bei der endgültigen Entfernung, nicht beim Upgrade. Die RPM-Entfernung löscht paketzugehörige Dateien; Betreiberkonfiguration und nicht zum Paket gehörende Laufzeitdaten können verbleiben. `%postun` lädt systemd bei der endgültigen Entfernung neu.

{{< callout type="error" >}}
xo-server liest `~/.config/xo-server/config.toml` (XDG-Suche). Diese Datei hat Vorrang vor jeder `config.toml` auf Paketebene. Ohne die Initialisierung durch `%post` würden HTTPS-Listener und Redis-URI unabhängig vom Paketinhalt nicht angewendet.
{{< /callout >}}

Laufzeitabhängigkeiten in ce40: Node.js 24 (unter 25), OpenSSL, Redis, `dnf-plugins-core` sowie die von Xen Orchestra für Remotes benötigten Mount-Helfer (`nfs-utils`, `cifs-utils`, `ntfs-3g`, `lvm2`). Das Paket enthält `Epoch: 1` und hat damit Vorrang vor Builds aus der Zeit vor dem aktuellen Nummerierungsschema.

---

## Buildumgebung {#build-environment}

`container/Containerfile` definiert das Buildimage: AlmaLinux 9 mit gcc/make/git/patch, Python 3, Node.js 24 (NodeSource), yarn und `rpm-build`/`rpmdevtools`. Dasselbe Image erstellt Tarball und RPM.

Builds laufen **ausschließlich auf GitHub Actions**; es gibt keinen lokalen Buildworkflow. CI erstellt das Image mit Docker und führt `build-xo.sh` darin aus. Tarball und Datei `VERSION` landen unter `out/` auf dem Runner und gehen in den RPM-Build ein.

---

## CI-Workflow (GitHub Actions) {#ci-workflow-github-actions}

`.github/workflows/build-xoa.yml` startet beim Push eines Tags `v*-ce<N>` und über `workflow_dispatch`:

1. Syntax aller Shellskripte prüfen: `scripts/*.sh` mit `bash` und die im RPM enthaltenen Skripte `SOURCES/*.sh` mit `sh`.
2. Containerimage erstellen und darin `build-xo.sh` ausführen (mit eingebundenen Verzeichnissen `patches/`, `scripts/`, `out/` und Datei `UPSTREAM_XO`).
3. `out/VERSION` lesen und `N` aus dem Tag als RPM-Release-Nummer übernehmen.
4. `rpmbuild -bb SPECS/xoa-hl.spec` im selben Image ausführen, mit dem Tarball unter `SOURCES/`.
5. Ein nach dem Tag benanntes GitHub-Release mit dem RPM veröffentlichen.

`.github/workflows/pages-repo.yml` veröffentlicht ausgewählte Release-RPMs mit signierten Repository-Metadaten. Die Repository-Konfiguration der Appliance definiert die Endpunkte; die Unterscheidung zwischen stable/testing beschreibt [Updates](/docs/guides/updates).

Die vom `xoa-vm-agent` des Orchestrators erstellten **VM-Image-Veröffentlichungen** (Tagpräfix `xoa-image-`, Artefakt `XOA-hl.xva`) erscheinen unter [`build-xoa-hl`](/docs/components/build-xoa-hl), dem Repository des Image-Builds, siehe [#22](https://github.com/Vagrantin/xcp-hl/issues/22).

{{< callout type="warning" >}}
Image-Veröffentlichungen von vor diesem Umzug bleiben hier, damit bereits ausgelieferte ISOs sie weiter auflösen können. Werkzeuge, die dieses Repository nach RPMs durchsuchen, müssen deshalb weiterhin Tags mit `xoa-image-*` überspringen.
{{< /callout >}}

---

## Beziehung zu anderen Komponenten {#relationship-to-other-components}

- [`build-xoa-hl`](/docs/components/build-xoa-hl) installiert dieses RPM in die AlmaLinux-9-Appliance und verpackt sie als XVA-Image.
- [`xolite-ce`](/docs/components/xolite-ce): Die XO-Lite-Bereitstellungsschaltfläche installiert diese Appliance.
- [`xoa-proxy`](/docs/components/xoa-proxy): HTTPS-/gzip-Brücke während der Übertragung des Appliance-Images.
- [`xcp-orchestrator`](https://github.com/Vagrantin/buildorchestration/tree/main/xcp-orchestrator) (im Repository `buildorchestration`): Sein `xoa-vm-agent` startet `build-xoa.yml` und wartet auf die RPM-Veröffentlichung, bevor er den VM-Image-Build startet.

---

## Mitarbeit {#contributing}

Um ein Problem zu melden oder eine Änderung vorzuschlagen, erstellen Sie ein Issue unter [Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).

## Geprüfter Versionsumfang {#reviewed-release-scope}

`v5.113.2_e281c536-ce40` / `xoa-hl@a28085219cdfe9d20700e6060377f5059e42e6b5`.

[UPSTREAM_XO](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/UPSTREAM_XO), [Buildskript](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/scripts/build-xo.sh), [RPM](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec), [Patch-Metadaten](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/patches/metadata.toml).
