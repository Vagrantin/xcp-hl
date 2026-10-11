---
title: Dépanner XOA-HL et signaler un problème
description: Identifier les vérifications utiles pour les échecs de connexion, sauvegarde et mise à jour.
weight: 42
translationKey: xoa-manual-troubleshooting
translationStatus: draft
sourceRevision: sha256:0b4aff1c1e2ce86c8e6e39cf46a9c33c23b4a840e997e96f5351a12e552a51df
glossaryTerms: ["appliance", "backup", "host", "vm"]
---

Partez du symptôme et de l’opération qui l’a précédé. Préservez les éléments de diagnostic avant de réessayer une mise à jour ou un import en échec.

{{< callout type="info" >}}
Prévisualisation vérifiée dans les sources pour l’image `xoa-image-20261009-5f33c81`, le paquet `v5.113.2_e281c536-ce38` et XO 5.113.2. Ces vérifications ne constituent pas un relevé de pannes reproduites ni de récupérations vérifiées. Les commandes ci-dessous s’exécutent dans l’appliance, pas sur l’hôte hyperviseur.
{{< /callout >}}

## Choisir la prochaine vérification

| Symptôme | Vérification et action suivante | À vérifier avant de continuer |
| --- | --- | --- |
| La page de l’appliance ne s’ouvre pas | Dans XO Lite, vérifiez que la VM fonctionne et que son adresse/réseau sont corrects. Examinez `xo-server` et l’espace disque par la console, ci-dessous. | L’URL correcte ouvre la page de connexion |
| Les identifiants initiaux échouent | Suivez la [première connexion](/docs/xoa-hl/first-login/) pour les identifiants web et le compte de secours. Examinez les journaux de provisionnement par un accès console autorisé. | La connexion fonctionne et le mot de passe initial a été changé |
| Hôte activé mais inventaire vide | Dans Settings → Servers, lisez l’erreur. Vérifiez adresse, identifiants, identité du certificat et connectivité depuis l’appliance. | Hôte et stockage attendus apparaissent sans erreur |
| Création ou installation de VM en échec | Revérifiez pool, modèle, capacité du SR, réseau et média de démarrage avec [le tutoriel VM](/docs/xoa-hl/create-vm/). Notez l’erreur de tâche avant de réessayer. | La VM jetable démarre l’installateur prévu |
| Sauvegarde ou restauration en échec | Lisez le journal de tâche et vérifiez destination, identifiants, capacité de stockage et SR cible. Suivez [le tutoriel de sauvegarde](/docs/xoa-hl/backup-restore/) ; retirez toutes les cartes réseau restaurées avant le premier démarrage. | La tâche réussit et l’invité restauré isolé possède les données attendues |
| Page de mise à jour déconnectée | Lisez le journal d’installation gérée et l’état du service ; le RPM redémarre `xo-server`. Ne lancez pas une seconde transaction. | Marqueur final de succès, version attendue, connexion et inventaire |
| La vérification indique ERROR | Lisez `/run/xoa-hl/status` et le journal du service de vérification. Examinez les erreurs réseau/dépôt ou l’outil occupé avant de revérifier. | Le nouveau verdict est `UP_TO_DATE` ou `AVAILABLE` |
| Mise à jour automatique non exécutée | Vérifiez mode enregistré, fuseau de l’appliance, délai et timers. Une fenêtre manquée pendant l’arrêt n’est pas rejouée au démarrage. | Le timer prévu est planifié ; les dates d’exécution ultérieures correspondent à la fenêtre |
| Import de configuration en échec | Conservez erreur et journal serveur ; des changements partiels peuvent rester. Suivez [le test d’import isolé](/docs/xoa-hl/configuration-backup/). | Le test sur une appliance jetable neuve réussit ; ne supposez pas la cible défaillante inchangée |

## Diagnostic en lecture dans l’appliance

Utilisez une console ou une session SSH autorisée, avec les privilèges root si nécessaire. L’absence d’un fichier d’état avant la première vérification ou après redémarrage ne prouve pas un échec. Un résultat non nul de `systemctl status` peut décrire une unité inactive ou défaillante ; lisez l’état affiché.

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

Ne supprimez pas base de données, journaux ou verrous pour masquer une erreur. Si le disque est plein, identifiez les fichiers qui grossissent et conservez les éléments de diagnostic avant de choisir un nettoyage. Consultez la [maintenance](/docs/xoa-hl/maintenance/) pour le sens des états et les décisions de mise à jour/redémarrage. L’état automatique peut concerner une ancienne exécution ; comparez ses dates UTC.

## Questions fréquentes

**Pourquoi des mises à jour sont-elles listées avec un code de retour 100 ?** Le vérificateur du paquet traduit le code 100 de `dnf check-update` en `AVAILABLE`, 0 en `UP_TO_DATE` et les autres en `ERROR`. Des mises à jour disponibles ne sont pas un échec d’installation.

**Stable annule-t-il une mise à jour testing ?** Non. Le canal sélectionne les dépôts des vérifications/installations suivantes. Revenir à stable ne rétrograde pas un candidat installé.

**L’export de configuration remplace-t-il une sauvegarde VM ou un retour arrière de l’appliance ?** Non. Consultez le [périmètre et les limites de récupération](/docs/xoa-hl/configuration-backup/) et conservez des sauvegardes distinctes des invités.

## Signaler un problème

[Ouvrez un ticket XCP-HL](https://github.com/Vagrantin/xcp-hl/issues/new). Fournissez ces informations sous forme de texte :

- URL et langue de la page, ou chemin de l’écran de l’appliance concerné.
- Tag de l’image, versions About, versions RPM/Node installées et canal stable/testing.
- Opération, étapes précises, résultat attendu et erreur réelle.
- Heure avec fuseau, mode manuel/automatique, état du service concerné et extrait de journal expurgé.
- Reproduction éventuelle sur une appliance jetable et dernière version fonctionnelle connue.

Retirez mots de passe, jetons, cookies, noms/adresses privés et données utilisateur/invité des journaux et captures. Les journaux `xo-server` et du premier démarrage peuvent contenir des identifiants. Ne joignez jamais d’export de configuration, clé TLS privée ou fichier de configuration complet. Gardez les éléments d’origine en privé.

## Sources

Comportement de cette version : [planification des mises à jour](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/docs/automatic-updates.md), [codes de vérification](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xoa-hl-check-update.sh), [service serveur](https://github.com/Vagrantin/xoa-hl/blob/5f33c81f1ae2e74a300dcc33103f4e06cf565c19/SOURCES/xo-server.service) et [provisionnement initial](https://github.com/Vagrantin/build-xoa-hl/blob/210396877e15d8761f579f569f1d911cc35b05e4/scripts/xoa-credentials.sh). Les chapitres liés citent leurs sources UI/API épinglées.
