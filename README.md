# Agentic Coding With Github Copilot

Ce repository est un support de workshop pour apprendre le refactoring agentique avec github copilot.

## 🎯 Objectif

- Appliquer les meilleures pratique de refactoring sur une API HTTP de gestion de tâches. 
- Apprendre  à utiliser efficacement GitHub Copilot pour améliorer la lisibilité et la maintenabilité du code.


## Prérequis
- GitHub Copilot activé dans VS Code
- Un environnement de développement python ou java (`python/README.md` ou `java/README.md`)


## 📖 Contexte

Tu es développeur au sein de **TaskFlow**, une startup qui conçoit une plateforme collaborative de gestion de tâches pour équipes projets. L'équipe Backend Core est responsable de l'évolution de l'API interne utilisée aussi bien par le frontend web que par les applications mobiles. L'API actuelle permet de gérer des listes de tâches simples, mais TaskFlow souhaite désormais accélérer très fortement la roadmap. En tant que nouveau développeur, tu rejoins l'équipe pour la renforcer.

### 🔌 API Endpoints

L'API existante fournit des endpoints pour la gestion des tâches :

- **GET /tasks** : Récupérer une liste de tâches.
- **POST /tasks** : Créer une nouvelle tâche.
- **GET /tasks/{id}** : Récupérer une tâche spécifique par ID.
- **PUT /tasks/{id}** : Mettre à jour une tâche spécifique par ID.
- **DELETE /tasks/{id}** : Supprimer une tâche spécifique par ID.

### 🚀 Démarrage rapide

0. **Installe le projet** avec le language de ton choix (`python/README.md` ou `java/README.md`)
1. **Lis attentivement** chaque user story (fichiers `US X - ...md`)
2. **Suis les instructions HOW** qui guident l'utilisation des modes Copilot
3. **Valides** que tous les critères d'acceptation sont remplis avant de passer à la suivante
4. **Expérimentes** : n'hésitez pas à essayer différentes formulations de prompts jusqu'à obtenir un prompt qui fonctionne du premier coup
