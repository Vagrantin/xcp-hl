---
title: Release Matrix
weight: 1
translationKey: release-matrix
aliases: ["/release-matrix/"]
---

Each XCP-hl ISO is built from independently-versioned components. This table
records exactly which version of each shipped together, and which upstream
release the patched components were forked from.

Every version links to its release page in the repository that produced it.
Under each version is the exact package the ISO installs, written the way
`rpm -q` prints it on a running host, so you can match a host back to a row:

```bash
rpm -q xoa-proxy xo-lite-ce
```

{{< release-matrix-iso >}}

[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) has no upstream column:
it is original code written for this project, not a fork, so its version is
its own. Its tag is `v<cargo version>.<build counter>` (for example `v0.1.1.8`
is Cargo version `0.1.1`, eighth build against it), and the RPM release field
carries the CI run number and the source commit it was built from
(`55.gc525575.static`). The two rows tagged `v-proxy-automated-*` predate that
scheme, their tag is a build-run identifier and only the RPM states the
version they shipped.

## XOA HL releases

The XOA-HL image is **not** baked into the ISO: XO Lite's deploy button
resolves the newest VM image release at deploy time, so the appliance is
versioned independently of the ISO. This table records each published image,
the [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) software release it
contains, and the upstream Xen Orchestra version that release was forked
from. Images are published on
[`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) since
[#22](https://github.com/Vagrantin/xcp-hl/issues/22); earlier entries link
back to `xoa-hl`, where they were originally published.

{{< release-matrix-xoa >}}
