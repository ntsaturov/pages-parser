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

    def start(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self._run())

    async def run(self):
        tasks = []

        async for conn in get_session():
            rows = await get_and_update_tasks(conn)
            for row in rows:
                parser = Parser(conn)
                task = asyncio.create_task(
                    parser.parse_page(row)
                )

                task.add_done_callback(parser.get_parse_result)
                tasks.append(task)

            await asyncio.gather(*tasks)

