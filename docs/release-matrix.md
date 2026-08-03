---
layout: default
title: Release Matrix
permalink: /release-matrix/
---

# Release Matrix

Each XCP-HL HomeLab Edition ISO is built from independently-versioned
components. This table records exactly which version of each shipped
together, and which upstream release the patched components were forked
from.

Every version links to its release page in the repository that produced it.
Under each version is the exact package the ISO installs, written the way
`rpm -q` prints it on a running host, so you can match a host back to a row:

```bash
rpm -q xoa-proxy xo-lite-ce
```

| ISO Version | Build Date | xolite-ce | Upstream (xo-lite) | xoa-proxy |
|---|---|---|---|---|
{% for r in site.data.releases %}| [{{ r.iso_version }}](https://github.com/Vagrantin/xcp-ng-ce-iso/releases/tag/{{ r.iso_version }}) | {{ r.build_date }} | [{{ r.components.xolite_ce.version }}](https://github.com/Vagrantin/xolite-ce/releases/tag/{{ r.components.xolite_ce.version }}){% if r.components.xolite_ce.rpm %}<br>`{{ r.components.xolite_ce.rpm }}`{% endif %} | [{{ r.components.xolite_ce.upstream }}]({{ r.components.xolite_ce.upstream_url }}) | [{{ r.components.xoa_proxy.version }}](https://github.com/Vagrantin/xoa-proxy/releases/tag/{{ r.components.xoa_proxy.version }}){% if r.components.xoa_proxy.rpm %}<br>`{{ r.components.xoa_proxy.rpm }}`{% endif %} |
{% endfor %}

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

| Image release | Build date | xoa-hl (software) | Upstream (Xen Orchestra) |
|---|---|---|---|
{% for r in site.data.xoa_releases %}| [{{ r.image_tag }}](https://github.com/Vagrantin/{{ r.repo | default: "build-xoa-hl" }}/releases/tag/{{ r.image_tag }}) | {{ r.build_date }} | [{{ r.xoa_hl_version }}](https://github.com/Vagrantin/xoa-hl/releases/tag/{{ r.xoa_hl_version }}) | [{{ r.upstream_xo }}]({{ r.upstream_url }}) |
{% endfor %}
