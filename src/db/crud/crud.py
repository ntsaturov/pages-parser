from uuid import uuid4

from sqlalchemy.orm import Session

from src.db.models import models


def get_task(db: Session, task_id: str):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, url: str):
    db_item = models.Task(id=str(uuid4()), url=url)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
