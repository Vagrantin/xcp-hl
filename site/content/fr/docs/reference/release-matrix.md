---
title: Matrice des versions
weight: 1
translationKey: release-matrix
---

Chaque ISO XCP-hl est construite à partir de composants versionnés
indépendamment. Ce tableau consigne exactement quelle version de
chacun a été livrée ensemble, et de quelle version amont les composants
modifiés ont été dérivés.

Chaque version renvoie vers sa page de release dans le dépôt qui l'a produite.
Sous chaque version figure le paquet exact que l'ISO installe, écrit comme
`rpm -q` l'affiche sur un hôte en fonctionnement, ce qui vous permet de faire
correspondre un hôte à une ligne :

```bash
rpm -q xoa-proxy xo-lite-ce
```

{{< release-matrix-iso >}}

[`xoa-proxy`](https://github.com/Vagrantin/xoa-proxy) n'a pas de colonne
amont : c'est du code original écrit pour ce projet, pas un fork, sa version
lui est donc propre. Son tag suit la forme
`v<version cargo>.<compteur de build>` (par exemple, `v0.1.1.8` correspond à
la version Cargo `0.1.1`, huitième build sur cette base), et le champ release
du RPM porte le numéro d'exécution de la CI et le commit source à partir
duquel il a été construit (`55.gc525575.static`). Les deux lignes taguées
`v-proxy-automated-*` sont antérieures à ce schéma : leur tag est un
identifiant d'exécution de build et seul le RPM indique la version livrée.

## Versions de XOA HL {#xoa-hl-releases}

L'image XOA-HL n'est **pas** intégrée à l'ISO : le bouton de déploiement de
XO Lite résout la dernière version publiée de l'image de VM au moment du
déploiement, l'appliance est donc versionnée indépendamment de l'ISO. Ce
tableau consigne chaque image publiée, la version du logiciel
[`xoa-hl`](https://github.com/Vagrantin/xoa-hl) qu'elle contient, et la
version amont de Xen Orchestra dont cette version est dérivée. Les images
sont publiées sur
[`build-xoa-hl`](https://github.com/Vagrantin/build-xoa-hl) depuis
[#22](https://github.com/Vagrantin/xcp-hl/issues/22) ; les entrées plus
anciennes renvoient vers `xoa-hl`, où elles avaient été publiées à
l'origine.

{{< release-matrix-xoa >}}
