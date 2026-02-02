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

# Project Structure

The `task_flow_api` project is organized into a three-layer architecture consisting of the following directories:
```
task_flow_api/
├── api.py          # API layer with routes for handling HTTP requests
├── service.py      # Business logic layer interacting with repository
├── repository.py   # Database interactions and CRUD operations
├── model.py        # Data models used in the application
├── db.py           # Database connection and schema initialization
├── tests/          # Tests directory
├── pyproject.toml  # Project dependencies and configuration
└── README.md       # Project documentation and setup instructions
```

# Dev guide
This project use [astral uv](https://docs.astral.sh/uv/) as a dependency manager.

To launch the FastAPI application, use the following command:

```bash
uv run uvicorn task_flow_api.main:app --reload
```

This command starts the server with auto-reload enabled, allowing you to see changes without restarting the server.

```bash
# Expected response: {"version":"1.0.0"}
curl 127.0.0.1:8000/version
```

To launch test:
```bash
uv run pytest
```