from uuid import uuid4

from sqlalchemy.orm import Session

from src.db.models import models
from src.db.models.models import Task


def get_task(db: Session, task_id: str):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session):
    return db.query(models.Task).filter(models.Task.status == 0)


def create_task(db: Session, url: str):
    db_item = models.Task(id=str(uuid4()), url=url)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_task(db: Session, task: Task):
    row = db.get(Task, task.id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
