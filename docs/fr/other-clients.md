---
layout: default
title: Autres clients XCP-ng
parent: Français
nav_order: 5
lang: fr
---

# Autres clients XCP-ng
{: .no_toc }

XO Lite et Xen Orchestra ne sont pas les seuls moyens de gérer un hôte
XCP-ng. Voici d'autres outils communautaires qui méritent d'être connus.

---

## XenAdminQt

[XenAdminQt](https://github.com/benapetr/XenAdminQt) est une réécriture en
C++/Qt6 du client lourd XenAdmin classique, qui l'amène sur macOS et
GNU/Linux (et, en principe, sur toute plateforme prise en charge par Qt) au
lieu du .NET réservé à Windows. Il dialogue avec la même API JSON-RPC xapi que
celle qui anime XCP-ng et XenServer, et vous donne accès aux consoles des
hôtes et des VM ainsi qu'aux métriques de performance depuis une application
de bureau native. Il est sous licence BSD-2-Clause et encore en version alpha,
mais c'est une excellente alternative pour qui veut un client de bureau
natif et multiplateforme pour XCP-ng. Merci à
[benapetr](https://github.com/benapetr) de le développer et de le maintenir.

---

Vous connaissez un autre client XCP-ng qui mériterait de figurer ici ? Ouvrez
un ticket sur [xcp-hl](https://github.com/Vagrantin/xcp-hl).
