import asyncio

from sqlalchemy.orm import Session

from src.api.api import get_db
from src.db.crud.crud import get_and_update_tasks
from src.tasks.tasks import parse_page_task, get_parse_result


class TasksScheduler:
    def __init__(self, time=2, db: Session = next(get_db())):
        self.time = time
        self.db = db

    async def _run(self):
        while True:
            await self.run()
            await asyncio.sleep(self.time)

    async def _start(self):
        asyncio.ensure_future(self._run())

    def start(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self._start())

    async def run(self):
        tasks = []

        for row in get_and_update_tasks(self.db):
            task = asyncio.create_task(
                parse_page_task(self.db, row)
            )

            task.add_done_callback(get_parse_result)
            tasks.append(task)

        await asyncio.gather(*tasks)

