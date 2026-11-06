---
title: "Dépanner les échecs de sauvegarde et autres problèmes"
linkTitle: "Dépannage"
description: "Trouvez la cause des problèmes de réseau, de sauvegarde, de mise à jour et de connexion, puis signalez un problème."
weight: 82
translationKey: xoa-manual-troubleshooting
translationStatus: draft
sourceRevision: sha256:ad4ea25dfe126d3b06321685ebdd65769812ad5e2231dacdc7fd7771ac464b47
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Partez du symptôme et de la dernière opération qui l’a précédé, puis suivez la vérification correspondante. La plupart des vérifications ne font que lire des informations : vous vous connectez à l’**appliance XOA-HL** dans votre navigateur, en tant qu’administrateur. Certaines demandent la console de l’appliance ou celle d’un invité. Avant de réessayer une mise à jour, un import ou une sauvegarde en échec, conservez l’erreur et les journaux.

{{< callout type="info" >}}
**S’applique à** l’image `xoa-image-20261022-a280852`, paquet `v5.113.2_e281c536-ce40` (Xen Orchestra 5.113.2). Rédigé d’après le code publié ; pas encore testé en laboratoire. Pour l’image reconstruite le 2026-10-27 avec le correctif de configuration (`build-xoa-hl@fa0c987`), voir la [première connexion](/docs/xoa-hl/first-login/#identify-the-rebuilt-image). Le périmètre des tests ci-dessus reste inchangé.
{{< /callout >}}

## Partir du symptôme {#symptoms}

| Problème | À vérifier |
| --- | --- |
| La page de l’appliance ne s’ouvre pas | Dans XO Lite, vérifiez que la VM de l’appliance fonctionne et que son adresse et son réseau sont corrects. Vérifiez ensuite `xo-server` et l’espace disque avec les [vérifications par la console](#appliance-checks). **Vérification :** la bonne URL ouvre la page de connexion. |
| La première connexion échoue | Suivez le [guide de première connexion](/docs/xoa-hl/first-login/) pour les identifiants web, la vérification de l’image reconstruite et le compte de secours des anciennes images. Avec un accès console autorisé, lisez le journal de provisionnement. **Vérification :** vous pouvez vous connecter, et le mot de passe initial a été changé. |
| Un hôte est activé mais rien n’apparaît | Dans **Paramètres → Serveurs**, lisez l’erreur de connexion. Vérifiez l’adresse de l’hôte, les identifiants, l’identité du certificat et que l’appliance peut atteindre l’hôte. **Vérification :** l’hôte et son stockage apparaissent, sans erreur de connexion. |
| La création ou l’installation d’une VM échoue | Notez l’erreur de la tâche avant de réessayer. Vérifiez le pool, le modèle, l’espace libre du SR, le réseau et le média de démarrage avec [Créer votre première VM](/docs/xoa-hl/create-vm/). **Vérification :** une VM de test démarre l’installateur choisi. |
| Une sauvegarde ou une restauration échoue | Lisez le journal de la tâche. Vérifiez la destination, les identifiants, l’espace libre et le SR cible, puis suivez [Diagnostiquer une sauvegarde NFS en échec](#backup-failures). Retirez toutes les cartes réseau d’une copie restaurée avant son premier démarrage, comme dans [Sauvegarder et restaurer une VM](/docs/xoa-hl/backup-restore/). **Vérification :** la tâche réussit, et une copie restaurée isolée contient les données attendues. |
| La page de mise à jour se déconnecte | L’installation du paquet redémarre `xo-server`. Lisez le journal de mise à jour et l’état du service. Ne lancez pas une seconde mise à jour. **Vérification :** le journal se termine par son marqueur de succès, la version est celle attendue, vous pouvez vous connecter et les hôtes sont listés. |
| La vérification des mises à jour affiche ERROR | Lisez `/run/xoa-hl/status` et le journal du service de vérification. Cherchez des erreurs de dépôt ou de réseau, ou une mise à jour déjà en cours, avant de vérifier de nouveau. **Vérification :** une nouvelle vérification renvoie `UP_TO_DATE` ou `AVAILABLE`. |
| Une mise à jour automatique ne s’est pas exécutée | Vérifiez le mode enregistré, le fuseau horaire de l’appliance et la liste des timers. Une fenêtre manquée pendant que l’appliance était éteinte n’est pas rattrapée au démarrage suivant. **Vérification :** le bon timer est planifié, et les heures d’exécution suivantes correspondent à la fenêtre. |
| Un import de configuration échoue | Conservez l’erreur et le journal du serveur : certains changements peuvent rester. Suivez le [test d’import isolé](/docs/xoa-hl/configuration-backup/). **Vérification :** le test réussit sur une nouvelle appliance jetable. Ne supposez pas que la cible en échec est inchangée. |
| Aucun administrateur ne peut se connecter | Mot de passe perdu, appareil du code à usage unique perdu, ou connexion LDAP ou SAML cassée. Suivez [Récupérer l’accès administrateur](#recover-admin-access) depuis la console de l’appliance. **Vérification :** le compte se connecte avec son nouveau mot de passe et apparaît comme **Administrateur**. |

Pour les problèmes de console, comme les commandes ou un écran vide ou figé, voir [Utiliser la console d’une VM](/docs/xoa-hl/vm-operations/#vm-console).

## Diagnostiquer la connectivité réseau {#network-connectivity}

Utilisez ces vérifications en lecture seule pour un réseau invité ordinaire existant, ou pour le [VLAN de laboratoire](/docs/xoa-hl/storage-networks/#host-vlan-network). Connectez-vous en tant qu’administrateur XOA-HL, pour voir chaque VM, chaque pool et chaque hôte.

**Avant de commencer**

- Les vérifications dans l’invité demandent une session autorisée sur sa console. Les responsables des commutateurs, du DNS et des pare-feu vérifient ces éléments.
- Gardez disponible un accès console séparé à l’hôte.
- Ne provoquez pas de panne, et ne modifiez pas le réseau de gestion, pour tester ce guide.
- Les agrégations, le SDN, les trunks VLAN dans les invités et la récupération réseau d’urgence ne sont pas traités ici.

### 1. Trouver le chemin en échec

Notez l’heure avec son fuseau horaire, la dernière opération qui a fonctionné et l’erreur exacte. Notez aussi la machine source, le nom ou l’adresse de destination, le protocole et le port du service. Conservez cet état de départ avant de réessayer. Un test qui fonctionne depuis votre ordinateur ne prouve pas l’accès depuis l’appliance, un hôte ou un invité.

| Chemin | Où regarder |
| --- | --- |
| Navigateur → appliance | Sur votre ordinateur, vérifiez l’URL, la résolution du nom et l’identité du certificat. Si la page ne s’ouvre pas, utilisez un accès console autorisé et les [vérifications par la console](#appliance-checks). |
| Appliance → hôte | Lisez l’erreur de connexion dans **Paramètres → Serveurs** (`/#/settings/servers`), puis suivez [Gérer les hôtes et les pools](/docs/xoa-hl/hosts-pools/). « Activé » est un réglage, pas la preuve que la connexion fonctionne. |
| Hôte → SR NFS | Vérifiez le SR exact, ainsi que l’attachement et le chemin de cet hôte, comme dans [Créer un stockage NFS pour les disques de VM](/docs/xoa-hl/storage-networks/#nfs-vm-storage). Un test depuis un invité ou depuis l’appliance ne remplace pas l’accès propre à l’hôte. |
| Appliance → destination de sauvegarde | Suivez [Diagnostiquer une sauvegarde NFS en échec](#backup-failures). Un SR NFS et une destination de sauvegarde utilisent des clients et des identités différents. |
| Invité → pair ou service | Suivez les étapes 2 à 4 ci-dessous. Se connecter à XO, ou voir la console, ne prouve pas que l’invité a accès au réseau. |

### 2. Relier l’interface de l’invité à la liaison de l’hôte

Lisez seulement ces écrans. Ne cliquez pas sur les champs réseau ou MAC modifiables, ni sur les boutons de connexion.

1. Notez l’UUID de la VM, son état d’alimentation, l’hôte sur lequel elle tourne et son pool. Ouvrez l’onglet **Réseaux** de la VM (`/#/vms/<id>/network`).
2. Copiez l’UUID de l’interface (VIF) avec le bouton de copie de la ligne. Notez le numéro de périphérique, l’adresse MAC, le réseau, le MTU et l’état.
3. Ouvrez la vue réseau du pool (`/#/pools/<id>/network`) et retrouvez l’UUID exact du réseau, pas seulement son nom.
4. Lisez **Connecté** : il indique si la VIF est attachée. Une VIF détachée sur une VM arrêtée n’est pas une panne.
5. Lisez **Adresses IP** : la valeur vient des métriques de l’invité, par périphérique VIF. Une adresse absente ne prouve pas que l’invité n’est pas configuré. Une adresse affichée n’est pas un test d’accessibilité en direct. Comparez avec la console de l’invité et les [vérifications de l’agent invité](/docs/xoa-hl/guest-tools/).
6. Notez l’indicateur de verrouillage et les **IPs autorisées** séparément des adresses signalées. Ce sont des règles de trafic, pas un formulaire pour donner son adresse IP à l’invité. Conservez tout avertissement, et demandez au responsable réseau d’expliquer les règles appliquées. Ne déverrouillez pas l’interface, ne retirez pas les restrictions, ne changez pas la MAC ou le MTU et ne désactivez pas la sécurité pour gagner du temps.
7. Dans la ligne réseau du pool, développez **PIFs** et repérez l’hôte sur lequel tourne la VM. Le résumé VLAN de cette ligne vient uniquement du maître du pool.
8. Ouvrez l’onglet **Réseaux** de cet hôte (`/#/hosts/<id>/network`). Notez l’UUID de la PIF, le périphérique, la MAC, le réseau, le VLAN, le MTU, l’indicateur de gestion et le mode IP. Comparez-les avec les relevés approuvés de câblage et de commutateurs. Un réseau peut être interne volontairement, sans liaison physique : vérifiez la configuration attendue avant de conclure à une panne.
9. Lisez séparément l’attachement et le lien physique (porteuse). Le bouton **Connecté** de l’hôte indique si la PIF est attachée. L’icône de lien physique, et l’état de la PIF dans la ligne développée du pool, indiquent la porteuse.

Des métriques PIF absentes peuvent aussi s’afficher comme une porteuse absente : un état négatif seul ne prouve donc pas qu’un câble est débranché. Actualisez, et comparez avec ce qu’indiquent l’hôte et le commutateur. Ne basculez pas les PIF, ne modifiez pas les réglages VLAN, MTU ou IP, ne supprimez pas de réseau et ne redémarrez pas le réseau pour sonder le chemin.

### 3. Vérifier les réglages de l’invité et le service

1. Dans la **console de l’invité**, repérez l’interface par son adresse MAC. Son nom dans l’invité peut différer du nom du périphérique sur l’hôte.
2. Avec les outils du système de l’invité, lisez son adresse et son préfixe, ses routes et ses réglages DNS. Comparez-les avec l’adresse unique et le sous-réseau approuvés par le responsable réseau. Sur le VLAN de laboratoire, l’invité voit normalement une interface non étiquetée.
3. Demandez aux administrateurs de l’invité ou du réseau de tester le pair et le service applicatif convenus depuis cet invité précis. Notez séparément les réponses DNS, la famille d’adresses utilisée, la destination, le protocole et le port, et le résultat.
4. Si un test par nom et un test par adresse donnent des résultats différents, vérifiez le DNS et l’identité applicative ou TLS avant de conclure. HTTPS vers une simple adresse IP peut changer le certificat ou l’hôte virtuel. Ne contournez jamais la vérification du certificat pour déclarer une réussite.

Un ping réussi ne prouve pas qu’un service fonctionne, et un ping qui échoue ne prouve pas l’isolation. Testez uniquement des destinations approuvées. Quand l’isolation est requise, testez aussi les destinations interdites définies par le responsable.

Un pair sur le même hôte ne teste pas la liaison physique. Les tests entre hôtes, ou hors de l’hôte, demandent des pairs identifiés et un chemin approuvé dans les commutateurs. Ne migrez pas une charge de travail pour improviser un test. Si vous constatez un accès inattendu à la production, conservez les preuves et arrêtez normalement l’invité de test. Si la gestion ou le stockage sont touchés, utilisez la console d’hôte séparée et le plan de récupération du responsable avant toute autre modification.

### 4. Vérifier la correction

1. Transmettez au responsable la correspondance exacte, les heures, l’erreur et vos résultats de comparaison.
2. Appliquez la correction convenue avec la procédure adaptée : invité, stockage, hôte ou réseau. Ce guide ne prescrit pas de réinitialisation générale.
3. Actualisez l’inventaire. Refaites le **même test de service, de la même source vers la même destination**.
4. Refaites les vérifications d’isolation requises, et vérifiez l’accès à la gestion et au stockage.
5. Notez ce qui a changé et le résultat.

**Vérification :** le même test réussit désormais. Un indicateur vert seul ne signifie pas que le problème est résolu. Si le chemin reste incertain, gardez l’incident ouvert et [signalez un problème](#report-a-problem) avec des détails expurgés.

## Diagnostiquer une sauvegarde NFS en échec {#backup-failures}

Utilisez cette partie uniquement pour la [tâche de sauvegarde complète vers NFS du tutoriel](/docs/xoa-hl/backup-restore/), connecté en tant qu’administrateur XOA-HL. Vous travaillez dans le **navigateur**. Les vérifications du stockage relèvent de son administrateur. Vous n’avez pas besoin de provoquer une panne.

**Avant de commencer**

- Notez les ID de la tâche et de la planification, l’UUID de la VM source, l’ID de la destination, l’heure d’exécution prévue avec son fuseau horaire et le résultat de la dernière restauration isolée.
- Les chaînes incrémentales, la réplication et la récupération en production ne sont pas traitées ici. Pour les autres tests de sauvegarde, voir [les sauvegardes incrémentales et la récupération de chaîne](/docs/xoa-hl/backup-restore/#delta-backups), [un fichier depuis une sauvegarde delta](/docs/xoa-hl/backup-restore/#file-restore), [une réplique DR sur un autre pool](/docs/xoa-hl/backup-restore/#dr-replica) et [une destination SMB sur Windows Server](/docs/xoa-hl/backup-restore/#smb-remote).

### 1. Trouver l’exécution et conserver ses détails

1. Ouvrez **Sauvegardes → Vue d’ensemble** (`/#/backup/overview`) et trouvez la tâche. Regardez le tableau **Logs** en dessous.
2. Effacez au besoin les filtres de recherche et d’état des journaux. Retrouvez l’exécution par sa tâche et son heure de début. Le tableau abrège l’ID de la tâche : utilisez les ID complets des détails, pas seulement le nom.
3. Sélectionnez le bouton d’état de l’exécution pour ouvrir ses détails. Notez l’`id` de l’exécution, `jobId`, `scheduleId`, les heures de début et de fin, et l’état.
4. Avant toute modification, conservez le JSON en privé avec le bouton du presse-papiers ou **Download log**. Le journal téléchargé n’est pas expurgé : pour un signalement, préparez un extrait expurgé.
5. Effacez la recherche des détails et sélectionnez tous les états de tâche. Au départ, la fenêtre peut n’afficher que les tâches en cours, en échec ou interrompues, cinq par page. Vérifiez chaque page.
6. Repérez l’UUID de la VM, puis ses tâches de snapshot, de destination, d’export et de transfert. Conservez les erreurs, les motifs d’omission et les avertissements à chaque niveau. Toutes les tâches brutes ne sont pas affichées : si l’arbre semble incomplet, lisez le JSON conservé.

**Vérification :** vos notes identifient une exécution précise, ainsi que la VM et la destination concernées. L’absence de journaux ou de tâches ne prouve pas que rien ne s’est exécuté.

### 2. Lire l’état avant de réessayer

| État (valeur JSON) | Ce qu’il signifie et ce qu’il faut vérifier |
| --- | --- |
| Démarré (`pending`) | L’exécution est enregistrée comme active. Actualisez et suivez sa progression. L’absence d’heure de fin ne signifie pas un succès. Ne lancez pas d’autre exécution. |
| Successful (`success`) | L’exécution et ses tâches enregistrées se sont terminées. Lisez les avertissements et vérifiez le nouveau point de restauration. Testez séparément la récupération de l’invité et de ses données. |
| Skipped (`skipped`) | Une partie du travail a été omise. Lisez le motif : des erreurs comme `no disks found`, `no VMs match this pattern` et `unhealthy VDI chain` comptent comme omises. Ce n’est pas une nouvelle sauvegarde vérifiée. |
| Failed (`failure`) | L’exécution ou une sous-tâche a échoué. D’autres opérations ont pu réussir : vérifiez l’étape en échec et les sauvegardes qui existent réellement. |
| Interrupted (`interrupted`) | Un début n’a pas de fin correspondante, et le serveur ne considère plus l’exécution comme active. Conservez la chronologie du serveur et la liste des objets partiels. Cet état ne prouve ni un retour arrière, ni qu’une nouvelle tentative est sans risque. |
{.xoa-backup-diagnosis}

### 3. Distinguer l’étape en échec des données conservées

Ouvrez **Sauvegardes → Restaurer** (`/#/backup/restore`) pour voir les points de restauration et les journaux de restauration.

| Problème | À vérifier |
| --- | --- |
| Aucune exécution correspondante | Vérifiez les filtres des journaux, les ID de la tâche et de la planification, l’activation, le fuseau horaire, la disponibilité du serveur et la [planification enregistrée](/docs/xoa-hl/backup-restore/#backup-schedules). Ne supposez pas que les exécutions manquées sont rattrapées, ni qu’un courriel a été envoyé. |
| Une erreur de VM ou de snapshot, ou une VM omise | Vérifiez l’UUID de la VM choisie, ses disques, la connexion de l’hôte et l’espace libre du SR source. Conservez le motif exact. Ne supprimez pas de snapshots et ne modifiez pas une chaîne VDI comme correction générale. |
| Une erreur de destination, d’export ou de transfert | Avec l’administrateur du stockage, vérifiez que l’appliance atteint l’export NFS, les droits et options de l’export, et l’espace libre de la destination. Un test de destination réussi ne prouve ni l’export complet ni une restauration. |
| Le transfert a réussi, puis l’exécution a échoué | Avec **Supprimer les anciennes sauvegardes** désactivé, cette sauvegarde complète écrit l’export et ses métadonnées avant de supprimer les anciens points. Un nouveau point peut donc survivre à un échec du nettoyage. Vérifiez les heures et les points conservés avant de relancer ou de supprimer des fichiers. |
| Le point n’apparaît pas dans Restaurer | Ouvrez **Sauvegardes → Restaurer** et actualisez. Vérifiez que la bonne destination est activée, et lisez toute erreur de chargement. Une destination illisible peut manquer dans la liste : une liste vide ne prouve pas que ses sauvegardes ont été supprimées. |
| La restauration a échoué | Lisez les journaux de restauration sur cette page. Vérifiez que la destination est lisible et que le SR et l’hôte cibles sont accessibles. Listez par UUID toute VM ou tout disque partiel. Gardez la VM source et la sauvegarde, et ne supprimez jamais d’après le seul nom. |
{.xoa-backup-diagnosis}

**Vérification :** vous savez distinguer l’étape en échec, les points de restauration conservés et les objets dont l’état reste inconnu. Un fichier ou un point listé ne prouve pas à lui seul que les données sont récupérables.

### 4. Corriger la cause et vérifier le résultat

1. Pour arrêter les prochaines exécutions, désactivez la planification exacte du laboratoire dans **Vue d’ensemble**, puis actualisez pour vérifier son état. Cela n’annule pas une sauvegarde en cours : le bouton d’annulation de **Vue d’ensemble** est désactivé dans cette version. Redémarrer `xo-server` n’annule pas une sauvegarde et ne la nettoie pas.
2. Corrigez le problème d’accès, d’espace ou de sélection avec son responsable. Vérifiez ensuite de nouveau la tâche, la planification, la VM et la destination.
3. Gardez **Supprimer les anciennes sauvegardes** désactivé, et gardez les copies de récupération nécessaires hors de la rétention de cette tâche. Si vous ne savez pas si une opération est encore en cours, ou à qui appartiennent des objets partiels, conservez les preuves et demandez de l’aide avant de réessayer.
4. Quand aucune exécution n’est active et que l’état est compris, lancez à la main cette tâche de laboratoire à une VM, comme dans le tutoriel. Les boutons de relance et de forçage de la fenêtre de détails **lancent des sauvegardes** : ils ne redémarrent pas l’invité et ne sont pas des vérifications en lecture seule. N’utilisez pas le forçage. Une nouvelle tentative peut aussi appliquer la rétention aux anciens points.
5. Vérifiez la nouvelle exécution et les points de restauration. Puis [restaurez une copie arrêtée, retirez toutes ses cartes réseau et vérifiez les données témoin](/docs/xoa-hl/backup-restore/).
6. Laissez la planification du laboratoire désactivée. Avant de réactiver les exécutions planifiées, notez l’erreur d’origine, la correction, les ID de la nouvelle exécution et du nouveau point, et le résultat de la restauration.

**Vérification :** la nouvelle exécution, les points conservés et la restauration isolée des données de l’invité réussissent tous. Sinon, gardez l’incident ouvert et [signalez un problème](#report-a-problem) avec des éléments expurgés.

## Vérifier l’appliance depuis sa console {#appliance-checks}

Ces commandes lisent seulement l’état. Exécutez-les dans l’appliance, pas sur l’hôte hyperviseur, depuis une console ou une session SSH autorisée. Certaines demandent les privilèges root.

```bash
rpm -q xoa-hl nodejs
timedatectl
df -h
systemctl status xo-server redis xoa-hl-update.service --no-pager
systemctl list-timers 'xoa-hl-*'
journalctl -u xo-server -u xoa-hl-check-update.service -u xoa-hl-update.service -u xoa-hl-auto-update.service --since '1 hour ago' --no-pager
tail -n 100 /var/log/xoa-first-boot.log
tail -n 100 /var/lib/xoa-hl/update.log
cat /run/xoa-hl/status
cat /var/lib/xoa-hl/auto-update.status
```

- Un fichier d’état absent avant la première vérification, ou après un redémarrage, n’est pas un échec en soi.
- `systemctl status` renvoie un code non nul pour une unité inactive ou en échec. Lisez l’état affiché.
- L’état de la mise à jour automatique peut décrire une ancienne exécution. Comparez ses heures UTC.
- Pour le sens de chaque état, et pour les décisions de mise à jour et de redémarrage, voir [Maintenir l’appliance à jour](/docs/xoa-hl/maintenance/).

Ne supprimez pas de fichiers de base de données, de journaux ou de verrous pour faire disparaître une erreur. Si le disque est plein, trouvez les fichiers qui grossissent et conservez les preuves avant de choisir quoi nettoyer.

## Réparer les paquets après une mise à jour interrompue {#interrupted-update}

N’utilisez cette procédure que si l’appliance s’est arrêtée pendant une mise à jour, par exemple après une coupure de courant. Lancez les commandes en root dans l’appliance, depuis une console ou une session SSH autorisée, quand aucune mise à jour n’est en cours.

1. Vérifiez la base des paquets. Tout problème signalé, par exemple un paquet en double, indique que la réparation est nécessaire :

   ```bash
   dnf check
   ```

2. Supprimez les entrées de paquets en double :

   ```bash
   dnf remove --duplicates
   ```

3. Vérifiez les paquets du noyau le plus récent. Une ligne qui commence par `S.5` signale un fichier endommagé :

   ```bash
   rpm -V kernel-core-<version> kernel-modules-core-<version> kernel-modules-<version>
   ```

4. Si un fichier est endommagé, réinstallez ces trois paquets, puis vérifiez à nouveau :

   ```bash
   dnf reinstall kernel-core-<version> kernel-modules-core-<version> kernel-modules-<version>
   dnf check
   rpm -V kernel-core-<version> kernel-modules-core-<version> kernel-modules-<version>
   grubby --default-kernel
   ```

5. Redémarrez normalement l’appliance. Vérifiez ensuite la connexion, la version installée et la liste des hôtes.

**Vérification :** `dnf check` et `rpm -V` ne signalent rien, et l’appliance démarre sur le noyau indiqué par `grubby --default-kernel`. Ne vous fiez pas au seul résultat d’une mise à jour suivante : une mise à jour lancée après une interruption peut indiquer un succès et laisser ces problèmes.

## Récupérer l’accès administrateur {#recover-admin-access}

Utilisez cette procédure quand aucun administrateur ne peut se connecter : mot de passe perdu, appareil du code à usage unique perdu, ou connexion LDAP ou SAML qui ne fonctionne plus. Vous lancez une commande de récupération **dans l’appliance**, en root, depuis la console de l’appliance ou en SSH. Toute personne qui a l’accès root à l’appliance peut ainsi prendre le contrôle d’un compte XO : protégez cet accès.

La commande modifie le compte indiqué :

- Elle définit un nouveau mot de passe.
- Elle retire le code à usage unique du compte.
- Elle fait du compte un **Administrateur**.
- Elle retire les liens LDAP ou SAML du compte, qui devient un compte local.
- Elle conserve les autres réglages du compte et ses jetons d’authentification existants.

Si aucun compte ne porte ce nom, la commande crée un nouvel administrateur local.

1. Ouvrez la console de l’appliance depuis XO Lite, ou une session SSH, et passez root.
2. Vérifiez que la base de données fonctionne : `systemctl is-active redis` affiche `active`.
3. Lancez la commande avec le nom d’utilisateur exact du compte, en général une adresse e-mail. Inutile d’arrêter `xo-server`.

   ```bash
   node /opt/xo/packages/xo-server/dist/recover-account-cli.mjs admin@example.net
   ```

4. À l’invite `Password (leave empty for random):`, tapez le nouveau mot de passe puis Entrée. Le mot de passe ne s’affiche pas. Si vous le laissez vide, la commande affiche un mot de passe aléatoire : rangez-le dans votre gestionnaire de mots de passe, puis effacez l’écran. Ne passez pas le mot de passe sur la ligne de commande : il resterait dans l’historique du shell.
5. Attendez `user admin@example.net has been successfully updated`. Si le message indique `created`, le nom ne correspondait à aucun compte. Une fois connecté, vérifiez le nom dans **Paramètres → Utilisateurs** et supprimez le compte en trop si vous n’en avez pas besoin.
6. Dans une nouvelle fenêtre de navigation privée, connectez-vous avec le compte et son nouveau mot de passe. Aucun code à usage unique n’est demandé.
7. Sur votre page utilisateur, lisez **Authentication tokens**. Si un appareil ou un mot de passe a été perdu, sélectionnez **Forget all authentication tokens**. Cela supprime tous les jetons, sauf celui de la session en cours.
8. Si le compte utilisait un code à usage unique, [configurez-le de nouveau](/docs/xoa-hl/sign-in-otp/) sur un appareil que vous maîtrisez. S’il utilisait LDAP ou SAML, c’est désormais un compte local : gardez-le comme administrateur local de secours, ou demandez au responsable de l’annuaire avant de le lier de nouveau.

**Vérification :** le compte se connecte avec le nouveau mot de passe, **Paramètres → Utilisateurs** l’affiche comme **Administrateur**, sa colonne **OTP** indique **Non configuré**, et seuls les jetons attendus restent.

| Problème | À vérifier |
| --- | --- |
| `node: command not found`, ou `Cannot find module` | Lancez `rpm -q xoa-hl nodejs`, et vérifiez que le fichier de la commande existe. Utilisez le chemin exactement comme indiqué. |
| La commande attend sans se terminer, ou signale une erreur Redis | Faites les [vérifications depuis la console](#appliance-checks) pour `redis` et l’espace disque. Ne supprimez pas de fichiers de base de données. |
| La connexion échoue encore | Vérifiez le nom d’utilisateur exact affiché par la commande, utilisez une nouvelle fenêtre privée, et lisez `journalctl -u xo-server --since '15 min ago'`. |

## Questions fréquentes {#common-questions}

**Pourquoi la maintenance a-t-elle laissé des VM sur l’hôte, ou l’hôte désactivé ?** Conservez la tâche. Vérifiez ensuite l’état activé réel de l’hôte et l’endroit où tourne chaque VM. Le [test du mode maintenance](/docs/xoa-hl/hosts-pools/#host-maintenance-mode) traite séparément l’évacuation et la réactivation. Une évacuation partielle ou un échec précoce demande le plan de récupération du responsable de l’hôte. Ne contournez pas les blocages de migration, et ne répétez pas le bouton à l’aveugle.

**Pourquoi un hôte n’a-t-il pas rejoint le pool ?** Conservez la tâche, l’erreur et les inventaires des deux pools. Le [test de jonction au pool](/docs/xoa-hl/hosts-pools/#pool-join) vérifie les ID exacts, les différences de correctifs, le maître, les réseaux et le stockage avant la confirmation. L’interface lance une jonction forcée : ne la répétez pas, et n’éjectez pas un hôte pour masquer un échec inexpliqué.

**Pourquoi la création de VM déléguée a-t-elle été refusée ?** Suivez le [test de l’ensemble de ressources et de son quota](/docs/xoa-hl/permissions/#resource-set-delegation). Comparez l’utilisateur exact, l’ensemble choisi, les ID du modèle, du SR et du réseau, et les quotas Used/Total. Voir un modèle ou un bouton ne prouve pas que le serveur autorise l’action. Conservez l’erreur, et cherchez une VM ou un disque partiel avant de réessayer. N’augmentez pas les quotas et n’accordez pas le droit Admin sur le pool pour masquer un échec inexpliqué.

**Pourquoi des mises à jour sont-elles listées alors que la commande de vérification renvoie 100 ?** Le script de vérification du paquet traduit le code de sortie 100 de `dnf check-update` en `AVAILABLE`, 0 en `UP_TO_DATE`, et tout autre code en `ERROR`. Des mises à jour listées ne sont pas une installation en échec.

**Passer à stable annule-t-il une mise à jour testing ?** Non. Le canal choisit les dépôts des vérifications et installations suivantes. Passer à stable ne rétrograde pas une version déjà installée.

**Un point de métadonnées du pool prouve-t-il qu’un hôte peut être récupéré ?** Non. Le [test des métadonnées du pool](/docs/xoa-hl/configuration-backup/#pool-metadata) vérifie seulement l’export, la rétention et l’identité des fichiers. La restauration sur un pool de test isolé n’est pas encore traitée.

**Un export de configuration peut-il remplacer une sauvegarde de VM ou un retour arrière de l’appliance ?** Non. Lisez le [périmètre de la configuration et les limites de récupération](/docs/xoa-hl/configuration-backup/), et gardez des sauvegardes séparées de vos invités.

## Signaler un problème {#report-a-problem}

[Ouvrez un ticket XCP-HL](https://github.com/Vagrantin/xcp-hl/issues/new). Donnez ces informations sous forme de texte :

- L’URL et la langue de la page, ou le chemin de l’écran de l’appliance où le problème se produit.
- Le tag de l’image, les versions affichées dans **À propos**, les versions RPM et Node installées, et le canal stable ou testing.
- L’opération, les étapes exactes, le résultat attendu et l’erreur réelle.
- L’heure avec son fuseau horaire, le mode manuel ou automatique, l’état du service concerné et un extrait de journal expurgé.
- Si le problème se reproduit sur une appliance jetable, et la dernière version qui fonctionnait.

Retirez des journaux et des captures d’écran les mots de passe, jetons, cookies, noms d’hôtes et adresses privés, et les données des utilisateurs ou des invités. Les journaux de `xo-server` et du premier démarrage peuvent contenir des identifiants. Ne joignez jamais un export de configuration, une clé privée TLS ou un fichier de configuration complet. Gardez les éléments d’origine en privé.

{{< details title="Sources" closed="true" >}}
- **Comportement de cette version** : [planification des mises à jour](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/docs/automatic-updates.md), [codes de sortie de la vérification](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xoa-hl-check-update.sh), [service serveur](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SOURCES/xo-server.service), [provisionnement au premier démarrage](https://github.com/Vagrantin/build-xoa-hl/blob/fc7ebfa7ad68664fc9b5701049cc314ebf18bea9/scripts/xoa-credentials.sh).
- **Diagnostic des sauvegardes** : [vue d’ensemble et détails d’exécution](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/index.js), [filtres, pages et affichage des tâches](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-body.js), [journal brut et boutons de relance](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/logs/backup-ng/log-alert-header.js), [calcul des états](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/backups-ng-logs.mjs), [ordre de l’export complet et du nettoyage](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/@xen-orchestra/backups/_runners/_writers/FullRemoteWriter.mjs), [erreurs de la liste des destinations et journaux de restauration](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/backup/restore/index.js).
- **Diagnostic réseau** : [vue réseau de la VM](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/vm/tab-network.js), [vue réseau de l’hôte](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/host/tab-network.js), [vue réseau du pool](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/pool/tab-network.js), [affichage de la porteuse des PIF](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/common/sorted-table/pifs-column.js), [métriques de l’invité et correspondance des interfaces](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xapi-object-to-xo.mjs), [état de connexion des serveurs](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-web/src/xo-app/settings/servers/index.js).
- **Récupération administrateur** : [commande de récupération](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/recover-account-cli.mjs), [mise à jour du compte](https://github.com/vatesfr/xen-orchestra/blob/e281c536d3b1e97ccfb3b0826f91b7dbb6c4478c/packages/xo-server/src/xo-mixins/subjects.mjs), [chemin installé et configuration](https://github.com/Vagrantin/xoa-hl/blob/a28085219cdfe9d20700e6060377f5059e42e6b5/SPECS/xoa-hl.spec).
{{< /details >}}
