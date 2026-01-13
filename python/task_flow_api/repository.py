from sqlmodel import select

from task_flow_api.db import create_session
from task_flow_api.model import Task


def save(task: Task):
    with create_session() as db_session:
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
    return task


def get(task_id) -> Task:
    with create_session() as db_session:
        task = db_session.get(Task, task_id)
        assert task is not None, f"Task not found with id {task_id}"
        return task


def delete(task_id):
    with create_session() as db_session:
        statement = select(Task).where(Task.id == task_id)
        task = db_session.exec(statement).first()
        if task:
            db_session.delete(task)
            db_session.commit()
    return task


def find_all():
    with create_session() as db_session:
        statement = select(Task)
        tasks = db_session.exec(statement).all()
        return list(tasks)
