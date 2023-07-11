from uuid import uuid4

from sqlalchemy.orm import Session

from src.db.models import models
from src.db.models.models import Task
from sqlalchemy import text


def get_task(db: Session, task_id: str):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session):
    return db.query(models.Task).filter(models.Task.status == 0)


def get_and_update_tasks(db: Session):
    sql = text("update tasks as b set status = 10 "
               "from (select * from tasks where status=0 order by creation_timestamp asc limit 100"
               "for update skip locked) as a where b.id = a.id  returning b.*")
    results = db.execute(sql)
    db.commit()
    return results


def create_task(db: Session, url: str):
    db_item = models.Task(id=str(uuid4()), url=url)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_task(db: Session, task: Task):
    row = db.get(Task, task.id)
    if row:
        row.status = task.status
        row.data = task.data
        row.execution_timestamp = task.execution_timestamp
        db.add(row)
        db.commit()
        db.refresh(row)
    return row
