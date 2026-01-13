from typing import List

from fastapi import APIRouter, HTTPException

from task_flow_api.service import TaskService
from task_flow_api.model import Task

task_router = APIRouter()

task_service = TaskService()


@task_router.get("/version")
async def get_version():
    return {"version": "1.0.0"}


@task_router.post("/tasks", response_model=Task)
async def create_task(task: Task):
    return task_service.create_task(task)


@task_router.get("/tasks")
async def get_all() -> List[Task]:
    return task_service.list_tasks()


@task_router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    task = task_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    updated_task = task_service.update_task(
        task_id, task.title, task.description, task.status
    )
    return updated_task


@task_router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}
