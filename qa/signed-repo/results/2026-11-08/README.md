# Repository consumer validation — 2026-11-08

Result: the required repository-consumer checks for xcp-hl#144 passed on
XCP-ng 8.3 yum/rpm and AlmaLinux 9 dnf/rpm. This is release-scoped repository
validation, not ce52 XVA deployment acceptance or a stable-promotion rehearsal.

## Consumers and tested releases

| Consumer | Identity | Package manager | Release scope |
|---|---|---|---|
| Host | Reset `docs-xcphl`, `v8.3-ce44`; Test host `192.168.0.10`, consumer `192.168.0.17` | yum 3.4.3-158.el7.centos, rpm 4.11.3-32.el7 | xcp-hl-release 0.0.4-4.gce1c74a → 0.0.5-5.g157727f; xo-lite-ce 0.21.0-27.g4e319cd → 0.21.0-39.g54c289b; xoa-proxy 0.1.2.4-68.gc3a2b38 → 0.1.3.1-73.g1b44984 |
| Appliance consumer | Existing `ga-x-xoa`, VM `9f58d3a9-a08d-ad65-a10d-315fa07c7fb6`, MAC verified against `192.168.0.96`; direct RPM installation on AlmaLinux 9 | dnf 4.14.0-34.el9_8.alma.1, rpm 4.16.1.3-40.el9 | xoa-hl 5.113.2_e281c536-51.g8da29b0, tag `v5.113.2_e281c536-ce51` |

The appliance consumer is suitable for testing this dnf implementation and
installed repository file. It is **not** evidence for the supported XO Lite XVA
beta deployment route. Direct RPM installation remains outside supported beta
installation scope. No ce52 artifact or candidate acceptance was used.

## Trust and exact bytes

`production-metadata/` preserves the original signed repomd.xml, signature and
primary XML metadata for all four repository streams. `manifests/` records their
SHA-256 values and verified package checksums; `mirror-*.log` records signature
and checksum verification. The XOA manifest explicitly covers ce51 only, not
all other packages listed in that stream. Other mirrors cover every listed RPM.
The shared public key matches `SOURCES/RPM-GPG-KEY-xcp-ng-ce` in xcp-hl@d3be48b.
Production metadata verified with signing subkey
`5220B3C06492A440AAF16E7AF6A459A03D61B7AB`.

The ce51 RPM is SHA-256
`ec1759c00ef1496c636df71e4a04cff2529ee1b4858db802f6ce54c16823da51`.
Both the published download and the fixture valid control match it. The host
valid control downloads XO Lite ce39 and matches its production manifest.

## Results

Tests use clean per-case caches and distinct repository IDs. Negative tests
force `skip_if_unavailable=0` to distinguish rejection from a silently skipped
repository. Each control must download an actual RPM; an empty/no-op transaction
is not accepted. The retained diagnostic attempts are not passing evidence.

| Case | Host exit | Appliance exit | Observed reason / result |
|---|---:|---:|---|
| Valid control | 0 | 0 | Real RPM downloaded; SHA-256 matches production manifest |
| Missing metadata signature | 1 | 1 | Missing `repomd.xml.asc`; GPG verification enabled |
| Wrong signing key | 1 | 1 | Metadata signature could not be verified / Bad GPG signature |
| Modified repomd.xml | 1 | 1 | Metadata signature could not be verified / Bad GPG signature |
| Modified primary metadata | 1 | 1 | Metadata checksum mismatch |
| Modified RPM bytes | 1 | 1 | Package does not match intended download / checksum mismatch |
| Unavailable repository | 1 | 1 | 404 for repomd.xml; availability control, not a security pass |
| Wrong key, shipped skip behavior | 0 | 1 | Host skips repo; appliance fails |
| Outage, shipped skip behavior | 0 | 1 | Host skips repo; appliance fails |
| Published repository cache/download | 0 | 0 | Production signed metadata and published RPM downloads succeed |
| Host package/config upgrade | 0 | n/a | Old release packages upgraded; RPM verification and refreshed metadata succeed |
| Host repository bootstrap install | 0 | n/a | Release package absent at start; documented bootstrap installs 0.0.5-5.g157727f |

`gpgcheck=0` and `repo_gpgcheck=1` were retained. Host `skip_if_unavailable=True`
and the appliance's shipped `False` were retained. A zero exit from a host
`check-update` against a bad/unavailable repo proves skipping, **not** a passed
signature check. These settings validate signed metadata and the package hash;
they do not enforce the package's own RPM signing key. The optional
`resigned-rpm` and `key-swap` explorations from the broader plan were not rerun.

## Fixture changes and limits

The old fixture tool ignored `<location xml:base=...>`. Current metadata uses
GitHub Release URLs there. Mirroring therefore tried the wrong package URL;
serving those original files for a negative test would also bypass the local
tampered RPM. The fixed mirror follows the signed location. For negative tests,
`localize` retains verified RPM bytes, removes external locations, regenerates
primary XML/checksums, drops stale SQLite metadata and signs with a disposable
fixture key. Consumers explicitly trust that local test key. This separately
proves the consumer rejection behavior; it does not represent a production
metadata signature on modified content. Original production signatures and
checksums are verified and archived independently.

Yum 3 requires the conventional default XML namespace: a first localized attempt
using prefixed element names produced `Nothing to do`, and was rejected as an
inconclusive control. The corrected fixture is tested by a real ce39 download.
The fixture key initially appeared future-dated because the nested VM clock was
141 seconds slow. The clock was corrected before the accepted host tests.

## Setup repairs and reproduction

Jenkins controller: `192.168.0.14`, deployed jenkins-infra@96233746.
A missing `/etc/jenkins-infra/admin-api-token` prevented operator CLI calls.
A named operator API token was created using existing controller credentials
and installed root-only, without printing it or restarting Jenkins.

Docs session 197, owner `qa144`, acquired both docs locks and reached Command-1.
`reset` reverted the two documented snapshots and reached Command-2. A session
job being `building` while awaiting an input is normal reservation ownership;
requiring global Jenkins idle after acquisition would deadlock the tests.
The nested host had zero configured NTP sources, so `chrony-wait` blocked XAPI
startup. Its clock was checked/corrected and the runtime wait stopped; no
persistent host configuration was changed. Production servers were untouched.

The repository-bootstrap test removes only xcp-hl-release with `rpm -e --nodeps`
on this resettable consumer to simulate its absence while retaining the dependent
UI package. It immediately reinstalls the dependency using the documented URL,
key import and yum install. Stock OS repos are disabled for these targeted test
transactions. This is test preparation, not administrator recovery guidance.

Follow `qa/signed-repo/README.md`, use the current `rpm.xcp-hl.org` endpoints,
mirror the exact release bytes, localize negative fixtures and use
`repofile-local-key`. Fixture `.repo` options come from the actual installed
consumer files preserved here. Commands and output are in the transcript files;
`run-appliance-fixtures.sh` preserves the executed appliance loop. The host loop
uses the same variants with yum, repository prefix `qa2-`, `install --downloadonly`
and its shipped `skip_if_unavailable=True` behavior.

## Remaining release gates

This result closes repository consumer validation only. XOA-HL ce52 provenance,
XO Lite XVA deployment/credential cleanup (#310/#311), interrupted appliance
updates (#306/#307), full appliance update/reboot checks, and same-byte
promotion/rollback rehearsal remain independent gates. The broader plan's U4
managed-appliance upgrade was not run in this session.

## Cleanup

Both docs VMs were halted and restored to their original baseline snapshots.
The separately reused ga-x-xoa was halted after removing its fixture repository
and downloads. The xcpng-ce-qa VM started during earlier investigation was also
halted. A final physical-host query showed no running non-dom0 guests.
Jenkins session 197 finished `SUCCESS`, description `released: qa144`.
The temporary fixture HTTP server was stopped.
