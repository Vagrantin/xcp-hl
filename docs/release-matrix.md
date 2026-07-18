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

| ISO Version | Build Date | xolite-ce | Upstream (xo-lite) | xoa-proxy | xoa-hl |
|---|---|---|---|---|---|
{% for r in site.data.releases %}| {{ r.iso_version }} | {{ r.build_date }} | {{ r.components.xolite_ce.version }} | [{{ r.components.xolite_ce.upstream }}]({{ r.components.xolite_ce.upstream_url }}) | {{ r.components.xoa_proxy.version }} |
{% endfor %}
