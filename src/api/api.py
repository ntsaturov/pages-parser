from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/api")


class TaskBody(BaseModel):
    url: str


@router.post("/tasks/parse_page")
def parse_page(body: TaskBody):
    return {"Hello": "World"}


@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"item_id": task_id}
