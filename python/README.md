# Task Flow API

## Project Structure

The `task_flow_api` project is organized into a three-layer architecture consisting of the following directories:
```
task_flow_api/
├── api.py          # API layer with routes for handling HTTP requests
├── service.py      # Business logic layer interacting with repository
├── repository.py   # Database interactions and CRUD operations
├── model.py        # Data models used in the application
├── db.py           # Database connection and schema initialization
├── pyproject.toml  # Project dependencies and configuration
└── README.md       # Project documentation and setup instructions
```

## Dev guide
This project use [astral uv](https://docs.astral.sh/uv/) as a dependency manager.
You need to [install it](https://docs.astral.sh/uv/getting-started/installation/) :
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```


To set up the project, follow these steps:
```bash
uv sync
```


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