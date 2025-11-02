# Rapidstory


**RapidStory** est un outil de ligne de commande en Python qui facilite la recherche et la réutilisation rapide de commandes dans l'historique Bash. Inspiré des fonctionnalités natives comme `Ctrl+R`, il propose deux modes d'interface : un mode **full-screen** pour ctrl+r par exemple et un mode **inline** compact pour l'utilisation avec ctrl+up. Il utilise une base de données SQLite pour une recherche optimisée et un cache en mémoire pour des performances fluides.

C'est en essayant le logiciel similaire Atuin qui ne me convenait pas parfaitement que j'ai décidé de creer mon propre logiciel d'historique et de recherche adapté à mes besoins

Il est modulaire, extensible et est concu pour être rapide et efficace. Idéal pour les personnes qui veulent pouvoir acceder rapidement et facilement a certaines entrées de leur historique. 

J'utilise ce logiciel en combinaison avec ble.sh qui est un script d'optimisation du shell bash, permettant d'ajouter des options comme l'autocompletion et la coloration syntaxique.

## Fonctionnalités

- **Recherche floue et exacte** : Utilise `difflib` pour matcher des commandes similaires (seuil configurable).
- **Mode full-screen** (Ctrl+R) : Interface complète avec numérotation, navigation fléchée et indicateurs visuels (couleurs ANSI configurables).
- **Mode inline** (Ctrl+Up) : Suggestions compactes intégrées au prompt, avec exécution directe ou insertion. Ce mode est une alternative améliorer de la touche fleche du haut dans le terminal.
- **Selection par chiffre** : J'ai implémenter un système de selection de résultats par chiffres (1 à 9)
- **Mode recherche avancé** : Utilisez des délimiteurs (ex: `'8000'`) pour chercher des séquences de chiffres sans les interpréter comme des sélections de résultats.
- **Surveillance en temps réel** : Détecte les changements dans `~/.bash_history` via un thread daemon.
- **Cache et DB** : Historique chargé en mémoire (limite configurable) et persisté en SQLite pour des recherches rapides.
- **Sécurité** : Validation des commandes pour bloquer les patterns dangereux (ex: `rm -rf /`).
- **Géstionnaire de doublons** : Doublons filtrer pour obtenir uniquement les derniers résultats.
- **Configuration flexible** : Fichier `config.py` pour personnaliser couleurs, limites, navigation, etc.

## Prérequis

- Python 3.8+ (testé sur 3.12).
- Bash (pour l'historique).
- Pas de dépendances externes : tout est standard library (sqlite3, threading, difflib/rapidfuzz, etc.).
- ble.sh dans mon cas (optionnel)

   ```bash
   ```

## Utilisation

### Mode Full-Screen (Ctrl+R)
- Appuyez sur **Ctrl+R** pour ouvrir l'interface full-screen.
- Tapez pour rechercher (ex: `git` pour matcher `git status`).
- **Navigation** : Flèches haut/bas (ou inversée via config).
- **Sélection** : Entrée pour la ligne active, ou tapez un chiffre (1-9) pour relative à l'active.
- **Mode chiffres** : Tapez `'8000'` pour chercher exactement "8000" sans sélection.
- Quittez avec **Ctrl+C** ou **Esc** (deux fois).

### Mode Inline (Ctrl+Up)
- Appuyez sur **Ctrl+Up** pour des suggestions compactes sous le prompt.
- Suggestions numérotées (1 pour actuelle, 2-4 pour suivantes).
- Sélectionnez avec un chiffre ou Entrée.
- Exécution directe par défaut (configurable).

**Exemple de sortie** :
```
[Recherche: git]
→ 1. git status -s
  2. git add .
  3. git commit -m "update"
```

## Configuration

Modifiez le fichier `~/.local/share/rapidstory/config.py` et modifiez-le:

Valeurs par défaut incluses dans le fichier. Pour les couleurs, consultez la section "CODES COULEURS ANSI" en bas du fichier.

## Licence

MIT License. Voir [LICENSE](LICENSE).

---

*Développé par Clément Stoyanov

