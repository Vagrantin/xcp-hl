---
title: xolite-ce
weight: 2
translationKey: xolite-ce
aliases: ["/de/developers/xolite-ce.html"]
---

XO Lite für XCP-hl neu gebaut: auswählbare XOA-Bereitstellungsimages und die RPM-Buildpipeline.
{class="lead"}

**Repository:** [Vagrantin/xolite-ce](https://github.com/Vagrantin/xolite-ce)
· Sprache: TypeScript / Vue 3 (Patch) · RPM-Spezifikation · Lizenz: AGPL-3.0

## Was ist XO Lite? {#what-is-xo-lite}

XO Lite ist die schlanke Verwaltungsanwendung als einzelne Webseite, die mit jedem XCP-ng-Host ausgeliefert wird. Sie läuft vollständig im Browser, wird direkt vom Host bereitgestellt und ist als Vue-3-/TypeScript-/Vite-SPA umgesetzt.

Auf einem regulären XCP-ng-Host lädt und importiert die XO-Lite-Ansicht **"Deploy XOA"** ein fest vorgegebenes Xen-Orchestra-Image. XCP-hl ersetzt diese Ansicht durch eine Auswahl **"XOA Image URL"** mit vier Quellen: XOA-hl (Standard), offizielles Vates-Image, Ronivays Image oder eine eigene XVA-URL. Hinzu kommt der Schalter **"Verify if ssl certificate is valid"**, mit dem `xoa-proxy` selbstsignierte Zertifikate der Image-Quelle akzeptieren kann.

---

## Der Patch {#the-patch}

Zum Patchen dient das Rust-Werkzeug `xoa-deploy-patcher`, das während des Builds musterbasierte Änderungen an `xoa-deploy.vue` anwendet. Es übernimmt außerdem `patches/en-hl.json` (HL-Sprachtexte) und `patches/xolite-loader.html` (Ersatz-Loader ohne den Fallback zum externen Laden von `lite.xen-orchestra.com`).

Die geänderte Ansicht **"Deploy XOA"** erhält eine Auswahl **"XOA Image URL"** mit vier Quellen:

  - **XOA-hl** *(Standard)*: Xen Orchestra für XCP-hl aus dem Quellcode erstellt
  - **Vates image**: die offizielle Appliance
  - **Ronivay's image**: ein aus Quellcode erstelltes Community-XO
  - **Custom URL**: beliebiges XVA, unkomprimiert oder gzip-komprimiert, über HTTP oder HTTPS

Der Schalter **"Verify if ssl certificate is valid"** ermöglicht `xoa-proxy`, selbstsignierte Zertifikate auf dem vorgeschalteten Image-Server zu akzeptieren.

---

## Buildpipeline {#build-pipeline}

### Überblick {#overview}

```
1. Read XO_VERSION from the RPM in the upstream XCP-ng ISO
2. Clone vatesfr/xen-orchestra at the matching release tag
3. Apply patches/community-xoa-deploy.patch
4. Install dependencies with Yarn (Corepack)
5. Build XO Lite: yarn build:xo-lite
6. Assemble RPM source tarball
7. rpmbuild -ba SPECS/xo-lite-community.spec
8. rpmsign with the RPM signing subkey (GPG_PRIVATE_KEY + GPG_PASSPHRASE)
9. Publish RPM + xcp-ng-ce-public.asc as GitHub Release assets
```

### Versionsermittlung {#version-detection}

Die gewünschte XO-Lite-Version wird aus dem bereits auf dem Upstream-XCP-ng-ISO enthaltenen RPM gelesen und ist nicht fest im Code hinterlegt:

```bash
XO_VERSION=$(rpm -qp --qf '%{VERSION}' xo-lite-*.rpm)
```

Dadurch stimmt das Community-RPM stets mit der Upstream-Version überein und kann diese direkt ersetzen.

### Tarball-Struktur {#tarball-structure}

Der an `rpmbuild` übergebene Quell-Tarball hat folgenden Aufbau:

```
xo-lite-{VERSION}/
├── dist/               ← compiled Vite output
├── CHANGELOG.md
├── LICENSE
└── xolite.html         ← renamed from scripts/xolite-loader.html
```

Der Dateiname `xolite.html` ist erforderlich: Dies ist der vom XCP-ng-Host bereitgestellte Einstiegspunkt, der XO Lite im Browser lädt.

### RPM-Spezifikation {#rpm-spec}

`SPECS/xo-lite-community.spec` definiert:

- `Name: xo-lite-community`
- `Version: %{XO_VERSION}` (beim Build eingefügt)
- `Provides: xo-lite` (erfüllt Abhängigkeiten vom Upstream-Paket)
- `Conflicts: xo-lite` (verhindert parallele Installation mit dem Upstream-RPM)
- Dateiliste: Inhalt von `dist/` und `xolite.html`

---

## Lokale Entwicklung {#local-development}

### Voraussetzungen {#prerequisites}

- Node.js 20+ und Yarn (über `corepack enable` aktiviert)
- `rpmbuild` (Paket `rpm-build` unter RHEL/CentOS/Fedora)
- `rpmsign` (Paket `rpm-sign`)
- Öffentlicher Community-GPG-Schlüssel im Schlüsselbund importiert

### Ablauf {#workflow}

```bash
# 1. Clone the repo
git clone https://github.com/Vagrantin/xolite-ce.git
cd xolite-ce

# 2. Clone upstream xen-orchestra at the target tag
XO_VERSION=<version>
git clone --depth 1 --branch v${XO_VERSION} \
    https://github.com/vatesfr/xen-orchestra.git upstream

# 3. Apply the community patch
cd upstream
git am ../patches/community-xoa-deploy.patch
cd ..

# 4. Install dependencies
cd upstream
corepack enable
yarn install
cd ..

# 5. Build XO Lite
cd upstream
yarn build:xo-lite
cd ..

# 6. Test the UI
scp -r lite/dist/ xcp-ng-host:/opt/xensource/www/
```

### Patch für eine neue Upstream-Version aktualisieren {#updating-the-patch-for-a-new-upstream-version}

```bash
# In a fresh upstream clone, make the changes manually
# then generate a new patch:
git diff HEAD > ../patches/community-xoa-deploy.patch
# or using format-patch for a clean commit:
git format-patch HEAD~1 -o ../patches/
```

---

## GPG-Signierung {#gpg-signing}

Das `xo-lite-community`-RPM wird mit dem **RPM-Signatur-Unterschlüssel** des XCP-hl-Schlüsselpaars signiert. Derselbe Unterschlüssel signiert auch das `xoa-proxy`-RPM: Ein gemeinsamer Unterschlüssel wird für alle Community-RPMs verwendet.

Das Projekt veröffentlicht seinen gemeinsamen [öffentlichen Schlüssel](https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc) im Wurzelverzeichnis der Produktionswebsite. Prüfen Sie vor dem Import den Fingerabdruck des Hauptschlüssels. Die folgenden Befehle benötigen eine RPM-Implementierung mit Unterstützung für Signatur-Unterschlüssel. XCP-ng 8.3 Dom0 verwendet das ältere RPM 4.11; installierte Hosts prüfen stattdessen signierte Repository-Metadaten mit `repo_gpgcheck=1`. Behalten Sie die Repository-Einstellungen aus [Updates](/docs/guides/updates) unverändert bei.

So prüfen Sie das RPM lokal:

```bash
curl -fLO https://vagrantin.github.io/xcp-hl/xcp-ng-ce-public.asc
gpg --show-keys --with-fingerprint xcp-ng-ce-public.asc
# 2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A
rpm --import xcp-ng-ce-public.asc
rpm --checksig xo-lite-ce-*.rpm
```

---

## CI-Workflow (GitHub Actions) {#ci-workflow-github-actions}

Der Workflow startet bei einem Push auf `main`.

Wichtige Schritte:

```yaml
- name: Detect XO version
  run: echo "XO_VERSION=$(rpm -qp --qf '%{VERSION}' ...)" >> $GITHUB_ENV

- name: Clone upstream at tag
  run: git clone --depth 1 --branch v${{ env.XO_VERSION }} ...

- name: Apply patch
  run: git am patches/community-xoa-deploy.patch

- name: Build XO Lite
  run: |
    corepack enable
    yarn install
    yarn build:xo-lite

- name: Build RPM
  run: rpmbuild -ba SPECS/xo-lite-community.spec

- name: Sign RPM
  run: |
    echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --import
    echo "${{ secrets.GPG_PASSPHRASE }}" | gpg --passphrase-fd 0 --batch \
      --pinentry-mode loopback --yes --armor
    rpm --addsign RPMS/x86_64/xo-lite-community-*.rpm

- name: Publish release
  uses: softprops/action-gh-release@v1
  with:
    files: |
      RPMS/x86_64/xo-lite-community-*.rpm
      xcp-ng-ce-public.asc
```

---

## Mitarbeit {#contributing}

Um ein Problem zu melden oder eine Änderung vorzuschlagen, erstellen Sie ein Issue unter [Vagrantin/xcp-hl](https://github.com/Vagrantin/xcp-hl/issues).
