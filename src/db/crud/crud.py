from sqlalchemy import select
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import models
from src.db.models.models import Task


async def get_task(session: AsyncSession, task_id: str):
    result = await session.execute(select(models.Task).where(models.Task.id == task_id).limit(1))
    return result.scalars().first()


async def get_tasks(session: AsyncSession):
    result = await session.query(models.Task).filter(models.Task.status == 0)
    return result


async def get_and_update_tasks(session: AsyncSession):
    sql = text("update tasks as b set status = 10 "
               "from (select * from tasks where status=0 order by creation_timestamp asc limit 100 "
               "for update skip locked) as a where b.id = a.id  returning b.*")
    results = await session.execute(sql)
    await session.commit()
    return results


async def create_task(session: AsyncSession, url: str):
    db_item = models.Task(id=str(uuid4()), url=url)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def update_task(session: AsyncSession, task: Task):
    row = await session.get(Task, task.id)
    if row:
        row.status = task.status
        row.data = task.data
        row.execution_timestamp = task.execution_timestamp
        session.add(row)
        await session.commit()
        await session.refresh(row)
    return row
