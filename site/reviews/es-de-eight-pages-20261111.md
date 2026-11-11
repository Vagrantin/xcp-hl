# Review of eight ES/DE pages — 2026-11-11

Requested by the owner in the first-beta readiness thread. Reviewer: Codex (AI agent).
Source: `xcp-hl@bb06ae9a70a4e5a386a97d6f515ce6366c8704e8`, merged by the owner in #335
as `2608000cf6637994dde4172a1dac4a540be4e26b`.

## Result

Read all eight pages against their English counterparts: features, updates,
roadmap and the ce51 VLAN observation, in Spanish and German. Checked meaning,
release/route limits, update-plane separation, opt-in automatic updates,
provisioning warnings, recovery commands, issue references and links.

Found and corrected four duplicate explicit heading IDs in the German update
guide. The appliance sections reused the host IDs. Their `-1` suffixes now match
English and Spanish, so appliance bookmarks address the intended sections.
No command or package/repository setting changed. The other seven pages needed
no translation correction in this review. GitHub issue titles remain in their
source language by the roadmap's explicit policy; its historical review date is
retained. This assessment does not establish current roadmap issue status.

Inline code and Markdown-link multisets match English on all eight pages;
commands/code fences were compared without translating their executable text.
The strict manual review gate passes (0 drafts), and structural parity passes
for 152 translated pages (38 × ES/DE/FR/JA). No local Hugo build was run.
Hosted CI provides rendered validation for the anchor change.

This is the requested agent technical/language review, not a new human signoff.
The eight entries remain in `pendingOwnerReview` with their exact current body
hashes and an `agentReview` record. The older owner receipt is not extended to
new translations and no second human reviewer is invented. ES/DE publication
scope remains governed by the owner's existing cutover decision.

## Reviewed body revisions

- `site/content/es/docs/features.md` — `sha256:9f5ae8f20d43f5e46a68aa37e8368cb204a769cdf0173c7fed7f52dc840d2834`
- `site/content/es/docs/guides/updates.md` — `sha256:5a83720b8cf410bf7bd20e1d4a26b81c3e5f99750e13799c6d457c6005a8e05f`
- `site/content/es/docs/reference/roadmap.md` — `sha256:d4706ccbf38ec4e794d29356033fdbf3cd3491b8c00dd1a8821d1e4edd8ffaae`
- `site/content/es/docs/components/known-observations/network-vlan-ce51.md` — `sha256:a235ba84a0d35b829603e057b54ef216aefd8d00a8dfac14f82ec896e75d2458`
- `site/content/de/docs/features.md` — `sha256:435f7a85b46107f6dc4ecabf7f5f1842d7f2687c546c6eec53d7471fb48e58f4`
- `site/content/de/docs/guides/updates.md` — `sha256:ef2ed852a71e4719604ddee2b613a99b8c30d0d73a02c4105270e9d3ffc7504b`
- `site/content/de/docs/reference/roadmap.md` — `sha256:bbf66fceed4cc2d43eaa3bd72b847ea5dc7ed9c085ac26e0799e1d0443ff771f`
- `site/content/de/docs/components/known-observations/network-vlan-ce51.md` — `sha256:b6f618f5dcfe09e37b3035365ad0b046734eace64b0bcbb7708acfb7de53a06d`
