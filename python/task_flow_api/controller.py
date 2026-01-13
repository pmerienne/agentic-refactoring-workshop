from typing import List

from fastapi import APIRouter, HTTPException

from task_flow_api import service
from task_flow_api.model import Task

router = APIRouter()


@router.get("/version")
async def get_version():
    return {"version": "1.0.0"}


@router.post("/tasks", response_model=Task)
async def create_task(task: Task):
    return service.create_task(task)


@router.get("/tasks")
async def get_all() -> List[Task]:
    return service.list_tasks()


@router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    updated_task = service.update_task(
        task_id, task.title, task.description, task.status
    )
    return updated_task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}
