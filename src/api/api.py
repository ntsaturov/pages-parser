from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connector import get_session
from src.db.crud import crud
from src.db.schemas.schemas import TaskBody

router = APIRouter(prefix="/api")


@router.post("/tasks/parse_page")
async def parse_page(body: TaskBody, session: AsyncSession = Depends(get_session)):
    task = await crud.create_task(session, **body.dict())
    return task


@router.get("/tasks/{task_id}")
async def get_task(task_id: str, session: AsyncSession = Depends(get_session)):
    task = await crud.get_task(session, task_id)
    return task
