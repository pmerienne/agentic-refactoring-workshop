from typing import List

from task_flow_api.email import TaskEmailingPipeline
from task_flow_api.repository import TaskRepository
from task_flow_api.model import Task, TaskStatus
from task_flow_api.validation import TaskValidationService


class TaskService:
    def __init__(self):
        self.repository = TaskRepository()
        self.validation_service = TaskValidationService()
        self.email_service = TaskEmailingPipeline()

    def create_task(self, task: Task) -> Task:
        assert task.id is None, f"Task already exists with id: {task.id}"
        self.validation_service._vld_tsk_bfr_crt(task)

        return self.repository.save(task)

    def get_task(self, task_id: int) -> Task:
        return self.repository.get(task_id)

    def update_task(
        self, task_id: int, title: str, description: str, status: TaskStatus
    ) -> Task:
        task = self.repository.get(task_id)
        self.validation_service._vld_tsk_bfr_crt(task)
        task.title = title
        task.description = description
        task.status = TaskStatus(status)
        if task.status == TaskStatus.DONE:
            task.completed = True
        self.email_service.send_emails(task)
        return self.repository.save(task)

    def delete_task(self, task_id: int):
        return self.repository.delete(task_id)

    def list_tasks(self) -> List[Task]:
        return self.repository.find_all()
