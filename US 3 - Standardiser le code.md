En tant que développeur de l'équipe, je souhaite configurer Copilot pour qu'il génère du code conforme aux standards de TaskFlow
==

## WHY

L'ajout de nouvelles fonctionnalités avec Copilot respecte vraiment les conventions de l'équipe :
- Les noms de variables sont trop courts (`t` au lieu de `task`)
- La gestion d'erreurs utilise des `try-catch` génériques au lieu des exceptions métier de TaskFlow
- Les tests générés ne suivent pas le pattern AAA (Arrange-Act-Assert) documenté dans le wiki

L’équipe veut éviter les débats sans fin en review, il faut cadrer Copilot comme un vrai membre de l’équipe. Nous avons d'ailleurs besoin de développer une nouvelle fonctionnalité : supprimer les tâches `ARCHIVED`.


## WHAT

Créer et appliquer des **instructions Copilot personnalisées** pour TaskFlow :

- Rédiger un fichier d'instructions couvrant :
  - Le **style de code** (nommage, formatage, conventions)
  - L'**organisation des classes** (structure, responsabilités)
  - Les **patterns de gestion d'erreur** spécifiques à TaskFlow
  - Les **conventions de tests** (structure, nommage, assertions)
- Valider l'efficacité des instructions sur un cas concret
- Mesurer l'amélioration de la qualité des suggestions


<details>
    <summary>copilot-instructions.md</summary>

```markdown
# Code style & readability
- Prefer clear, intention-revealing names for files, functions, variables, and types.
- Keep functions small and single-purpose; extract helpers when logic branches or repeats.
- Prefer early returns/guard clauses to reduce nesting.
- Prefer immutable data; minimize shared mutable state.
- Add comments/docstrings only for non-obvious intent, invariants, or surprising behavior.

# Architecture & design
- Separate concerns: keep UI/handlers, domain logic, and data access in distinct layers/modules.
- Prefer dependency inversion: higher-level code should not depend on low-level details directly.
- Prefer composition over inheritance; keep abstractions minimal and justified.
- Avoid tight coupling: pass dependencies explicitly and keep module boundaries clear.
- Keep public APIs small and stable; avoid leaking internal representations.

# Error handling
- Validate inputs at boundaries; fail fast with explicit, actionable errors.
- Handle nullability/optionals explicitly; avoid unchecked assumptions.
- Prefer typed/structured errors over stringly-typed failures where possible.
- Never swallow errors silently; log or propagate with context.

# Testing
- Add/adjust tests for new behavior and bug fixes; cover critical paths and failure modes.
- Prefer deterministic tests: control time, randomness, and external dependencies via fakes/mocks.
- Use clear test names that describe behavior and expected outcomes.
- Keep tests focused and independent; avoid order dependence and shared state.
  ```
</details>


## HOW
- Intègre les conventions d'équipes dans un fichier `.github/copilot-instructions.md`
- **Teste les instructions** sur un cas concret ajouter un endpoint pour supprimer les tâches `ARCHIVED`
- Affine les instructions si nécessaire selon les résultats

## RESSOURCES

- [Copilot Custom Instructions Documentation](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [Best Practices for Copilot Instructions](https://github.blog/2024-06-18-how-to-write-better-prompts-for-github-copilot/)
- [Clean Code Principles - Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)

## VALIDATION CRITERIA
Le code généré avec les instructions respecte :
- Couverture par les tests
- Les tests générés ne suivent pas le pattern AAA (Arrange-Act-Assert) documenté dans le wiki
- Les noms de variables sont trop courts (`t` au lieu de `task`)
- La gestion d'erreurs avec des exceptions métier de TaskFlow
