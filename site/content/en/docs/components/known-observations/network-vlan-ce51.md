---
title: "Network wizard VLAN observation (ce51)"
translationKey: network-vlan-ce51
excludeSearch: true
weight: 90
---

## Scope

This is a release-scoped, partial observation from SN04 (inventory row 14), run
on 2026-11-03 in Group A full cell n. The nested XCP-HL 8.3.0 build ce55 host
ran an RPM-installed XOA-HL appliance `xoa-hl-5.113.2_e281c536-51.g8da29b0.xcpng8.3.el9.x86_64`
(tag `v5.113.2_e281c536-ce51`, XO server 5.193.1, AlmaLinux 9.8). This was not
the published XVA image. No claim is made about other releases or installation
paths, including the ce52 XVA.

## Observed

In New network, entering VLAN 392 while leaving Interface empty created a
network with no PIF and no VLAN object, without an error or warning. The VLAN
placeholder said “No VLAN if empty”, while the chapter said an empty value is
sent as 0. After using the wizard with the spare uplink, the VLAN PIF reported
`carrier=false` even though the OS link was up and 12 tagged frames were seen
on nested `eth1`.

This was a partial pass only: there was no second pool member, cross-host check,
or recovery fixture. The carrier result is recorded as observed; its meaning is
not established here.

## Post-beta fix plan

After beta launch, inspect the wizard form, request construction, and backend
network/PIF creation path. Then:

1. Make VLAN-without-interface invalid in the UI, with a clear validation
   message; confirm the backend also rejects or safely handles the equivalent
   request.
2. Choose and document one empty-VLAN meaning, then align the placeholder,
   chapter, request value, and backend behavior.
3. Trace the VLAN PIF carrier value against host link state and packet
   observation. Fix it only if its contract is wrong; otherwise document what
   the flag means.
4. Add automated coverage for validation, empty VLAN, and carrier semantics.
5. Run focused acceptance on a disposable beta-derived appliance first. Only
   after that evidence is reviewed, test a ce52 candidate through the supported
   XO Lite XVA route. Record XVA identity, host/build, steps, and results before
   making any ce52 claim.

Do not attribute this ce51 RPM/nested-host result to the ce52 XVA without that
separate test.
