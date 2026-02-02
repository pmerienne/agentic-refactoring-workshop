En tant que développeur de l'équipe, je souhaite sécuriser le comportement de `TaskScoringService`
==

## WHY
Avant un refactoring plus profond de `TaskScoringService`, l'équipe veut **sécuriser le comportement actuel**.

> "On refactorera quand on saura exactement ce que le code fait."

Le problème actuel :
- Le module `TaskScoringService` n'est pas couvert par les tests
- Impossible de refactorer en toute confiance sans filet de sécurité
- Risque de régression lors de modifications futures
- La logique métier de scoring est complexe et critique

Sans tests, toute modification du code est dangereuse. L'équipe a besoin de capturer le comportement existant avant d'envisager des améliorations.

## WHAT
Écrire une suite de tests complète pour le module `TaskScoringService` :

- **Capturer le comportement existant** sans le modifier
- **Couvrir les cas principaux** : calculs de score nominaux
- **Identifier et tester les edge cases** : valeurs limites, nulls, cas exceptionnels
- **Documenter le comportement** via des tests explicites et bien nommés
- Atteindre une couverture de code satisfaisante pour le module

## HOW
- Utilise le mode **Agent** de Github copilot
- Utilise le mode **Agent** de Github copilot et analyse le code de `TaskScoringService` pour comprendre sa logique et identifer les common/edge cases : "Analyse #sym:TaskScoringService pour identifier les fonctionnalités basiques et les cas limites"
- Utilise Copilot avec `/test` pour générer des tests ciblés sans modifier le comportement
- Vérifie l'exécution des tests avec `#runTests`


## VALIDATION CRITERIA
- Les tests couvrent les cas principaux du `TaskScoringService`
- Les edge cases sont identifiés et testés (nulls, valeurs limites, etc.)
- Tous les tests passent **sans modifier le code métier**
