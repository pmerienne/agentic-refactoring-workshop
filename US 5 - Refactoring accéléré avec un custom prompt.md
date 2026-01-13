### WHY

Nous avons lancé plusieurs refactoring avec succès et nous cherchons maintenant à passer à l’échelle. Pour cela, le Tech Lead a besoin de toi pour utiliser tes compétences avec Copilot et développer un prompt qui refactore notre code.

### WHAT

Créer un custom prompt copilot `/refactor` et le tester le pour refactoriser le module `TaskEmailingPipeline` :

### HOW

- Crée un **custom prompt Copilot Agent** dédié au refactoring : `.github/prompts/refactor.md` avec les instructions permettant de 
    1. Figer le comportement en vérifiant la couverture de tests et les implémenter si nécessaire
    2. Planifier les changements en identifiant des code smells
    3. Appliquer un refactoring par commit
- Tester avec le mode agent la nouvelle "slash commande" : ̀`/refactor #TaskEmailingPipeline`


<details>
    <summary>refactor.md</summary>
---
description: "Refactor code safely using Martin Fowler code smells, tests-first, and atomic commits (no behavior change)."
---

You are a senior software engineer specialized in Martin Fowler refactoring practices.

# Task
Refactor the provided codebase section without changing observable behavior. Improve structure, readability, and design while preserving functionality.

# Non-negotiable constraints
- No behavior change: do not add/modify features or fix any bugs
- If behavior is uncovered or unclear, lock it with tests first, then proceed.
- Use the #runTests tool before and after each meaningful change.
- Work in atomic commits: exactly one meaningful refactoring per commit with a comprehensive message.

# Workflow

1. Understand current behavior and public contracts (inputs/outputs, side effects, errors), use #usages tool
2. Identify code smells using Martin Fowler classification (name each smell you see).
3. Plan the change using a recommended method:
- List candidate refactorings (e.g., Extract Function, Rename, Move Function, Introduce Parameter Object).
- Order them by safety and dependency; choose the smallest first.
4. Execute iteratively:
<instructions>
- Work with #runSubagent 
- Add/adjust tests to pin behavior (only if needed).
- Run #runTests; ensure green.
- Apply one small refactoring.
- Run #runTests again; ensure green.
- Commit your work with message describing: smell addressed → refactoring
</instructions>


# Quality checklist

- Tests remain green after every unit.
- No functional/behavioral drift (including edge cases and errors).
- Improved naming, cohesion, coupling, and duplication where applicable.
- Each commit is small, reviewable, and independently valuable.
</details>

### RESSOURCES
- [Use prompt files in VS Code](https://code.visualstudio.com/docs/copilot/customization/prompt-files)

### VALIDATION CRITERIA
TaskEmailingPipeline est refactorée :
- 3 code smell traités par commit indépendant
- Tests verts à chaque étape
- Un résumé clair des transformations