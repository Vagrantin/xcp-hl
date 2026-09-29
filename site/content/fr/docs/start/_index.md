---
title: Bien démarrer
weight: 1
translationKey: getting-started
---

Installez l’hyperviseur, ouvrez XO Lite et déployez XOA-hl pour gérer vos machines virtuelles.
{class="lead"}

<span id="start-overview"></span>

## Qu’est-ce que XCP-hl ?

XCP-hl est une distribution pour homelab basée sur XCP-ng 8.3. Elle s’installe directement sur votre matériel et héberge vos machines virtuelles. **XO Lite** est l’interface légère servie par l’hôte. **XOA-hl** est une VM distincte qui exécute Xen Orchestra, l’interface Web d’administration des hôtes et des VM.

XO Lite propose quatre choix d’appliance : **XOA-hl** (par défaut), l’appliance officielle de Vates, l’image de Ronivay ou une image XVA personnalisée. Ce guide suit le parcours XOA-hl. Consultez les [Fonctionnalités](/docs/guides/features) pour les différences.

<span id="start-requirements"></span>

## Avant de commencer

- Prévoyez une machine dédiée compatible avec XCP-ng 8.3, avec la virtualisation matérielle activée. Consultez les [prérequis amont](https://docs.xcp-ng.org/installation/requirements/) pour le processeur, la mémoire et le réseau.
- Sauvegardez les données des disques concernés. **L’installation efface les disques sélectionnés.**
- Prévoyez au moins **100 Go** sur le disque d’installation pour la bibliothèque ISO automatique de 20 Go, ainsi que l’espace nécessaire aux VM. Les disques compatibles plus petits utilisent le partitionnement amont sans cette bibliothèque. Voir [Stockage ISO](/docs/guides/features#iso-storage).
- Préparez une adresse IP de gestion stable, la passerelle, le DNS et le NTP. Une adresse statique ou une réservation DHCP facilite l’accès à l’hôte.
- Prévoyez un second ordinateur avec un navigateur et un accès réseau à l’hôte. Le déploiement de l’appliance nécessite aussi l’accès à l’URL de l’image choisie.

{{< callout type="warning" >}}
XCP-hl est un logiciel alpha destiné aux homelabs et aux tests. Lisez les notes de version et attendez-vous à des changements entre les versions. Conservez des sauvegardes en dehors de l’hôte.
{{< /callout >}}

<span id="start-download"></span>

## Télécharger et vérifier {#téléchargement-et-vérification}

{{< latest-iso-download text="Télécharger la dernière ISO" shaText="Somme de contrôle SHA256" >}}

<span id="start-verification"></span>

### Vérifier l’ISO

Téléchargez la somme de contrôle et sa signature depuis la même release, puis utilisez la clé publique du projet proposée ci-dessous. Vérifiez l’empreinte avant de faire confiance à la clé : **2F59 1DB9 D2C1 28C4 C3D9 63F4 6DA0 0DCA 5BBA 215A**. Son nom historique est `XCP-ng Community Edition (Master signing key)`.

{{< verify-iso >}}

Écrivez l’ISO sur une clé USB avec un outil d’écriture d’images, ou attachez-la comme média d’installation virtuel. L’écriture efface la clé USB : vérifiez le périphérique sélectionné.

<span id="start-quick-start"></span>

## Démarrage rapide

<span id="start-install"></span>

### 1 · Installer XCP-hl

Voici une **bonne configuration de départ pour un homelab à un seul hôte**, adaptée du [guide de première installation XCP-ng de l’auteur](https://vagrantin.github.io/blog/20260107/xcp-ng-first-install.html). Adaptez les disques, le stockage et le réseau à vos besoins. Les photos montrent XCP-ng 8.3 amont ; les libellés peuvent différer dans XCP-hl. Le [guide d’installation amont](https://docs.xcp-ng.org/installation/install-xcp-ng/) décrit les autres options.

1. **Démarrez l’installateur et choisissez le clavier.** Lisez l’avertissement d’installation et le contrat de licence avant de continuer.

   {{< screenshot src="install/keyboard.jpg" alt="Choix de la disposition du clavier" >}}

2. **Sélectionnez le disque système et le disque destiné aux VM.** Vérifiez les noms et les capacités. Ne sélectionnez ni la clé d’installation ni un disque dont vous souhaitez conserver les données.

   {{< screenshot src="install/system-disk.jpg" alt="Sélection du disque système" >}}
   {{< screenshot src="install/vm-disk.jpg" alt="Sélection du disque destiné aux machines virtuelles" >}}

3. **Choisissez le type de stockage.** EXT avec allocation fine est un choix de départ pratique en homelab : les disques virtuels occupent l’espace au fur et à mesure des écritures. LVM réserve leur capacité allouée. Adaptez ce choix aux charges de travail et surveillez l’espace libre dans les deux cas.

   {{< screenshot src="install/storage-type.jpg" alt="Choix du stockage EXT ou LVM" >}}

4. **Choisissez Local media comme source.** Effectuez la vérification du média proposée, notamment si vous soupçonnez un téléchargement ou une clé USB endommagés.

   {{< screenshot src="install/source.jpg" alt="Sélection de Local media comme source d’installation" >}}

5. **Définissez et conservez le mot de passe root.** Ce compte permet d’ouvrir XO Lite et de connecter l’hôte à Xen Orchestra.

   {{< screenshot src="install/password.jpg" alt="Définition du mot de passe root de l’hôte" >}}

6. **Configurez le réseau de gestion et le DNS.** Utilisez une adresse statique ou une réservation DHCP ; configurez un VLAN seulement si votre réseau le nécessite. Renseignez le nom de l’hôte et des serveurs DNS accessibles.

   {{< screenshot src="install/network.jpg" alt="Configuration de l’adresse IP de gestion et de la passerelle" >}}
   {{< screenshot src="install/dns.jpg" alt="Configuration du nom de l’hôte et des serveurs DNS" >}}

7. **Réglez le fuseau horaire et les serveurs NTP, puis vérifiez l’installation.** Utilisez un serveur NTP interne si l’hôte ne peut pas accéder aux serveurs publics. Vérifiez les disques sélectionnés avant de lancer l’installation.

   {{< screenshot src="install/ntp.jpg" alt="Configuration de la synchronisation horaire" >}}
   {{< screenshot src="install/confirm.jpg" alt="Confirmation finale de l’installation" >}}

8. **Terminez, retirez le média et redémarrez.** Notez l’adresse de gestion affichée sur la console de l’hôte.

   {{< screenshot src="install/complete.jpg" alt="Installation terminée, prête à redémarrer" >}}

<span id="start-open-xo-lite"></span>

### 2 · Ouvrir XO Lite

Ouvrez `https://<adresse-ip-hôte>` dans le navigateur. L’hôte utilise initialement un certificat autosigné : assurez-vous de joindre votre propre hôte avant de l’accepter. Connectez-vous en tant que `root` avec le mot de passe défini à l’installation.

XO Lite est déjà servi par l’hôte ; il n’y a pas de VM XO Lite à installer.

<span id="start-deploy-xoa"></span>

### 3 · Déployer XOA

Cliquez sur **Deploy XOA** dans XO Lite et choisissez **XOA-hl**. Renseignez les champs de réseau et de déploiement du formulaire, vérifiez l’image et les identifiants, puis lancez le déploiement. Attendez le démarrage de la VM et l’attribution de son adresse. Changez les mots de passe par défaut lors de la première connexion.

Le service xoa-proxy de l’hôte transmet l’image XVA choisie à XAPI, qui crée la VM. L’image XOA-hl est déterminée au moment du déploiement, indépendamment de la version de l’ISO.

<span id="start-connect-host"></span>

### 4 · Connecter XO à votre hôte

Ouvrez l’adresse de l’appliance XOA-hl dans votre navigateur. Dans Xen Orchestra, utilisez `Settings → Servers → Add server`, saisissez l’adresse de l’hôte et ses identifiants root, puis confirmez la connexion. L’appliance possède sa propre adresse, distincte de celle de XO Lite sur l’hôte.

Vérifiez ensuite l’hôte et le stockage dans Xen Orchestra, importez une ISO d’installation dans la bibliothèque ISO et créez votre première VM.

<span id="start-updates"></span>

### 5 · Maintenir le système à jour

La mise à jour de l’hôte et celle de l’appliance sont deux opérations distinctes. Utilisez l’onglet **Patches** de l’hôte pour XCP-hl et **Settings → XOA-HL Updates** pour XOA-hl. Lisez le [guide des mises à jour](/docs/guides/updates) avant de commencer.

<span id="start-architecture"></span>

## Architecture en un coup d’œil

{{< architecture >}}

Votre navigateur accède soit à **XO Lite sur l’hôte**, soit à **Xen Orchestra dans la VM XOA-hl**. XOA-hl administre ensuite l’hôte via XAPI. Les autres VM sont hébergées à côté de XOA-hl, et non à l’intérieur.

<span id="start-components"></span>

## Composants

La section [Composants](/docs/components/) décrit les dépôts, les versions amont fixées, les paquets et les chaînes de build. La [Matrice des versions](/docs/reference/release-matrix) indique les versions livrées ensemble dans chaque ISO et image d’appliance ; ce n’est pas une certification de tests d’intégration.

<span id="start-license"></span>

## Licence

XCP-hl est publié sous **AGPL-3.0** et s’appuie sur XCP-ng et Xen Orchestra. C’est un projet communautaire indépendant, sans affiliation, approbation ni support de Vates SAS ou du projet XCP-ng.
