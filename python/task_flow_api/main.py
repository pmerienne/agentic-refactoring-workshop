from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from task_flow_api.controller import task_router
from task_flow_api import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.init_db()
    yield
    # Shutdown (add cleanup code here if needed)


app = FastAPI(lifespan=lifespan)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler that catches all unhandled exceptions
    and returns a standardized HTTP 503 Service Unavailable response.
    """
    return JSONResponse(
        status_code=503,
        content={
            "error": "Service Unavailable",
            "description": f"An unexpected error occurred: {str(exc)}",
            "type": type(exc).__name__,
        },
    )


app.include_router(task_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
