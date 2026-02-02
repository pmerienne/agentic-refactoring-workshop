# Code style & readability
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
