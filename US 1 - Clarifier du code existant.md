En tant que développeur nouvellement onboardé, je souhaite améliorer la lisibilité du code existant afin de faciliter sa maintenance et son évolution futures.
==

## WHY

C'est ta deuxième semaine chez TaskFlow. Après avoir compris l'architecture globale, tu reçois ton **premier ticket de refactoring** :

> "Le module `TaskValidationService` fonctionne en prod, mais plusieurs développeurs se sont plaints de sa difficulté de lecture. Avant d'ajouter de nouvelles règles métier, on a besoin de le rendre plus maintenable."

Le Tech Lead est clair : *"Ce code a été écrit à la hâte lors d'un hotfix. Il marche, mais personne n'ose y toucher par peur de casser quelque chose. Clarifie-le sans modifier son comportement, et garde un historique propre de tes changements."*

C'est l'occasion de montrer tes compétences en **refactoring assisté par Copilot**.

## WHAT

Améliorer la **lisibilité et la maintenabilité du module `TaskValidationService`** :

- Clarifier les **noms de variables, fonctions et paramètres** pour refléter l'intention métier
- Simplifier les **conditions imbriquées** et rendre la logique plus explicite
- Éliminer la **duplication de code** et les portions inutiles
- Rendre le code **auto-documenté** sans ajouter de commentaires superflus

## HOW

- Ouvre le fichier `TaskValidationService` et analyse sa structure actuelle
- Utilise Copilot pour t'assister dans le refactoring :
    - **Renommage intelligent** : sélectionne une variable/méthode et utilise `F2` pour que Copilot te suggére un meilleur nom
    - **Simplification de conditions** : sélectionne du code complexe et demande via l'inline chat (`Ctrl` + `I` ou `Cmd` + `I`) : "Simplifie cette logique en gardant le même comportement"
    - **Extraction de méthodes** : identifie les blocs dupliqués et demande "Extrait cette logique dans une méthode réutilisable"
- **Travaille par petites étapes** : chaque amélioration = un commit atomique avec un message clair

## RESSOURCES

- [Refactoring with GitHub Copilot](https://docs.github.com/fr/copilot/tutorials/refactor-code)
- [Best practices for prompting GitHub Copilot](https://docs.github.com/en/copilot/using-github-copilot/prompt-engineering-for-github-copilot)

## VALIDATION CRITERIA

- Le code est significativement plus lisible sans changement de comportement
- Les noms de variables/méthodes reflètent clairement leur intention métier
- Les conditions complexes ont été simplifiées ou décomposées
- Chaque amélioration est isolée dans un commit avec un message explicite