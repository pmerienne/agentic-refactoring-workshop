Guide formateur
==

Ce guide permet au formateur de comprendre l’intention pédagogique, structurer la séance de travaux dirigé et faciliter l’apprentissage actif.

# Cadre général

Cette formation se déroule sous forme de mini-projet dans lequel les apprenants réalisent une suite d’exercices fortement guidés pour développer leurs usages de l’IA en situation de développement.

**Guidelines** :
- **Installation en amont** : les prérequis techniques sont clairs et réalisables avant la session.
- **Fortement guidé** : chaque exercice fournit un cadre, des consignes et des attentes explicites.
- **Exercices indépendants** : chaque étape peut être réalisée sans bloquer l’ensemble du TP.
- **Alignement pédagogique** : chaque exercice sert un objectif d’apprentissage identifié.
- **Mini-projet proche du réel** : contexte, contraintes et livrables reflètent des situations professionnelles.

# Déroulement 

## En amont

Les apprenants installent et initialisent le projet (environnement, dépendances, repo) à partir des consignes fournies.

## Pendant la session

Le formateur :

- introduit le contexte et le déroulé global du TP
- reste disponible pour débloquer les apprenants,
- assure le **cadencement** de la session.
- le contexte narratif est là pour rapprocher du réel et sa compréhension ne doit en aucun cas ralentir les apprenants

## Cadence par exercice

Pour chaque exercice, le formateur :

- laisse du temps à l’exploration et à la tentative autonome,
- restitue et explique la solution par une démonstration en **live coding**
- transmet les élements théoriques et concepts mentaux à l'oral

## Pédagogie

Fortement guidé par le formateur, cette formation verticale est **100 % orientée pratique**. La théorie est transmise à l’oral, au fil de l’exécution et des questions, jamais comme un prérequis formel.


# Pré-requis et préparation formateur
- Installation et initialisation du projet (environnement, dépendances, repo) à partir des consignes fournies.
- Vérification de la connection de l'IDE à Github Copilot
- Vérification de l'adéquation des exercices avec la version actuelle de Github Copilot


# Objectifs pédagogiques
|                    Objectifs principaux                   |                                                   Objectifs secondaires                                                  |                                                                                                              Savoirs et compétences                                                                                                             |
|:---------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Je refactorise efficacement un code existant avec Copilot | 01 - J’analyse une base de code legacy avec Copilot pour en comprendre le fonctionnement et identifier des code smells   | Inline mode, /explain, utilisation des custom instructions Copilot, repérage des dettes techniques, Typologie des code smells, Semantic Anchoring, bonnes pratiques issues de Martin Fowler, formulation de diagnostics exploitables (Plan/Act) |
|                                                           | 02 - J’utilise Copilot pour réécrire et restructurer du code existant                                                    | Ask/Edit/Agent mode de Github Copilot, Renaming avec Copilot                                                                                                                                                                                    |
|                                                           | 03 - Je définis et maintiens des instructions de clean code pour guider Copilot                                          | Custom instructions Copilot, principes de clean code, alignement des conventions d’équipe, réduction de la variabilité des réponses de l’IA                                                                                                     |
|                                                           | 04 - J’écris et maintiens des tests automatisés avec Copilot pour figer le comportement existant                         | Principes du refactoring sans changement de comportement, cycle TDD, génération de tests unitaires avec Copilot, exécution de tests via #runTests, analyse de call hierarchy avec #usages                                                       |
|                                                           | 05 - Je créé un custom agent Copilot qui applique des méthodes de refactoring tout en garantissant des commits atomiques | Techniques de refactoring (extraction, renommage, simplification), Custom Agent, sélection de design patterns pertinents, refactoring assisté par IA, gestion de commits atomiques, itération contrôlée avec Copilot                            |


# Détails des exercices

## Pré-requis :
- **Contexte pour LLM** : fichiers ouverts, sélection de code, références (#file, @workspace)
- **Modes Copilot** : Ask (lecture seule), Edit (modifications ciblées), Agent (modifications étendues)
- **Slash command** : accélération des use-cases communs avec `/explain` sur du code sélectionné


## US - 1
Développer le réflexe d'utiliser Copilot pour clarifier du code legacy via refactoring assisté, en préservant le comportement et en travaillant par étapes atomiques.

**Concepts théoriques** :
- **Intention** : Le refactoring selon Martin Fowler => Améliorer lisibilité et maintenabilité sans changer le comportement (refactoring).
- **Le refactoring commence** par l'identification des zones du code difficiles à comprendre ou à maintenir, souvent à l'aide d'une analyse des code smells.
- **Le refactoring se fait** : de manière atomique par des actions chirugicales ( renommage intelligent, extraction de méthodes, simplification logique)


**Erreurs fréquentes** :
- Prompts vagues ("clarifie ça") sans contexte précis.
- Ne pas comprendre le fonctionnement d'une méthode avant de la refactorer

## US - 2
Développer la capacité à diagnostiquer du code legacy avec Copilot sans le modifier, en identifiant les code smells selon une taxonomie reconnue et en produisant un diagnostic exploitable.

**Concepts théoriques** :
- **Intention** : Analyse avant action => Avant tout refactoring, comprendre l'existant et identifier les risques
- **Code smells (Fowler)** : Symptômes de problèmes structurels (Long Method, Feature Envy, etc.)
- **Ask Mode** : Mode de consultation pour comprendre sans modifier
- **Plan Mode** : Analyse systématique pour identifier améliorations et risques
- **Diagnostic exploitable** : Document structuré (localisation, impact, piste d'amélioration) pour travailler en **Spec-Driven-Development**

**Points d'attention** :
- Prompts structurés : "Explique le rôle", "Identifie les smells selon Fowler"
- Différencier Ask (comprendre) vs Edit (modifier)
- Prioriser les smells selon impact maintenabilité

**Erreurs fréquentes** :
- Vouloir modifier le code immédiatement sans diagnostic
- Prompts génériques sans référence à Fowler
- Confondre bug et code smell

## US - 3
Créer des instructions Copilot personnalisées pour cadrer la génération de code selon les conventions d'équipe, réduisant ainsi la variabilité et les débats en code review.

**Concepts théoriques** :
- **Intention** : Custom instructions = contrat explicite pour aligner l'IA sur les standards d'équipe
- **Reduction de variabilité** : Instructions claires => code homogène et prédictible
- **Clean Code (Martin)** : Noms explicites, fonctions courtes, gestion d'erreur structurée
- **Fichier `.github/copilot-instructions.md`** : Point central de configuration projet

**Points d'attention** :
- Instructions concises mais exhaustives (style, architecture, erreurs, tests)
- Tester efficacité sur cas concret (ex: nouvelle feature)

**Erreurs fréquentes** :
- Instructions trop vagues ou génériques
- Ne pas valider l'effet sur code généré
- Oublier patterns spécifiques au domaine métier

## US - 4
Développer la capacité à sécuriser le comportement d'un code legacy par des tests automatisés avant refactoring, en utilisant Copilot pour générer et exécuter une couverture complète.

**Concepts théoriques** :
- **Refactoring sans régression** : Martin Fowler insiste sur les tests comme prérequis au refactoring sûr
- **Intention** : Tests = filet de sécurité avant refactoring => Capturer le comportement existant sans le modifier
- **Utilitaires Copilot** :
    - **`/test`** : Génération contextuelle de tests avec Copilot
    - **`#runTests`** : Exécution et validation immédiate dans l'IDE

**Points d'attention** :
- Ne **jamais modifier** le code métier pendant la phase de test
- Utilisation des outils copilot pour accélérer cette phase

**Erreurs fréquentes** :
- Corriger un bug pendant la phase de couverture des tests
- Tests peu précis, trop génériques sans cas limites documentés

**Prompt de mise en place de test** :
```
/tests tout ces cas avec des tests unitaire pour capturer le comportement actuel : sans modifier le code de TaskScoringService.
Identifie 5 cas prioritaire et utilise une #todo list pour chaque cas et traite les indépendament avec #runSubagent en suivant les instructions : 
1. Créer 1 test unitaire sur le cas
2. Vérifie son fonctionnement avec #runTests 
3. NE JAMAIS MODIFIER TaskScoringService
```


## US - 5
Développer la capacité à créer un workflow AI Copilot personnalisé qui automatise le refactoring sécurisé en appliquant les méthodes de Fowler.

**Concepts théoriques** :
- **Intention** : Custom Prompt = automatisation de workflows complexes → Packager les bonnes pratiques en commande réutilisable
- **Prompt Files** : `.github/prompts/*.md` structure les workflows multi-étapes (tests → diagnostic → refactoring → commit)
- **#runSubagent** : Délégation de tâches itératives pour exécution autonome contrôlée
- **Workflow refactoring sécurisé** : Understand → Identify smells → Plan → Execute avec tests verts à chaque étape

**Points d'attention** :
- Le prompt doit **interdire explicitement** tout changement de comportement
- Contraintes non-négociables claires (tests verts, commits atomiques, un smell/commit)
- Utilisation des outils Copilot (#usages, #runTests, #runSubagent) dans les instructions
- Tester le custom agent sur cas réel (TaskEmailingPipeline) pour valider efficacité

**Erreurs fréquentes** :
- Prompt trop permissif autorisant des changements fonctionnels
- Instructions vagues sans workflow structuré étape par étape
- Oublier la vérification automatique des tests entre refactorings
- Ne pas ancré sémantiquement Martin Fowler