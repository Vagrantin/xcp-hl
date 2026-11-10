---
title: "Observation VLAN de l’assistant réseau (ce51)"
translationKey: network-vlan-ce51
weight: 90
---

## Périmètre

Il s’agit d’une observation partielle et limitée à une version, issue de SN04
(ligne d’inventaire 14), exécuté le 2026-11-03 dans la cellule complète A. Sur
l’hôte XCP-HL 8.3.0 build ce55 imbriqué, l’appliance XOA-HL installée par RPM
était `xoa-hl-5.113.2_e281c536-51.g8da29b0.xcpng8.3.el9.x86_64` (tag
`v5.113.2_e281c536-ce51`, serveur XO 5.193.1, AlmaLinux 9.8). Ce n’était pas
l’image XVA publiée. Aucune conclusion ne concerne les autres versions ou modes
d’installation, notamment la XVA ce52.

## Observation

Dans « New network », saisir VLAN 392 en laissant Interface vide a créé un
réseau sans PIF ni objet VLAN, sans erreur ni avertissement. L’indication du
champ VLAN disait « No VLAN if empty », alors que le chapitre indiquait qu’une
valeur vide est envoyée comme 0. Après utilisation correcte de l’assistant avec
la liaison montante de réserve, le PIF VLAN indiquait `carrier=false`, alors que
la liaison était active dans le système et que 12 trames balisées avaient été
observées sur `eth1` imbriqué.

Le résultat est un succès partiel : aucun second membre du pool, contrôle entre
hôtes ou dispositif de récupération n’était disponible. La signification de
l’indicateur carrier n’est pas établie ici.

## Plan de correction après le lancement bêta

Après le lancement bêta, examiner le formulaire, la construction de la requête
et le chemin backend de création du réseau/PIF.

1. Refuser dans l’interface un VLAN sans interface et afficher une explication
   claire ; vérifier aussi que le backend rejette ou traite sûrement la requête.
2. Définir le sens d’un VLAN vide et harmoniser l’indication, le chapitre, la
   valeur envoyée et le comportement backend.
3. Comparer l’indicateur carrier du PIF VLAN à l’état de la liaison et aux
   paquets observés. Ne le corriger que si son contrat est incorrect ; sinon,
   documenter sa signification.
4. Ajouter des tests automatisés pour la validation, le VLAN vide et la
   sémantique de carrier.
5. D’abord effectuer une acceptation ciblée sur une appliance bêta jetable.
   Après examen de ces preuves seulement, tester un candidat ce52 par la voie
   prise en charge XO Lite XVA. Consigner l’identité XVA, l’hôte/build, les
   étapes et les résultats avant toute conclusion sur ce52.

Ne pas attribuer ce résultat RPM/nested-host de ce51 à la XVA ce52 sans ce test
distinct.
