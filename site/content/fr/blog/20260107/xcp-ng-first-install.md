---
title: "Guide de première installation de XCP-ng"
date: 2026-01-07T09:00:00+09:00
slug: xcp-ng-first-install
translationKey: blog-xcp-ng-first-install
---

La procédure pas à pas de l'auteur pour une première installation d'XCP-ng 8.3 amont, de l'ISO d'installation à une appliance Xen Orchestra déployée, avec des photographies de l'installateur amont.
{class="lead"}

{{< callout type="warning" >}}
Ce guide décrit **XCP-ng 8.3 amont**, pas XCP-hl. XCP-hl est un logiciel bêta fondé sur XCP-ng 8.3, donc les libellés de l'installateur et certains réglages par défaut peuvent différer dans XCP-hl. Les photographies ci-dessous montrent l'installateur 8.3 amont.
{{< /callout >}}

## À propos de cette page

Ceci est le guide de première installation XCP-ng 8.3 de l'auteur, publié à l'origine sur son blog personnel le 2026-01-07 et migré sur ce site le 2026-11-11 conformément à la décision du propriétaire enregistrée dans la [PR #409](https://github.com/Vagrantin/xcp-hl/pull/409), afin que les pages [premiers pas](/docs/start/) y fassent référence sur le domaine de production. Pour la procédure XCP-hl (téléchargement de l'ISO, vérification de la somme de contrôle, appliance XOA-hl), suivez plutôt [Premiers pas](/docs/start/).

## Avant de commencer

- Une machine dédiée prise en charge par XCP-ng 8.3, avec la virtualisation matérielle activée ; voir les [prérequis amont](https://docs.xcp-ng.org/installation/requirements/).
- Sauvegardez les données des disques que vous allez utiliser. **L'installation efface les disques sélectionnés.**
- Au moins 100 Go sur le disque d'installation, plus de l'espace pour vos VM.
- Une adresse IP de gestion, une passerelle, des DNS et des NTP stables. Une adresse statique ou une réservation DHCP rend l'hôte plus facile à trouver.
- Un second ordinateur avec un navigateur et un accès réseau à l'hôte.

## Écrire l'ISO sur une clé USB

Téléchargez l'ISO XCP-ng 8.3 depuis la [page de téléchargement amont](https://xcp-ng.org/download/), puis écrivez-la sur une clé USB. L'écriture efface la clé USB : vérifiez d'abord avec `dmesg` quel périphérique correspond à la clé, et remplacez `sdX` ci-dessous par ce périphérique :

```bash
sudo dd if=xcp-ng-8.3.0-20250606.iso of=/dev/sdX bs=8M oflag=direct
```

Revérifiez le nom du périphérique avant d'exécuter la commande : écrire sur le mauvais disque l'efface. Attendez la fin de la copie ; cela peut prendre un moment selon la clé USB.

## Installer XCP-ng

XCP-ng est un hyperviseur de type 1, conçu pour être le seul système installé sur la machine. Branchez la clé USB, démarrez dessus et appuyez sur Entrée à l'invite d'amorçage.

1. **Sélectionnez votre disposition de clavier**, puis lisez l'avertissement d'installation et le contrat de licence avant de continuer.

   {{< screenshot src="install/keyboard.jpg" alt="Sélection de la disposition de clavier de l'installateur" >}}

2. **Sélectionnez le disque système et le disque de stockage des VM.** Vérifiez les noms et capacités des périphériques ; ne sélectionnez ni la clé USB d'installation ni un disque dont vous voulez garder les données.

   {{< screenshot src="install/system-disk.jpg" alt="Sélection du disque système" >}}
   {{< screenshot src="install/vm-disk.jpg" alt="Sélection du disque de stockage des machines virtuelles" >}}

3. **Choisissez le type de stockage.** EXT (provisionnement fin) n'utilise que l'espace réellement occupé par vos données : un disque virtuel de 1 To contenant 20 Go de données occupe environ 20 Go sur l'hôte, au prix de l'agrandissement du fichier disque au fur et à mesure. LVM (provisionnement épais) réserve toute la capacité dès le départ et évite cette croissance, au prix de l'espace. EXT est un choix pertinent pour un laboratoire domestique ; LVM convient aux charges sensibles aux performances. Vous pourrez agrandir le disque plus tard depuis Xen Orchestra.

   {{< screenshot src="install/storage-type.jpg" alt="Choix entre le stockage EXT et LVM" >}}

4. **Utilisez Local media comme source d'installation**, et lancez la vérification du média lorsqu'elle est proposée, particulièrement si vous soupçonnez un téléchargement ou une clé USB endommagée.

   {{< screenshot src="install/source.jpg" alt="Sélection de Local media comme source d'installation" >}}

5. **Définissez et conservez le mot de passe root.** C'est le mot de passe le plus important de la plateforme ; conservez-le en lieu sûr. Vous l'utiliserez pour vous connecter à XO Lite et pour connecter l'hôte à Xen Orchestra.

   {{< screenshot src="install/password.jpg" alt="Définition du mot de passe root de l'hôte" >}}

6. **Configurez le réseau de gestion et les DNS.** Utilisez une adresse statique ou une réservation DHCP ; n'utilisez un VLAN que si votre réseau l'exige. Saisissez le nom d'hôte et des serveurs DNS joignables. Si l'adresse changeait plus tard, il vous faudrait un DNS dans votre labo pour retrouver l'hôte.

   {{< screenshot src="install/network.jpg" alt="Configuration de l'adresse IP de gestion et de la passerelle" >}}
   {{< screenshot src="install/dns.jpg" alt="Configuration du nom d'hôte et des serveurs DNS" >}}

7. **Réglez le fuseau horaire et les serveurs NTP, puis relisez l'installation.** Utilisez des serveurs NTP publics si l'hôte atteint internet, ou un serveur NTP interne sinon. Confirmez les disques sélectionnés avant de lancer l'installation.

   {{< screenshot src="install/ntp.jpg" alt="Configuration de la synchronisation horaire" >}}
   {{< screenshot src="install/confirm.jpg" alt="Confirmation finale de l'installation" >}}

8. **Terminez, retirez le média d'installation et redémarrez.** Notez l'adresse de gestion affichée sur la console de l'hôte.

   {{< screenshot src="install/complete.jpg" alt="Installation terminée, prêt à redémarrer" >}}

## Après le premier démarrage : XO Lite

La console de l'hôte n'offre qu'une administration de base pour cet hôte (réseau, VM, ressources, sauvegarde et restauration). L'autre façon d'administrer un hôte unique est XO Lite, l'interface web servie par l'hôte sur le port HTTPS par défaut : ouvrez `https://<ip-de-votre-hôte>` (ou `https://<nom-d'hôte>`) dans votre navigateur. L'hôte utilise initialement un certificat auto-signé ; confirmez que vous vous connectez à votre propre hôte avant de l'accepter. Connectez-vous en `root` avec le mot de passe défini pendant l'installation.

## Déployer XOA

XOA (Xen Orchestra) est l'application web qui administre un ou plusieurs hôtes XCP-ng et leurs VM. Elle s'exécute comme une machine virtuelle sur l'hôte.

1. Dans XO Lite, cliquez sur **Deploy XOA** et choisissez l'image de l'appliance. Dans XCP-hl, le choix par défaut est **XOA-hl** ; voir [Premiers pas](/docs/start/).
2. Remplissez les champs réseau et de déploiement du formulaire, relisez l'image et les identifiants sélectionnés, puis cliquez sur **Deploy**.
3. Attendez le démarrage de la VM appliance, puis ouvrez son adresse dans votre navigateur et connectez-vous. L'appliance a sa propre adresse, différente de l'adresse XO Lite de l'hôte.

Une fois l'hôte connecté dans Xen Orchestra (`Settings → Servers → Add server`, avec l'adresse de l'hôte et ses identifiants root), téléversez un ISO d'installation dans la bibliothèque d'ISO et créez votre première VM. Le [guide d'installation amont](https://docs.xcp-ng.org/installation/install-xcp-ng/) décrit d'autres options.
