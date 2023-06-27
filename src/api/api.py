from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.db.connector import SessionLocal
from src.db.crud import crud

router = APIRouter(prefix="/api")


class TaskBody(BaseModel):
    url: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tasks/parse_page")
def parse_page(body: TaskBody,  db: Session = Depends(get_db)):
    task = crud.create_task(db, **body.dict())
    return task


@router.get("/tasks/{task_id}")
def get_task(task_id: str,  db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    return task
