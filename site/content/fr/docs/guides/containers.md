---
title: Conteneurs Docker
weight: 5
translationKey: containers
---

Exécutez des conteneurs Docker depuis XOA-hl dans une VM dédiée, sans toucher à l’hôte ni à l’appliance.
{class="lead"}

{{< callout type="warning" >}}
**Non publié.** Ce guide décrit une fonction en cours de développement. Aucune image XOA-hl publiée ne la contient. Suivez [le ticket #7](https://github.com/Vagrantin/xcp-hl/issues/7) pour connaître son état.
{{< /callout >}}

## Ce que vous obtenez {#what-you-get}

XOA-hl ajoute une page **Containers** pour les administrateurs. Les conteneurs s’exécutent dans une **VM Docker** : une VM normale, créée à partir d’un modèle préparé, qui ne fait tourner que Docker.

- Les hôtes XCP-hl et l’appliance XOA-hl n’exécutent jamais Docker eux-mêmes.
- Une VM Docker se sauvegarde, se capture, démarre et s’arrête comme toute autre VM.
- Chaque conteneur a une limite de CPU et une limite de mémoire : une application ne peut pas priver les autres de ressources.

## Avant de commencer {#before-you-begin}

- Connectez-vous à XOA-hl en tant qu’administrateur.
- Activez la fonction ; elle est désactivée par défaut. Sur la console de l’appliance XOA-hl, exécutez `touch /etc/xoa-hl/containers.enabled`, puis rechargez la page. L’entrée de menu **Containers** apparaît.
- Importez le modèle de VM Docker dans votre pool et ajoutez-lui le tag `xcp-hl-docker-template-v1`. La page Containers vous le rappelle quand aucun modèle n’est trouvé.
- Utilisez un réseau avec DHCP que XOA-hl peut joindre. La VM Docker a besoin d’un accès à Internet, ou d’un registre sur votre réseau, pour télécharger les images.

## Déployer une VM Docker {#deploy-a-docker-vm}

1. Ouvrez **Containers**. Sans VM Docker, la page affiche un court guide et le formulaire **Deploy Docker VM**.
2. Saisissez un nom, le nombre de vCPU et la mémoire. Avec un seul modèle, un stockage par défaut et un seul réseau, la page les sélectionne pour vous.
3. Sélectionnez **Deploy Docker VM** une seule fois. La VM est créée avec son propre disque de 32 Gio, puis démarre.
4. Patientez quelques minutes pendant le premier démarrage. Tant que la VM n’est pas prête, la page l’indique ; ne déployez pas une seconde VM.

## Lancer un conteneur {#run-a-container}

1. Dans **Create container**, saisissez un nom et une image, par exemple `nginx:alpine`.
2. Conservez ou modifiez les limites. Les valeurs par défaut sont 1 CPU et 256 Mio.
3. Sélectionnez **Create container**. Une image absente de la VM est d’abord téléchargée, puis le conteneur démarre tout seul. Le téléchargement apparaît au-dessus de la liste jusqu’à sa fin.
4. Utilisez **Start**, **Stop**, **Restart**, **Logs** et **Remove** sur chaque conteneur. Seul un conteneur arrêté peut être supprimé, et ses volumes sont conservés.

Les **Advanced options** acceptent une entrée par ligne :

| Champ | Format | Exemple |
|---|---|---|
| Ports publiés | `HOST:CONTAINER/tcp` | `8080:80/tcp` |
| Volumes persistants | `NAME:/path` | `web:/usr/share/nginx/html` |
| Environnement | `KEY=value` | `TZ=UTC` |

Un port publié est joignable à l’adresse de la VM Docker, affichée sur la page. Ne placez pas de mots de passe dans les variables d’environnement : d’autres administrateurs et les journaux peuvent les afficher.

## Suivre l’utilisation sur le tableau de bord {#dashboard}

Dès qu’une VM Docker existe, le **Dashboard** affiche aux administrateurs une carte **Docker containers**. Pour chaque VM Docker, elle indique les conteneurs en cours d’exécution et leur total, la charge, la mémoire et le disque utilisés, ainsi que les limites réservées par les conteneurs en cours d’exécution.

La carte met en évidence ce qui demande votre attention : une VM Docker arrêtée ou qui ne répond pas, un téléchargement en échec, une mémoire ou un disque presque pleins, et des limites réservées supérieures à la taille de la VM.

## Limites et ressources {#limits}

Une limite est un plafond pour un conteneur, pas une réservation. La somme des limites peut dépasser la VM ; la page vous en avertit alors. Réduisez une limite, ou donnez plus de vCPU ou de mémoire à la VM Docker depuis sa page de VM.

L’espace disque est partagé par toutes les images, tous les conteneurs et tous les volumes de la VM Docker. Supprimez les images inutilisées sous **Images** pour libérer de l’espace.

## Sauvegarder et récupérer {#back-up-and-recover}

- Sauvegardez la VM Docker avec une tâche de sauvegarde XOA-hl normale. Elle contient les images, les conteneurs et les volumes.
- Sauvegardez aussi l’appliance XOA-hl. Elle détient les clés d’accès de chaque VM Docker, et elles ne peuvent pas être recréées.
- Après la suppression d’une VM Docker, la page liste ses clés sous **Unused access keys**. Ne les supprimez que si la VM a vraiment disparu : un pool déconnecté fait paraître ses VM Docker supprimées.
- La mise à jour de XOA-hl ne met pas à jour la VM Docker. Son système et Docker se maintiennent séparément.

## Absent de cette version {#not-in-this-version}

Pas de fichiers Compose, pas de terminal dans un conteneur, pas de conteneurs privilégiés, pas de dossiers partagés depuis la VM, et pas de mots de passe de registre enregistrés.

Ces choix gardent la première version petite et prévisible.
