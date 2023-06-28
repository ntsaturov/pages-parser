import concurrent.futures
import logging
from threading import Thread

from sqlalchemy.orm import Session

from src.api.api import get_db
from src.db.crud.crud import get_tasks
from src.tasks.tasks import parse_page_task


class TasksScheduler:
    def __init__(self, max_workers=5):
        self._max_workers = max_workers

    def __run(self, db: Session = next(get_db())):
        while True:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self._max_workers) as executor:
                exec_future = {executor.submit(parse_page_task, db, task): task for task in get_tasks(db)}
                for future in concurrent.futures.as_completed(exec_future):
                    url = exec_future[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (url, exc))
                    else:
                        logging.info(123123)
                        print(data)

    def run(self):
        t = Thread(target=self.__run)
        t.setDaemon(True)
        t.start()
