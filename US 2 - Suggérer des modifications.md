En tant que développeur de l'équipe, je souhaite comprendre le module legacy `TaskRulesEngine` et identifier ses points d'amélioration, afin de préparer l'ajout de nouvelles règles de validation de manière sécurisée.
==

## WHY

Une nouvelle fonctionnalité arrive bientôt : **validation des dépendances entre tâches**. Le Product Owner veut s'assurer qu'une tâche parent ne peut pas être fermée si ses sous-tâches sont encore ouvertes.

Problème : le module `TaskRulesEngine` gère déjà plusieurs règles de validation, mais personne dans l'équipe actuelle ne maîtrise vraiment son fonctionnement. Le code date de 2 ans, l'auteur original a quitté la boîte, et la documentation est inexistante.

Le Tech Lead est formel :

> "Avant de toucher quoi que ce soit dans ce module critique, j'ai besoin que tu nous fasses un diagnostic complet. Explique-nous ce qu'il fait vraiment, où sont les risques, et comment on pourrait l'améliorer. Mais attention : **aucune modification de code pour l'instant**, juste une analyse exploitable."

C'est l'occasion de montrer tes compétences en **analyse de code legacy assistée par Copilot**.

## WHAT

Produire un **diagnostic technique complet** du module `TaskRulesEngine` :

- Comprendre son **rôle exact** dans l'architecture et son fonctionnement interne
- Identifier et **prioriser les code smells** selon la taxonomie de Fowler
- Proposer des **axes d'amélioration concrets** sans modifier le code
- Documenter les **risques** liés à une future évolution

## HOW

- Ouvre le fichier `TaskRulesEngine` et familiarise-toi avec sa structure
- Utilise Copilot en **Ask Mode** pour comprendre cette classe :"Explique-moi ce module comme si j'étais nouveau dans l'équipe. "
- Utilise maintenant `/explain` sur les fonctions clés pour comprendre leur logique interne
- Passe en mode **Plan** et demande à Copilot : "Identifie les code smells dans ce code, classe-les selon Martin Fowler, explique l'impact sur la maintenabilité et propose une piste d'amélioration"
- Compile les résultats dans un document de synthèse pour l'équipe

## RESSOURCES

- [GitHub Copilot Ask Mode](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide)
- [Using /explain command](https://docs.github.com/en/copilot/reference/cheat-sheet#slash-commands)

## VALIDATION CRITERIA

- Un document de diagnostic contenant :
    - Une description claire du rôle et du fonctionnement du module
    - **3 code smells identifiés**, classés selon Fowler, avec :
        - Le nom du smell (ex: "Long Method", "Feature Envy")
        - Sa localisation précise dans le code
        - Son **impact concret** sur la maintenabilité
        - Une **piste de changement** prioritaire
    - Une liste de risques pour l'ajout de nouvelles règles
- Le diagnostic est **exploitable** par l'équipe sans avoir besoin de re-analyser le code