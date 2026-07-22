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

| ISO Version | Build Date | xolite-ce | Upstream (xo-lite) | xoa-proxy |
|---|---|---|---|---|
{% for r in site.data.releases %}| {{ r.iso_version }} | {{ r.build_date }} | {{ r.components.xolite_ce.version }} | [{{ r.components.xolite_ce.upstream }}]({{ r.components.xolite_ce.upstream_url }}) | {{ r.components.xoa_proxy.version }} |
{% endfor %}

## XOA HL releases

The XOA-HL image is **not** baked into the ISO: XO Lite's deploy button
resolves the newest VM image release at deploy time, so the appliance is
versioned independently of the ISO. This table records each published image,
the [`xoa-hl`](https://github.com/Vagrantin/xoa-hl) software release it
contains, and the upstream Xen Orchestra version that release was forked
from.

| Image release | Build date | xoa-hl (software) | Upstream (Xen Orchestra) |
|---|---|---|---|
{% for r in site.data.xoa_releases %}| [{{ r.image_tag }}](https://github.com/Vagrantin/xoa-hl/releases/tag/{{ r.image_tag }}) | {{ r.build_date }} | [{{ r.xoa_hl_version }}](https://github.com/Vagrantin/xoa-hl/releases/tag/{{ r.xoa_hl_version }}) | [{{ r.upstream_xo }}]({{ r.upstream_url }}) |
{% endfor %}
