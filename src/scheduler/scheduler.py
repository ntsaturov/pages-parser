import asyncio

from src.db.connector import get_session
from src.db.crud.crud import get_and_update_tasks
from src.tasks.tasks import Parser


class TasksScheduler:
    def __init__(self, time=2):
        self.time = time

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
        conn = [item async for item in get_session()]
        rows = await get_and_update_tasks(conn[0])
        for row in rows:
            parser = Parser(conn[0])
            task = asyncio.create_task(
                parser.parse_page(row)
            )

            task.add_done_callback(parser.get_parse_result)
            tasks.append(task)

        await asyncio.gather(*tasks)

